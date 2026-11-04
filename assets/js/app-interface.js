/**
 * TimerHaven App Interface Bridge
 * Handles communication between the website and the native Android/iOS wrappers.
 * This allows the web-based tools to trigger native notifications and haptics.
 */
(function () {
    window.TimerHavenApp = {
        /**
         * Notify the native app that a timer has finished.
         * @param {string} title - The title of the notification.
         * @param {string} message - The body text of the notification.
         */
        notifyTimerEnd: function (title, message) {
            console.log("Timer End Notification:", title, message);

            // 1. Android Native Bridge
            // The Android app provides 'AndroidBridge' via JavascriptInterface
            if (window.AndroidBridge && window.AndroidBridge.onTimerEnd) {
                try {
                    window.AndroidBridge.onTimerEnd(title, message);
                } catch (e) {
                    console.error("AndroidBridge failed:", e);
                }
            }

            // 2. iOS (React Native WebView) Bridge
            // The iOS app listens for messages via 'window.ReactNativeWebView'
            if (window.ReactNativeWebView && window.ReactNativeWebView.postMessage) {
                try {
                    window.ReactNativeWebView.postMessage(JSON.stringify({
                        type: 'timer_end',
                        title: title,
                        body: message,
                        haptic: 'success'
                    }));
                } catch (e) {
                    console.error("ReactNativeWebView bridge failed:", e);
                }
            }
        },

        /**
         * Request haptic feedback from the native device.
         * @param {string} type - 'success', 'warning', 'error', 'impactLight', etc.
         */
        triggerHaptic: function (type) {
            if (window.ReactNativeWebView && window.ReactNativeWebView.postMessage) {
                window.ReactNativeWebView.postMessage(JSON.stringify({
                    type: 'haptic',
                    effect: type || 'impactLight'
                }));
            }
        }
    };

    console.log("TimerHaven App Interface Initialized");
})();
