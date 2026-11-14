package com.sergenet.TimerHavenApp

import android.content.Intent
import android.net.Uri
import androidx.annotation.DrawableRes

/**
 * Every tool the app ships, so shortcuts can point straight at one page instead of the menu.
 * Pages live in assets/ and are listed in assets/index.html.
 */
data class Tool(
    val id: String,
    val title: String,
    val shortLabel: String,
    val page: String,
    @DrawableRes val icon: Int
)

object ToolCatalog {

    /** Deep link scheme used by shortcuts: timerhaven://tool/<id> */
    const val SCHEME = "timerhaven"
    const val HOST = "tool"
    const val HOME_PAGE = "index.html"

    val tools: List<Tool> = listOf(
        Tool("pomodoro", "Pomodoro Timer", "Pomodoro", "pomodoro-en.html", R.drawable.ic_tool_pomodoro),
        Tool("countdown", "Countdown Timer", "Countdown", "countdown-en.html", R.drawable.ic_tool_countdown),
        Tool("stopwatch", "Stopwatch", "Stopwatch", "stopwatch-en.html", R.drawable.ic_tool_stopwatch),
        Tool("tasktimer", "Task Timer", "Task Timer", "timer-en.html", R.drawable.ic_tool_tasktimer),
        Tool("calendar", "Calendar", "Calendar", "calendar-en.html", R.drawable.ic_tool_calendar),
        Tool("habits", "Habit Tracker", "Habits", "habit-tracker-en.html", R.drawable.ic_tool_habits),
        Tool("meeting", "Meeting Planner", "Meeting", "meeting-planner-en.html", R.drawable.ic_tool_meeting),
        Tool("clipboard", "Clipboard Manager", "Clipboard", "clipboard-manager-en.html", R.drawable.ic_tool_clipboard),
        Tool("focusmusic", "Focus Music", "Focus Music", "focus-music-en.html", R.drawable.ic_tool_music),
        Tool("notes", "Notes", "Notes", "notes-en.html", R.drawable.ic_tool_notes),
        Tool("currency", "Currency Converter", "Currency", "currency-en.html", R.drawable.ic_tool_currency),
        Tool("passwords", "Password Generator", "Passwords", "password-generator-en.html", R.drawable.ic_tool_password),
        Tool("units", "Unit Converter", "Units", "unit-converter-en.html", R.drawable.ic_tool_units),
        Tool("weather", "Weather", "Weather", "weather-en.html", R.drawable.ic_tool_weather),
        Tool("worldclock", "World Clock", "World Clock", "world-clock-en.html", R.drawable.ic_tool_worldclock)
    )

    fun homeUrl(): String = "file:///android_asset/$HOME_PAGE"

    fun assetUrl(tool: Tool): String = "file:///android_asset/${tool.page}"

    fun uriFor(id: String): Uri = Uri.parse("$SCHEME://$HOST/$id")

    fun byId(id: String?): Tool? = tools.firstOrNull { it.id == id }

    /** Matches a currently loaded page (asset URL) back to its tool. */
    fun byUrl(url: String?): Tool? {
        val page = url?.substringAfterLast('/')?.substringBefore('?')?.substringBefore('#') ?: return null
        return tools.firstOrNull { it.page.equals(page, ignoreCase = true) }
    }

    /**
     * Turns a shortcut's timerhaven://tool/<id> intent into the asset URL to load.
     * Returns null when the intent carries no tool deep link.
     */
    fun resolveLaunchUrl(intent: Intent?): String? {
        val data = intent?.data ?: return null
        if (!SCHEME.equals(data.scheme, ignoreCase = true)) return null
        if (!HOST.equals(data.host, ignoreCase = true)) return null
        val id = data.pathSegments?.firstOrNull() ?: return null
        return byId(id)?.let { assetUrl(it) }
    }
}
