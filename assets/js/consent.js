// Centralized consent.js for TimerHaven with Google Consent Mode v2
// - Implements Google Consent Mode v2 (analytics_storage, ad_storage, ad_user_data, ad_personalization)
// - Loads GA4 (G-R1F6Y45MW2) immediately with denied defaults for cookieless measurement & traffic modeling
// - Loads AdSense (ca-pub-0467059729557007) and updates consent to granted upon user approval
// - Shows consent banner (Accept / Decline / Manage)
// - Exposes window.timerhavenConsentGiven(), window.timerhavenLoadAdsAfterConsent(cb), window.timerhavenRevokeConsent()

(function () {
  'use strict';

  var STORAGE_KEY = 'timerhavenConsent';
  var GA_ID = 'G-R1F6Y45MW2';
  var AD_CLIENT = 'ca-pub-0467059729557007';
  var QUEUE = [];
  var ADS_LOADED_FLAG = '__timerhaven_ads_loaded';
  var ANALYTICS_LOADED_FLAG = '__timerhaven_analytics_loaded';

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

  // Fill every <ins class="adsbygoogle"> on the page.
  function fillAdUnits() {
    try {
      var units = document.querySelectorAll('ins.adsbygoogle');
      if (!units.length) return;
      window.adsbygoogle = window.adsbygoogle || [];
      for (var i = 0; i < units.length; i++) {
        if (units[i].getAttribute('data-ad-filled')) continue;
        units[i].setAttribute('data-ad-filled', '1');
        window.adsbygoogle.push({});
      }
    } catch (e) { console.warn('fillAdUnits error', e); }
  }
  window.timerhavenFillAdUnits = fillAdUnits;

  // --- Google Consent Mode v2 & Analytics ---
  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  // Establish default consent state before tags load
  if (isGranted()) {
    gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted'
    });
  } else {
    gtag('consent', 'default', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      wait_for_update: 500
    });
  }

  function loadAnalytics() {
    if (window[ANALYTICS_LOADED_FLAG]) return;
    window[ANALYTICS_LOADED_FLAG] = true;

    try {
      if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
        var g = document.createElement('script');
        g.async = true;
        g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
        document.head.appendChild(g);
      }
      gtag('js', new Date());
      gtag('config', GA_ID, {
        anonymize_ip: true
      });
    } catch (e) {
      console.warn('loadAnalytics error', e);
    }
  }

  // Load AdSense (only after explicit consent)
  function loadAdSense() {
    try {
      if (window[ADS_LOADED_FLAG]) { fillAdUnits(); return; }
      window[ADS_LOADED_FLAG] = true;

      var existing = document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]');
      if (!existing) {
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(AD_CLIENT);
        s.crossOrigin = 'anonymous';
        s.onload = fillAdUnits;
        s.onerror = function () { console.warn('AdSense loader failed to load'); };
        document.head.appendChild(s);
      } else {
        fillAdUnits();
      }

      if (document.readyState !== 'complete') {
        window.addEventListener('load', fillAdUnits);
      }
    } catch (e) {
      console.warn('loadAdSense error', e);
    }
  }

  // Load analytics immediately on script evaluation so cookieless measurement operates
  loadAnalytics();

  // consent accept/decline handlers
  function acceptConsent() {
    setStored('granted');
    hideBanner();
    gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted'
    });
    runQueue();
    loadAdSense();
  }

  function declineConsent() {
    setStored('denied');
    hideBanner();
    gtag('consent', 'update', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
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
        loadAdSense();
      } else if (!isDenied()) {
        showBanner();
      }
    } catch (e) { console.warn(e); }
  });

  // Expose API
  window.timerhavenConsentGiven = timerhavenConsentGiven;
  window.timerhavenLoadAdsAfterConsent = timerhavenLoadAdsAfterConsent;
  window.timerhavenRevokeConsent = timerhavenRevokeConsent;
  window.timerhavenFillAdUnits = fillAdUnits;

  // Expose helper to programmatically accept for testing
  window.timerhavenAcceptForTesting = acceptConsent;

})();
