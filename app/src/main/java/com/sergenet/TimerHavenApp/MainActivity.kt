package com.sergenet.TimerHavenApp

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.enableEdgeToEdge

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        
        Log.d("MainActivity", "========== MAINACTIVITY LAUNCHED ==========")

        // No longer requiring login. User is signed in, proceed to WebView
        val url = "file:///android_asset/index.html"
        Log.d("MainActivity", "Launching in-app WebView for URL: $url")

        // Start the in-app WebViewActivity
        val i = Intent(this, WebViewActivity::class.java)
        i.putExtra(WebViewActivity.EXTRA_URL, url)
        startActivity(i)

        // Close MainActivity so the app doesn't stay visible
        finish()
    }
}