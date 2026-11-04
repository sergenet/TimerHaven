/**
 * TimerHaven Tool Directory Engine
 * Provides instant search, category filtering, quick-launch recent tools, and native app mode detection.
 */
(function () {
  // 1. Detect Native App Mode
  var urlParams = new URLSearchParams(window.location.search);
  var isAppMode = urlParams.get('app') === '1' || window.ReactNativeWebView !== undefined;
  if (isAppMode) {
    document.body.classList.add('is-native-app');
  }

  // 2. Initialize Directory Controls
  document.addEventListener('DOMContentLoaded', function () {
    var searchInput = document.getElementById('tool-search-input');
    var clearBtn = document.getElementById('tool-search-clear');
    var categoryPills = document.querySelectorAll('.category-pill');
    var toolGrid = document.getElementById('tools');
    var cards = document.querySelectorAll('.tool-grid .menu-card');
    var noResults = document.getElementById('tool-no-results');
    var quickLaunchBar = document.getElementById('quick-launch-bar');
    var quickLaunchItems = document.getElementById('quick-launch-items');

    var activeCategory = 'all';
    var activeSearchQuery = '';

    // Render Quick Launch (Recently Used Tools)
    function renderQuickLaunch() {
      if (!quickLaunchBar || !quickLaunchItems) return;
      try {
        var recent = JSON.parse(localStorage.getItem('th_recent_tools') || '[]');
        if (recent && recent.length > 0) {
          quickLaunchItems.innerHTML = '';
          recent.slice(0, 4).forEach(function (tool) {
            var a = document.createElement('a');
            a.className = 'quick-launch-item';
            a.href = tool.url;
            a.innerHTML = (tool.icon ? '<span>' + tool.icon + '</span> ' : '') + '<span>' + tool.title + '</span>';
            quickLaunchItems.appendChild(a);
          });
          quickLaunchBar.style.display = 'flex';
        }
      } catch (e) {
        console.warn('Could not read recent tools:', e);
      }
    }

    // Save Clicked Tool to Recent
    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        try {
          var titleEl = card.querySelector('.menu-title');
          var title = titleEl ? titleEl.textContent.trim() : '';
          var iconEl = card.querySelector('.menu-icon');
          var icon = iconEl ? iconEl.textContent.trim() || '⚡' : '⚡';
          var url = card.getAttribute('href');

          if (title && url) {
            var recent = JSON.parse(localStorage.getItem('th_recent_tools') || '[]');
            // Remove existing duplicate
            recent = recent.filter(function (t) { return t.url !== url; });
            recent.unshift({ title: title, url: url, icon: icon });
            localStorage.setItem('th_recent_tools', JSON.stringify(recent.slice(0, 6)));
          }
        } catch (e) {}
      });
    });

    // Filter Logic
    function applyFilter() {
      var visibleCount = 0;
      var query = activeSearchQuery.toLowerCase().trim();

      cards.forEach(function (card) {
        var cardCategory = card.getAttribute('data-category') || '';
        var title = (card.querySelector('.menu-title') || {}).textContent || '';
        var desc = (card.querySelector('.menu-description') || {}).textContent || '';
        var keywords = card.getAttribute('data-keywords') || '';
        var fullText = (title + ' ' + desc + ' ' + keywords).toLowerCase();

        var matchesCategory = (activeCategory === 'all' || cardCategory === activeCategory);
        var matchesQuery = !query || fullText.indexOf(query) !== -1;

        if (matchesCategory && matchesQuery) {
          card.classList.remove('is-hidden');
          visibleCount++;
        } else {
          card.classList.add('is-hidden');
        }
      });

      if (noResults) {
        noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    }

    // Bind Search Input
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        activeSearchQuery = this.value;
        if (clearBtn) {
          clearBtn.style.display = activeSearchQuery.length > 0 ? 'flex' : 'none';
        }
        applyFilter();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        if (searchInput) {
          searchInput.value = '';
          searchInput.focus();
        }
        activeSearchQuery = '';
        clearBtn.style.display = 'none';
        applyFilter();
      });
    }

    // Bind Category Pills
    categoryPills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        categoryPills.forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');
        activeCategory = pill.getAttribute('data-category') || 'all';
        applyFilter();
      });
    });

    renderQuickLaunch();
  });
})();
