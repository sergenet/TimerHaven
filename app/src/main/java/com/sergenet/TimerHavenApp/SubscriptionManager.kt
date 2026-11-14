package com.sergenet.TimerHavenApp

import android.content.Context
import android.content.SharedPreferences

object SubscriptionManager {
    private const val PREFS_NAME = "subscription_prefs"
    private const val KEY_IS_PRO = "is_pro"
    
    fun isPremiumActive(context: Context): Boolean {
        val prefs = getPrefs(context)
        return prefs.getBoolean(KEY_IS_PRO, false)
    }
    
    fun updateSubscriptionStatus(context: Context, isPro: Boolean) {
        val prefs = getPrefs(context)
        prefs.edit().putBoolean(KEY_IS_PRO, isPro).apply()
    }
    
    private fun getPrefs(context: Context): SharedPreferences {
        return context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }
}
