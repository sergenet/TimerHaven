#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_stopwatch.py

Generates static HTML pages for the "Stopwatch" tool in 7 languages:
 - Main Tool Pages:      stopwatch-xx.html
 - How-to Article Pages: stopwatch-how-to-xx.html
 - Tips Article Pages:   stopwatch-tips-xx.html
 - A redirect landing page: stopwatch.html (in output folder)

Output folder (default): ./stopwatch_pages

Usage:
  python generate_stopwatch.py            # writes files to ./stopwatch_pages
  python generate_stopwatch.py --root     # also writes stopwatch.html into current dir
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "stopwatch_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "start": "Start",
            "pause": "Pause",
            "reset": "Reset",
            "lap": "Lap",
            "howto_title": "How to Use Stopwatch",
            "tips_title": "Stopwatch Productivity Tips",
        },
        "main": {
            "title": "Stopwatch — TimerHaven",
            "desc": "Measure elapsed time for any activity. Learn how to use Stopwatch, get productivity tips, FAQs, and read expert articles.",
            "howto_link": "stopwatch-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "stopwatch-tips-en.html",
            "tips_btn": "Read Full Article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Can I track multiple laps?</b> Yes, use the lap button.",
                "<b>Will the time persist?</b> No, it resets after page reload.",
                "<b>Is this free?</b> Yes, all TimerHaven tools are free."
            ],
            "back_main": "Back to Main Menu",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Stopwatch — TimerHaven",
            "desc": "The Stopwatch tool is ideal for tracking elapsed time and split intervals.",
            "steps": [
                "<b>Start the timer:</b> Click <strong>Start</strong> to begin tracking time.",
                "<b>Pause or reset:</b> Use <strong>Pause</strong> and <strong>Reset</strong> as needed.",
                "<b>Track laps:</b> Click <strong>Lap</strong> to record split times."
            ],
            "back_btn": "Back to Stopwatch",
            "back_link": "stopwatch-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Stopwatch Tips — TimerHaven",
            "desc": "Maximize accuracy and efficiency with these Stopwatch tips:",
            "tips": [
                "<b>Use laps for intervals:</b> Track split times in workouts or sets.",
                "<b>Pause and resume:</b> Useful for rest periods or interruptions.",
                "<b>Reset between activities:</b> Start fresh each session."
            ],
            "back_btn": "Back to Stopwatch",
            "back_link": "stopwatch-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {"start":"Démarrer","pause":"Pause","reset":"Réinitialiser","lap":"Tour"},
        "main": {
            "title":"Chronomètre — TimerHaven",
            "desc":"Mesurez le temps écoulé pour toute activité. Apprenez à utiliser le Chronomètre, obtenez des conseils, FAQs et articles.",
            "howto_link":"stopwatch-how-to-fr.html","howto_btn":"Lire l'article",
            "tips_link":"stopwatch-tips-fr.html","tips_btn":"Lire l'article",
            "faq_title":"FAQs",
            "faq_items":[
                "<b>Puis-je suivre plusieurs tours ?</b> Oui, utilisez le bouton Tour.",
                "<b>Le temps persiste-t-il ?</b> Non, il est réinitialisé au rechargement.",
                "<b>Est-ce gratuit ?</b> Oui, tous les outils TimerHaven sont gratuits."
            ],
            "back_main": "Retour au menu principal",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique</a>'
        },
        "howto": {
            "title":"Comment utiliser le Chronomètre — TimerHaven",
            "desc":"Le Chronomètre est parfait pour suivre le temps écoulé et les intervalles.",
            "steps":[
                "<b>Démarrez le minuteur :</b> Cliquez sur <strong>Démarrer</strong>.",
                "<b>Pause / Réinitialiser :</b> Utilisez <strong>Pause</strong> et <strong>Réinitialiser</strong>.",
                "<b>Enregistrez des tours :</b> Cliquez sur <strong>Tour</strong>."
            ],
            "back_btn":"Retour au Chronomètre","back_link":"stopwatch-fr.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"Conseils Chronomètre — TimerHaven",
            "desc":"Optimisez la précision et l'efficacité avec ces conseils :",
            "tips":[
                "<b>Utilisez les tours :</b> Suivez les temps partiels pour l'entraînement.",
                "<b>Pause et reprise :</b> Pratique pour les interruptions.",
                "<b>Réinitialisez :</b> Pour des sessions séparées."
            ],
            "back_btn":"Retour au Chronomètre","back_link":"stopwatch-fr.html","footer":DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {"start":"Iniciar","pause":"Pausa","reset":"Reiniciar","lap":"Vuelta"},
        "main": {
            "title":"Cronómetro — TimerHaven",
            "desc":"Mide el tiempo transcurrido para cualquier actividad. Aprende a usar el Cronómetro, obtén consejos, FAQs y artículos.",
            "howto_link":"stopwatch-how-to-es.html","howto_btn":"Leer el artículo",
            "tips_link":"stopwatch-tips-es.html","tips_btn":"Leer el artículo",
            "faq_title":"FAQs",
            "faq_items":[
                "<b>¿Puedo registrar varias vueltas?</b> Sí, usa el botón Vuelta.",
                "<b>¿Persiste el tiempo?</b> No, se reinicia al recargar la página.",
                "<b>¿Es gratis?</b> Sí, todas las herramientas TimerHaven son gratis."
            ],
            "back_main": "Volver al menú principal",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política</a>'
        },
        "howto": {
            "title":"Cómo usar el Cronómetro — TimerHaven",
            "desc":"El Cronómetro es ideal para medir el tiempo y los intervalos.",
            "steps":[
                "<b>Inicie el temporizador:</b> Haga clic en <strong>Iniciar</strong>.",
                "<b>Pausa / Reiniciar:</b> Use <strong>Pausa</strong> y <strong>Reiniciar</strong>.",
                "<b>Registre vueltas:</b> Haga clic en <strong>Vuelta</strong>."
            ],
            "back_btn":"Volver al Cronómetro","back_link":"stopwatch-es.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"Consejos Cronómetro — TimerHaven",
            "desc":"Maximiza precisión y eficiencia con estos consejos:",
            "tips":[
                "<b>Usa vueltas para intervalos:</b> Registra tiempos parciales.",
                "<b>Pausa y reanuda:</b> Útil en interrupciones.",
                "<b>Reinicia entre actividades:</b> Mantén registros limpios."
            ],
            "back_btn":"Volver al Cronómetro","back_link":"stopwatch-es.html","footer":DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {"start":"Start","pause":"Pause","reset":"Zurücksetzen","lap":"Runde"},
        "main": {
            "title":"Stoppuhr — TimerHaven",
            "desc":"Messe die verstrichene Zeit für jede Aktivität. Erfahren Sie, wie die Stoppuhr funktioniert, erhalten Sie Tipps, FAQs und Artikel.",
            "howto_link":"stopwatch-how-to-de.html","howto_btn":"Artikel lesen",
            "tips_link":"stopwatch-tips-de.html","tips_btn":"Artikel lesen",
            "faq_title":"FAQs",
            "faq_items":[
                "<b>Kann ich mehrere Runden aufzeichnen?</b> Ja, verwenden Sie die Schaltfläche Runde.",
                "<b>Bleibt die Zeit erhalten?</b> Nein, beim Neuladen wird zurückgesetzt.",
                "<b>Ist das kostenlos?</b> Ja, alle TimerHaven-Tools sind kostenlos."
            ],
            "back_main": "Zurück zum Hauptmenü",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a>'
        },
        "howto": {
            "title":"So verwenden Sie die Stoppuhr — TimerHaven",
            "desc":"Die Stoppuhr ist ideal zum Messen von Zeit und Intervallen.",
            "steps":[
                "<b>Starten:</b> Klicken Sie auf <strong>Start</strong>.",
                "<b>Pausieren / Zurücksetzen:</b> Nutze <strong>Pause</strong> und <strong>Zurücksetzen</strong>.",
                "<b>Runden aufzeichnen:</b> Klicken Sie auf <strong>Runde</strong>."
            ],
            "back_btn":"Zurück zur Stoppuhr","back_link":"stopwatch-de.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"Stoppuhr-Tipps — TimerHaven",
            "desc":"Verbessern Sie Genauigkeit und Effizienz mit diesen Tipps:",
            "tips":[
                "<b>Runden für Intervalle:</b> Verfolgen Sie Split-Zeiten.",
                "<b>Pausieren und fortsetzen:</b> Praktisch bei Unterbrechungen.",
                "<b>Zurücksetzen zwischen Sessions:</b> Für klare Aufzeichnungen."
            ],
            "back_btn":"Zurück zur Stoppuhr","back_link":"stopwatch-de.html","footer":DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {"start":"Старт","pause":"Пауза","reset":"Сброс","lap":"Круг"},
        "main": {
            "title":"Секундомер — TimerHaven",
            "desc":"Измеряйте прошедшее время для любой активности. Узнайте, как пользоваться секундомером, получите советы и FAQs.",
            "howto_link":"stopwatch-how-to-ru.html","howto_btn":"Читать статью",
            "tips_link":"stopwatch-tips-ru.html","tips_btn":"Читать статью",
            "faq_title":"FAQs",
            "faq_items":[
                "<b>Можно ли записывать несколько кругов?</b> Да, нажмите кнопку Круг.",
                "<b>Сохранится ли время?</b> Нет, после перезагрузки сбрасывается.",
                "<b>Это бесплатно?</b> Да, все инструменты TimerHaven бесплатны."
            ],
            "back_main": "Назад в главное меню",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика</a>'
        },
        "howto": {
            "title":"Как пользоваться секундомером — TimerHaven",
            "desc":"Секундомер отлично подходит для измерения времени и интервалов.",
            "steps":[
                "<b>Запустите таймер:</b> Нажмите <strong>Старт</strong>.",
                "<b>Пауза/сброс:</b> Используйте <strong>Пауза</strong> и <strong>Сброс</strong>.",
                "<b>Запись кругов:</b> Нажмите <strong>Круг</strong>."
            ],
            "back_btn":"Вернуться к секундомеру","back_link":"stopwatch-ru.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"Советы по секундомеру — TimerHaven",
            "desc":"Повышайте точность и эффективность с этими советами:",
            "tips":[
                "<b>Используйте круги для интервалов:</b> Фиксируйте сплит‑время.",
                "<b>Пауза и возобновление:</b> Удобно при прерываниях.",
                "<b>Сброс между сессиями:</b> Для чистых записей."
            ],
            "back_btn":"Вернуться к секундомеру","back_link":"stopwatch-ru.html","footer":DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {"start":"Έναρξη","pause":"Παύση","reset":"Επαναφορά","lap":"Γύρος"},
        "main": {
            "title":"Χρονόμετρο — TimerHaven",
            "desc":"Μετρήστε τον χρόνο για οποιαδήποτε δραστηριότητα. Μάθετε πώς λειτουργεί το Χρονόμετρο, δείτε συμβουλές και FAQs.",
            "howto_link":"stopwatch-how-to-el.html","howto_btn":"Διαβάστε το άρθρο",
            "tips_link":"stopwatch-tips-el.html","tips_btn":"Διαβάστε το άρθρο",
            "faq_title":"FAQs",
            "faq_items":[
                "<b>Μπορώ να καταγράψω πολλούς γύρους;</b> Ναι, χρησιμοποιήστε το κουμπί Γύρος.",
                "<b>Θα διατηρηθεί ο χρόνος;</b> Όχι, επανέρχεται μετά από ανανέωση.",
                "<b>Είναι δωρεάν;</b> Ναι, όλα τα εργαλεία TimerHaven είναι δωρεάν."
            ],
            "back_main": "Επιστροφή στο κύριο μενού",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική</a>'
        },
        "howto": {
            "title":"Πώς να χρησιμοποιήσετε το Χρονόμετρο — TimerHaven",
            "desc":"Το χρονόμετρο είναι ιδανικό για καταγραφή χρόνου και διαστημάτων.",
            "steps":[
                "<b>Εκκίνηση:</b> Πατήστε <strong>Έναρξη</strong>.",
                "<b>Παύση/Επαναφορά:</b> Χρησιμοποιήστε <strong>Παύση</strong> και <strong>Επαναφορά</strong>.",
                "<b>Καταγραφή γύρων:</b> Πατήστε <strong>Γύρος</strong>."
            ],
            "back_btn":"Επιστροφή στο Χρονόμετρο","back_link":"stopwatch-el.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"Συμβουλές Χρονόμετρου — TimerHaven",
            "desc":"Βελτιώστε την ακρίβεια και αποδοτικότητα με αυτές τις συμβουλές:",
            "tips":[
                "<b>Χρησιμοποιήστε γύρους για διαστήματα:</b> Καταγράψτε τα split times.",
                "<b>Παύση και συνέχιση:</b> Χρήσιμο σε διακοπές.",
                "<b>Επαναφορά ανά δραστηριότητα:</b> Για καθαρά αρχεία."
            ],
            "back_btn":"Επιστροφή στο Χρονόμετρο","back_link":"stopwatch-el.html","footer":DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {"start":"ابدأ","pause":"إيقاف مؤقت","reset":"إعادة ضبط","lap":"لفة"},
        "main": {
            "title":"الموقت — TimerHaven",
            "desc":"قِس الوقت المنقضي لأي نشاط. تعلّم كيفية استخدام الموقت، واحصل على نصائح والأسئلة الشائعة.",
            "howto_link":"stopwatch-how-to-ar.html","howto_btn":"اقرأ المقالة",
            "tips_link":"stopwatch-tips-ar.html","tips_btn":"اقرأ المقالة",
            "faq_title":"الأسئلة الشائعة",
            "faq_items":[
                "<b>هل يمكن تسجيل لفات متعددة؟</b> نعم، استخدم زر اللفة.",
                "<b>هل يبقى الوقت محفوظاً؟</b> لا، يعاد عند إعادة التحميل.",
                "<b>هل هو مجاني؟</b> نعم، جميع أدوات TimerHaven مجانية."
            ],
            "back_main": "العودة إلى القائمة الرئيسية",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a>'
        },
        "howto": {
            "title":"كيفية استخدام الموقت — TimerHaven",
            "desc":"الموقت مناسب لقياس الوقت والفترات.",
            "steps":[
                "<b>ابدأ المؤقت:</b> اضغط <strong>ابدأ</strong>.",
                "<b>إيقاف/إعادة ضبط:</b> استخدم <strong>إيقاف مؤقت</strong> و <strong>إعادة ضبط</strong>.",
                "<b>سجل لفات:</b> اضغط <strong>لفة</strong>."
            ],
            "back_btn":"العودة إلى الموقت","back_link":"stopwatch-ar.html","footer":DEFAULT_COPYRIGHT
        },
        "tips": {
            "title":"نصائح الموقت — TimerHaven",
            "desc":"حسّن الدقة والكفاءة بهذه النصائح:",
            "tips":[
                "<b>استخدم اللفات للفترات:</b> سجل split times.",
                "<b>إيقاف مؤقت واستئناف:</b> مفيد عند المقاطعات.",
                "<b>إعادة ضبط بين الجلسات:</b> للحفاظ على سجلات نظيفة."
            ],
            "back_btn":"العودة إلى الموقت","back_link":"stopwatch-ar.html","footer":DEFAULT_COPYRIGHT
        }
    }
}

ALLOWED_INLINE_TAGS = {"b", "strong", "a", "br"}

def escape_allow_tags(s: str) -> str:
    if not isinstance(s, str):
        return ""
    esc = html.escape(s, quote=True)
    for tag in ALLOWED_INLINE_TAGS:
        esc = esc.replace(html.escape(f"<{tag}>"), f"<{tag}>")
        esc = esc.replace(html.escape(f"</{tag}>"), f"</{tag}>")
        esc = esc.replace(html.escape(f"<{tag} "), f"<{tag} ")
    return esc

def generate_main_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]

    # MAIN CARD: localized back_main (falls back to English)
    back_label = main.get("back_main", "Back to Main Menu")

    faq_html = "\n".join(f"<li>{escape_allow_tags(item)}</li>" for item in main.get("faq_items", []))
    language_options = [
        ("en", "English"), ("fr", "Français"), ("es", "Español"),
        ("de", "Deutsch"), ("ru", "Русский"), ("el", "Ελληνικά"), ("ar", "العربية")
    ]
    options_html = "".join(
        f'<option value="{lang}"{" selected" if lang == code else ""}>{html.escape(name)}</option>'
        for lang, name in language_options
    )

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape_allow_tags(main.get('title',''))}</title>
  <meta name="description" content="{escape_allow_tags(main.get('desc',''))}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body {{ background:#f4f7fb; font-family:'Montserrat', Arial, sans-serif; color:#0b2545; }}
    .page-wrap {{ max-width:1200px; margin:2rem auto; padding:0 1rem; }}
    .top-row {{ display:flex; justify-content:flex-end; gap:.6rem; margin-bottom:.6rem; }}
    .language-select {{ width:220px; border-radius:10px; padding:.28rem .6rem; border:1px solid rgba(13,110,253,0.25); background:#fff; color:#0d6efd; }}
    .center-row {{ display:flex; gap:1.6rem; justify-content:center; align-items:flex-start; }}
    .article-card, .tool-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); width:340px; padding:1.3rem; }}
    .article-card h2 {{ color:#185a9d; font-size:1.25rem; margin-bottom:.6rem; }}
    .tool-card h3 {{ color:#185a9d; font-size:1.35rem; margin-bottom:.5rem; }}
    .stopwatch-display {{ font-weight:700; font-size:1.25rem; margin-top:.5rem; margin-bottom:.5rem; }}
    .controls-row {{ display:flex; gap:.5rem; align-items:center; flex-wrap:wrap; margin-top:.5rem; }}
    .lap-list {{ margin-top:.8rem; }}
    .faq-section {{ margin-top:1rem; background:#f7fafc; border-radius:8px; padding:1rem; }}
    .btn-small {{ padding:.35rem .7rem; font-size:.9rem; }}
    footer.site {{ text-align:center; margin-top:1.5rem; color:#6b7280; }}
    @media (max-width:900px) {{ .center-row{{flex-direction:column;align-items:center;}} .article-card, .tool-card{{width:98%; max-width:540px;}} }}
  </style>
</head>
<body>
  <div class="page-wrap">
    <div class="top-row">
      <label for="language-select-top" style="align-self:center; font-weight:600; margin-right:.5rem;">Language:</label>
      <select id="language-select-top" class="language-select" aria-label="Language selector">
        {options_html}
      </select>
    </div>

    <div class="text-center mb-4">
      <h1 style="margin-bottom:.25rem;">{escape_allow_tags(main.get('title',''))}</h1>
      <p class="lead" style="color:#374151; margin-bottom:1rem;">{escape_allow_tags(main.get('desc',''))}</p>
    </div>

    <div class="center-row">
      <!-- Left summary card -->
      <div class="article-card">
        <div>
          <h2><i class="fa fa-clock"></i> {escape_allow_tags(data.get('howto',{}).get('title', ui.get('howto_title','How to Use Stopwatch')))}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in data.get('howto',{}).get('steps', []))}
          </ol>
        </div>
        <a href="{main.get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <!-- Main tool card -->
      <div class="tool-card" role="region" aria-label="Stopwatch">
        <a href="index.html" class="d-block mb-2" style="text-decoration:none; color:#0d6efd; font-weight:600;">&larr; {escape_allow_tags(back_label)}</a>
        <h3><i class="fa fa-clock"></i> {escape_allow_tags(main.get('title','Stopwatch'))}</h3>

        <div class="stopwatch-section" aria-live="polite">
          <div id="swDisplay" class="stopwatch-display">00:00:00</div>

          <div class="controls-row">
            <button id="swStartBtn" class="btn btn-success btn-small">{escape_allow_tags(ui.get('start','Start'))}</button>
            <button id="swPauseBtn" class="btn btn-secondary btn-small">{escape_allow_tags(ui.get('pause','Pause'))}</button>
            <button id="swResetBtn" class="btn btn-danger btn-small">{escape_allow_tags(ui.get('reset','Reset'))}</button>
            <button id="swLapBtn" class="btn btn-info btn-small">{escape_allow_tags(ui.get('lap','Lap'))}</button>
          </div>

          <div id="lapList" class="lap-list"></div>

          <details class="faq-section" style="margin-top:1rem;">
            <summary style="font-weight:700; font-size:1rem;">{escape_allow_tags(main.get('faq_title'))}</summary>
            <ul style="padding-left:1.1rem; color:#374151;">
              {faq_html}
            </ul>
          </details>
        </div>
      </div>

      <!-- Right summary card -->
      <div class="article-card">
        <div>
          <h2><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {escape_allow_tags(data.get('tips',{}).get('title', ui.get('tips_title','Stopwatch Tips')))}</h2>
          <ul style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in data.get('tips',{}).get('tips', []))}
          </ul>
        </div>
        <a href="{main.get('tips_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('tips_btn'))}</a>
      </div>
    </div>

    <footer class="site" style="text-align:center; margin-top:1.5rem; color:#6b7280;">
      {main.get('footer')}
    </footer>
  </div>

  <script>
  (function(){{
    // language selector redirect
    var sel = document.getElementById('language-select-top');
    if (sel) {{
      sel.addEventListener('change', function() {{
        var v = this.value || 'en';
        window.location.href = 'stopwatch-' + v + '.html';
      }});
    }}

    // Stopwatch logic (keeps the same behavior on all localized pages)
    var swTimer = null, swStart = null, swElapsed = 0, swRunning = false, laps = [];
    function swFormat(ms) {{
      var t = Math.floor(ms / 1000);
      var h = Math.floor(t / 3600);
      var m = Math.floor((t % 3600) / 60);
      var s = t % 60;
      return String(h).padStart(2,'0')+":"+String(m).padStart(2,'0')+":"+String(s).padStart(2,'0');
    }}
    function renderLaps() {{
      var lapList = document.getElementById('lapList');
      lapList.innerHTML = laps.map(function(l,i){{
        return '<div class="lap-item">Lap '+(i+1)+': '+swFormat(l)+'</div>';
      }}).join('');
    }}
    function swUpdateDisplay() {{
      document.getElementById('swDisplay').textContent = swFormat(swElapsed);
      renderLaps();
    }}
    document.getElementById('swStartBtn').onclick = function() {{
      if (swRunning) return;
      swRunning = true;
      swStart = Date.now() - swElapsed;
      swTimer = setInterval(function(){{
        swElapsed = Date.now() - swStart;
        swUpdateDisplay();
      }}, 100);
    }};
    document.getElementById('swPauseBtn').onclick = function() {{
      swRunning = false;
      clearInterval(swTimer);
    }};
    document.getElementById('swResetBtn').onclick = function() {{
      swRunning = false;
      clearInterval(swTimer);
      swElapsed = 0;
      laps = [];
      swUpdateDisplay();
    }};
    document.getElementById('swLapBtn').onclick = function() {{
      if (swRunning) laps.push(swElapsed);
      swUpdateDisplay();
    }};
    swUpdateDisplay();
  }})();
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js"></script>
</body>
</html>
"""
    return html_out

def generate_article_html(code: str, section: Dict, page_type: str) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    title = escape_allow_tags(section.get("title",""))
    desc = escape_allow_tags(section.get("desc",""))
    back_link = section.get("back_link", f"stopwatch-{code}.html")
    back_btn = escape_allow_tags(section.get("back_btn","Back to Stopwatch"))

    if page_type == "howto":
        steps_html = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in section.get("steps", []))
        extra = f"""
      <h2>Step-by-Step Guide</h2>
      <ol>
        {steps_html}
      </ol>
"""
    else:
        tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", []))
        extra = f"""
      <h2>Top Tips</h2>
      <ul>
        {tips_html}
      </ul>
"""

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body {{ background:#f4f7fb; font-family:'Montserrat', Arial, sans-serif; color:#0b2545; }}
    .page {{ max-width:820px; margin:2.2rem auto; padding:0 1rem; }}
    .article-card {{ background:#fff; border-radius:14px; padding:2rem; box-shadow:0 6px 18px rgba(11,37,69,0.06); }}
    a.back-link {{ color:#0d6efd; font-weight:600; display:inline-block; margin-bottom:1rem; text-decoration:none; }}
    h1.title {{ color:#2bbf9a; font-size:2rem; margin-bottom:.4rem; }}
    p.lead {{ color:#374151; margin-bottom:1rem; }}
    .section-title {{ font-size:1.125rem; margin-top:1.25rem; margin-bottom:.6rem; }}
    ul, ol {{ color:#374151; padding-left:1.2rem; }}
    .back-bottom {{ margin-top:1.25rem; display:inline-block; }}
    footer.site {{ color:#6b7280; margin-top:1.5rem; text-align:center; }}
    @media (max-width:900px) {{ .page {{ margin:1rem auto; }} .article-card {{ padding:1rem; }} h1.title {{ font-size:1.6rem; }} }}
  </style>
</head>
<body>
  <div class="page">
    <a class="back-link" href="{back_link}">&larr; {back_btn}</a>

    <div class="article-card">
      <h1 class="title">{title}</h1>
      <p class="lead">{desc}</p>

      {extra}

      <a class="btn btn-outline-primary back-bottom" href="{back_link}">{back_btn}</a>
    </div>

    <footer class="site">{section.get('footer','')}</footer>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return html_out

def generate_redirect_html() -> str:
    html_out = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Stopwatch — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=stopwatch-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'stopwatch-en.html',
        'fr': 'stopwatch-fr.html',
        'es': 'stopwatch-es.html',
        'de': 'stopwatch-de.html',
        'ru': 'stopwatch-ru.html',
        'el': 'stopwatch-el.html',
        'ar': 'stopwatch-ar.html'
      };
      function getQueryLang() {
        try {
          var m = location.search.match(/[?&]lang=([a-z]{2})/i);
          return m ? m[1].toLowerCase() : null;
        } catch (e) { return null; }
      }
      function pickByNavigator() {
        var langs = [];
        try {
          if (navigator.languages) langs = langs.concat(navigator.languages);
          if (navigator.language) langs.push(navigator.language);
          if (navigator.userLanguage) langs.push(navigator.userLanguage);
        } catch (e) {}
        for (var i=0;i<langs.length;i++) {
          if (!langs[i]) continue;
          var code = String(langs[i]).toLowerCase().split('-')[0];
          if (map[code]) return code;
        }
        return null;
      }
      var q = getQueryLang();
      if (q && map[q]) { window.location.replace(map[q]); return; }
      var d = pickByNavigator();
      if (d && map[d]) { window.location.replace(map[d]); return; }
      window.location.replace(map['en']);
    })();
  </script>
</head>
<body>
  <div class="box">
    <h1>Stopwatch — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="stopwatch-en.html">English</a></li>
      <li><a href="stopwatch-fr.html">Français</a></li>
      <li><a href="stopwatch-es.html">Español</a></li>
      <li><a href="stopwatch-de.html">Deutsch</a></li>
      <li><a href="stopwatch-ru.html">Русский</a></li>
      <li><a href="stopwatch-el.html">Ελληνικά</a></li>
      <li><a href="stopwatch-ar.html">العربية</a></li>
    </ul>
  </div>
</body>
</html>
"""
    return html_out

def write_files(write_root_redirect: bool = False) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for code, data in TRANSLATIONS.items():
        data.setdefault("howto", {})
        data.setdefault("tips", {})
        data["howto"].setdefault("back_link", f"stopwatch-{code}.html")
        data["tips"].setdefault("back_link", f"stopwatch-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"stopwatch-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"stopwatch-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["howto"], "howto"))

        tips_path = os.path.join(OUTPUT_DIR, f"stopwatch-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["tips"], "tips"))

    redirect_path = os.path.join(OUTPUT_DIR, "stopwatch.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        with open("stopwatch.html", "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('stopwatch.html')}'.")

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)

if __name__ == "__main__":
    main()