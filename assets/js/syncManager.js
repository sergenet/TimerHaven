/**
 * TimerHaven Sync Manager
 * Bridges the gap between web tools and the Android CloudSyncBridge.
 */
(function () {
    'use strict';

    const SyncManager = {
        isAvailable: function () {
            return typeof TimerHavenSync !== 'undefined' && TimerHavenSync.isSyncAvailable();
        },

        // --- Clipboard Ops ---
        saveClip: function (id, text, timestamp) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveClipboardItem(id, text, timestamp || Date.now());
        },
        deleteClip: function (id) {
            if (!this.isAvailable()) return;
            TimerHavenSync.deleteClipboardItem(id);
        },

        // --- Notes Ops ---
        saveNote: function (id, title, content) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveNote(id, title, content);
        },
        deleteNote: function (id) {
            if (!this.isAvailable()) return;
            TimerHavenSync.deleteNote(id);
        },

        // --- Habit Ops ---
        saveHabit: function (id, habitObj) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveHabit(id, JSON.stringify(habitObj));
        },
        deleteHabit: function (id) {
            if (!this.isAvailable()) return;
            TimerHavenSync.deleteHabit(id);
        },

        // --- Task Ops ---
        saveTaskSession: function (id, sessionObj) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveTaskSession(id, JSON.stringify(sessionObj));
        },
        // --- Calendar Ops ---
        saveCalendar: function (id, dataObj) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveCalendarData(id, JSON.stringify(dataObj));
        },
        deleteCalendar: function (id) {
            if (!this.isAvailable()) return;
            TimerHavenSync.deleteCalendarData(id);
        },
        // --- Meeting Ops ---
        saveMeeting: function (id, dataObj) {
            if (!this.isAvailable()) return;
            TimerHavenSync.saveMeetingData(id, JSON.stringify(dataObj));
        },
        deleteMeeting: function (id) {
            if (!this.isAvailable()) return;
            TimerHavenSync.deleteMeetingData(id);
        },

        // --- Lifecycle ---
        initialize: function () {
            if (this.isAvailable()) {
                console.log('[SyncManager] Initializing cloud sync...');
                TimerHavenSync.initializeSync();
                TimerHavenSync.enableRealtimeSync();
            }
        }
    };

    // Global listeners called by Android Bridge
    window.onCloudDataLoaded = function (data) {
        console.log('[SyncManager] Multi-collection data loaded', data);
        // Custom event for tools to listen to
        const event = new CustomEvent('timerhaven:cloudDataLoaded', { detail: data });
        window.dispatchEvent(event);
    };

    window.onCloudDataChanged = function () {
        console.log('[SyncManager] Remote data changed, refreshing...');
        const event = new CustomEvent('timerhaven:cloudDataChanged');
        window.dispatchEvent(event);
    };

    window.SyncManager = SyncManager;

    // Auto-init on load if in Android app
    if (document.readyState === 'complete') {
        SyncManager.initialize();
    } else {
        window.addEventListener('load', () => SyncManager.initialize());
    }
})();
