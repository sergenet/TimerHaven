#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_world_clock.py

Generates localized static HTML pages for the "World Clock" tool in 7 languages.
This version installs a single header (top-right) language selector with defensive
CSS/JS to prevent any in-card selector from appearing. Run:

  python generate_world_clock.py

Output goes to ./world_clock_pages/
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "world_clock_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

# --- TRANSLATIONS (en, fr, es, de, ru, el, ar) ---
TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "dir": "",
        "ui": {
            "select_prompt": "Select city...",
            "placeholder": "Or enter city or time zone (e.g. London, America/Denver, GMT+2, EST)",
            "add_btn": "Add Clock",
            "no_clocks": "No clocks added yet.",
            "faqs": "FAQs",
            "read_article": "Read Full Article",
            "back_main": "Back to Main Menu",
            "error_not_recognized": "City not recognized. Try the dropdown, autocomplete, or enter a valid IANA time zone (e.g. Europe/London).",
            "please_select": "Please select or enter a city or time zone."
        },
        "main": {
            "title": "World Clock — TimerHaven",
            "h1": "World Clock",
            "desc": "See the time anywhere in the world, instantly."
        },
        "howto": {
            "title": "How to Use World Clock",
            "steps": [
                "<b>Add a city:</b> Use the dropdown for popular cities or start typing any city name.",
                "<b>Compare times:</b> Add multiple cities to view their current local time side by side.",
                "<b>Remove:</b> Click the Remove button to delete a city from your list.",
                "<b>Refresh:</b> Times update automatically every second."
            ],
            "back_btn": "Back to World Clock"
        },
        "tips": {
            "title": "World Clock Tips",
            "tips": [
                "<b>Plan meetings easily:</b> Add all relevant cities and compare times to pick the best slot.",
                "<b>Travel smart:</b> Check the local time before you depart or land.",
                "<b>Use autocomplete:</b> Start typing any city for instant suggestions."
            ],
            "back_btn": "Back to World Clock"
        }
    },

    "fr": {
        "lang_name": "Français",
        "dir": "",
        "ui": {
            "select_prompt": "Sélectionnez une ville...",
            "placeholder": "Ou saisissez une ville ou fuseau (ex. Paris, Europe/Paris, GMT+2)",
            "add_btn": "Ajouter l'horloge",
            "no_clocks": "Aucune horloge ajoutée.",
            "faqs": "FAQ",
            "read_article": "Lire l'article",
            "back_main": "Retour au menu principal",
            "error_not_recognized": "Ville non reconnue. Essayez le menu, l'autocomplétion, ou saisissez un fuseau IANA (ex. Europe/Paris).",
            "please_select": "Veuillez sélectionner ou saisir une ville ou un fuseau horaire."
        },
        "main": {
            "title": "Horloge mondiale — TimerHaven",
            "h1": "Horloge mondiale",
            "desc": "Voyez l'heure partout dans le monde instantanément."
        },
        "howto": {
            "title": "Comment utiliser l'Horloge mondiale",
            "steps": [
                "<b>Ajouter une ville :</b> Utilisez le menu pour les villes populaires ou commencez à taper le nom.",
                "<b>Comparer les heures :</b> Ajoutez plusieurs villes pour voir les heures côte à côte.",
                "<b>Supprimer :</b> Cliquez sur Supprimer pour retirer une ville.",
                "<b>Actualisation :</b> Les heures se mettent à jour automatiquement."
            ],
            "back_btn": "Retour à l'Horloge"
        },
        "tips": {
            "title": "Conseils Horloge mondiale",
            "tips": [
                "<b>Planifiez vos réunions :</b> Ajoutez vos villes pour trouver le meilleur créneau.",
                "<b>Voyagez malin :</b> Vérifiez l'heure locale avant de partir.",
                "<b>Utilisez l'autocomplétion :</b> Commencez à taper pour trouver rapidement une ville."
            ],
            "back_btn": "Retour à l'Horloge"
        }
    },

    "es": {
        "lang_name": "Español",
        "dir": "",
        "ui": {
            "select_prompt": "Seleccione ciudad...",
            "placeholder": "O introduzca ciudad o zona horaria (p. ej. Madrid, Europe/Madrid, GMT+2)",
            "add_btn": "Agregar Reloj",
            "no_clocks": "No hay relojes añadidos.",
            "faqs": "Preguntas frecuentes",
            "read_article": "Leer el artículo",
            "back_main": "Volver al menú principal",
            "error_not_recognized": "Ciudad no reconocida. Pruebe el desplegable, la autocompletación o introduzca una zona IANA válida (p. ej. Europe/Madrid).",
            "please_select": "Seleccione o introduzca una ciudad o zona horaria."
        },
        "main": {
            "title": "Reloj mundial — TimerHaven",
            "h1": "Reloj mundial",
            "desc": "Vea la hora en cualquier lugar del mundo al instante."
        },
        "howto": {
            "title": "Cómo usar el Reloj mundial",
            "steps": [
                "<b>Agregar una ciudad:</b> Use el desplegable para ciudades populares o comience a escribir.",
                "<b>Comparar horas:</b> Agregue varias ciudades para verlas lado a lado.",
                "<b>Eliminar:</b> Haga clic en Eliminar para quitar una ciudad.",
                "<b>Actualización:</b> Las horas se actualizan automáticamente."
            ],
            "back_btn": "Volver al Reloj"
        },
        "tips": {
            "title": "Consejos Reloj mundial",
            "tips": [
                "<b>Planifique reuniones:</b> Añada ciudades relevantes y compare horarios.",
                "<b>Viaje inteligente:</b> Verifique la hora local antes de salir.",
                "<b>Use la autocompletación:</b> Escriba para obtener sugerencias rápidas."
            ],
            "back_btn": "Volver al Reloj"
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "dir": "",
        "ui": {
            "select_prompt": "Stadt auswählen...",
            "placeholder": "Oder Stadt/Zeitzone eingeben (z. B. Berlin, Europe/Berlin, GMT+2)",
            "add_btn": "Uhr hinzufügen",
            "no_clocks": "Noch keine Uhren hinzugefügt.",
            "faqs": "FAQ",
            "read_article": "Artikel lesen",
            "back_main": "Zurück zum Hauptmenü",
            "error_not_recognized": "Stadt nicht erkannt. Verwenden Sie die Auswahl, Autocomplete oder geben Sie eine gültige IANA-Zeitzone ein (z. B. Europe/Berlin).",
            "please_select": "Bitte wählen oder geben Sie eine Stadt oder Zeitzone ein."
        },
        "main": {
            "title": "Weltuhr — TimerHaven",
            "h1": "Weltuhr",
            "desc": "Sehen Sie die Uhrzeit überall auf der Welt sofort."
        },
        "howto": {
            "title": "So verwenden Sie die Weltuhr",
            "steps": [
                "<b>Stadt hinzufügen:</b> Verwenden Sie die Auswahl oder tippen Sie den Städtenamen.",
                "<b>Zeiten vergleichen:</b> Fügen Sie mehrere Städte hinzu, um Zeiten nebeneinander zu sehen.",
                "<b>Entfernen:</b> Klicken Sie auf Entfernen, um eine Stadt zu löschen.",
                "<b>Aktualisierung:</b> Die Uhrzeiten aktualisieren sich automatisch."
            ],
            "back_btn": "Zurück zur Weltuhr"
        },
        "tips": {
            "title": "Weltuhr Tipps",
            "tips": [
                "<b>Meetings planen:</b> Fügen Sie alle relevanten Städte hinzu und wählen Sie die beste Zeit.",
                "<b>Reisen planen:</b> Prüfen Sie die Ortszeit vor Abreise.",
                "<b>Autocomplete nutzen:</b> Tippen Sie zum schnellen Finden einer Stadt."
            ],
            "back_btn": "Zurück zur Weltuhr"
        }
    },

    "ru": {
        "lang_name": "Русский",
        "dir": "",
        "ui": {
            "select_prompt": "Выберите город...",
            "placeholder": "Или введите город/зону (например, Москва, Europe/Moscow, GMT+3)",
            "add_btn": "Добавить часы",
            "no_clocks": "Часы не добавлены.",
            "faqs": "Вопросы",
            "read_article": "Читать статью",
            "back_main": "Вернуться в главное меню",
            "error_not_recognized": "Город не распознан. Попробуйте выпадающий список, автозаполнение или введите корректную IANA зону (например, Europe/Moscow).",
            "please_select": "Пожалуйста, выберите или введите город или временную зону."
        },
        "main": {
            "title": "Мировые часы — TimerHaven",
            "h1": "Мировые часы",
            "desc": "Смотрите время в любой точке мира мгновенно."
        },
        "howto": {
            "title": "Как использовать Мировые часы",
            "steps": [
                "<b>Добавьте город:</b> Используйте выпадающий список или начните вводить название.",
                "<b>Сравните время:</b> Добавьте несколько городов, чтобы сравнить время.",
                "<b>Удалить:</b> Нажмите Удалить, чтобы убрать город.",
                "<b>Обновление:</b> Время обновляется автоматически."
            ],
            "back_btn": "Вернуться к часам"
        },
        "tips": {
            "title": "Советы по Мировым часам",
            "tips": [
                "<b>Планируйте встречи:</b> Добавьте города и выберите удобное время.",
                "<b>Путешествуйте грамотно:</b> Узнайте местное время перед поездкой.",
                "<b>Используйте автозаполнение:</b> Начните ввод, чтобы быстро найти город."
            ],
            "back_btn": "Вернуться к часам"
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "dir": "",
        "ui": {
            "select_prompt": "Επιλέξτε πόλη...",
            "placeholder": "Ή εισάγετε πόλη/ζώνη (π.χ. Αθήνα, Europe/Athens, GMT+2)",
            "add_btn": "Προσθήκη ρολογιού",
            "no_clocks": "Δεν έχουν προστεθεί ρολόγια.",
            "faqs": "Συχνές ερωτήσεις",
            "read_article": "Διαβάστε το άρθρο",
            "back_main": "Επιστροφή στο κύριο μενού",
            "error_not_recognized": "Η πόλη δεν αναγνωρίστηκε. Δοκιμάστε τη λίστα ή εισάγετε μια έγκυρη ζώνη IANA (π.χ. Europe/Athens).",
            "please_select": "Επιλέξτε ή εισάγετε πόλη ή ζώνη ώρας."
        },
        "main": {
            "title": "Παγκόσμιο Ρολόι — TimerHaven",
            "h1": "Παγκόσμιο Ρολόι",
            "desc": "Δείτε την ώρα σε όλο τον κόσμο άμεσα."
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε το Παγκόσμιο Ρολόι",
            "steps": [
                "<b>Προσθέστε πόλη:</b> Χρησιμοποιήστε το μενού ή ξεκινήστε να πληκτρολογείτε.",
                "<b>Συγκρίνετε ώρες:</b> Προσθέστε πολλές πόλεις για σύγκριση.",
                "<b>Κατάργηση:</b> Κάντε κλικ για να διαγράψετε πόλη.",
                "<b>Ανανέωση:</b> Οι ώρες ενημερώνονται αυτόματα."
            ],
            "back_btn": "Επιστροφή στο Ρολόι"
        },
        "tips": {
            "title": "Συμβουλές Παγκόσμιου Ρολογιού",
            "tips": [
                "<b>Προγραμματίστε συναντήσεις:</b> Προσθέστε πόλεις και βρείτε την καλύτερη ώρα.",
                "<b>Ταξιδέψτε έξυπνα:</b> Ελέγξτε την τοπική ώρα πριν ταξιδέψετε.",
                "<b>Χρησιμοποιήστε autocomplete:</b> Πληκτρολογήστε για γρήγορες προτάσεις."
            ],
            "back_btn": "Επιστροφή στο Ρολόι"
        }
    },

    "ar": {
        "lang_name": "العربية",
        "dir": ' dir="rtl"',
        "ui": {
            "select_prompt": "اختر مدينة...",
            "placeholder": "أو ادخل المدينة/المنطقة الزمنية (مثال: Cairo, Africa/Cairo, GMT+2)",
            "add_btn": "أضف ساعة",
            "no_clocks": "لم تتم إضافة ساعات بعد.",
            "faqs": "الأسئلة الشائعة",
            "read_article": "اقرأ المقال",
            "back_main": "العودة إلى القائمة الرئيسية",
            "error_not_recognized": "لم يتم التعرف على المدينة. جرب القائمة أو أدخل منطقة IANA صالحة (مثال: Africa/Cairo).",
            "please_select": "يرجى اختيار أو إدخال مدينة أو منطقة زمنية."
        },
        "main": {
            "title": "الوقت العالمي — TimerHaven",
            "h1": "الوقت العالمي",
            "desc": "شاهد الوقت في أي مكان بالعالم فورًا."
        },
        "howto": {
            "title": "كيفية استخدام الوقت العالمي",
            "steps": [
                "<b>أضف مدينة:</b> استخدم القائمة أو ابدأ بالكتابة.",
                "<b>قارن الأوقات:</b> أضف مدنًا متعددة للمقارنة.",
                "<b>إزالة:</b> انقر لإزالة مدينة من قائمتك.",
                "<b>التحديث:</b> يتم تحديث الأوقات تلقائيًا."
            ],
            "back_btn": "العودة إلى أداة الوقت"
        },
        "tips": {
            "title": "نصائح الوقت العالمي",
            "tips": [
                "<b>خطط للاجتماعات:</b> أضف المدن واختر الوقت الأنسب.",
                "<b>سافر بذكاء:</b> تحقق من الوقت المحلي قبل السفر.",
                "<b>استخدم الإكمال التلقائي:</b> ابدأ بالكتابة للحصول على اقتراحات سريعة."
            ],
            "back_btn": "العودة إلى أداة الوقت"
        }
    }
}

# --- Embedded CSS & JS snippets to be included in templates ---
# This version uses a header (top-row) language selector and defensive CSS/JS.

LANGUAGE_CSS = r"""
/* Header-first language selector styling, defensive rules to hide any in-card selectors */
.top-row { display:flex !important; justify-content:flex-end !important; gap:.6rem !important; align-items:center !important; }
.top-row label[for="language-select-top"] { font-weight:600; margin-right:.5rem; color:#0b2545; }

/* Ensure header select is visible and styled to match other tools */
.top-row .language-select {
  width:180px !important;
  border-radius:10px !important;
  padding:.28rem .6rem !important;
  border:1px solid rgba(13,110,253,0.18) !important;
  background:#fff !important;
  color:#0d6efd !important;
  font-weight:600 !important;
  box-shadow:none !important;
}

/* Defensive: hide any selectors inserted into the tool-card */
.tool-card .lang-wrap,
.tool-card #language-select-top {
  display: none !important;
  visibility: hidden !important;
}

/* RTL tweak for Arabic pages (if dir attr used) */
[dir="rtl"] .top-row { justify-content:flex-start !important; }

/* Small-screen: move header selector above content for better UX */
@media (max-width:900px) {
  .top-row { justify-content:flex-start !important; }
  .top-row .language-select { width:140px !important; }
}
"""

LANGUAGE_JS = r"""
/* Header language selector script (defensive). This script:
   - Creates/populates the header select (#language-select-top)
   - Sets the current selected language based on filename
   - Hooks change to redirect to the matching page type
   - Removes any in-card selectors if present
*/
(function(){
  const LANGS = [
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
    { code: 'de', name: 'Deutsch' },
    { code: 'ru', name: 'Русский' },
    { code: 'el', name: 'Ελληνικά' },
    { code: 'ar', name: 'العربية' }
  ];

  function detectPageInfo() {
    const path = (location.pathname || '').split('/').pop() || '';
    const m = path.match(/^world-(clock|how-to|tips)-([a-z]{2})\.html$/i);
    if (m) return { type: m[1], lang: m[2].toLowerCase() };
    if (/^world-clock\.html$/i.test(path)) return { type: 'clock', lang: 'en' };
    const m2 = path.match(/^world-(clock|how-to|tips)\.html$/i);
    if (m2) return { type: m2[1], lang: 'en' };
    return { type: 'clock', lang: 'en' };
  }

  function removeInCardSelectors() {
    document.querySelectorAll('.tool-card .lang-wrap, .tool-card #language-select-top').forEach(function(el){ try{ el.remove(); }catch(e){} });
  }

  function buildHeaderSelector(selectedLang) {
    // ensure .top-row exists (page templates include it; create if missing)
    let top = document.querySelector('.page-wrap .top-row') || document.querySelector('.top-row');
    if (!top) {
      top = document.createElement('div');
      top.className = 'top-row';
      const pw = document.querySelector('.page-wrap') || document.body;
      pw.insertBefore(top, pw.firstChild);
    }

    // remove any existing header select/label
    top.querySelectorAll('label[for="language-select-top"], #language-select-top').forEach(function(n){ try{ n.remove(); }catch(e){} });

    const label = document.createElement('label');
    label.setAttribute('for','language-select-top');
    label.textContent = 'Language:';
    label.style.fontWeight = '600';
    label.style.marginRight = '.5rem';

    const sel = document.createElement('select');
    sel.id = 'language-select-top';
    sel.className = 'language-select';
    sel.setAttribute('aria-label','Language selector');

    LANGS.forEach(function(l){
      const o = document.createElement('option');
      o.value = l.code;
      o.textContent = l.name;
      if (l.code === selectedLang) o.selected = true;
      sel.appendChild(o);
    });

    top.appendChild(label);
    top.appendChild(sel);
    // ensure visible
    sel.style.display = 'inline-flex';
    sel.style.visibility = 'visible';
    return sel;
  }

  function hookSelector(sel) {
    if (!sel) return;
    // remove previous handler if any
    if (sel._handler) sel.removeEventListener('change', sel._handler);
    sel._handler = function() {
      const code = this.value || 'en';
      const info = detectPageInfo();
      if ((location.pathname || '').match(/world-clock\.html$/i)) {
        window.location.href = 'world-clock-' + code + '.html';
        return;
      }
      window.location.href = 'world-' + info.type + '-' + code + '.html';
    };
    sel.addEventListener('change', sel._handler);
  }

  // Run on DOM ready
  function init() {
    removeInCardSelectors();
    const info = detectPageInfo();
    const sel = buildHeaderSelector(info.lang);
    hookSelector(sel);

    // Defensive: observe for a short time and remove inserted in-card selectors (legacy scripts)
    const observer = new MutationObserver(function(muts){
      muts.forEach(function(m){
        if (m.addedNodes) {
          m.addedNodes.forEach(function(n){
            try {
              if (n.querySelectorAll) {
                n.querySelectorAll('.tool-card .lang-wrap, .tool-card #language-select-top').forEach(function(el){ try{ el.remove(); }catch(e){} });
              }
              if (n.matches && (n.matches('.tool-card .lang-wrap') || n.matches('.tool-card #language-select-top'))) {
                try{ n.remove(); }catch(e){}
              }
            } catch(e){}
          });
        }
      });
    });
    observer.observe(document.documentElement || document.body, { childList: true, subtree: true });
    // stop observing after 6s
    setTimeout(function(){ try{ observer.disconnect(); }catch(e){} }, 6000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
"""

# --- Templates (unchanged except they reference LANGUAGE_CSS and LANGUAGE_JS) ---
MAIN_TEMPLATE = """<!doctype html>
<html lang="%%LANG%%"%%DIR%%>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>%%TITLE%%</title>
  <meta name="description" content="%%DESC%%">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.5/awesomplete.min.css" />
  <script src="https://cdn.jsdelivr.net/npm/luxon@3.4.3/build/global/luxon.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.5/awesomplete.min.js"></script>

  <style>
    /* Strong page-level override to match other tools */
    body { background:#f4f7fb !important; font-family: 'Montserrat', Arial, sans-serif !important; color:#0b2545 !important; margin:0; }
    .page-wrap { max-width:1200px; margin:2.4rem auto !important; padding:0 1rem !important; box-sizing:border-box !important; }
    .top-row { display:flex !important; justify-content:flex-end !important; gap:.6rem !important; margin-bottom:.6rem !important; align-items:center; }
    .language-select { width:180px !important; border-radius:10px !important; padding:.28rem .6rem !important; border:1px solid rgba(13,110,253,0.18) !important; background:#fff !important; color:#0d6efd !important; font-weight:600 !important; }
    .text-center.mb-4 { margin-bottom:1.5rem !important; }
    .text-center.mb-4 h1 { font-size:2.4rem !important; margin:0 !important; color:#0b2545 !important; }
    .text-center.mb-4 p.lead { margin-top:.4rem !important; color:#6b7280 !important; }

    .center-row { display:flex !important; gap:1.6rem !important; justify-content:center !important; align-items:flex-start !important; flex-wrap:nowrap !important; }

    .article-card, .tool-card {
      background:#fff !important;
      border-radius:18px !important;
      box-shadow: 0 6px 20px rgba(11,37,69,0.06) !important;
      padding:1.3rem !important;
      box-sizing:border-box !important;
      min-height:340px !important;
      display:flex !important;
      flex-direction:column !important;
      justify-content:space-between !important;
    }

    .article-card { width:330px !important; }
    .tool-card { width:420px !important; }

    .article-card h2, .tool-card h3 { color:#185a9d !important; margin:0 0 .6rem 0 !important; font-size:1.25rem !important; }
    .article-card ul, .article-card ol, .tool-card ul { color:#374151 !important; padding-left:1.1rem !important; }

    .article-card > a.btn,
    .article-card .btn-outline-primary {
      width:100% !important;
      box-sizing:border-box !important;
      display:inline-block !important;
      padding:.5rem .75rem !important;
      border-radius:8px !important;
      border:1px solid rgba(13,110,253,0.18) !important;
      color:#0d6efd !important;
      background:transparent !important;
      text-align:center !important;
      margin-top:.35rem !important;
      font-weight:600 !important;
    }

    .tool-card .back-link { color:#0d6efd !important; display:inline-block !important; margin-bottom:.6rem !important; text-decoration:none !important; }

    .clock-item { background:#f7fafc !important; border-radius:8px !important; padding:.8rem !important; margin-bottom:.6rem !important; display:flex !important; align-items:center !important; justify-content:space-between !important; }

    footer.site { text-align:center !important; margin-top:1.6rem !important; color:#6b7280 !important; }

    @media (max-width:900px) {
      .center-row { flex-direction:column !important; align-items:center !important; gap:1rem !important; }
      .article-card, .tool-card { width:98vw !important; max-width:540px !important; }
      .text-center.mb-4 h1 { font-size:1.8rem !important; }
    }

    /* --- Embedded language placement CSS --- */
    %%LANGUAGE_CSS%%
  </style>
</head>
<body>
  <div class="page-wrap">
    <div class="top-row">
      <label for="language-select-top" style="font-weight:600; margin-right:.5rem;">Language:</label>
      <!-- populated by JS; header select is primary -->
      <select id="language-select-top" class="language-select" aria-label="Language selector"></select>
    </div>

    <div class="text-center mb-4">
      <h1>%%TITLE%%</h1>
      <p class="lead">%%DESC%%</p>
    </div>

    <div class="center-row">
      <div class="article-card" aria-labelledby="howto-title">
        <div>
          <h2 id="howto-title"><i class="fa fa-globe"></i> %%HOWTO_TITLE%%</h2>
          <ol>
            %%HOWTO_STEPS%%
          </ol>
        </div>
        <a href="world-how-to-%%LANG%%.html" class="btn btn-outline-primary btn-sm">%%READ_ARTICLE%%</a>
      </div>

      <div class="tool-card" role="region" aria-label="World Clock">
        <a href="index.html" class="back-link">&larr; %%BACK_MAIN%%</a>
        <div class="world-section">
          <form class="clock-form" id="clockForm">
            <select id="cityDropdown" class="form-select city-dropdown">
              <option value="">%%SELECT_PROMPT%%</option>
            </select>
            <input type="text" id="cityInput" class="form-control awesomplete" placeholder="%%PLACEHOLDER%%" autocomplete="off" style="margin-top:.6rem;">
            <button type="submit" class="btn btn-success btn-sm" style="margin-top:.5rem; width:110px;">%%ADD_BTN%%</button>
          </form>

          <div id="errorMsg" style="color:#b00;margin-bottom:.6em;"></div>
          <div id="clockList" class="clock-list"></div>

        </div>

        <details class="faq-section" style="margin-top:1rem;">
          <summary style="font-weight:700; font-size:1rem;">%%FAQS%%</summary>
          <ul style="padding-left:1.1rem;">
            %%FAQ_BULLETS%%
          </ul>
        </details>
      </div>

      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> %%TIPS_TITLE%%</h2>
          <ul>
            %%TIPS_LIST%%
          </ul>
        </div>
        <a href="world-tips-%%LANG%%.html" class="btn btn-outline-primary btn-sm">%%READ_ARTICLE%%</a>
      </div>
    </div>

    <footer class="site">
      %%FOOTER%%
    </footer>
  </div>

  <script>
    // Clock logic (identical behavior as previous generator)
    const { DateTime } = luxon;
    let cityList = [];
    let cityToZone = {};
    let cityNames = [];
    let awesompleteInstance;

    fetch('world-cities.json')
      .then(r => r.json())
      .then(data => {
        cityList = data;
        cityToZone = {};
        cityNames = [];
        data.forEach(city => {
          cityToZone[city.name.toLowerCase()] = city.timezone;
          cityNames.push(city.name);
        });
        let dropdown = document.getElementById("cityDropdown");
        cityList.forEach(city => {
          if (city.name.toLowerCase() !== 'tokyo') {
            let opt = document.createElement("option");
            opt.value = city.timezone;
            opt.textContent = city.name;
            dropdown.appendChild(opt);
          }
        });
        let input = document.getElementById("cityInput");
        awesompleteInstance = new Awesomplete(input, {
          list: cityNames.filter(n => n.toLowerCase() !== 'tokyo'),
          minChars: 1,
          maxItems: 12,
          autoFirst: true
        });
      });

    let clocks = JSON.parse(localStorage.getItem('worldClocks') || '[]');
    function saveClocks() { localStorage.setItem('worldClocks', JSON.stringify(clocks)); }
    function renderClocks() {
      const list = document.getElementById('clockList');
      list.innerHTML = '';
      if (clocks.length === 0) {
        list.innerHTML = '<div style="color:#888;">%%NO_CLOCKS%%</div>';
        return;
      }
      clocks.forEach((clock, idx) => {
        let timeStr = '...';
        let error = false;
        try {
          let now = DateTime.now().setZone(clock.tz);
          if (!now.isValid) throw new Error("Invalid zone");
          timeStr = now.toFormat('cccc, dd LLL yyyy<br>HH:mm:ss');
        } catch {
          timeStr = 'Invalid time zone';
          error = true;
        }
        list.innerHTML += `
          <div class="clock-item">
            <span class="clock-meta"><i class="fa fa-clock"></i></span>
            <span><b>${clock.label}</b><br>${timeStr}${error ? ' <span style="color:#b00;">(Check spelling or use a valid city or IANA time zone)</span>' : ''}</span>
            <button class="btn btn-outline-danger btn-sm clock-btn" onclick="deleteClock(${idx})"><i class="fa fa-trash"></i></button>
          </div>
        `;
      });
    }

    function normalizeInput(input) { return input.trim().toLowerCase().replace(/[\\s\\-_]+/g, " "); }

    function addClock(label, tz) {
      clocks.push({ label, tz });
      saveClocks();
      renderClocks();
    }

    document.getElementById('clockForm').addEventListener('submit', function(e) {
      e.preventDefault();
      document.getElementById('errorMsg').textContent = '';
      let cityInput = document.getElementById('cityInput').value.trim();
      let dropdown = document.getElementById('cityDropdown').value;
      let label = '';
      let zone = '';
      if (dropdown) {
        label = document.getElementById('cityDropdown').options[document.getElementById('cityDropdown').selectedIndex].text;
        zone = dropdown;
      } else if (cityInput) {
        label = cityInput;
        if (/^[A-Za-z]+\\/[A-Za-z_]+$/.test(cityInput)) {
          zone = cityInput;
        } else {
          let norm = normalizeInput(cityInput);
          if (cityToZone[norm] && norm !== 'tokyo') {
            zone = cityToZone[norm];
          } else {
            document.getElementById('errorMsg').innerHTML = '%%ERROR_NOT_RECOGNIZED%% <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">Full list here</a>.';
            return;
          }
        }
      } else {
        document.getElementById('errorMsg').textContent = '%%PLEASE_SELECT%%';
        return;
      }
      addClock(label, zone);
      document.getElementById('cityInput').value = '';
      document.getElementById('cityDropdown').selectedIndex = 0;
    });

    window.deleteClock = function(idx) {
      clocks.splice(idx, 1);
      saveClocks();
      renderClocks();
    }

    setInterval(renderClocks, 1000);
    renderClocks();
  </script>

  <!-- Embedded unified header language selector + defensive localizer JS -->
  <script>
  %%LANGUAGE_JS%%
  </script>
</body>
</html>
"""

ARTICLE_TEMPLATE = """<!doctype html>
<html lang="%%LANG%%"%%DIR%%>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>%%PAGE_TITLE%%</title>
  <meta name="description" content="%%PAGE_DESC%%">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body { background:#f4f7fb !important; font-family:'Montserrat', Arial, sans-serif !important; color:#0b2545 !important; margin:0; }
    .page-wrap { max-width:1200px; margin:2.4rem auto !important; padding:0 1rem !important; box-sizing:border-box; }
    .top-row { display:flex !important; justify-content:flex-end !important; gap:.6rem !important; margin-bottom:.6rem !important; align-items:center; }
    .language-select { width:180px !important; border-radius:10px !important; padding:.28rem .6rem !important; border:1px solid rgba(13,110,253,0.18) !important; background:#fff !important; color:#0d6efd !important; font-weight:600 !important; }
    .container { max-width:820px; margin:0 auto; }
    .article-card { background:#fff !important; border-radius:14px !important; padding:2rem !important; box-shadow:0 6px 18px rgba(11,37,69,0.06) !important; box-sizing:border-box !important; }
    .back-link { color:#0d6efd !important; font-weight:600 !important; display:inline-block !important; margin-bottom:1rem !important; text-decoration:none !important; }
    h1.title { color:#185a9d !important; font-size:2rem !important; margin-bottom:.4rem !important; }
    ul, ol { color:#374151 !important; padding-left:1.2rem !important; }
    .article-card a.btn { width:100% !important; box-sizing:border-box !important; display:inline-block !important; padding:.5rem .75rem !important; border-radius:8px !important; border:1px solid rgba(13,110,253,0.18) !important; color:#0d6efd !important; background:transparent !important; text-align:center !important; margin-top:1rem !important; font-weight:600 !important; }
    %%LANGUAGE_CSS%%
  </style>
</head>
<body>
  <div class="page-wrap">
    <div class="top-row">
      <label for="language-select-top" style="font-weight:600; margin-right:.5rem;">Language:</label>
      <select id="language-select-top" class="language-select" aria-label="Language selector"></select>
    </div>

    <a class="back-link" href="world-clock-%%LANG%%.html">&larr; %%BACK_BTN%%</a>

    <div class="container">
      <div class="article-card">
        <h1 class="title">%%PAGE_TITLE%%</h1>
        <p class="lead">%%PAGE_DESC%%</p>
        %%BODY_HTML%%
        <a class="btn btn-outline-primary" href="world-clock-%%LANG%%.html" style="margin-top:1rem;">%%BACK_BTN%%</a>
      </div>

      <footer class="site">
        &copy; 2025 TimerHaven.
      </footer>
    </div>
  </div>

  <!-- Unified header language selector (same as main) -->
  <script>
  %%LANGUAGE_JS%%
  </script>
</body>
</html>
"""

# Helper functions
def escape_html(s: str) -> str:
    return html.escape(s) if isinstance(s, str) else ""

def build_lang_options(selected: str) -> str:
    order = [("en", "English"), ("fr", "Français"), ("es", "Español"),
             ("de", "Deutsch"), ("ru", "Русский"), ("el", "Ελληνικά"), ("ar", "العربية")]
    parts: List[str] = []
    for code, name in order:
        sel = " selected" if code == selected else ""
        parts.append(f'<option value="{code}"{sel}>{html.escape(name)}</option>')
    return "\n        ".join(parts)

def ensure_out_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_faq_bullets(lang: str) -> str:
    mapping = {
        "en": [
            "<li><b>Add a city:</b> Use the dropdown for popular cities or start typing any city name.</li>",
            "<li><b>Compare times:</b> Add multiple clocks to compare zones.</li>",
            "<li><b>Remove:</b> Click the Remove button to delete a city from your list.</li>",
            '<li>Full list of time zones: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">See here</a></li>'
        ],
        "fr": [
            "<li><b>Ajouter une ville :</b> Utilisez le menu pour les villes populaires ou commencez à taper le nom.</li>",
            "<li><b>Comparer les heures :</b> Ajoutez plusieurs horloges pour comparer les fuseaux.</li>",
            "<li><b>Supprimer :</b> Cliquez sur Supprimer pour retirer une ville de votre liste.</li>",
            '<li>Liste complète des fuseaux horaires : <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">Voir ici</a></li>'
        ],
        "es": [
            "<li><b>Agregar una ciudad:</b> Use el desplegable para ciudades populares o comience a escribir.</li>",
            "<li><b>Comparar horas:</b> Agregue varias ciudades para verlas lado a lado.</li>",
            "<li><b>Eliminar:</b> Haga clic en Eliminar para quitar una ciudad de su lista.</li>",
            '<li>Lista completa de zonas horarias: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">Ver aquí</a></li>'
        ],
        "de": [
            "<li><b>Stadt hinzufügen:</b> Verwenden Sie das Auswahlmenü oder beginnen Sie mit der Eingabe des Stadtnamens.</li>",
            "<li><b>Zeiten vergleichen:</b> Fügen Sie mehrere Städte hinzu, um Zeiten nebeneinander zu sehen.</li>",
            "<li><b>Entfernen:</b> Klicken Sie auf Entfernen, um eine Stadt aus Ihrer Liste zu löschen.</li>",
            '<li>Vollständige Liste der Zeitzonen: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">Hier ansehen</a></li>'
        ],
        "ru": [
            "<li><b>Добавьте город:</b> Используйте выпадающий список или начните вводить название города.</li>",
            "<li><b>Сравнить время:</b> Добавьте несколько городов, чтобы сравнить время.</li>",
            "<li><b>Удалить:</b> Нажмите Удалить, чтобы удалить город из списка.</li>",
            '<li>Полный список часовых поясов: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">См. здесь</a></li>'
        ],
        "el": [
            "<li><b>Προσθέστε πόλη:</b> Χρησιμοποιήστε τη λίστα ή ξεκινήστε να πληκτρολογείτε το όνομα.</li>",
            "<li><b>Συγκρίνετε ώρες:</b> Προσθέστε πολλές πόλεις για σύγκριση.</li>",
            "<li><b>Κατάργηση:</b> Κάντε κλικ για να διαγράψετε μια πόλη από τη λίστα σας.</li>",
            '<li>Πλήρης λίστα ζωνών ώρας: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">Δείτε εδώ</a></li>'
        ],
        "ar": [
            "<li><b>أضف مدينة:</b> استخدم القائمة أو ابدأ بالكتابة لاسم المدينة.</li>",
            "<li><b>قارن الأوقات:</b> أضف مدنًا متعددة للمقارنة.</li>",
            "<li><b>إزالة:</b> انقر لإزالة المدينة من قائمتك.</li>",
            '<li>القائمة الكاملة للمناطق الزمنية: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones" target="_blank">انظر هنا</a></li>'
        ]
    }
    arr = mapping.get(lang, mapping['en'])
    return "\n            ".join(arr)

def generate_pages(write_root: bool = False) -> None:
    ensure_out_dir()
    for code, data in TRANSLATIONS.items():
        ui = data["ui"]
        main = data["main"]
        howto = data["howto"]
        tips = data["tips"]

        howto_steps = "\n            ".join(f"<li>{s}</li>" for s in howto["steps"])
        tips_list = "\n            ".join(f"<li>{t}</li>" for t in tips["tips"])
        faq_bullets = build_faq_bullets(code)

        repl = {
            "%%LANG%%": code,
            "%%DIR%%": data.get("dir", ""),
            "%%TITLE%%": escape_html(main.get("title", "")),
            "%%DESC%%": escape_html(main.get("desc", "")),
            "%%H1%%": escape_html(main.get("h1", "")),
            "%%SELECT_PROMPT%%": escape_html(ui.get("select_prompt", "")),
            "%%PLACEHOLDER%%": escape_html(ui.get("placeholder", "")),
            "%%ADD_BTN%%": escape_html(ui.get("add_btn", "")),
            "%%NO_CLOCKS%%": escape_html(ui.get("no_clocks", "")),
            "%%FAQS%%": escape_html(ui.get("faqs", "")),
            "%%READ_ARTICLE%%": escape_html(ui.get("read_article", "")),
            "%%BACK_MAIN%%": escape_html(ui.get("back_main", "")),
            "%%HOWTO_TITLE%%": escape_html(howto.get("title", "")),
            "%%HOWTO_STEPS%%": howto_steps,
            "%%TIPS_TITLE%%": escape_html(tips.get("title", "")),
            "%%TIPS_LIST%%": tips_list,
            "%%ERROR_NOT_RECOGNIZED%%": escape_html(ui.get("error_not_recognized", "")),
            "%%PLEASE_SELECT%%": escape_html(ui.get("please_select", "")),
            "%%FOOTER%%": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>',
            "%%LANG_OPTIONS%%": build_lang_options(code),
            "%%FAQ_BULLETS%%": faq_bullets,
            "%%LANGUAGE_CSS%%": LANGUAGE_CSS,
            "%%LANGUAGE_JS%%": LANGUAGE_JS
        }

        # Main page
        html_out = MAIN_TEMPLATE
        for k, v in repl.items():
            html_out = html_out.replace(k, v)
        main_path = os.path.join(OUTPUT_DIR, f"world-clock-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(html_out)

        # How-to article
        howto_body = "<ol>\n        " + howto_steps + "\n      </ol>"
        howto_html = ARTICLE_TEMPLATE
        howto_html = howto_html.replace("%%LANG%%", code).replace("%%DIR%%", data.get("dir", ""))
        howto_html = howto_html.replace("%%PAGE_TITLE%%", escape_html(howto.get("title", "")))
        howto_html = howto_html.replace("%%PAGE_DESC%%", "")
        howto_html = howto_html.replace("%%BODY_HTML%%", howto_body)
        howto_html = howto_html.replace("%%BACK_BTN%%", escape_html(howto.get("back_btn", "")))
        howto_html = howto_html.replace("%%LANG_OPTIONS%%", build_lang_options(code))
        # inject language CSS/JS
        howto_html = howto_html.replace("%%LANGUAGE_CSS%%", LANGUAGE_CSS).replace("%%LANGUAGE_JS%%", LANGUAGE_JS)
        howto_path = os.path.join(OUTPUT_DIR, f"world-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(howto_html)

        # Tips article
        tips_body = "<ul>\n        " + tips_list + "\n      </ul>"
        tips_html = ARTICLE_TEMPLATE
        tips_html = tips_html.replace("%%LANG%%", code).replace("%%DIR%%", data.get("dir", ""))
        tips_html = tips_html.replace("%%PAGE_TITLE%%", escape_html(tips.get("title", "")))
        tips_html = tips_html.replace("%%PAGE_DESC%%", "")
        tips_html = tips_html.replace("%%BODY_HTML%%", tips_body)
        tips_html = tips_html.replace("%%BACK_BTN%%", escape_html(tips.get("back_btn", "")))
        tips_html = tips_html.replace("%%LANG_OPTIONS%%", build_lang_options(code))
        tips_html = tips_html.replace("%%LANGUAGE_CSS%%", LANGUAGE_CSS).replace("%%LANGUAGE_JS%%", LANGUAGE_JS)
        tips_path = os.path.join(OUTPUT_DIR, f"world-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(tips_html)

    # landing redirect inside output dir
    redirect_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="refresh" content="0; url=world-clock-en.html"/>
  <meta name="robots" content="noindex"/>
</head>
<body>If you are not redirected, <a href="world-clock-en.html">open World Clock (English)</a>.</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, "world-clock.html"), "w", encoding="utf-8") as f:
        f.write(redirect_html)

    if write_root:
        with open("world-clock.html", "w", encoding="utf-8") as f:
            f.write(redirect_html)

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    generate_pages(write_root=write_root)
    print(f"All pages generated in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()