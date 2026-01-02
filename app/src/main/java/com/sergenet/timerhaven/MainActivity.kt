package com.sergenet.timerhaven

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Explicitly request the root index page
        val url = "https://timerhaven.com/index.html"

        // Show and log the exact URL we launch
        Toast.makeText(this, "Opening URL: $url", Toast.LENGTH_LONG).show()
        Log.d("MainActivity", "Opening URL: $url")

        try {
            val browserIntent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            browserIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(browserIntent)
        } catch (e: Exception) {
            Log.e("MainActivity", "Failed to open browser: ${e.message}")
        }

        finish()
    }
}