package com.sergenet.TimerHavenApp

import android.app.Application
import com.google.android.gms.ads.MobileAds

class App : Application() {
    override fun onCreate() {
        super.onCreate()
        // Initialize the Mobile Ads SDK manually (reads the APPLICATION_ID meta-data).
        // Because we set INITIALIZE_ON_CREATE = false in the manifest, the provider won't
        // auto-initialize and cause the crash.
        MobileAds.initialize(this) { initializationStatus ->
            // optional: inspect initializationStatus if you want
        }
    }
}