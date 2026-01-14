# create_th_files.ps1 - creates ads.txt, sitemap.xml, and assets files for TimerHaven
$ErrorActionPreference = "Stop"

# ensure directories exist
$dirs = @("assets\js","assets\css")
foreach ($d in $dirs) {
  if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}

# ads.txt
Set-Content -Path "ads.txt" -Value "google.com, pub-0467059729557007, DIRECT, f08c47fec0942fa0" -Encoding UTF8

# sitemap.xml (minimal template)
Set-Content -Path "sitemap.xml" -Value @'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Add canonical pages here; update lastmod when you publish -->
  <url>
    <loc>https://timerhaven.com/</loc>
    <lastmod>2025-11-24</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Add other pages as needed -->
</urlset>
'@ -Encoding UTF8

# consent.js
Set-Content -Path "assets\js\consent.js" -Value @'
/* assets/js/consent.js — minimal consent banner + API */
(function(){
  if (window.timerhavenConsentInstalled) return;
  window.timerhavenConsentInstalled = true;

  function getConsent() {
    try { return localStorage.getItem("timerhavenConsent") === "yes"; } catch(e) { return false; }
  }
  function setConsent(val) {
    try { localStorage.setItem("timerhavenConsent", val ? "yes" : "no"); } catch(e){}
    document.dispatchEvent(new CustomEvent("timerhavenConsentChanged", { detail: { consent: !!val } }));
  }

  window.timerhavenConsentGiven = function(){ return getConsent(); };

  function createBanner(){
    if (getConsent()) return;
    var banner = document.createElement("div");
    banner.id = "th-consent-banner";
    banner.innerHTML = '<div class="th-consent-inner"><div class="th-consent-text">We use cookies for analytics and ads. <a href="/privacy.html" target="_blank">Privacy</a></div><div class="th-consent-actions"><button id="th-accept" class="th-btn">Accept</button> <button id="th-reject" class="th-btn th-btn-muted">Reject</button></div></div>';
    document.body.appendChild(banner);

    document.getElementById("th-accept").addEventListener("click", function(){
      setConsent(true);
      banner.remove();
    });
    document.getElementById("th-reject").addEventListener("click", function(){
      setConsent(false);
      banner.remove();
    });
  }

  window.timerhavenLoadAdsAfterConsent = function(cb){
    if (getConsent()) { try { cb && cb(); } catch(e){}; return; }
    var onChange = function(e){
      if (e && e.detail && e.detail.consent) {
        try { cb && cb(); } catch(e){}
        document.removeEventListener("timerhavenConsentChanged", onChange);
      }
    };
    document.addEventListener("timerhavenConsentChanged", onChange);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", createBanner);
  } else { createBanner(); }
})();
'@ -Encoding UTF8

# consent.css
Set-Content -Path "assets\css\consent.css" -Value @'
#th-consent-banner {
  position: fixed;
  left: 12px;
  right: 12px;
  bottom: 12px;
  z-index: 2147483647;
  background: rgba(6, 30, 45, 0.98);
  color: #fff;
  border-radius: 10px;
  box-shadow: 0 12px 36px rgba(2,10,20,0.45);
  padding: 10px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
  font-size: 14px;
}
#th-consent-banner .th-consent-inner { display:flex; gap:12px; width:100%; align-items:center; justify-content:space-between; }
#th-consent-banner .th-btn { background:#0b63a0; color:#fff; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; font-weight:700; }
#th-consent-banner .th-btn.th-btn-muted { background:transparent; border:1px solid rgba(255,255,255,0.15); color:#fff; }
#th-consent-banner a { color: #bfe7ff; text-decoration: underline; }
'@ -Encoding UTF8

# site-tweaks.css
Set-Content -Path "assets\css\site-tweaks.css" -Value @'
/* Mobile/touch improvements */
@media (max-width: 900px) {
  body { font-size: 16px; } /* ensure readable text size */
  .menu-card, .menu-card a { min-height: 44px; padding: 0.6em; }
  .menu-card { touch-action: manipulation; }
  .menu-card .menu-title { font-size: 0.95rem; }
  a.menu-card, .menu-card { -webkit-tap-highlight-color: rgba(0,0,0,0.05); }
}

.image-aspect { display:block; max-width:100%; height:auto; aspect-ratio:16/9; }
'@ -Encoding UTF8

Write-Host "Files created: ads.txt, sitemap.xml, assets/js/consent.js, assets/css/consent.css, assets/css/site-tweaks.css"