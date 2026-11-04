(function () {
    // 1. Load the Ko-fi Widget
    const script = document.createElement('script');
    script.src = 'https://storage.ko-fi.com/cdn/scripts/overlay-widget.js';
    script.async = true;
    script.onload = function () {
        if (typeof kofiWidgetOverlay !== 'undefined') {
            kofiWidgetOverlay.draw('sergenet', {
                'type': 'floating-chat',
                'floating-chat.donate_button.text': 'Support Me',
                'floating-chat.donate_button.background_color': '#185a9d',
                'floating-chat.donate_button.text_color': '#fff'
            });
        }
    };
    document.head.appendChild(script);

    // 2. Auto-Hide Logic (The "Hunter-Killer" V2)
    // We use a polling mechanism that waits 60 seconds, then continuously scans/destroys.

    // Start trying to remove it after 60 seconds
    setTimeout(function () {
        console.log("TimerHaven: 60s passed. Auto-hide support widget activated.");

        // We run a "cleanup" interval for a few seconds to ensure we catch it even if it re-renders
        var cleanupCount = 0;
        var cleanupInterval = setInterval(function () {
            var destroyed = false;

            // Strategy A: Target known classes
            var wrappers = document.querySelectorAll('.floatingchat-container-wrap, .floatingchat-container-wrap-mobi, [id*="kofi-wo-container"]');
            wrappers.forEach(function (el) {
                el.style.display = 'none';
                el.remove();
                destroyed = true;
            });

            // Strategy B: Find fixed iframes (The "Hunter")
            var frames = document.querySelectorAll('iframe[src*="ko-fi.com"]');
            frames.forEach(function (frame) {
                // Check if it has a fixed parent
                var candidate = frame;
                while (candidate && candidate.tagName !== 'BODY') {
                    var style = window.getComputedStyle(candidate);
                    if (style.position === 'fixed') {
                        candidate.style.display = 'none';
                        candidate.remove();
                        destroyed = true;
                        break;
                    }
                    candidate = candidate.parentElement;
                }
                // Fallback: kill iframe itself
                if (!destroyed) {
                    frame.style.display = 'none';
                    frame.remove();
                }
            });

            cleanupCount++;
            if (cleanupCount > 10) clearInterval(cleanupInterval); // Stop trying after 10 seconds of aggressive cleaning

        }, 1000); // Check every second

    }, 60000); // Wait 60 seconds before starting cleanup

})();
