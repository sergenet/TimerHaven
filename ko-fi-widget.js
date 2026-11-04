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
})();
