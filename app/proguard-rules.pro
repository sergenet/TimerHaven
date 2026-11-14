# JavaScript Interface Support
-keepattributes JavascriptInterface
-keepattributes Annotation
# Crashlytics needs the source file name and line numbers to render a readable
# frame list; without these every release trace collapses to "Unknown Source".
-keepattributes SourceFile,LineNumberTable

# Keep the bridge classes and their @JavascriptInterface methods
-keepclassmembers class com.sergenet.TimerHavenApp.WebViewActivity$ClipboardBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keepclassmembers class com.sergenet.TimerHavenApp.WebViewActivity$JSBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keepclassmembers class com.sergenet.TimerHavenApp.CloudSyncBridge {
    @android.webkit.JavascriptInterface <methods>;
}
