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
