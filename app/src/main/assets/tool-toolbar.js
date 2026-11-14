// Injects uniform Tips / How-to toolbar and panel for every .tool-card on the page.
// Safe, idempotent, and exits immediately on pages that do not contain .tool-card.
// Install: upload to /public_html/tool-toolbar.js and add <script src="/tool-toolbar.js"></script> before </body>.

(function(){
  'use strict';

  // Initialize only after DOM ready, and bail out quickly if no .tool-card on the page
  function init() {
    if (!document.querySelector('.tool-card')) {
      // No tool cards on this page — nothing to do.
      return;
    }

    // --- Original injector code follows (unchanged except for being nested here) ---

    // Create or return the shared panel overlay (reused across all tools)
    function ensurePanel() {
      let overlay = document.getElementById('tool-panel-overlay');
      if (overlay) return { overlay, panel: document.getElementById('tool-panel'), body: document.getElementById('panel-body'), title: document.getElementById('panel-title'), openExternal: document.getElementById('panel-open-external') };

      overlay = document.createElement('div');
      overlay.id = 'tool-panel-overlay';
      overlay.setAttribute('role','dialog');
      overlay.setAttribute('aria-hidden','true');
      overlay.style.display = 'none';
      overlay.style.zIndex = '1100';
      overlay.style.left = '0';
      overlay.style.right = '0';
      overlay.style.top = '0';
      overlay.style.bottom = '0';
      overlay.style.position = 'fixed';
      overlay.style.background = 'rgba(0,0,0,0.35)';
      overlay.style.alignItems = 'flex-end';
      overlay.style.justifyContent = 'center';

      const panel = document.createElement('div');
      panel.id = 'tool-panel';
      panel.style.width = '100%';
      panel.style.maxHeight = '92%';
      panel.style.background = '#fff';
      panel.style.borderTopLeftRadius = '12px';
      panel.style.borderTopRightRadius = '12px';
      panel.style.boxShadow = '0 -8px 30px rgba(8,20,40,0.2)';
      panel.style.overflow = 'auto';
      panel.style.padding = '1rem';
      panel.style.boxSizing = 'border-box';
      panel.style.transform = 'translateY(100%)';
      panel.style.transition = 'transform .28s ease';

      const header = document.createElement('div');
      header.className = 'panel-header';
      header.style.display = 'flex';
      header.style.justifyContent = 'space-between';
      header.style.alignItems = 'center';
      header.style.marginBottom = '.5rem';

      const title = document.createElement('h4');
      title.id = 'panel-title';
      title.textContent = 'Panel';
      title.style.margin = '0';
      title.style.fontSize = '1.05rem';

      const headerBtns = document.createElement('div');

      const openExternal = document.createElement('button');
      openExternal.id = 'panel-open-external';
      openExternal.className = 'btn btn-sm btn-outline-secondary';
      openExternal.style.marginRight = '.5rem';
      openExternal.style.display = 'none';
      openExternal.textContent = 'Open page';

      const closeBtn = document.createElement('button');
      closeBtn.id = 'panel-close';
      closeBtn.className = 'btn btn-sm btn-outline-danger';
      closeBtn.textContent = 'Close';
      closeBtn.addEventListener('click', closePanel);

      headerBtns.appendChild(openExternal);
      headerBtns.appendChild(closeBtn);
      header.appendChild(title);
      header.appendChild(headerBtns);

      const body = document.createElement('div');
      body.id = 'panel-body';
      body.className = 'panel-body';
      body.style.fontSize = '.95rem';
      body.style.color = '#22313f';
      body.style.lineHeight = '1.4';

      panel.appendChild(header);
      panel.appendChild(body);
      overlay.appendChild(panel);
      document.body.appendChild(overlay);

      // overlay click closes when clicking backdrop
      overlay.addEventListener('click', function(e){ if (e.target === overlay) closePanel(); });
      // ESC closes
      document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && overlay.style.display === 'flex') closePanel(); });

      return { overlay, panel, body, title, openExternal };
    }

    function openPanel(kind, targetUrl) {
      const { overlay, panel, body, title, openExternal } = ensurePanel();
      title.textContent = (kind === 'tips') ? 'Tips' : 'How‑to';
      body.innerHTML = '<div style="padding:.6rem;color:#666">Loading…</div>';
      openExternal.style.display = 'none';
      overlay.style.display = 'flex';
      // small delay then slide in
      requestAnimationFrame(()=> panel.style.transform = 'translateY(0%)');
      overlay.setAttribute('aria-hidden','false');

      if (!targetUrl) {
        body.innerHTML = '<div style="padding:.6rem;color:#666">No page configured.</div>';
        return;
      }

      fetch(targetUrl, { method: 'GET' }).then(resp => {
        if (!resp.ok) throw new Error('Not found');
        return resp.text();
      }).then(html => {
        try {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const candidate = doc.querySelector('.card-content') || doc.querySelector('.main-container') || doc.querySelector('main') || doc.body;
          body.innerHTML = candidate ? candidate.innerHTML : doc.body.innerHTML;
        } catch (e) {
          body.innerHTML = html;
        }
        openExternal.style.display = 'inline-block';
        openExternal.onclick = () => { window.location.href = targetUrl + window.location.search; };
      }).catch(err => {
        body.innerHTML = '<div style="padding:.6rem;color:#666">Full page not available inline — opening page.</div>';
        openExternal.style.display = 'inline-block';
        openExternal.onclick = () => { window.location.href = targetUrl + window.location.search; };
      });
    }

    function closePanel() {
      const { overlay, panel, body, openExternal } = ensurePanel();
      panel.style.transform = 'translateY(100%)';
      overlay.setAttribute('aria-hidden','true');
      setTimeout(()=> { overlay.style.display = 'none'; body.innerHTML = ''; openExternal.style.display = 'none'; }, 280);
    }

    // Utility: try to find tips/how-to URL for this tool-card
    function resolveTargetsForTool(card) {
      // 1) explicit data attributes
      const dataTips = card.getAttribute('data-tips');
      const dataHow = card.getAttribute('data-howto') || card.getAttribute('data-how');
      if (dataTips || dataHow) {
        return { tips: dataTips || null, howto: dataHow || null };
      }

      // 2) look for anchors on page that mention tips/how-to (prefer anchors near this card)
      function findNearestHref(keyword) {
        // search anchors containing keyword
        const anchors = Array.from(document.querySelectorAll('a[href*="' + keyword + '"]'));
        if (!anchors.length) return null;
        // choose anchor closest to this card in DOM (by ancestor depth) - fallback to first
        let best = anchors[0], bestDistance = 1e9;
        anchors.forEach(a => {
          let node = a;
          let dist = 0;
          while (node && node !== document.body) { node = node.parentElement; dist++; if (node === card) break; }
          if (node === card) dist = 0; // inside card -> best
          if (dist < bestDistance) { bestDistance = dist; best = a; }
        });
        return best ? best.getAttribute('href') : null;
      }
      const foundTips = findNearestHref('tips');
      const foundHow = findNearestHref('how-to') || findNearestHref('howto') || findNearestHref('how-to') || findNearestHref('how_to');

      if (foundTips || foundHow) return { tips: foundTips || null, howto: foundHow || null };

      // 3) derive from current page filename with some heuristics
      const path = window.location.pathname;
      let file = path.substring(path.lastIndexOf('/') + 1) || '';
      if (!file) file = document.location.hostname; // fallback
      const name = file.replace(/\.html$/, '').replace(/-[a-z]{2}$/, ''); // remove .html and language suffix
      // common patterns seen on this site:
      // clipboard-manager.html -> clipboard-tips.html and clipboard-how-to.html
      let base = name.replace(/-manager$/, '').replace(/-tool$/, '').replace(/-app$/, '');
      base = base.replace(/_$/, '').replace(/-$/, '');
      const candidates = [
        '/' + base + '-tips.html',
        '/' + base + '-how-to.html',
        '/' + base + '-howto.html',
        '/' + base + '-tips/index.html'
      ];
      // validate existence via HEAD is expensive; just return candidate strings and let fetch decide
      return { tips: candidates[0], howto: candidates[1] };
    }

    // Insert toolbar into a tool-card if missing
    function ensureToolbarForTool(card) {
      if (card.querySelector('.tool-top-actions')) return; // already present

      const toolbar = document.createElement('div');
      toolbar.className = 'tool-top-actions';
      toolbar.setAttribute('role','toolbar');
      toolbar.setAttribute('aria-label','Tool actions');

      const btnTips = document.createElement('button');
      btnTips.className = 'btn tips';
      btnTips.type = 'button';
      btnTips.textContent = 'Tips';
      btnTips.style.cursor = 'pointer';

      const btnHow = document.createElement('button');
      btnHow.className = 'btn howto';
      btnHow.type = 'button';
      btnHow.textContent = 'How‑to';
      btnHow.style.cursor = 'pointer';

      toolbar.appendChild(btnTips);
      toolbar.appendChild(btnHow);

      // insert toolbar at top of card-content if exists, otherwise at top of card
      const content = card.querySelector('.card-content') || card;
      content.insertBefore(toolbar, content.firstChild);

      // wire click handlers with resolved targets
      const targets = resolveTargetsForTool(card);

      btnTips.addEventListener('click', function(e){
        setActiveVisual(btnTips, btnHow);
        openPanel('tips', targets.tips);
      });
      btnHow.addEventListener('click', function(e){
        setActiveVisual(btnHow, btnTips);
        openPanel('howto', targets.howto);
      });

      // set initial visual state (tips primary)
      setActiveVisual(btnTips, btnHow);
    }

    function setActiveVisual(activeBtn, otherBtn) {
      if (otherBtn) otherBtn.classList.remove('active');
      if (activeBtn) activeBtn.classList.add('active');
      try { localStorage.setItem('th-last-tool-btn', activeBtn && activeBtn.classList.contains('howto') ? 'howto' : 'tips'); } catch(e){}
    }

    // Main runner: find all .tool-card and inject toolbar
    function runInjector() {
      const cards = Array.from(document.querySelectorAll('.tool-card'));
      if (!cards.length) return false;
      cards.forEach(c => ensureToolbarForTool(c));
      return true;
    }

    // Try run now; if DOM not yet ready, wait
    if (!runInjector()) {
      document.addEventListener('DOMContentLoaded', runInjector);
      // as a fallback, run again after a short delay
      setTimeout(runInjector, 600);
    }

    // --- End original injector code ---
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();