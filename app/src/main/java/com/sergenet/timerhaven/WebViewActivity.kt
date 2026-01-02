package com.sergenet.timerhaven

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity

class WebViewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Create a WebView programmatically so no XML / Compose changes are required.
        val webView = WebView(this)
        setContentView(webView)

        // Allow debugging while testing (optional)
        WebView.setWebContentsDebuggingEnabled(true)

        // Read URL from Intent extra "url" or from intent data (deep link)
        val urlFromExtra = intent?.getStringExtra("url")
        val urlFromData = intent?.dataString
        val finalUrl = when {
            !urlFromExtra.isNullOrBlank() -> urlFromExtra
            !urlFromData.isNullOrBlank() -> urlFromData
            else -> ""
        }

        Log.d("Guide", "WebViewActivity got url:'$finalUrl' (extra:'$urlFromExtra' data:'$urlFromData')")
        Toast.makeText(this, "WebView URL: ${if (finalUrl.isBlank()) "<empty>" else finalUrl}", Toast.LENGTH_LONG).show()

        if (finalUrl.isBlank()) {
            // No URL provided — open a safe test page in external browser, then finish.
            val fallbackUrl = "https://example.com"
            Toast.makeText(this, "No URL provided — opening external browser for test.", Toast.LENGTH_SHORT).show()
            try {
                startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(fallbackUrl)))
            } catch (e: Exception) {
                Log.e("Guide", "Cannot open fallback browser: ${e.message}")
            }
            finish()
            return
        }

        // Basic WebView setup
        webView.settings.javaScriptEnabled = true
        webView.webViewClient = WebViewClient() // keep simple: let WebView handle navigation

        // Load the URL
        try {
            webView.loadUrl(finalUrl)
        } catch (e: Exception) {
            Toast.makeText(this, "Failed to load URL: ${e.message}", Toast.LENGTH_LONG).show()
            Log.e("Guide", "loadUrl failed: ${e.message}")
        }
    }
}