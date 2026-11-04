// TimerHaven Popup Logic
document.addEventListener('DOMContentLoaded', () => {
  // Internationalization: populate text for elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const msg = chrome.i18n.getMessage(el.getAttribute('data-i18n'));
    if (msg) el.textContent = msg;
  });

  // Add any future dynamic UI logic here (e.g., fetching active timer status)
  console.log('TimerHaven Extension Popup Loaded.');
});

// Deep link handling is done purely via <a> tags with target="_blank" in popup.html
