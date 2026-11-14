/* i18n.js - place on every tool page (e.g. /assets/js/i18n.js)
   Usage:
     1) Include <script src="/assets/js/i18n.js"></script> early in <head> or before page script.
     2) On each page call i18n.registerTranslations(pageTranslations) to merge long page-specific strings.
     3) Mark up HTML with data-i18n / data-i18n-html / data-i18n-placeholder / data-i18n-title / data-i18n-aria.
     4) Changing localStorage.timerhavenLang will update pages live; index.html should set that key.
*/

(function(global){
  const i18n = {
    // Core translations. Add languages and keys here; pages can call registerTranslations() to add page-scoped keys.
    translations: {
      en: {
        // generic keys used across tools
        back: "Back to Main Menu",
        readFull: "Read Full Article",
        faqs: "FAQs",
        // weather defaults
        "weather.getWeather": "Get Weather",
        "weather.useLocation": "Use My Location",
        // unit defaults
        "unit.convert": "Convert",
        // example fallback phrases
        "placeholder.city": "Or enter city...",
        "placeholder.value": "Value"
      },
      fr: {
        back: "Retour au menu principal",
        readFull: "Lire l'article complet",
        faqs: "FAQ",
        "weather.getWeather": "Obtenir la météo",
        "weather.useLocation": "Utiliser ma position",
        "unit.convert": "Convertir",
        "placeholder.city": "Ou saisissez une ville...",
        "placeholder.value": "Valeur"
      }
      // add other languages as needed
    },

    // merge page-specific translations (pageTranslations is an object like { en: {...}, fr: {...} })
    registerTranslations(pageTranslations){
      if(!pageTranslations || typeof pageTranslations !== 'object') return;
      Object.keys(pageTranslations).forEach(lang=>{
        this.translations[lang] = this.translations[lang] || {};
        Object.assign(this.translations[lang], pageTranslations[lang]);
      });
    },

    getLang(){
      try {
        const l = localStorage.getItem('timerhavenLang') || 'en';
        return this.translations[l] ? l : 'en';
      } catch(e){ return 'en'; }
    },

    // return translation for key in current language, or fallback to en, or return the key itself
    t(key, lang){
      lang = lang || this.getLang();
      const dict = this.translations[lang] || {};
      if (dict[key] !== undefined) return dict[key];
      if (this.translations.en && this.translations.en[key] !== undefined) return this.translations.en[key];
      return key;
    },

    // apply translation to a single element according to attribute hints
    applyToElement(el, lang){
      if(!el || el.nodeType !== 1) return;
      // textContent
      const key = el.getAttribute('data-i18n');
      if(key){
        el.textContent = this.t(key, lang);
      }
      // innerHTML (for lists or markup)
      const keyHtml = el.getAttribute('data-i18n-html');
      if(keyHtml){
        el.innerHTML = this.t(keyHtml, lang);
      }
      // placeholder
      const ph = el.getAttribute('data-i18n-placeholder');
      if(ph) el.setAttribute('placeholder', this.t(ph, lang));
      // title
      const tt = el.getAttribute('data-i18n-title');
      if(tt) el.setAttribute('title', this.t(tt, lang));
      // value
      const val = el.getAttribute('data-i18n-value');
      if(val) el.setAttribute('value', this.t(val, lang));
      // aria
      const ar = el.getAttribute('data-i18n-aria');
      if(ar) el.setAttribute('aria-label', this.t(ar, lang));
    },

    // apply to whole document
    applyLanguage(lang){
      if(!lang) lang = this.getLang();
      if(!this.translations[lang]) lang = 'en';
      document.documentElement.lang = lang;
      // translate all nodes that have any data-i18n related attribute
      const selector = [
        '[data-i18n]',
        '[data-i18n-html]',
        '[data-i18n-placeholder]',
        '[data-i18n-title]',
        '[data-i18n-value]',
        '[data-i18n-aria]'
      ].join(',');
      document.querySelectorAll(selector).forEach(el => {
        this.applyToElement(el, lang);
      });
      // Update document.title if key present on <title data-i18n="...">
      const titleEl = document.querySelector('title[data-i18n]');
      if(titleEl){
        const k = titleEl.getAttribute('data-i18n');
        document.title = this.t(k, lang);
      }
    },

    // Initialize: set DOMContentLoaded handler and storage listener
    init(){
      const self = this;
      document.addEventListener('DOMContentLoaded', ()=>{
        // apply language once DOM ready
        self.applyLanguage(self.getLang());
      });
      // listen for language changes across tabs
      window.addEventListener('storage', (e)=>{
        if(e.key === 'timerhavenLang'){
          self.applyLanguage(e.newValue || 'en');
        }
      });
      // expose API to programmatically change language
      window._applyTimerHavenLang = function(lang){
        try{ localStorage.setItem('timerhavenLang', lang); } catch(e){}
        self.applyLanguage(lang);
      };
      // mutation observer for dynamically inserted elements (translate when nodes added)
      const observer = new MutationObserver((mutations)=>{
        const lang = self.getLang();
        mutations.forEach(m=>{
          m.addedNodes && m.addedNodes.forEach(node=>{
            if(node.nodeType === 1){
              // if new node or its descendants have i18n attributes, apply
              if(node.matches && node.matches('[data-i18n],[data-i18n-html],[data-i18n-placeholder],[data-i18n-title],[data-i18n-value],[data-i18n-aria]')) {
                self.applyToElement(node, lang);
              }
              node.querySelectorAll && node.querySelectorAll('[data-i18n],[data-i18n-html],[data-i18n-placeholder],[data-i18n-title],[data-i18n-value],[data-i18n-aria]').forEach(el=>{
                self.applyToElement(el, lang);
              });
            }
          });
        });
      });
      observer.observe(document.documentElement, { childList:true, subtree:true });
    }
  };

  // expose i18n global
  global.i18n = i18n;
  // auto-init
  i18n.init();

})(window);