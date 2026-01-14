// Centralized consent.js for TimerHaven
// - Shows consent banner (Accept / Decline / Manage)
// - Exposes window.timerhavenConsentGiven(), window.timerhavenLoadAdsAfterConsent(cb), window.timerhavenRevokeConsent()
// - Loads AdSense + GA only after consent and guards against double-load.

(function () {
  'use strict';

  var STORAGE_KEY = 'timerhavenConsent';
  var QUEUE = [];
  var ADS_LOADED_FLAG = '__timerhaven_ads_loaded';

  // Utility helpers
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function createEl(tag, attrs, html) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') el.className = attrs[k];
      else el.setAttribute(k, attrs[k]);
    });
    if (html !== undefined) el.innerHTML = html;
    return el;
  }

  // consent state functions
  function getStored() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function isGranted() {
    return getStored() === 'granted';
  }
  function isDenied() {
    return getStored() === 'denied';
  }

  function setStored(v) {
    try { localStorage.setItem(STORAGE_KEY, v); } catch (e) {}
    try { document.dispatchEvent(new CustomEvent('timerhavenConsentChanged', { detail: { consent: v === 'granted' } })); } catch (e) {}
  }

  function timerhavenConsentGiven() { return isGranted(); }

  // register callback to run after consent
  function timerhavenLoadAdsAfterConsent(cb) {
    if (typeof cb !== 'function') return;
    try {
      if (isGranted()) {
        cb();
      } else {
        QUEUE.push(cb);
      }
    } catch (e) { console.warn(e); }
  }

  // revoke consent (for testing/admin)
  function timerhavenRevokeConsent() {
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
    showBanner();
  }

  // Run queued callbacks
  function runQueue() {
    try {
      while (QUEUE.length) {
        var cb = QUEUE.shift();
        try { cb(); } catch (e) { console.warn('consent callback error', e); }
      }
    } catch (e) {}
  }

  // Load AdSense + GA (idempotent)
  function loadAdsAndAnalytics() {
    try {
      if (window[ADS_LOADED_FLAG]) return;
      window[ADS_LOADED_FLAG] = true;

      // AdSense
      if (!document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]')) {
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0467059729557007';
        s.crossOrigin = 'anonymous';
        document.head.appendChild(s);
      }

      // gtag
      if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
        var g = document.createElement('script');
        g.async = true;
        g.src = 'https://www.googletagmanager.com/gtag/js?id=G-R1F6Y45MW2';
        document.head.appendChild(g);
      }

      window.dataLayer = window.dataLayer || [];
      function gtag(){ dataLayer.push(arguments); }
      window.gtag = window.gtag || gtag;
      gtag('js', new Date());
      gtag('config', 'G-R1F6Y45MW2');
    } catch (e) {
      console.warn('loadAdsAndAnalytics error', e);
    }
  }

  // consent accept/decline handlers
  function acceptConsent() {
    setStored('granted');
    hideBanner();
    runQueue();
    loadAdsAndAnalytics();
  }

  function declineConsent() {
    setStored('denied');
    hideBanner();
    QUEUE = [];
  }

  // Build the banner DOM
  var banner = null;

  function buildBanner() {
    if (banner) return banner;

    banner = createEl('div', { class: 'th-consent-banner', role: 'dialog', 'aria-live': 'polite' });
    var inner = createEl('div', { class: 'th-consent-inner' });
    var message = createEl('div', { class: 'th-consent-message' }, '<strong>We use cookies and third‑party services</strong> — TimerHaven uses ads and analytics to improve the site. <a href="/privacy.html" target="_blank" rel="noopener">Read our Privacy Policy</a>.');
    var actions = createEl('div', { class: 'th-consent-actions' });

    var acceptBtn = createEl('button', { class: 'th-btn th-accept', type: 'button', 'aria-label': 'Accept tracking and ads' }, 'Accept');
    var declineBtn = createEl('button', { class: 'th-btn th-decline', type: 'button', 'aria-label': 'Decline tracking and ads' }, 'Decline');
    var manageBtn = createEl('button', { class: 'th-btn th-manage', type: 'button', 'aria-label': 'Manage settings' }, 'Manage');

    acceptBtn.addEventListener('click', function (e) { e.preventDefault(); acceptConsent(); });
    declineBtn.addEventListener('click', function (e) { e.preventDefault(); declineConsent(); });
    manageBtn.addEventListener('click', function (e) { e.preventDefault(); window.open('/privacy.html', '_blank', 'noopener'); });

    actions.appendChild(acceptBtn);
    actions.appendChild(declineBtn);
    actions.appendChild(manageBtn);

    inner.appendChild(message);
    inner.appendChild(actions);
    banner.appendChild(inner);

    // keyboard close
    banner.addEventListener('keydown', function (evt) { if (evt.key === 'Escape') hideBanner(); });

    return banner;
  }

  function showBanner() {
    try {
      var stored = getStored();
      if (stored === 'granted' || stored === 'denied') return;
      var b = buildBanner();
      if (!document.body.contains(b)) {
        document.body.appendChild(b);
        setTimeout(function () { b.classList.add('th-consent-visible'); }, 20);
      }
    } catch (e) { console.warn('showBanner error', e); }
  }

  function hideBanner() {
    try {
      if (!banner) return;
      banner.classList.remove('th-consent-visible');
      setTimeout(function () { try { banner.remove(); } catch (e) {} }, 240);
    } catch (e) {}
  }

  // Auto-run: if consent granted, load ads; else show banner
  document.addEventListener('DOMContentLoaded', function () {
    try {
      if (isGranted()) {
        runQueue();
        loadAdsAndAnalytics();
      } else {
        showBanner();
      }
    } catch (e) { console.warn(e); }
  });

  // Expose API
  window.timerhavenConsentGiven = timerhavenConsentGiven;
  window.timerhavenLoadAdsAfterConsent = timerhavenLoadAdsAfterConsent;
  window.timerhavenRevokeConsent = timerhavenRevokeConsent;

  // Expose helper to programmatically accept for testing
  window.timerhavenAcceptForTesting = acceptConsent;

})();