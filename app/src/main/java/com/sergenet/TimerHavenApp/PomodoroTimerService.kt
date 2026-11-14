package com.sergenet.TimerHavenApp

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat

/**
 * Keeps a running Pomodoro session visible outside the web page: an ongoing notification with
 * pause/resume/stop, a completion alert, and a nudge to the home-screen widget.
 */
class PomodoroTimerService : Service() {

    private val handler = Handler(Looper.getMainLooper())
    private var ticking = false

    private val tick = object : Runnable {
        override fun run() {
            val current = PomodoroTimer.snapshot(this@PomodoroTimerService)
            if (!current.running) {
                ticking = false
                return
            }
            if (current.remainingSec <= 0) {
                finishSession()
                return
            }
            notifyOngoing(current)
            handler.postDelayed(this, 1000L)
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createChannels()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_PAUSE -> {
                PomodoroTimer.pause(this)
                notifyOngoing(PomodoroTimer.snapshot(this))
            }
            ACTION_RESUME -> {
                PomodoroTimer.resume(this)
                notifyOngoing(PomodoroTimer.snapshot(this))
            }
            ACTION_STOP -> {
                PomodoroTimer.reset(this)
            }
            else -> Unit
        }

        val current = PomodoroTimer.snapshot(this)
        if (!current.running) {
            stopForegroundNow()
            return START_NOT_STICKY
        }

        notifyOngoing(current)
        startTicker()
        return START_STICKY
    }

    private fun startTicker() {
        if (ticking) return
        ticking = true
        handler.removeCallbacks(tick)
        handler.post(tick)
    }

    private fun finishSession() {
        ticking = false
        handler.removeCallbacks(tick)
        val next = PomodoroTimer.complete(this)
        showCompletion(next)
        stopForegroundNow()
        PomodoroTimer.refresh(this)
    }

    private fun stopForegroundNow() {
        ServiceCompat.stopForeground(this, ServiceCompat.STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun notificationManager() =
        getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

    private fun createChannels() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = notificationManager()

        val ongoing = NotificationChannel(
            CHANNEL_ONGOING,
            "Pomodoro session",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Shows the running focus or break countdown."
            setShowBadge(false)
            setSound(null, null)
        }
        manager.createNotificationChannel(ongoing)

        if (manager.getNotificationChannel(CHANNEL_ALERTS) == null) {
            val alerts = NotificationChannel(
                CHANNEL_ALERTS,
                "Timer Alerts",
                NotificationManager.IMPORTANCE_HIGH
            )
            manager.createNotificationChannel(alerts)
        }
    }

    private fun openAppIntent(): PendingIntent {
        val intent = Intent(this, MainActivity::class.java).apply {
            action = Intent.ACTION_MAIN
            addCategory(Intent.CATEGORY_LAUNCHER)
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        return PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    private fun serviceIntent(action: String): PendingIntent {
        val intent = Intent(this, PomodoroTimerService::class.java).setAction(action)
        return PendingIntent.getService(
            this,
            action.hashCode(),
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    private fun notifyOngoing(snapshot: PomodoroSnapshot) {
        val toggleLabel = if (snapshot.running) "Pause" else "Resume"
        val toggleAction = if (snapshot.running) ACTION_PAUSE else ACTION_RESUME

        val notification = NotificationCompat.Builder(this, CHANNEL_ONGOING)
            .setSmallIcon(R.drawable.ic_timer)
            .setContentTitle("${snapshot.phaseLabel} · ${snapshot.clock}")
            .setContentText("Pomodoro · ${snapshot.cycles} completed")
            .setContentIntent(openAppIntent())
            .setOnlyAlertOnce(true)
            .setOngoing(true)
            .setSilent(true)
            .setShowWhen(false)
            .addAction(0, toggleLabel, serviceIntent(toggleAction))
            .addAction(0, "Stop", serviceIntent(ACTION_STOP))
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
        } else {
            0
        }
        try {
            ServiceCompat.startForeground(this, NOTIFICATION_ONGOING, notification, type)
        } catch (e: Exception) {
            // Foreground start was refused (background start limit); show it as a plain
            // notification so the countdown is still visible.
            try {
                notificationManager().notify(NOTIFICATION_ONGOING, notification)
            } catch (ignored: SecurityException) {
                // No notification permission either; nothing else to do here.
            }
        }
    }

    private fun showCompletion(next: PomodoroSnapshot) {
        val finishedWork = next.phase == PomodoroSnapshot.PHASE_BREAK
        val title = if (finishedWork) "Work session complete" else "Break over"
        val text = if (finishedWork) {
            "Nice work. Time for a ${next.breakMin}-minute break."
        } else {
            "Back to it: ${next.workMin} minutes of focus."
        }

        val notification = NotificationCompat.Builder(this, CHANNEL_ALERTS)
            .setSmallIcon(R.drawable.ic_timer)
            .setContentTitle(title)
            .setContentText(text)
            .setContentIntent(openAppIntent())
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .build()

        try {
            notificationManager().notify(NOTIFICATION_ALERT, notification)
        } catch (e: SecurityException) {
            // The user has not granted notification permission; the timer still finished.
        }
    }

    override fun onDestroy() {
        ticking = false
        handler.removeCallbacks(tick)
        super.onDestroy()
    }

    companion object {
        const val CHANNEL_ONGOING = "pomodoro_session"
        const val CHANNEL_ALERTS = "timer_notifications"
        const val NOTIFICATION_ONGOING = 2001
        const val NOTIFICATION_ALERT = 2002

        const val ACTION_PAUSE = "com.sergenet.TimerHavenApp.POMODORO_PAUSE"
        const val ACTION_RESUME = "com.sergenet.TimerHavenApp.POMODORO_RESUME"
        const val ACTION_STOP = "com.sergenet.TimerHavenApp.POMODORO_STOP"

        fun start(context: Context) {
            val intent = Intent(context, PomodoroTimerService::class.java)
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
            } catch (e: Exception) {
                // Background start restrictions: the page still keeps its own countdown.
            }
        }

        fun refresh(context: Context) {
            val intent = Intent(context, PomodoroTimerService::class.java)
            try {
                context.startService(intent)
            } catch (e: Exception) {
                // Nothing to refresh.
            }
        }

        fun stop(context: Context) {
            context.stopService(Intent(context, PomodoroTimerService::class.java))
        }
    }
}
