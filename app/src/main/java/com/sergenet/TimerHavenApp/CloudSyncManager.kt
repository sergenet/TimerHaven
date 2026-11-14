package com.sergenet.TimerHavenApp

import android.content.Context
import android.util.Log
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.ListenerRegistration
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.ktx.Firebase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

class CloudSyncManager(private val context: Context) {
    private val db: FirebaseFirestore = Firebase.firestore
    private val auth: FirebaseAuth = FirebaseAuth.getInstance()
    private val coroutineScope = CoroutineScope(Dispatchers.Main)
    
    private var clipboardListener: ListenerRegistration? = null
    private var notesListener: ListenerRegistration? = null
    private var habitsListener: ListenerRegistration? = null
    private var calendarListener: ListenerRegistration? = null
    private var meetingListener: ListenerRegistration? = null
    
    companion object {
        private const val TAG = "CloudSyncManager"
        private const val COLLECTION_CLIPBOARD = "clipboard"
        private const val COLLECTION_NOTES = "notes"
        private const val COLLECTION_HABITS = "habits"
        private const val COLLECTION_TASKS = "tasks"
        private const val COLLECTION_CALENDAR = "calendar"
        private const val COLLECTION_MEETING = "meeting"
    }
    
    /**
     * Check if cloud sync is available (user is Pro and authenticated)
     */
    fun isSyncAvailable(): Boolean {
        val isPro = SubscriptionManager.isPremiumActive(context)
        val isAuthenticated = auth.currentUser != null
        return isPro && isAuthenticated
    }
    
    /**
     * Initialize cloud sync - pull all data from Firestore
     */
    suspend fun initializeSync(): JSONObject? {
        if (!isSyncAvailable()) {
            Log.d(TAG, "Sync not available - user not Pro or not authenticated")
            return null
        }
        
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Initializing cloud sync...")
                val clipboardData = fetchClipboardData()
                val notesData = fetchNotesData()
                val habitsData = fetchHabitsData()
                val tasksData = fetchTasksData()
                val calendarData = fetchCalendarData()
                val meetingData = fetchMeetingData()
                
                JSONObject().apply {
                    put("clipboard", clipboardData)
                    put("notes", notesData)
                    put("habits", habitsData)
                    put("tasks", tasksData)
                    put("calendar", calendarData)
                    put("meeting", meetingData)
                }
            } catch (e: Exception) {
                Log.e(TAG, "Failed to initialize sync", e)
                null
            }
        }
    }
    
    /**
     * Fetch clipboard data from Firestore
     */
    private suspend fun fetchClipboardData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val clips = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_CLIPBOARD).get().await()
            for (doc in snapshot.documents) {
                val clip = JSONObject().apply {
                    put("id", doc.id)
                    put("text", doc.getString("text") ?: "")
                    put("timestamp", doc.getLong("timestamp") ?: 0)
                }
                clips.put(clip)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchClipboardData error", e) }
        return clips
    }

    private suspend fun fetchNotesData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val notes = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_NOTES).get().await()
            for (doc in snapshot.documents) {
                val note = JSONObject().apply {
                    put("id", doc.id)
                    put("title", doc.getString("title") ?: "")
                    put("content", doc.getString("content") ?: "")
                    put("updatedAt", doc.getLong("updatedAt") ?: 0)
                }
                notes.put(note)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchNotesData error", e) }
        return notes
    }

    private suspend fun fetchHabitsData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val habits = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_HABITS).get().await()
            for (doc in snapshot.documents) {
                val habit = JSONObject(doc.getString("data") ?: "{}")
                habit.put("id", doc.id)
                habits.put(habit)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchHabitsData error", e) }
        return habits
    }

    private suspend fun fetchTasksData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val tasks = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_TASKS).get().await()
            for (doc in snapshot.documents) {
                val task = JSONObject(doc.getString("data") ?: "{}")
                task.put("id", doc.id)
                tasks.put(task)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchTasksData error", e) }
        return tasks
    }

    private suspend fun fetchCalendarData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val calendar = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_CALENDAR).get().await()
            for (doc in snapshot.documents) {
                val item = JSONObject(doc.getString("data") ?: "{}")
                item.put("id", doc.id)
                calendar.put(item)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchCalendarData error", e) }
        return calendar
    }

    private suspend fun fetchMeetingData(): JSONArray {
        val userId = auth.currentUser?.uid ?: return JSONArray()
        val meetings = JSONArray()
        try {
            val snapshot = db.collection("users").document(userId).collection(COLLECTION_MEETING).get().await()
            for (doc in snapshot.documents) {
                val item = JSONObject(doc.getString("data") ?: "{}")
                item.put("id", doc.id)
                meetings.put(item)
            }
        } catch (e: Exception) { Log.e(TAG, "fetchMeetingData error", e) }
        return meetings
    }
    
    /**
     * Save clipboard item to cloud
     */
    fun saveClipboardItem(id: String, text: String, timestamp: Long) {
        if (!isSyncAvailable()) return
        
        val userId = auth.currentUser?.uid ?: return
        
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val clipData = hashMapOf(
                    "text" to text,
                    "timestamp" to timestamp,
                    "updatedAt" to System.currentTimeMillis()
                )
                
                db.collection("users")
                    .document(userId)
                    .collection(COLLECTION_CLIPBOARD)
                    .document(id)
                    .set(clipData)
                    .await()
                
                Log.d(TAG, "Saved clipboard item to cloud: $id")
            } catch (e: Exception) {
                Log.e(TAG, "Failed to save clipboard item", e)
            }
        }
    }
    
    /**
     * Delete clipboard item from cloud
     */
    fun deleteClipboardItem(id: String) {
        if (!isSyncAvailable()) return
        
        val userId = auth.currentUser?.uid ?: return
        
        coroutineScope.launch(Dispatchers.IO) {
            try {
                db.collection("users")
                    .document(userId)
                    .collection(COLLECTION_CLIPBOARD)
                    .document(id)
                    .delete()
                    .await()
                
                Log.d(TAG, "Deleted clipboard item from cloud: $id")
            } catch (e: Exception) {
                Log.e(TAG, "Failed to delete clipboard item", e)
            }
        }
    }
    
    /**
     * Delete note from cloud
     */
    fun deleteNote(id: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                db.collection("users").document(userId).collection(COLLECTION_NOTES).document(id).delete().await()
                Log.d(TAG, "Deleted note from cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to delete note", e) }
        }
    }

    /**
     * Save/Update note to cloud
     */
    fun saveNote(id: String, title: String, content: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val noteData = hashMapOf(
                    "title" to title,
                    "content" to content,
                    "updatedAt" to System.currentTimeMillis()
                )
                db.collection("users").document(userId).collection(COLLECTION_NOTES).document(id).set(noteData).await()
                Log.d(TAG, "Saved note to cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to save note", e) }
        }
    }

    /**
     * Save/Update habit to cloud
     */
    fun saveHabit(id: String, habitJson: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val habitData = hashMapOf(
                    "data" to habitJson,
                    "updatedAt" to System.currentTimeMillis()
                )
                db.collection("users").document(userId).collection(COLLECTION_HABITS).document(id).set(habitData).await()
                Log.d(TAG, "Saved habit to cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to save habit", e) }
        }
    }

    /**
     * Delete habit from cloud
     */
    fun deleteHabit(id: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                db.collection("users").document(userId).collection(COLLECTION_HABITS).document(id).delete().await()
                Log.d(TAG, "Deleted habit from cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to delete habit", e) }
        }
    }

    /**
     * Save task session to cloud
     */
    fun saveTaskSession(id: String, sessionJson: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val sessionData = hashMapOf(
                    "data" to sessionJson,
                    "timestamp" to System.currentTimeMillis()
                )
                db.collection("users").document(userId).collection(COLLECTION_TASKS).document(id).set(sessionData).await()
                Log.d(TAG, "Saved task session to cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to save task session", e) }
        }
    }

    /**
     * Save calendar data to cloud
     */
    fun saveCalendarData(id: String, dataJson: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val docData = hashMapOf(
                    "data" to dataJson,
                    "updatedAt" to System.currentTimeMillis()
                )
                db.collection("users").document(userId).collection(COLLECTION_CALENDAR).document(id).set(docData).await()
                Log.d(TAG, "Saved calendar item to cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to save calendar item", e) }
        }
    }

    /**
     * Delete calendar data from cloud
     */
    fun deleteCalendarData(id: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                db.collection("users").document(userId).collection(COLLECTION_CALENDAR).document(id).delete().await()
                Log.d(TAG, "Deleted calendar item from cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to delete calendar item", e) }
        }
    }

    /**
     * Save meeting data to cloud
     */
    fun saveMeetingData(id: String, dataJson: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                val docData = hashMapOf(
                    "data" to dataJson,
                    "updatedAt" to System.currentTimeMillis()
                )
                db.collection("users").document(userId).collection(COLLECTION_MEETING).document(id).set(docData).await()
                Log.d(TAG, "Saved meeting item to cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to save meeting item", e) }
        }
    }

    /**
     * Delete meeting data from cloud
     */
    fun deleteMeetingData(id: String) {
        if (!isSyncAvailable()) return
        val userId = auth.currentUser?.uid ?: return
        coroutineScope.launch(Dispatchers.IO) {
            try {
                db.collection("users").document(userId).collection(COLLECTION_MEETING).document(id).delete().await()
                Log.d(TAG, "Deleted meeting item from cloud: $id")
            } catch (e: Exception) { Log.e(TAG, "Failed to delete meeting item", e) }
        }
    }
    
    /**
     * Enable real-time sync listeners
     */
    fun enableRealtimeSync(onDataChanged: () -> Unit) {
        if (!isSyncAvailable()) return
        
        val userId = auth.currentUser?.uid ?: return
        
        // Listen to clipboard changes
        clipboardListener = db.collection("users")
            .document(userId)
            .collection(COLLECTION_CLIPBOARD)
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e(TAG, "Clipboard listener error", error)
                    return@addSnapshotListener
                }
                
                Log.d(TAG, "Clipboard data changed in cloud")
                onDataChanged()
            }
        // Listen to all other collections as well
        notesListener = db.collection("users").document(userId).collection(COLLECTION_NOTES)
            .addSnapshotListener { _, _ -> onDataChanged() }
        habitsListener = db.collection("users").document(userId).collection(COLLECTION_HABITS)
            .addSnapshotListener { _, _ -> onDataChanged() }
        calendarListener = db.collection("users").document(userId).collection(COLLECTION_CALENDAR)
            .addSnapshotListener { _, _ -> onDataChanged() }
        meetingListener = db.collection("users").document(userId).collection(COLLECTION_MEETING)
            .addSnapshotListener { _, _ -> onDataChanged() }
        
        Log.d(TAG, "Real-time sync enabled")
    }
    
    /**
     * Disable real-time sync listeners
     */
    fun disableRealtimeSync() {
        clipboardListener?.remove()
        notesListener?.remove()
        habitsListener?.remove()
        
        clipboardListener = null
        notesListener = null
        habitsListener = null
        calendarListener?.remove()
        meetingListener?.remove()
        calendarListener = null
        meetingListener = null
        
        Log.d(TAG, "Real-time sync disabled")
    }
}
