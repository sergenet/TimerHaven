package com.sergenet.TimerHavenApp

import android.content.Context
import android.content.SharedPreferences

object ThemeManager {
    private const val PREFS_NAME = "theme_prefs"
    private const val KEY_THEME = "selected_theme"
    
    const val THEME_DEFAULT = "default"
    const val THEME_DARK_OCEAN = "dark_ocean"
    const val THEME_MIDNIGHT_PURPLE = "midnight_purple"
    const val THEME_FOREST_GREEN = "forest_green"
    
    // Premium themes that require Pro subscription
    private val PREMIUM_THEMES = setOf(
        THEME_DARK_OCEAN,
        THEME_MIDNIGHT_PURPLE,
        THEME_FOREST_GREEN
    )
    
    fun getSelectedTheme(context: Context): String {
        val prefs = getPrefs(context)
        return prefs.getString(KEY_THEME, THEME_DEFAULT) ?: THEME_DEFAULT
    }
    
    fun setTheme(context: Context, theme: String): Boolean {
        // Check if theme is premium and user doesn't have Pro
        if (isPremiumTheme(theme) && !SubscriptionManager.isPremiumActive(context)) {
            return false // Cannot set premium theme without Pro
        }
        
        val prefs = getPrefs(context)
        prefs.edit().putString(KEY_THEME, theme).apply()
        return true
    }
    
    fun isPremiumTheme(theme: String): Boolean {
        return PREMIUM_THEMES.contains(theme)
    }
    
    fun getAvailableThemes(context: Context): List<ThemeOption> {
        val isPro = SubscriptionManager.isPremiumActive(context)
        return listOf(
            ThemeOption("Default", THEME_DEFAULT, false),
            ThemeOption("Dark Ocean", THEME_DARK_OCEAN, !isPro),
            ThemeOption("Midnight Purple", THEME_MIDNIGHT_PURPLE, !isPro),
            ThemeOption("Forest Green", THEME_FOREST_GREEN, !isPro)
        )
    }
    
    fun applyTheme(context: Context) {
        val theme = getSelectedTheme(context)
        val themeResId = when (theme) {
            THEME_DARK_OCEAN -> R.style.Theme_TimerHaven_DarkOcean
            THEME_MIDNIGHT_PURPLE -> R.style.Theme_TimerHaven_MidnightPurple
            THEME_FOREST_GREEN -> R.style.Theme_TimerHaven_ForestGreen
            else -> R.style.Theme_TimerhavenNewApp
        }
        
        if (context is android.app.Activity) {
            context.setTheme(themeResId)
        }
    }
    
    private fun getPrefs(context: Context): SharedPreferences {
        return context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }
    
    data class ThemeOption(
        val name: String,
        val id: String,
        val isLocked: Boolean
    )
}
