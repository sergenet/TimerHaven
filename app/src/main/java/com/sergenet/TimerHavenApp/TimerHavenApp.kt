package com.sergenet.TimerHavenApp

import android.app.Application
import android.util.Log

class TimerHavenApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Log.d("TimerHavenApp", "Application onCreate")
    }
}