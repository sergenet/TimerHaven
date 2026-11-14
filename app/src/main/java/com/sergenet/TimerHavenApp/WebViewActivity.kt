package com.sergenet.TimerHavenApp

import android.Manifest
import android.annotation.SuppressLint
import android.content.ActivityNotFoundException
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.MailTo
import androidx.core.net.toUri
import android.location.Geocoder
import android.net.Uri
import android.os.Bundle
import android.os.Message
import android.util.Log
import android.view.View
import android.widget.ImageButton
import android.webkit.GeolocationPermissions
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AlertDialog
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.activity.enableEdgeToEdge
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.bottomnavigation.BottomNavigationView
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.VibrationEffect
import android.os.Vibrator
import androidx.core.app.NotificationCompat
import android.os.Build

import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException
import java.net.URLEncoder
import java.util.Locale

class WebViewActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_URL = "extra_url"
        private const val TAG = "WebViewActivity"

        // Consider moving this secret to BuildConfig for production.
        private const val CONTACT_ENDPOINT = "https://timerhaven.com/api/contact.php"

        private val JSON_MEDIA_TYPE = "application/json; charset=utf-8".toMediaType()
        private const val REQ_NOTIFICATIONS = 9137
    }

    private lateinit var webView: WebView
    private lateinit var adView: AdView
    private lateinit var progress: ProgressBar

    private lateinit var permissionLauncher: ActivityResultLauncher<Array<String>>
    private var pendingGeoOrigin: String? = null
    private var pendingGeoCallback: GeolocationPermissions.Callback? = null

    private val httpClient = OkHttpClient()
	private var lastLoadedUrl: String = ""
    private var notificationPermissionAsked = false

    // Injection snippets removed - no longer needed for offline tools mode

    @SuppressLint("SetJavaScriptEnabled")
    @Suppress("DEPRECATION")
    override fun onCreate(savedInstanceState: Bundle?) {
        // Draw edge-to-edge on every Android version instead of relying on the
        // API 36 platform enforcement, then inset the content below.
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_webview)

        val mainLayout = findViewById<View>(R.id.main_layout)
        ViewCompat.setOnApplyWindowInsetsListener(mainLayout) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.updatePadding(
                left = systemBars.left,
                top = systemBars.top,
                right = systemBars.right,
                bottom = systemBars.bottom
            )
            insets
        }

        adView = findViewById(R.id.adView)
        
        // Check if user is Pro and hide ads
        val isPro = SubscriptionManager.isPremiumActive(this)
        if (isPro) {
            adView.visibility = View.GONE
            Log.d(TAG, "Pro user - ads hidden")
        } else {
            val adRequest = AdRequest.Builder().build()
            adView.loadAd(adRequest)
            Log.d(TAG, "Free user - loading ads")
        }

        WebView.setWebContentsDebuggingEnabled(true)

        permissionLauncher = registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            val fine = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false
            val coarse = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false
            val granted = fine || coarse

            pendingGeoOrigin?.let { origin ->
                try {
                    pendingGeoCallback?.invoke(origin, granted, false)
                } catch (e: Exception) {
                    Log.w(TAG, "Error invoking pending geolocation callback", e)
                } finally {
                    pendingGeoOrigin = null
                    pendingGeoCallback = null
                }
            }
        }

        try {
            val toolbar = findViewById<MaterialToolbar>(R.id.topAppBar)
            setSupportActionBar(toolbar)  // Enable menu to appear
            
            val dismissible = intent?.getBooleanExtra("dismissible", false) ?: false
            toolbar?.let { tb ->
                fun removeNav() {
                    try {
                        tb.navigationIcon = null
                        tb.setNavigationOnClickListener(null)
                        tb.navigationContentDescription = null
                        for (i in 0 until tb.childCount) {
                            val child = tb.getChildAt(i)
                            if (child is ImageButton) child.visibility = View.GONE
                        }
                    } catch (e: Exception) {
                        Log.w(TAG, "Error clearing toolbar nav", e)
                    }
                }
                if (!dismissible) {
                    removeNav()
                    tb.post { removeNav() }
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "Toolbar adjustment failed", e)
        }

        progress = findViewById<ProgressBar>(R.id.progressBar)
        webView = findViewById<WebView>(R.id.webview)

        val settings: WebSettings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.javaScriptCanOpenWindowsAutomatically = true
        settings.setSupportMultipleWindows(true)
        settings.loadsImagesAutomatically = true
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        settings.allowFileAccess = true
        settings.allowContentAccess = true
        settings.allowFileAccessFromFileURLs = true
        settings.allowUniversalAccessFromFileURLs = true
        settings.setGeolocationEnabled(true)
        
        // Use default caching for fast local asset loading
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        
        // Ensure media playback doesn't require extra user gesture interaction
        settings.mediaPlaybackRequiresUserGesture = false


        webView.addJavascriptInterface(ClipboardBridge(this@WebViewActivity), "AndroidClipboard")
        webView.addJavascriptInterface(JSBridge(), "AndroidBridge")
        webView.addJavascriptInterface(CloudSyncBridge(this@WebViewActivity, webView), "TimerHavenSync")

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url?.toString() ?: return false
                val lower = url.lowercase()
                // Let WebView handle http(s) and local asset links; only intercept non-http schemes
                return if (lower.startsWith("http://") || 
                    lower.startsWith("https://") || 
                    lower.startsWith("file:///android_asset/") || 
                    lower.startsWith("file:///android_res/")) {
                    false
                } else {
                    handleUrl(url)
                }
            }

            @Suppress("OverridingDeprecatedMember")
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                val u = url ?: return false
                val lower = u.lowercase()
                return if (lower.startsWith("http://") || 
                    lower.startsWith("https://") || 
                    lower.startsWith("file:///android_asset/")) {
                    false
                } else {
                    handleUrl(u)
                }
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                val u = url ?: ""
                lastLoadedUrl = u
                Log.d(TAG, "Page finished loading: $u")
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progress.visibility = if (newProgress >= 100) View.GONE else View.VISIBLE
                progress.progress = newProgress
            }

            override fun onConsoleMessage(consoleMessage: android.webkit.ConsoleMessage?): Boolean {
                Log.d("WebViewConsole", "[${consoleMessage?.messageLevel()}] ${consoleMessage?.message()} -- From line ${consoleMessage?.lineNumber()} of ${consoleMessage?.sourceId()}")
                return true
            }

            override fun onCreateWindow(view: WebView?, isDialog: Boolean, isUserGesture: Boolean, resultMsg: Message?): Boolean {
                val newWebView = WebView(this@WebViewActivity).apply {
                    settings.javaScriptEnabled = true
                    settings.domStorageEnabled = true
                    settings.javaScriptCanOpenWindowsAutomatically = true
                    settings.setSupportMultipleWindows(true)
                    webViewClient = object : WebViewClient() {
                        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                            val url = request?.url?.toString() ?: return false
                            val lower = url.lowercase()
                            if (lower.startsWith("http://") || lower.startsWith("https://")) {
                                this@WebViewActivity.runOnUiThread {
                                    try { this@WebViewActivity.webView.loadUrl(url) } catch (_: Exception) {}
                                }
                                return true
                            } else {
                                return handleUrl(url)
                            }
                        }

                        @Suppress("OverridingDeprecatedMember")
                        override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                            val u = url ?: return false
                            val lower = u.lowercase()
                            if (lower.startsWith("http://") || lower.startsWith("https://")) {
                                this@WebViewActivity.runOnUiThread {
                                    try { this@WebViewActivity.webView.loadUrl(u) } catch (_: Exception) {}
                                }
                                return true
                            } else {
                                return handleUrl(u)
                            }
                        }
                    }
                }

                return try {
                    val transport = resultMsg?.obj as? WebView.WebViewTransport
                    transport?.webView = newWebView
                    resultMsg?.sendToTarget()
                    true
                } catch (e: Exception) {
                    Log.w(TAG, "onCreateWindow transport failed", e)
                    false
                }
            }

            override fun onGeolocationPermissionsShowPrompt(origin: String, callback: GeolocationPermissions.Callback) {
                runOnUiThread {
                    try {
                        Toast.makeText(this@WebViewActivity, "Page requested location access", Toast.LENGTH_SHORT).show()
                    } catch (e: Exception) {
                        Log.w(TAG, "toast failed", e)
                    }
                }

                if (ContextCompat.checkSelfPermission(this@WebViewActivity, Manifest.permission.ACCESS_FINE_LOCATION)
                    == PackageManager.PERMISSION_GRANTED) {
                    callback.invoke(origin, true, false)
                } else {
                    pendingGeoOrigin = origin
                    pendingGeoCallback = callback
                    permissionLauncher.launch(
                        arrayOf(
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                        )
                    )
                }
            }
        }

        val url = ToolCatalog.resolveLaunchUrl(intent)
            ?: intent?.getStringExtra(EXTRA_URL)
            ?: ToolCatalog.homeUrl()
        webView.loadUrl(url)

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) webView.goBack() else finish()
            }
        })
    }

    private fun handleUrl(url: String): Boolean {
        Log.d(TAG, "handleUrl called: $url")
        val lower = url.lowercase()
        return try {
            when {
                // mailto: -> open contact page in webview (prefer site form)
                lower.startsWith("mailto:") -> {
                    try {
                        val mailTo = try { MailTo.parse(url) } catch (e: Exception) { null }
                        val to = mailTo?.to ?: ""
                        val subject = mailTo?.subject ?: ""
                        val body = mailTo?.body ?: ""

                        // Load contact.html (site form); do not rely on query params if the form doesn't support them
                        val contactPage = "https://timerhaven.com/contact.html"

                        this@WebViewActivity.runOnUiThread {
                            try {
                                webView.loadUrl(contactPage)
                            } catch (e: Exception) {
                                Log.w(TAG, "Failed to load contact page, falling back to showContactFallbackDialog", e)
                                showContactFallbackDialog("", to, body)
                            }
                        }
                    } catch (e: Exception) {
                        Log.w(TAG, "mailto handling failed", e)
                        runOnUiThread {
                            showContactFallbackDialog("", "", "")
                        }
                    }
                    true
                }

                lower.startsWith("tel:") -> {
                    startActivity(Intent(Intent.ACTION_DIAL, url.toUri()))
                    true
                }

                lower.startsWith("http://") || 
                lower.startsWith("https://") || 
                lower.startsWith("file:///android_asset/") -> {
                    false
                }

                else -> {
                    val intent = Intent(Intent.ACTION_VIEW, url.toUri())
                    if (intent.resolveActivity(packageManager) != null) {
                        startActivity(intent)
                    } else {
                        Toast.makeText(this, "No app to handle this link", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
            }
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(this, "No application found to handle this action", Toast.LENGTH_SHORT).show()
            true
        } catch (e: Exception) {
            Log.w(TAG, "handleUrl failed for $url", e)
            true
        }
    }

    override fun onDestroy() {
        try {
            webView.stopLoading()
            webView.clearHistory()
            webView.removeAllViews()
            webView.destroy()
        } catch (e: Exception) {
            Log.w(TAG, "Error destroying WebView", e)
        }
        super.onDestroy()
    }

    inner class ClipboardBridge(private val ctx: Context) {
        private val clip = ctx.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

        @JavascriptInterface
        fun readText(): String {
            return try {
                val c = clip.primaryClip
                if (c != null && c.itemCount > 0) {
                    c.getItemAt(0).coerceToText(ctx).toString()
                } else {
                    ""
                }
            } catch (e: Exception) {
                Log.w(TAG, "clipboard read failed", e)
                ""
            }
        }

        @JavascriptInterface
        fun writeText(text: String) {
            try {
                val cd = ClipData.newPlainText("timerhaven", text)
                clip.setPrimaryClip(cd)
            } catch (e: Exception) {
                Log.w(TAG, "clipboard write failed", e)
            }
        }
    }

    inner class JSBridge {
        @JavascriptInterface
        fun openLink(url: String) {
            runOnUiThread {
                try {
                    if (url.isBlank()) return@runOnUiThread
                    val lower = url.lowercase()
                    if (lower.startsWith("http://") || lower.startsWith("https://")) {
                        try {
                            webView.loadUrl(url)
                        } catch (e: Exception) {
                            Log.w(TAG, "Failed to load url in WebView, falling back to external handler: $url", e)
                            handleUrl(url)
                        }
                    } else {
                        handleUrl(url)
                    }
                } catch (e: Exception) {
                    Log.w(TAG, "JSBridge.openLink failed for $url", e)
                    try { handleUrl(url) } catch (_: Exception) {}
                }
            }
        }

        @JavascriptInterface
        fun submitContact(jsonString: String) {
            try {
// --- SUBMIT GUARD: only allow submissions coming from contact pages ---
val currentUrl = try { webView.url ?: lastLoadedUrl ?: "" } catch (e: Exception) { lastLoadedUrl ?: "" }
if (currentUrl.isNullOrEmpty()) return

// Strictly require 'contact' in the URL before we even look at the payload
if (!currentUrl.contains("contact", ignoreCase = true)) {
    Log.d(TAG, "submitContact ignored: url does not contain 'contact'. currentUrl=$currentUrl")
    return
}

// Extra safety: block known tool pages even if they have 'contact' (unlikely but possible)
val disallowedToolMarkers = listOf("calendar", "habit", "notes", "checklist", "clipboard", "clips", "clipboard-manager", "timer", "stopwatch", "pomodoro", "password")
if (disallowedToolMarkers.any { currentUrl.contains(it, ignoreCase = true) }) {
    Log.d(TAG, "submitContact ignored: request from tool page. currentUrl=$currentUrl")
    return
}
// --- END GUARD ---

                Log.d(TAG, "submitContact called with payload: $jsonString")

                val obj = JSONObject(jsonString)
                val name = obj.optString("name", "").trim()
                val email = obj.optString("email", "").trim()
                val message = obj.optString("message", "").trim()
                val pageUrlFromJs = obj.optString("pageUrl").takeIf { it.isNotEmpty() }
                val userAgent = obj.optString("userAgent", "")

                // Also fetch current webview URL if JS didn't provide one
                // val currentUrl = try { webView.url ?: "" } catch (e: Exception) { "" }

                // Decide whether this is a genuine contact-page submission:
                val effectivePageUrl = pageUrlFromJs ?: currentUrl
                val pageLooksLikeContact = effectivePageUrl.contains("contact", ignoreCase = true)

                if (!pageLooksLikeContact && name.isBlank() && email.isBlank() && message.isBlank()) {
                    Log.d(TAG, "submitContact ignored: not from contact page and payload empty or trivial. page=$effectivePageUrl")
                    return
                }

                if (!pageLooksLikeContact && message.length < 3 && email.isBlank() && name.isBlank()) {
                    Log.d(TAG, "submitContact ignored: tiny payload not from contact page. messageLen=${message.length}")
                    return
                }

                fun buildAndSend(pageUrlValue: String) {
                    val requestJson = JSONObject().apply {
                        put("name", name)
                        put("email", email)
                        put("message", message)
                        put("pageUrl", pageUrlValue)
                        put("userAgent", userAgent)
                    }
                    sendContactRequest(requestJson.toString(), name, email, message)
                }

                if (!pageUrlFromJs.isNullOrEmpty()) {
                    buildAndSend(pageUrlFromJs)
                } else {
                    runOnUiThread {
                        val cur = try { webView.url ?: "" } catch (e: Exception) { "" }
                        buildAndSend(cur)
                    }
                }
            } catch (e: Exception) {
                Log.w(TAG, "submitContact parse failed", e)
                runOnUiThread {
                    Toast.makeText(this@WebViewActivity, "Failed to read form data", Toast.LENGTH_SHORT).show()
                }
            }
        }

        @JavascriptInterface
        fun onTimerEnd(title: String, message: String) {
            runOnUiThread {
                showNativeNotification(title, message)
                triggerVibration()
            }
        }

        /** Mirrors a Pomodoro session started on the page into the notification, widget and service. */
        @JavascriptInterface
        fun timerStart(workMin: Int, breakMin: Int, phase: String, remainingSec: Int) {
            runOnUiThread {
                ensureNotificationPermission()
                PomodoroTimer.start(this@WebViewActivity, workMin, breakMin, phase, remainingSec)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        @JavascriptInterface
        fun timerPause() {
            runOnUiThread {
                PomodoroTimer.pause(this@WebViewActivity)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        @JavascriptInterface
        fun timerResume() {
            runOnUiThread {
                PomodoroTimer.resume(this@WebViewActivity)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        @JavascriptInterface
        fun timerReset() {
            runOnUiThread {
                PomodoroTimer.reset(this@WebViewActivity)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        @JavascriptInterface
        fun timerSetLengths(workMin: Int, breakMin: Int, phase: String) {
            runOnUiThread {
                PomodoroTimer.setLengths(this@WebViewActivity, workMin, breakMin, phase)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        /** JSON snapshot so the page can pick a running session back up after a relaunch. */
        @JavascriptInterface
        fun timerState(): String = PomodoroTimer.snapshot(this@WebViewActivity).toJson()

        @JavascriptInterface
        fun timerStop() {
            runOnUiThread {
                PomodoroTimerService.stop(this@WebViewActivity)
                PomodoroTimer.refresh(this@WebViewActivity)
                PomodoroWidgetProvider.updateAll(this@WebViewActivity)
            }
        }

        @JavascriptInterface
        fun vibratePhone() {
            runOnUiThread {
                triggerVibration()
            }
        }
    }

    private fun requestPomodoroWidget() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            Toast.makeText(this, "Widgets need Android 8 or newer. Long-press your home screen instead.", Toast.LENGTH_LONG).show()
            return
        }
        try {
            val manager = android.appwidget.AppWidgetManager.getInstance(this)
            val provider = android.content.ComponentName(this, PomodoroWidgetProvider::class.java)
            if (!manager.isRequestPinAppWidgetSupported) {
                Toast.makeText(this, "Long-press your home screen and pick Widgets to add the Pomodoro widget.", Toast.LENGTH_LONG).show()
                return
            }
            val added = manager.requestPinAppWidget(provider, null, null)
            if (!added) {
                Toast.makeText(this, "Long-press your home screen and pick Widgets to add the Pomodoro widget.", Toast.LENGTH_LONG).show()
            }
        } catch (e: Exception) {
            Log.w(TAG, "requestPinAppWidget failed", e)
            Toast.makeText(this, "Long-press your home screen and pick Widgets to add the Pomodoro widget.", Toast.LENGTH_LONG).show()
        }
    }

    private fun ensureNotificationPermission() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) return
        val granted = ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.POST_NOTIFICATIONS
        ) == PackageManager.PERMISSION_GRANTED
        if (!granted && !notificationPermissionAsked) {
            notificationPermissionAsked = true
            try {
                requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), REQ_NOTIFICATIONS)
            } catch (e: Exception) {
                Log.w(TAG, "POST_NOTIFICATIONS request failed", e)
            }
        }
    }

    private fun showNativeNotification(title: String, message: String) {
        val channelId = "timer_notifications"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, "Timer Alerts", NotificationManager.IMPORTANCE_HIGH)
            manager.createNotificationChannel(channel)
        }

        val builder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.ic_timer)
            .setContentTitle(title)
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)

        manager.notify(1001, builder.build())
    }

    private fun triggerVibration() {
        val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vibratorManager = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as android.os.VibratorManager
            vibratorManager.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE))
        } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(500)
        }
    }

    private fun sendContactRequest(jsonBody: String, name: String, email: String, message: String) {
        val body = jsonBody.toRequestBody(JSON_MEDIA_TYPE)
        val request = Request.Builder()
            .url(CONTACT_ENDPOINT)
            .addHeader("Content-Type", "application/json")
            .addHeader("X-Contact-Secret", BuildConfig.CONTACT_SECRET)
            .post(body)
            .build()

        httpClient.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    showContactFallbackDialog(name, email, message)
                }
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (response.isSuccessful) {
                        runOnUiThread {
                            Toast.makeText(this@WebViewActivity, "Message sent — thank you!", Toast.LENGTH_SHORT).show()
                            val thankYouHtml = """
                                <html>
                                  <head>
                                    <meta name="viewport" content="width=device-width,initial-scale=1" />
                                    <style>
                                      body { font-family: sans-serif; padding: 24px; text-align: center; }
                                      h1 { color: #2c6bed; }
                                      p { color: #333; }
                                      .btn { display:inline-block; margin-top:20px; padding:10px 18px; background:#2c6bed; color:#fff; border-radius:6px; text-decoration:none; }
                                    </style>
                                  </head>
                                  <body>
                                    <h1>Thank you</h1>
                                    <p>Your message was sent successfully. We'll get back to you soon.</p>
                                    <a href="javascript:window.history.back()" class="btn">Return</a>
                                  </body>
                                </html>
                            """.trimIndent()
                            webView.loadDataWithBaseURL(null, thankYouHtml, "text/html", "utf-8", null)
                        }
                    } else {
                        runOnUiThread {
                            showContactFallbackDialog(name, email, message)
                        }
                    }
                }
            }
        })
    }

    private fun showContactFallbackDialog(name: String, email: String, message: String) {
        try {
            val builder = AlertDialog.Builder(this@WebViewActivity)
                .setTitle("Can't send message")
                .setMessage("We couldn't send your message automatically. Choose an action:")
                .setCancelable(true)
                .setPositiveButton("Open mail app") { _, _ ->
                    openMailClientFallback(name, email, message)
                }
                .setNeutralButton("Copy email") { _, _ ->
                    try {
                        val cb = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("email", "support@timerhaven.com")
                        cb.setPrimaryClip(clip)
                        Toast.makeText(this@WebViewActivity, "Support email copied to clipboard", Toast.LENGTH_SHORT).show()
                    } catch (e: Exception) {
                        Toast.makeText(this@WebViewActivity, "Unable to copy email", Toast.LENGTH_SHORT).show()
                    }
                }
                .setNegativeButton("Open contact page") { _, _ ->
                    try {
                        webView.loadUrl("https://timerhaven.com/contact.html")
                    } catch (e: Exception) {
                        Toast.makeText(this@WebViewActivity, "Unable to open contact page", Toast.LENGTH_SHORT).show()
                    }
                }

            runOnUiThread {
                try {
                    builder.show()
                } catch (e: Exception) {
                    Toast.makeText(this@WebViewActivity, "Unable to send message. Support: support@timerhaven.com", Toast.LENGTH_LONG).show()
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "showContactFallbackDialog failed", e)
            Toast.makeText(this@WebViewActivity, "Unable to send message. Support: support@timerhaven.com", Toast.LENGTH_LONG).show()
        }
    }

    private fun openMailClientFallback(name: String, email: String, message: String) {
        val subject = "Contact from TimerHaven App"
        val body = StringBuilder()
            .append("Name: ").append(name).append("\n")
            .append("Email: ").append(email).append("\n\n")
            .append(message).toString()

        val uri = "mailto:support@timerhaven.com".toUri().buildUpon()
            .appendQueryParameter("subject", subject)
            .appendQueryParameter("body", body)
            .build()

        val intent = Intent(Intent.ACTION_SENDTO, uri)
        try {
            startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(this, "No mail client available", Toast.LENGTH_SHORT).show()
        }
    }

    /** Pins the tool currently on screen, or asks which tool when the menu is open. */
    private fun pinCurrentToolOrAsk() {
        val current = try { webView.url } catch (e: Exception) { null } ?: lastLoadedUrl
        val tool = ToolCatalog.byUrl(current)
        if (tool != null) {
            ToolShortcuts.requestPin(this, tool)
            return
        }

        val tools = ToolCatalog.tools
        val labels = tools.map { it.title }.toTypedArray()
        AlertDialog.Builder(this)
            .setTitle(R.string.pin_tool_dialog_title)
            .setItems(labels) { _, which ->
                tools.getOrNull(which)?.let { ToolShortcuts.requestPin(this, it) }
            }
            .setNegativeButton(android.R.string.cancel, null)
            .show()
    }

    // injectContactFormInterceptorToView removed - no longer needed
    override fun onCreateOptionsMenu(menu: android.view.Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_webview, menu)

        // Hide upgrade button if user is already Pro
        val upgradeItem = menu?.findItem(R.id.action_upgrade)
        val isPro = SubscriptionManager.isPremiumActive(this)
        upgradeItem?.isVisible = !isPro

        return true
    }

    override fun onOptionsItemSelected(item: android.view.MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_pin_tool -> {
                pinCurrentToolOrAsk()
                true
            }
            R.id.action_pomodoro_widget -> {
                requestPomodoroWidget()
                true
            }
            R.id.action_upgrade -> {
                // Open PaywallActivity
                val intent = Intent(this, PaywallActivity::class.java)
                startActivity(intent)
                true
            }
            R.id.action_settings -> {
                // Open SettingsActivity
                val intent = Intent(this, SettingsActivity::class.java)
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}