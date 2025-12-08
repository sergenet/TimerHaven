// consolidation module for guide cards (regex-free normalizeToolId)
// Place under assets/js/consolidate-guides.js and include it on the page.
// This only changes the DOM on load and replaces groups of guide-related
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

  function isAlphaAscii(str) {
    if (!str || typeof str !== 'string') return false;
    for (let i = 0; i < str.length; i++) {
      const c = str.charCodeAt(i);
      if (!((c >= 65 && c <= 90) || (c >= 97 && c <= 122))) return false;
    }
    return true;
  }

  // Normalize a data-tool id WITHOUT using regex literals
  function normalizeToolId(raw) {
    if (!raw || typeof raw !== 'string') return '';
    let s = raw.trim();

    const lower = s.toLowerCase();
    if (lower.endsWith('-how-to')) s = s.slice(0, -7);
    else if (lower.endsWith('-tips')) s = s.slice(0, -5);
    else if (lower.endsWith('-index')) s = s.slice(0, -6);

    const parts = s.split('-');
    const last = parts[parts.length - 1] || '';
    if (last.length === 2 && isAlphaAscii(last)) {
      parts.pop();
      s = parts.join('-');
    } else if (last.length === 5 && last[2] === '-') {
      const p1 = last.slice(0,2), p2 = last.slice(3);
      if (isAlphaAscii(p1) && isAlphaAscii(p2)) {
        parts.pop();
        s = parts.join('-');
      }
    }

    return s.trim();
  }

  function getLang() {
    try {
      const s = localStorage.getItem('timerhavenLang');
      if (s && typeof s === 'string') return s.slice(0,2);
    } catch(e){}
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
        if (!group || group.length < 2) return;

        const first = group[0];
        const parent = first.parentNode;
        if (!parent) return;

        // FIXED: use template literal (backticks) not regex literal
        const guideHref = `/TH-Guides/${lang}/${base}-index.html`;

        const newA = first.cloneNode(true);
        newA.setAttribute('data-tool', base);
        newA.setAttribute('href', guideHref);
        newA.href = guideHref;

        const desc = newA.querySelector('.menu-description');
        if (desc) desc.textContent = READ_GUIDE[lang] || READ_GUIDE.en;

        newA.classList.add('consolidated-guide');

        parent.insertBefore(newA, first);
        group.forEach(el => {
          try { parent.removeChild(el); } catch(e){}
        });
      });
    } catch(e) {
      console.warn('consolidate-guides error', e);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', consolidateOnce);
  } else {
    setTimeout(consolidateOnce, 0);
  }

  window.addEventListener('storage', function(e){
    if (e.key === 'timerhavenLang') {
      try { consolidateOnce(); } catch(e){}
    }
  });

  try {
    const sel = document.getElementById('lang-select');
    if (sel) {
      sel.addEventListener('change', function() {
        setTimeout(function() {
          try { consolidateOnce(); } catch(e){}
        }, 80);
      });
    }
  } catch(e){}

})();