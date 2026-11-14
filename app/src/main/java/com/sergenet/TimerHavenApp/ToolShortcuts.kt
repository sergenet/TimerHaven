package com.sergenet.TimerHavenApp

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.util.Log
import android.widget.Toast
import androidx.core.content.pm.ShortcutInfoCompat
import androidx.core.content.pm.ShortcutManagerCompat
import androidx.core.graphics.drawable.IconCompat

/**
 * Home-screen shortcuts: one icon per tool, opening that tool directly.
 *
 * Static shortcuts (long-press on the app icon) are declared in res/xml/shortcuts.xml.
 * Pinned shortcuts (an icon of its own on the home screen) are requested at runtime,
 * because only the user can approve them.
 */
object ToolShortcuts {

    private const val TAG = "ToolShortcuts"

    fun shortcutId(tool: Tool): String = "tool_${tool.id}"

    fun isPinSupported(context: Context): Boolean =
        try {
            ShortcutManagerCompat.isRequestPinShortcutSupported(context)
        } catch (e: Exception) {
            Log.w(TAG, "isRequestPinShortcutSupported failed", e)
            false
        }

    /** Asks the launcher to add [tool] to the user's home screen. */
    fun requestPin(activity: Activity, tool: Tool) {
        if (!isPinSupported(activity)) {
            Toast.makeText(
                activity,
                "This launcher doesn't support adding shortcuts. Long-press the Timer Haven icon for quick access.",
                Toast.LENGTH_LONG
            ).show()
            return
        }

        val launchIntent = Intent(activity, WebViewActivity::class.java).apply {
            action = Intent.ACTION_VIEW
            data = ToolCatalog.uriFor(tool.id)
        }

        val shortcut = ShortcutInfoCompat.Builder(activity, shortcutId(tool))
            .setShortLabel(tool.shortLabel)
            .setLongLabel(tool.title)
            .setIcon(IconCompat.createWithResource(activity, tool.icon))
            .setIntent(launchIntent)
            .build()

        try {
            val requested = ShortcutManagerCompat.requestPinShortcut(activity, shortcut, null)
            val message = if (requested) {
                "Confirm \"Add to Home screen\" to keep ${tool.title} one tap away."
            } else {
                "Couldn't add the shortcut on this device."
            }
            Toast.makeText(activity, message, Toast.LENGTH_LONG).show()
        } catch (e: Exception) {
            Log.w(TAG, "requestPinShortcut failed for ${tool.id}", e)
            Toast.makeText(activity, "Couldn't add the shortcut on this device.", Toast.LENGTH_LONG).show()
        }
    }
}
