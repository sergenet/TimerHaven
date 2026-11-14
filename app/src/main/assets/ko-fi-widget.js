(function () {
    // Official Ko-fi Widget Loader
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

    // "HUNTER-KILLER" Auto-Hide Protocol (1 Minute)
    // This script actively hunts for the widget's "Fixed" container and destroys it.
    // It does not rely on specific class names sticking, but rather on the *behavior* (iframe inside a fixed container).

    setTimeout(function () {
        console.log("TimerHaven: Initiating Support Widget cleanup...");

        // 1. Find all Ko-fi related iframes
        var frames = document.querySelectorAll('iframe[src*="ko-fi.com"]');

        frames.forEach(function (frame) {
            // Traverse up to find the "fixed" container holding this iframe
            var candidate = frame;
            var destroyed = false;

            // Go up up to 5 levels to find the sticky wrapper
            for (var i = 0; i < 5; i++) {
                if (!candidate || candidate.tagName === 'BODY') break;

                var style = window.getComputedStyle(candidate);

                // If this element is the fixed container
                if (style.position === 'fixed') {
                    // This is our target. Destroy it.
                    candidate.style.display = 'none !important';
                    candidate.innerHTML = '';
                    candidate.remove();
                    destroyed = true;
                    console.log("TimerHaven: Destroyed fixed container.");
                    break;
                }
                candidate = candidate.parentElement;
            }

            // If we didn't find a wrapper but found the iframe, kill the iframe itself logic
            if (!destroyed) {
                frame.remove();
                console.log("TimerHaven: Destroyed naked iframe.");
            }
        });

        // 2. Secondary Sweep: Target known class names explicitly just in case
        var wrappers = document.querySelectorAll('.floatingchat-container-wrap, .floatingchat-container-wrap-mobi, [id*="kofi-wo-container"]');
        wrappers.forEach(function (el) {
            el.remove();
        });

    }, 60000); // 60000ms = 60 seconds

})();
