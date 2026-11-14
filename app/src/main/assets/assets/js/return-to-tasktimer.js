// return-to-tasktimer.js
(function () {
  try {
    if (document.querySelector('[data-return-pill="tasktimer"]')) return;
    var url = 'https://timerhaven.com/timer.html#startBtn';
    var pill = document.createElement('a');
    pill.href = url;
    pill.setAttribute('role', 'button');
    pill.setAttribute('aria-label', 'Back to Task Timer');
    pill.setAttribute('data-return-pill', 'tasktimer');
    pill.style.cssText = [
      'position:fixed','right:20px','bottom:20px','z-index:2147483647',
      'display:inline-flex','align-items:center','gap:12px','padding:10px 16px',
      'border-radius:999px','background:linear-gradient(180deg,#2faaff,#0b63a0)',
      'color:#fff','font-weight:700','text-decoration:none','box-shadow:0 18px 40px rgba(3,56,102,0.22)',
      'cursor:pointer','min-height:48px','-webkit-tap-highlight-color:transparent','backface-visibility:hidden','transform:translateZ(0)'
    ].join(';');
    var icon = document.createElement('span');
    icon.innerHTML = '↩';
    icon.setAttribute('aria-hidden', 'true');
    icon.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:10px;background:rgba(255,255,255,0.12);color:#fff;font-size:18px;flex:0 0 44px';
    var label = document.createElement('span');
    label.textContent = 'Back to Task Timer';
    label.style.cssText = 'font-size:16px;line-height:1;white-space:nowrap;padding-right:6px;display:inline-block';
    pill.appendChild(icon);
    pill.appendChild(label);
    pill.tabIndex = 0;
    pill.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.location.href = url;
      }
    });
    try {
      var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
      if (!mq || !mq.matches) {
        pill.style.opacity = '0';
        pill.style.transform = 'translateY(10px)';
        window.addEventListener('load', function () {
          setTimeout(function () {
            pill.style.transition = 'transform .32s cubic-bezier(.2,.9,.2,1), opacity .28s ease';
            pill.style.opacity = '1';
            pill.style.transform = 'translateY(0)';
          }, 120);
        });
      }
    } catch (err) {}
    document.body.appendChild(pill);
    function toggleOpacity() { try { pill.style.opacity = (window.scrollY < 80) ? '0.95' : '1.0'; } catch (e) {} }
    window.addEventListener('scroll', toggleOpacity);
    toggleOpacity();
  } catch (e) { console.error('return-to-tasktimer.js error', e); }
})();// /assets/js/return-to-tasktimer.js
(function () {
  try {
    if (document.querySelector('[data-return-pill="tasktimer"]')) return;
    var url = '/timer.html#startBtn'; // target tool
    var pill = document.createElement('a');
    pill.href = url;
    pill.setAttribute('role', 'button');
    pill.setAttribute('aria-label', 'Back to Task Timer');
    pill.setAttribute('data-return-pill', 'tasktimer');

    pill.style.cssText = [
      'position:fixed','right:20px','bottom:20px','z-index:2147483647',
      'display:inline-flex','align-items:center','gap:12px','padding:10px 16px',
      'border-radius:999px','background:linear-gradient(180deg,#2faaff,#0b63a0)',
      'color:#fff','font-weight:700','text-decoration:none','box-shadow:0 18px 40px rgba(3,56,102,0.22)',
      'cursor:pointer','min-height:48px','-webkit-tap-highlight-color:transparent','backface-visibility:hidden','transform:translateZ(0)'
    ].join(';');

    var icon = document.createElement('span');
    icon.innerHTML = '↩';
    icon.setAttribute('aria-hidden', 'true');
    icon.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:10px;background:rgba(255,255,255,0.12);color:#fff;font-size:18px;flex:0 0 44px';

    var label = document.createElement('span');
    label.textContent = 'Back to Task Timer';
    label.style.cssText = 'font-size:16px;line-height:1;white-space:nowrap;padding-right:6px;display:inline-block';

    pill.appendChild(icon);
    pill.appendChild(label);
    pill.tabIndex = 0;
    pill.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.location.href = url;
      }
    });

    // Entrance animation (skip when reduced motion)
    try {
      var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
      if (!mq || !mq.matches) {
        pill.style.opacity = '0';
        pill.style.transform = 'translateY(10px)';
        window.addEventListener('load', function () {
          setTimeout(function () {
            pill.style.transition = 'transform .32s cubic-bezier(.2,.9,.2,1), opacity .28s ease';
            pill.style.opacity = '1';
            pill.style.transform = 'translateY(0)';
          }, 120);
        });
      }
    } catch (err) {}

    document.body.appendChild(pill);

    function toggleOpacity() {
      try { pill.style.opacity = (window.scrollY < 80) ? '0.95' : '1.0'; } catch (e) {}
    }
    window.addEventListener('scroll', toggleOpacity);
    toggleOpacity();
  } catch (e) {
    console.error('return-to-tasktimer.js error', e);
  }
})();