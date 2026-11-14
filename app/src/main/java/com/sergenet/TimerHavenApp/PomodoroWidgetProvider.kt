package com.sergenet.TimerHavenApp

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.os.SystemClock
import android.widget.RemoteViews

/**
 * Pomodoro widget: shows the session that [PomodoroTimer] holds and starts, pauses or resets it
 * without opening the app. The countdown is drawn by the system Chronometer, so the widget needs no
 * per-second work.
 */
class PomodoroWidgetProvider : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        updateAll(context)
    }

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            ACTION_TOGGLE -> {
                if (PomodoroTimer.snapshot(context).running) {
                    PomodoroTimer.pause(context)
                } else {
                    PomodoroTimer.resume(context)
                }
                updateAll(context)
            }
            ACTION_RESET -> {
                PomodoroTimer.reset(context)
                updateAll(context)
            }
            PomodoroTimer.ACTION_STATE -> updateAll(context)
        }
        super.onReceive(context, intent)
    }

    companion object {
        const val ACTION_TOGGLE = "com.sergenet.TimerHavenApp.WIDGET_TOGGLE"
        const val ACTION_RESET = "com.sergenet.TimerHavenApp.WIDGET_RESET"

        fun updateAll(context: Context) {
            val manager = AppWidgetManager.getInstance(context)
            val ids = manager.getAppWidgetIds(
                ComponentName(context, PomodoroWidgetProvider::class.java)
            )
            ids.forEach { id ->
                manager.updateAppWidget(
                    id,
                    RemoteViews(context.packageName, R.layout.widget_pomodoro).also { views ->
                        bind(context, views)
                    }
                )
            }
        }

        private fun bind(context: Context, views: RemoteViews) {
            val snapshot = PomodoroTimer.snapshot(context)
            views.setTextViewText(R.id.widget_phase, snapshot.phaseLabel.uppercase())
            views.setTextViewText(R.id.widget_cycles, "${snapshot.cycles} done")

            if (snapshot.running) {
                views.setViewVisibility(R.id.widget_clock, android.view.View.VISIBLE)
                views.setViewVisibility(R.id.widget_clock_paused, android.view.View.GONE)
                views.setChronometer(
                    R.id.widget_clock,
                    SystemClock.elapsedRealtime() + snapshot.remainingSec * 1000L,
                    null,
                    true
                )
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.N) {
                    views.setChronometerCountDown(R.id.widget_clock, true)
                }
                views.setTextViewText(R.id.widget_toggle, "Pause")
            } else {
                views.setViewVisibility(R.id.widget_clock, android.view.View.GONE)
                views.setViewVisibility(R.id.widget_clock_paused, android.view.View.VISIBLE)
                views.setTextViewText(R.id.widget_clock_paused, snapshot.clock)
                views.setTextViewText(
                    R.id.widget_toggle,
                    if (snapshot.remainingSec > 0) "Start" else "Reset"
                )
            }

            views.setOnClickPendingIntent(R.id.widget_toggle, broadcast(context, ACTION_TOGGLE, 1))
            views.setOnClickPendingIntent(R.id.widget_reset, broadcast(context, ACTION_RESET, 2))
            views.setOnClickPendingIntent(R.id.widget_root, openApp(context))
        }

        private fun broadcast(context: Context, action: String, requestCode: Int): PendingIntent {
            val intent = Intent(context, PomodoroWidgetProvider::class.java).setAction(action)
            return PendingIntent.getBroadcast(
                context,
                requestCode,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
        }

        private fun openApp(context: Context): PendingIntent {
            val intent = Intent(context, MainActivity::class.java).apply {
                action = Intent.ACTION_MAIN
                addCategory(Intent.CATEGORY_LAUNCHER)
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            return PendingIntent.getActivity(
                context,
                3,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
        }
    }
}
