// consolidation module for guide cards
// Place under js/consolidate-guides.js and include it on the page.
// This is safe: it only changes the DOM on load and replaces groups of guide-related
// cards with a single card pointing to /TH-Guides/<lang>/<base>-index.html

(function window_timerhaven_consolidate_guides(){
  'use strict';

  // Localized "Read full guide" strings
  const READ_GUIDE = {
    en: "Read full guide",
    fr: "Lire le guide complet",
    es: "Leer la guía completa",
    de: "Vollständigen Leitfaden lesen",
    ru: "Читать полное руководство",
    el: "Διαβάστε τον πλήρη οδηγό",
    ar: "اقرأ الدليل الكامل"
  };

  // Normalize a data-tool value to a base name (remove how-to/tips/index and trailing lang suffix)
  function normalizeToolId(raw) {
    if (!raw || typeof raw !== 'string') return '';
    return raw
      .replace(/-(how-to|tips|index)$/i, '')
      .replace(/-(?:[a-z]{2}(?:-[A-Z]{2})?)$/, '')
      .trim();
  }

  // Use the same stored language getter as page (fallback to 'en')
  function getLang() {
    try {
      const s = localStorage.getItem('timerhavenLang');
      if (s && typeof s === 'string') return s.slice(0,2);
    } catch(e){}
    // fallback to any select on the page
    try {
      const sel = document.getElementById('lang-select');
      if (sel && sel.value) return ('' + sel.value).slice(0,2);
    } catch(e){}
    return 'en';
  }

  function consolidateOnce() {
    try {
      const lang = getLang() || 'en';
      const anchors = Array.from(document.querySelectorAll('a[data-tool]'));
      if (!anchors.length) return;

      // Group anchors by normalized base tool
      const groups = {};
      anchors.forEach(a => {
        const dt = a.getAttribute('data-tool') || '';
        const norm = normalizeToolId(dt);
        if (!norm) return;
        groups[norm] = groups[norm] || [];
        groups[norm].push(a);
      });

      Object.keys(groups).forEach(base => {
        const group = groups[base];
        // Heuristic: only consolidate where there are 2+ cards (tool + how-to/tips)
        if (!group || group.length < 2) return;

        const first = group[0];
        const parent = first.parentNode;
        if (!parent) return;

        // Build the target guide href using the copied guide location
        // (we assume TH-Guides/<lang>/<base>-index.html exists because you copied the English sources)
        const guideHref = `/TH-Guides/${lang}/${base}-index.html`;

        // Create the new consolidated anchor: clone first to preserve styling and classes
        const newA = first.cloneNode(true);

        // Set data-tool to canonical base (no language suffix)
        newA.setAttribute('data-tool', base);

        // Set the href to the guide page we created/copy to
        newA.setAttribute('href', guideHref);
        newA.href = guideHref;

        // Set the description to localized "Read full guide"
        const desc = newA.querySelector('.menu-description');
        if (desc) desc.textContent = READ_GUIDE[lang] || READ_GUIDE.en;

        // Optionally, you can add a small marker class to identify consolidated items
        newA.classList.add('consolidated-guide');

        // Insert the new node before the first group node, then remove all originals
        parent.insertBefore(newA, first);
        group.forEach(el => {
          try { parent.removeChild(el); } catch(e){}
        });
      });
    } catch(e) {
      // never throw in production; silently ignore
      console.warn('consolidate-guides error', e);
    }
  }

  // Run after DOM ready and also after your existing rewrite/localize calls
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', consolidateOnce);
  } else {
    // already ready
    setTimeout(consolidateOnce, 0);
  }

  // Re-run if language changes elsewhere (other tabs / storage events)
  window.addEventListener('storage', function(e){
    if (e.key === 'timerhavenLang') {
      try {
        consolidateOnce();
      } catch(e){}
    }
  });

})();