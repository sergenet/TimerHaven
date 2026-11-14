package com.sergenet.TimerHavenApp

import android.content.Context
import android.content.Intent
import kotlin.math.ceil
import kotlin.math.max

/** Immutable view of the Pomodoro timer shared by the page, the notification and the widget. */
data class PomodoroSnapshot(
    val running: Boolean,
    val phase: String,
    val remainingSec: Int,
    val workMin: Int,
    val breakMin: Int,
    val cycles: Int
) {
    val phaseLabel: String
        get() = if (phase == PHASE_WORK) "Work" else "Break"

    val clock: String
        get() {
            val minutes = remainingSec / 60
            val seconds = remainingSec % 60
            return "%02d:%02d".format(minutes, seconds)
        }

    fun toJson(): String =
        """{"running":$running,"phase":"$phase","remaining":$remainingSec,"workMin":$workMin,"breakMin":$breakMin,"cycles":$cycles}"""

    companion object {
        const val PHASE_WORK = "work"
        const val PHASE_BREAK = "break"
    }
}

/**
 * The single source of truth for a running Pomodoro session.
 *
 * The web page owns the on-screen countdown, but every start/pause/reset is mirrored here so the
 * session survives leaving the page and can drive the notification and the home-screen widget.
 * State is stored as an end timestamp, so nothing has to tick in the background to stay accurate.
 */
object PomodoroTimer {

    const val PREFS = "pomodoro_timer"
    const val ACTION_STATE = "com.sergenet.TimerHavenApp.POMODORO_STATE"

    private const val KEY_RUNNING = "running"
    private const val KEY_PHASE = "phase"
    private const val KEY_END = "endsAt"
    private const val KEY_REMAINING = "remaining"
    private const val KEY_WORK = "workMin"
    private const val KEY_BREAK = "breakMin"
    private const val KEY_CYCLES = "cycles"

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    fun snapshot(context: Context): PomodoroSnapshot {
        val store = prefs(context)
        val workMin = store.getInt(KEY_WORK, 25)
        val breakMin = store.getInt(KEY_BREAK, 5)
        val phase = store.getString(KEY_PHASE, PomodoroSnapshot.PHASE_WORK) ?: PomodoroSnapshot.PHASE_WORK
        val running = store.getBoolean(KEY_RUNNING, false)
        val stored = store.getInt(KEY_REMAINING, workMin * 60)
        val endsAt = store.getLong(KEY_END, 0L)

        val remaining = if (running && endsAt > 0L) {
            max(0, ceil((endsAt - System.currentTimeMillis()) / 1000.0).toInt())
        } else {
            stored
        }

        return PomodoroSnapshot(
            running = running && remaining > 0,
            phase = phase,
            remainingSec = remaining,
            workMin = workMin,
            breakMin = breakMin,
            cycles = store.getInt(KEY_CYCLES, 0)
        )
    }

    fun start(context: Context, workMin: Int, breakMin: Int, phase: String, remainingSec: Int) {
        val safeWork = workMin.coerceIn(1, 180)
        val safeBreak = breakMin.coerceIn(1, 180)
        val safePhase = if (phase == PomodoroSnapshot.PHASE_BREAK) PomodoroSnapshot.PHASE_BREAK else PomodoroSnapshot.PHASE_WORK
        val seconds = remainingSec.coerceIn(1, max(safeWork, safeBreak) * 60)

        prefs(context).edit()
            .putInt(KEY_WORK, safeWork)
            .putInt(KEY_BREAK, safeBreak)
            .putString(KEY_PHASE, safePhase)
            .putInt(KEY_REMAINING, seconds)
            .putLong(KEY_END, System.currentTimeMillis() + seconds * 1000L)
            .putBoolean(KEY_RUNNING, true)
            .apply()

        PomodoroTimerService.start(context)
        refresh(context)
    }

    fun pause(context: Context) {
        val current = snapshot(context)
        prefs(context).edit()
            .putBoolean(KEY_RUNNING, false)
            .putInt(KEY_REMAINING, current.remainingSec)
            .putLong(KEY_END, 0L)
            .apply()
        PomodoroTimerService.refresh(context)
        refresh(context)
    }

    fun resume(context: Context) {
        val current = snapshot(context)
        if (current.remainingSec <= 0) return
        prefs(context).edit()
            .putBoolean(KEY_RUNNING, true)
            .putLong(KEY_END, System.currentTimeMillis() + current.remainingSec * 1000L)
            .apply()
        PomodoroTimerService.start(context)
        refresh(context)
    }

    fun reset(context: Context) {
        val store = prefs(context)
        val workMin = store.getInt(KEY_WORK, 25)
        store.edit()
            .putBoolean(KEY_RUNNING, false)
            .putString(KEY_PHASE, PomodoroSnapshot.PHASE_WORK)
            .putInt(KEY_REMAINING, workMin * 60)
            .putLong(KEY_END, 0L)
            .putInt(KEY_CYCLES, 0)
            .apply()
        PomodoroTimerService.stop(context)
        refresh(context)
    }

    /** Moves on to the next period once a session hits zero. */
    fun complete(context: Context): PomodoroSnapshot {
        val store = prefs(context)
        val current = snapshot(context)
        val nextPhase = if (current.phase == PomodoroSnapshot.PHASE_WORK) {
            PomodoroSnapshot.PHASE_BREAK
        } else {
            PomodoroSnapshot.PHASE_WORK
        }
        val nextLength = if (nextPhase == PomodoroSnapshot.PHASE_WORK) current.workMin else current.breakMin
        val cycles = if (current.phase == PomodoroSnapshot.PHASE_WORK) current.cycles + 1 else current.cycles

        store.edit()
            .putBoolean(KEY_RUNNING, false)
            .putString(KEY_PHASE, nextPhase)
            .putInt(KEY_REMAINING, nextLength * 60)
            .putLong(KEY_END, 0L)
            .putInt(KEY_CYCLES, cycles)
            .apply()

        return snapshot(context)
    }

    fun setLengths(context: Context, workMin: Int, breakMin: Int, phase: String) {
        val store = prefs(context)
        if (!store.getBoolean(KEY_RUNNING, false)) {
            val minutes = if (phase == PomodoroSnapshot.PHASE_BREAK) breakMin else workMin
            store.edit()
                .putInt(KEY_WORK, workMin.coerceIn(1, 180))
                .putInt(KEY_BREAK, breakMin.coerceIn(1, 180))
                .putString(KEY_PHASE, phase)
                .putInt(KEY_REMAINING, minutes.coerceIn(1, 180) * 60)
                .apply()
        }
        refresh(context)
    }

    /** Tells the widget (and anyone else listening) that the state changed. */
    fun refresh(context: Context) {
        context.sendBroadcast(Intent(ACTION_STATE).setPackage(context.packageName))
    }
}
