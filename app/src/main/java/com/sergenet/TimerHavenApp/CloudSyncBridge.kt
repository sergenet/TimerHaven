package com.sergenet.TimerHavenApp

import android.content.Context
import android.util.Log
import android.webkit.JavascriptInterface
import android.webkit.WebView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

/**
 * JavaScript bridge for cloud sync functionality
 * Allows web app to save/load data to/from Firestore
 */
class CloudSyncBridge(
    private val context: Context,
    private val webView: WebView
) {
    private val cloudSyncManager = CloudSyncManager(context)
    private val scope = CoroutineScope(Dispatchers.Main)
    
    companion object {
        private const val TAG = "CloudSyncBridge"
    }
    
    /**
     * Check if cloud sync is available (user is Pro + authenticated)
     */
    @JavascriptInterface
    fun isSyncAvailable(): Boolean {
        val available = cloudSyncManager.isSyncAvailable()
        Log.d(TAG, "isSyncAvailable called: $available")
        return available
    }
    
    /**
     * Save a clipboard item to cloud
     * Called from JavaScript: TimerHavenSync.saveClipboardItem(id, text, timestamp)
     */
    @JavascriptInterface
    fun saveClipboardItem(id: String, text: String, timestamp: Long) {
        Log.d(TAG, "saveClipboardItem: id=$id, timestamp=$timestamp")
        cloudSyncManager.saveClipboardItem(id, text, timestamp)
    }
    
    /**
     * Delete a clipboard item from cloud
     * Called from JavaScript: TimerHavenSync.deleteClipboardItem(id)
     */
    @JavascriptInterface
    fun deleteClipboardItem(id: String) {
        Log.d(TAG, "deleteClipboardItem: id=$id")
        cloudSyncManager.deleteClipboardItem(id)
    }
    
    /**
     * Save a note to cloud
     * Called from JavaScript: TimerHavenSync.saveNote(id, title, content)
     */
    @JavascriptInterface
    fun saveNote(id: String, title: String, content: String) {
        Log.d(TAG, "saveNote: id=$id, title=$title")
        cloudSyncManager.saveNote(id, title, content)
    }
    
    /**
     * Delete a note from cloud
     * Called from JavaScript: TimerHavenSync.deleteNote(id)
     */
    @JavascriptInterface
    fun deleteNote(id: String) {
        Log.d(TAG, "deleteNote: id=$id")
        cloudSyncManager.deleteNote(id)
    }

    /**
     * Save a habit to cloud
     * Called from JavaScript: TimerHavenSync.saveHabit(id, habitJson)
     */
    @JavascriptInterface
    fun saveHabit(id: String, habitJson: String) {
        Log.d(TAG, "saveHabit: id=$id")
        cloudSyncManager.saveHabit(id, habitJson)
    }

    /**
     * Delete a habit from cloud
     * Called from JavaScript: TimerHavenSync.deleteHabit(id)
     */
    @JavascriptInterface
    fun deleteHabit(id: String) {
        Log.d(TAG, "deleteHabit: id=$id")
        cloudSyncManager.deleteHabit(id)
    }

    /**
     * Save a task session to cloud
     * Called from JavaScript: TimerHavenSync.saveTaskSession(id, sessionJson)
     */
    @JavascriptInterface
    fun saveTaskSession(id: String, sessionJson: String) {
        Log.d(TAG, "saveTaskSession: id=$id")
        cloudSyncManager.saveTaskSession(id, sessionJson)
    }

    /**
     * Save calendar data to cloud
     * Called from JavaScript: TimerHavenSync.saveCalendarData(id, dataJson)
     */
    @JavascriptInterface
    fun saveCalendarData(id: String, dataJson: String) {
        Log.d(TAG, "saveCalendarData: id=$id")
        cloudSyncManager.saveCalendarData(id, dataJson)
    }

    /**
     * Delete calendar data from cloud
     * Called from JavaScript: TimerHavenSync.deleteCalendarData(id)
     */
    @JavascriptInterface
    fun deleteCalendarData(id: String) {
        Log.d(TAG, "deleteCalendarData: id=$id")
        cloudSyncManager.deleteCalendarData(id)
    }

    /**
     * Save meeting data to cloud
     * Called from JavaScript: TimerHavenSync.saveMeetingData(id, dataJson)
     */
    @JavascriptInterface
    fun saveMeetingData(id: String, dataJson: String) {
        Log.d(TAG, "saveMeetingData: id=$id")
        cloudSyncManager.saveMeetingData(id, dataJson)
    }

    /**
     * Delete meeting data from cloud
     * Called from JavaScript: TimerHavenSync.deleteMeetingData(id)
     */
    @JavascriptInterface
    fun deleteMeetingData(id: String) {
        Log.d(TAG, "deleteMeetingData: id=$id")
        cloudSyncManager.deleteMeetingData(id)
    }

    /**
     * Initialize cloud sync and pull all data
     * Called from JavaScript: TimerHavenSync.initializeSync()
     */
    @JavascriptInterface
    fun initializeSync() {
        Log.d(TAG, "initializeSync called")
        scope.launch {
            val allData = cloudSyncManager.initializeSync()
            val success = allData != null
            Log.d(TAG, "initializeSync success: $success")
            
            // Notify web app that sync completed and send data
            webView.post {
                if (allData != null) {
                    webView.evaluateJavascript(
                        "if(window.onCloudDataLoaded) window.onCloudDataLoaded(${allData.toString()});",
                        null
                    )
                }
                webView.evaluateJavascript(
                    "if(window.onSyncComplete) window.onSyncComplete($success);",
                    null
                )
            }
        }
    }
    
    /**
     * Enable real-time sync listeners
     * Called from JavaScript: TimerHavenSync.enableRealtimeSync()
     */
    @JavascriptInterface
    fun enableRealtimeSync() {
        Log.d(TAG, "enableRealtimeSync called")
        cloudSyncManager.enableRealtimeSync {
            // Data changed in cloud, notify web app to refresh
            webView.post {
                webView.evaluateJavascript(
                    "if(window.onCloudDataChanged) window.onCloudDataChanged();",
                    null
                )
            }
        }
    }
    
    /**
     * Disable real-time sync listeners
     * Called from JavaScript: TimerHavenSync.disableRealtimeSync()
     */
    @JavascriptInterface
    fun disableRealtimeSync() {
        Log.d(TAG, "disableRealtimeSync called")
        cloudSyncManager.disableRealtimeSync()
    }
    
    /**
     * Log from JavaScript for debugging
     * Called from JavaScript: TimerHavenSync.log(message)
     */
    @JavascriptInterface
    fun log(message: String) {
        Log.d(TAG, "JS Log: $message")
    }
}
