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
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import com.google.android.material.appbar.MaterialToolbar

import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException

class WebViewActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_URL = "extra_url"
        private const val TAG = "WebViewActivity"

        // Consider moving this secret to BuildConfig for production.
        private const val CONTACT_ENDPOINT = "https://timerhaven.com/api/contact.php"
        private const val CONTACT_SECRET = "469b5d7e1ef245d7b82185dda0572841cf7fdd9d223148f0b8debb90bcb9697f"

        private val JSON_MEDIA_TYPE = "application/json; charset=utf-8".toMediaType()
    }

    private lateinit var webView: WebView
    private lateinit var progress: ProgressBar

    private lateinit var permissionLauncher: ActivityResultLauncher<Array<String>>
    private var pendingGeoOrigin: String? = null
    private var pendingGeoCallback: GeolocationPermissions.Callback? = null

    private val httpClient = OkHttpClient()

    // Compact per-page injection snippets (kept behavioral)
    private val calendarInjectionReplace = """(function(){ try{ if (!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro')||document.querySelector('.tool-intro-in-card'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Quick access to scheduling — <a href="/en/calendar-planning/calendar-planning-index.html">Read full guide</a></p>'; }catch(e){} } var table=document.getElementById('calendar-table')||document.querySelector('.calendar-table'); if(table){ try{ table.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'calendar:applied'; } return 'calendar:applied-no-table'; }catch(e){ return 'calendar:error:'+e.toString(); }})();""".trimIndent()

    private val clipboardScrollJs = """(function(){ try{ var el=document.getElementById('clipboardForm')||document.getElementById('clips-list')||document.querySelector('.clipboard-form'); if(el){ el.scrollIntoView({behavior:'auto', block:'start'}); return 'clipboard:scrolled'; } return 'clipboard:tool-not-found'; }catch(e){ return 'clipboard:error:'+e.toString(); }})();""".trimIndent()

    private val countdownScrollJs = """(function(){ try{ var el=document.getElementById('display')||document.getElementById('minutes')||document.querySelector('.countdown-row'); if(el){ el.scrollIntoView({behavior:'auto', block:'start'}); return 'countdown:scrolled'; } return 'countdown:tool-not-found'; }catch(e){ return 'countdown:error:'+e.toString(); }})();""".trimIndent()

    private val currencyInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Quick currency checks — <a href="/en/currency-converter/currency-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('currencyForm')||document.querySelector('.converter-section')||document.getElementById('result'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'currency:applied'; } return 'currency:applied-no-tool'; }catch(e){ return 'currency:error:'+e.toString(); }})();""".trimIndent()

    private val focusMusicInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro-in-card'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Play focus music — <a href="/en/focus-music/focus-music-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('music-select')||document.querySelector('.music-player'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'focus-music:applied'; } return 'focus-music:applied-no-tool'; }catch(e){ return 'focus-music:error:'+e.toString(); }})();""".trimIndent()

    private val habitTrackerInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro-in-card'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Track daily habits — <a href="/en/habit-tracker/habit-tracker-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('habitForm')||document.getElementById('habitList')||document.querySelector('.habit-section'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'habit-tracker:applied'; } return 'habit-tracker:applied-no-tool'; }catch(e){ return 'habit-tracker:error:'+e.toString(); }})();""".trimIndent()

    private val meetingInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro')||document.querySelector('.tool-intro-in-card'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Plan meetings & choose times — <a href="/en/meeting-planner/meeting-planner-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('meetingForm')||document.getElementById('meetingTimes')||document.getElementById('participantList'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'meeting:applied'; } return 'meeting:applied-no-tool'; }catch(e){ return 'meeting:error:'+e.toString(); }})();""".trimIndent()

    private val notesInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro')||document.querySelector('.tool-intro-in-card'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Quick notes — <a href="/en/notes/notes-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('noteInput')||document.getElementById('notesList')||document.querySelector('.notes-section'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'notes:applied'; } return 'notes:applied-no-tool'; }catch(e){ return 'notes:error:'+e.toString(); }})();""".trimIndent()

    private val passwordInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Generate secure passwords locally — <a href="/en/password-generator/password-generator-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('passwordForm')||document.getElementById('pwResult')||document.querySelector('.password-section'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'password:applied'; } return 'password:applied-no-tool'; }catch(e){ return 'password:error:'+e.toString(); }})();""".trimIndent()

    private val timerInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var el=document.getElementById('timerDisplay')||document.getElementById('minutes'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'timer:scrolled'; } return 'timer:no-tool'; }catch(e){ return 'timer:error:'+e.toString(); }})();""".trimIndent()

    private val stopwatchInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var el=document.getElementById('swDisplay')||document.getElementById('swStartBtn'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'stopwatch:scrolled'; } return 'stopwatch:no-tool'; }catch(e){ return 'stopwatch:error:'+e.toString(); }})();""".trimIndent()

    private val pomodoroInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var el=document.getElementById('pomodoroDisplay')||document.getElementById('startBtn'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'pomodoro:scrolled'; } return 'pomodoro:no-tool'; }catch(e){ return 'pomodoro:error:'+e.toString(); }})();""".trimIndent()

    private val unitConverterInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Quick unit conversions — <a href="/en/unit-converter/unit-converter-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('unitForm')||document.getElementById('unitResult')||document.querySelector('.unit-section'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'unit-converter:applied'; } return 'unit-converter:no-tool'; }catch(e){ return 'unit-converter:error:'+e.toString(); }})();""".trimIndent()

    private val weatherInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">Quick weather lookup — <a href="/en/weather/weather-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('weatherForm')||document.getElementById('weatherResult')||document.querySelector('.weather-main'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'weather:applied'; } return 'weather:no-tool'; }catch(e){ return 'weather:error:'+e.toString(); }})();""".trimIndent()

    private val worldClockInjectionReplace = """(function(){ try{ if(!location||!location.hostname||location.hostname.indexOf('timerhaven.com')===-1) return 'not-target-domain'; var intro=document.getElementById('tool-help')||document.querySelector('.tool-intro'); if(intro){ try{ intro.innerHTML='<p style="margin:0;color:#51606b;font-size:.95rem">World Clock — add cities to compare times quickly — <a href="/world-clock/world-clock-index.html">Read full guide</a></p>'; }catch(e){} } var el=document.getElementById('clockForm')||document.getElementById('clockList')||document.querySelector('.clock-main'); if(el){ try{ el.scrollIntoView({behavior:'auto', block:'start'}); }catch(e){}; return 'world-clock:applied'; } return 'world-clock:no-tool'; }catch(e){ return 'world-clock:error:'+e.toString(); }})();""".trimIndent()

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_webview)

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
            val toolbar = findViewById(R.id.topAppBar) as? MaterialToolbar
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
        settings.setGeolocationEnabled(true)

        webView.addJavascriptInterface(ClipboardBridge(this), "AndroidClipboard")
        webView.addJavascriptInterface(JSBridge(), "AndroidBridge")

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url?.toString() ?: return false
                val lower = url.lowercase()
                // Let WebView handle http(s) links; only intercept non-http schemes
                return if (lower.startsWith("http://") || lower.startsWith("https://")) {
                    false
                } else {
                    handleUrl(url)
                }
            }

            @Suppress("OverridingDeprecatedMember")
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                val u = url ?: return false
                val lower = u.lowercase()
                return if (lower.startsWith("http://") || lower.startsWith("https://")) {
                    false
                } else {
                    handleUrl(u)
                }
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                try {
                    val aggressiveMailtoInterceptor = """
                      (function(){
                        try{
                          document.addEventListener('click', function(e){
                            try {
                              var t = e.target;
                              while (t && t.tagName !== 'A') t = t.parentElement;
                              if (t && t.href && t.href.indexOf('mailto:') === 0) {
                                e.preventDefault();
                                try { AndroidBridge.openLink(t.href); } catch(err) {}
                              }
                            } catch(err) {}
                          }, true);

                          document.addEventListener('submit', function(e){
                            try {
                              var f = e.target;
                              if (!f) return;
                              var action = f.action || '';
                              if (action.indexOf('mailto:') === 0) {
                                e.preventDefault();
                                var fd = new FormData(f);
                                var parts = [];
                                fd.forEach(function(value, key){
                                  parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
                                });
                                var url = action;
                                if (parts.length > 0) {
                                  if (url.indexOf('?') === -1) url += '?' + parts.join('&');
                                  else url += '&' + parts.join('&');
                                }
                                try { AndroidBridge.openLink(url); } catch(err) {}
                              }
                            } catch(err) {}
                          }, true);

                          (function(){
                            var _open = window.open;
                            window.open = function(url){
                              try {
                                if (url && String(url).indexOf('mailto:') === 0) {
                                  try { AndroidBridge.openLink(url); } catch(e){}
                                  return null;
                                }
                              } catch(e){}
                              return _open.apply(window, arguments);
                            };
                          })();

                          (function(){
                            var _assign = window.location.assign;
                            var _replace = window.location.replace;
                            window.location.assign = function(url){
                              try {
                                if (url && String(url).indexOf('mailto:') === 0) {
                                  try { AndroidBridge.openLink(url); } catch(e){}
                                  return;
                                }
                              } catch(e){}
                              return _assign.apply(window.location, arguments);
                            };
                            window.location.replace = function(url){
                              try {
                                if (url && String(url).indexOf('mailto:') === 0) {
                                  try { AndroidBridge.openLink(url); } catch(e){}
                                  return;
                                }
                              } catch(e){}
                              return _replace.apply(window.location, arguments);
                            };
                          })();
                        }catch(e){}
                      })();
                    """.trimIndent()
                    view?.evaluateJavascript(aggressiveMailtoInterceptor, null)

                    val u = url ?: ""
                    val isMobile = resources.configuration.smallestScreenWidthDp < 600
                    val forceCompact = intent?.getBooleanExtra("compact", false) ?: false
                    if (!isMobile && !forceCompact) {
                        // skip assists on large screens
                    }

                    when {
                        u.contains("/calendar-en.html") || u.endsWith("calendar-en.html") -> view?.evaluateJavascript(calendarInjectionReplace, null)
                        u.contains("/clipboard-manager-en.html") || u.endsWith("clipboard-manager-en.html") -> view?.evaluateJavascript(clipboardScrollJs, null)
                        u.contains("/countdown-en.html") || u.endsWith("countdown-en.html") -> view?.evaluateJavascript(countdownScrollJs, null)
                        u.contains("/currency-en.html") || u.endsWith("currency-en.html") -> view?.evaluateJavascript(currencyInjectionReplace, null)
                        u.contains("/focus-music-en.html") || u.endsWith("focus-music-en.html") -> view?.evaluateJavascript(focusMusicInjectionReplace, null)
                        u.contains("/habit-tracker-en.html") || u.endsWith("habit-tracker-en.html") -> view?.evaluateJavascript(habitTrackerInjectionReplace, null)
                        u.contains("/meeting-planner-en.html") || u.endsWith("meeting-planner-en.html") -> view?.evaluateJavascript(meetingInjectionReplace, null)
                        u.contains("/notes-en.html") || u.endsWith("notes-en.html") -> view?.evaluateJavascript(notesInjectionReplace, null)
                        u.contains("/password-generator-en.html") || u.endsWith("password-generator-en.html") -> view?.evaluateJavascript(passwordInjectionReplace, null)
                        u.contains("/timer-en.html") || u.endsWith("timer-en.html") -> view?.evaluateJavascript(timerInjectionReplace, null)
                        u.contains("/stopwatch-en.html") || u.endsWith("stopwatch-en.html") -> view?.evaluateJavascript(stopwatchInjectionReplace, null)
                        u.contains("/pomodoro-en.html") || u.endsWith("pomodoro-en.html") -> view?.evaluateJavascript(pomodoroInjectionReplace, null)
                        u.contains("/unit-converter-en.html") || u.endsWith("unit-converter-en.html") -> view?.evaluateJavascript(unitConverterInjectionReplace, null)
                        u.contains("/weather-en.html") || u.endsWith("weather-en.html") -> view?.evaluateJavascript(weatherInjectionReplace, null)
                        u.contains("/world-clock-en.html") || u.endsWith("world-clock-en.html") -> view?.evaluateJavascript(worldClockInjectionReplace, null)
                    }

                    try {
                        injectContactFormInterceptorToView(view)
                    } catch (e: Exception) {
                        Log.w(TAG, "injectContactFormInterceptor failed", e)
                    }
                } catch (e: Exception) {
                    Log.w(TAG, "onPageFinished injections failed", e)
                }
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progress.visibility = if (newProgress >= 100) View.GONE else View.VISIBLE
                progress.progress = newProgress
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

        val url = intent?.getStringExtra(EXTRA_URL) ?: "https://timerhaven.com/index.html"
        webView.loadUrl(url)

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) webView.goBack() else finish()
            }
        })
    }

    private fun handleUrl(url: String): Boolean {
        Log.d(TAG, "handleUrl called: $url")

        Log.d(TAG, "handleUrl: $url")
        val lower = url.lowercase()
        return try {
            when {
                lower.startsWith("mailto:") -> {
                    val mailUri = try { url.toUri() } catch (e: Exception) { null }
                    try {
                        if (mailUri != null) {
                            val sendToIntent = Intent(Intent.ACTION_SENDTO, mailUri)
                            if (sendToIntent.resolveActivity(packageManager) != null) {
                                startActivity(Intent.createChooser(sendToIntent, "Send email"))
                                return true
                            }
                        }
                    } catch (e: Exception) {
                        Log.w(TAG, "Primary mailto ACTION_SENDTO failed", e)
                    }

                    try {
                        val mailTo = try { MailTo.parse(url) } catch (e: Exception) { null }
                        val to = mailTo?.to ?: ""
                        val subject = mailTo?.subject ?: ""
                        val body = mailTo?.body ?: ""
                        val webUrl = "https://mail.google.com/mail/?view=cm&fs=1" +
                                (if (to.isNotBlank()) "&to=${Uri.encode(to)}" else "") +
                                (if (subject.isNotBlank()) "&su=${Uri.encode(subject)}" else "") +
                                (if (body.isNotBlank()) "&body=${Uri.encode(body)}" else "")
                        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(webUrl)))
                        return true
                    } catch (e: Exception) {
                        Log.w(TAG, "Web compose fallback failed", e)
                    }

                    try {
                        val mailTo = try { MailTo.parse(url) } catch (e: Exception) { null }
                        val cb = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("email", mailTo?.to ?: "")
                        cb.setPrimaryClip(clip)
                        Toast.makeText(this, "Email address copied to clipboard", Toast.LENGTH_LONG).show()
                    } catch (ignored: Exception) {
                        Toast.makeText(this, "No app available to handle this link", Toast.LENGTH_LONG).show()
                    }
                    true
                }

                lower.startsWith("tel:") -> {
                    startActivity(Intent(Intent.ACTION_DIAL, url.toUri()))
                    true
                }

                lower.startsWith("http://") || lower.startsWith("https://") -> {
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
                val obj = JSONObject(jsonString)
                val name = obj.optString("name", "")
                val email = obj.optString("email", "")
                val message = obj.optString("message", "")
                val pageUrlFromJs = obj.optString("pageUrl").takeIf { it.isNotEmpty() }
                val userAgent = obj.optString("userAgent", "")

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
                        val currentUrl = try { webView.url ?: "" } catch (e: Exception) { "" }
                        buildAndSend(currentUrl)
                    }
                }
            } catch (e: Exception) {
                Log.w(TAG, "submitContact parse failed", e)
                runOnUiThread {
                    Toast.makeText(this@WebViewActivity, "Failed to read form data", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun sendContactRequest(jsonBody: String, name: String, email: String, message: String) {
        val body = jsonBody.toRequestBody(JSON_MEDIA_TYPE)
        val request = Request.Builder()
            .url(CONTACT_ENDPOINT)
            .addHeader("Content-Type", "application/json")
            .addHeader("X-Contact-Secret", CONTACT_SECRET)
            .post(body)
            .build()

        httpClient.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@WebViewActivity, "Failed to send — opening mail app", Toast.LENGTH_SHORT).show()
                    openMailClientFallback(name, email, message)
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
                            Toast.makeText(this@WebViewActivity, "Server rejected message — opening mail app", Toast.LENGTH_SHORT).show()
                            openMailClientFallback(name, email, message)
                        }
                    }
                }
            }
        })
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

    private fun injectContactFormInterceptorToView(view: WebView?) {
        val script = """
            (function() {
                function getElValue(el) {
                    try {
                        if (!el) return "";
                        if (el.tagName === 'SELECT') return el.value || "";
                        if (typeof el.value !== 'undefined') return el.value || "";
                        if (el.getAttribute && el.getAttribute('contenteditable') === 'true') return el.innerText || "";
                        return el.textContent || "";
                    } catch (e) { return ""; }
                }

                function guessNameFor(el) {
                    try {
                        var candidates = [];
                        if (el.name) candidates.push(el.name);
                        if (el.id) candidates.push(el.id);
                        if (el.placeholder) candidates.push(el.placeholder);
                        if (el.getAttribute && el.getAttribute('aria-label')) candidates.push(el.getAttribute('aria-label'));
                        if (el.getAttribute && el.getAttribute('data-name')) candidates.push(el.getAttribute('data-name'));
                        return (candidates.join(' ') || '').toLowerCase();
                    } catch (e) { return ''; }
                }

                function detectSemanticKey(hint) {
                    if (!hint) return null;
                    hint = hint.toLowerCase();
                    if (/(^|\s)(name|your name|full name|first name|last name)/.test(hint)) return 'name';
                    if (/(^|\s)(email|e-mail|your email)/.test(hint)) return 'email';
                    if (/(^|\s)(message|comment|note|feedback|question|bug|description)/.test(hint)) return 'message';
                    return null;
                }

                function serializeFormBestEffort(form) {
                    var data = {};
                    try {
                        var inputs = Array.prototype.slice.call(form.querySelectorAll('input,textarea,select,[contenteditable=true]'));
                        inputs.forEach(function(el) {
                            var n = el.name || el.id;
                            var v = getElValue(el);
                            if (n) {
                                if (data[n] === undefined) data[n] = v;
                            }
                        });
                        inputs.forEach(function(el) {
                            var v = getElValue(el);
                            if (!v) return;
                            var hint = guessNameFor(el);
                            var key = detectSemanticKey(hint);
                            if (key && !data[key]) {
                                data[key] = v;
                            }
                        });
                        inputs.forEach(function(el) {
                            var v = getElValue(el);
                            if (!v) return;
                            var hint = (el.placeholder || '').toLowerCase();
                            var key = detectSemanticKey(hint);
                            if (key && !data[key]) data[key] = v;
                        });
                        if (!data['message']) {
                            var textareas = form.querySelectorAll('textarea');
                            if (textareas && textareas.length > 0) {
                                for (var i=0;i<textareas.length;i++) {
                                    var val = getElValue(textareas[i]);
                                    if (val && val.trim().length>0) { data['message'] = val; break; }
                                }
                            }
                        }
                        if (data['name'] === undefined) data['name'] = '';
                        if (data['email'] === undefined) data['email'] = '';
                        if (data['message'] === undefined) data['message'] = '';
                    } catch (e) {}
                    return data;
                }

                try {
                    var hooked = new WeakSet();

                    function hookForm(form) {
                        if (!form || hooked.has(form)) return;
                        hooked.add(form);

                        function handleSubmitEvent(e) {
                            try {
                                e.preventDefault();
                                if (e.stopImmediatePropagation) e.stopImmediatePropagation();

                                var payloadFields = serializeFormBestEffort(form) || {};
                                payloadFields.pageUrl = location.href;
                                payloadFields.userAgent = navigator.userAgent || '';

                                if (window.AndroidBridge && typeof window.AndroidBridge.submitContact === 'function') {
                                    try {
                                        window.AndroidBridge.submitContact(JSON.stringify(payloadFields));
                                        return;
                                    } catch (err) {}
                                }

                                try { form.submit(); } catch (x) {}
                            } catch (err) {
                                try { form.submit(); } catch (x) {}
                            }
                        }

                        form.addEventListener('submit', handleSubmitEvent, true);

                        form.addEventListener('click', function(e) {
                            try {
                                var t = e.target;
                                if (!t) return;
                                var isSubmit = false;
                                if (t.tagName === 'BUTTON') isSubmit = true;
                                var type = (t.getAttribute && t.getAttribute('type')) || '';
                                if (type && type.toLowerCase() === 'submit') isSubmit = true;
                                if (t.tagName === 'INPUT' && (t.type === 'submit' || t.type === 'image')) isSubmit = true;
                                if (isSubmit) {
                                    try { e.preventDefault(); if (e.stopImmediatePropagation) e.stopImmediatePropagation(); } catch(_) {}
                                    handleSubmitEvent(e);
                                }
                            } catch (err) {}
                        }, true);
                    }

                    var forms = document.getElementsByTagName('form');
                    for (var i = 0; i < forms.length; i++) {
                        hookForm(forms[i]);
                    }

                    var observer = new MutationObserver(function(mutations) {
                        try {
                            mutations.forEach(function(m) {
                                m.addedNodes && m.addedNodes.forEach(function(node) {
                                    try {
                                        if (!node) return;
                                        if (node.nodeType !== 1) return;
                                        if (node.tagName === 'FORM') hookForm(node);
                                        var nested = node.querySelectorAll && node.querySelectorAll('form');
                                        if (nested && nested.length) {
                                            for (var j=0;j<nested.length;j++) hookForm(nested[j]);
                                        }
                                    } catch (e) {}
                                });
                            });
                        } catch (e) {}
                    });
                    observer.observe(document.documentElement || document.body, { childList: true, subtree: true });
                } catch (e) {}
            })();
        """.trimIndent()

        view?.post {
            try {
                view.evaluateJavascript(script, null)
            } catch (ignored: Exception) {
            }
        }
    }
}