#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_timer.py

Generates localized Task Timer pages (7 languages).
Fixed: localized section headings for How-to (steps_title) and Tips (tips_title)
and safer JS insertion for the timeout alert string.
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "timer_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "minutes_label": "Minutes:",
            "seconds_label": "Seconds:",
            "start_btn": "Start",
            "pause_btn": "Pause",
            "reset_btn": "Reset",
            "timeout_msg": "Time's up!"
        },
        "main": {
            "title": "Task Timer — TimerHaven",
            "desc": "Track work sessions, focus tasks, and breaks. Learn how to use Task Timer, get productivity tips, FAQs, and read expert articles.",
            "howto_link": "timer-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "timer-tips-en.html",
            "tips_btn": "Read Full Article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Can I set custom durations?</b> Yes, choose any time period.",
                "<b>Will the timer persist?</b> No, it resets after page reload.",
                "<b>Is this free?</b> Yes, all TimerHaven tools are free."
            ],
            "back_main": "Back to Main Menu",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Task Timer — TimerHaven",
            "steps_title": "Step-by-Step Guide",
            "desc": "The Task Timer tool is ideal for tracking any activity. Here’s how to use it:",
            "steps": [
                "<b>Set timer:</b> Choose a duration for your work session.",
                "<b>Start the timer:</b> Click <strong>Start</strong> to begin timing.",
                "<b>Take breaks:</b> Use short breaks between sessions."
            ],
            "back_btn": "Back to Task Timer",
            "back_link": "timer-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Task Timer Tips — TimerHaven",
            "tips_title": "Top Tips",
            "desc": "Maximize your productivity with these Task Timer tips:",
            "tips": [
                "<b>Use for breaks:</b> Time your rest periods to recharge.",
                "<b>Track sessions:</b> Monitor how long each task takes.",
                "<b>Start fresh:</b> Reset between activities for accurate records."
            ],
            "back_btn": "Back to Task Timer",
            "back_link": "timer-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {
            "minutes_label": "Minutes:",
            "seconds_label": "Secondes:",
            "start_btn": "Démarrer",
            "pause_btn": "Pause",
            "reset_btn": "Réinitialiser",
            "timeout_msg": "Le temps est écoulé !"
        },
        "main": {
            "title": "Minuteur de tâche — TimerHaven",
            "desc": "Suivez les sessions de travail, tâches de concentration et pauses. Apprenez à utiliser le Minuteur, obtenez des conseils et FAQs.",
            "howto_link": "timer-how-to-fr.html",
            "howto_btn": "Lire l'article",
            "tips_link": "timer-tips-fr.html",
            "tips_btn": "Lire l'article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Puis-je définir des durées personnalisées ?</b> Oui, choisissez n'importe quelle période.",
                "<b>Le minuteur persiste-t-il ?</b> Non, il se réinitialise après le rechargement.",
                "<b>Est-ce gratuit ?</b> Oui, tous les outils TimerHaven sont gratuits."
            ],
            "back_main": "Retour au menu principal",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique</a>'
        },
        "howto": {
            "title": "Comment utiliser le Minuteur — TimerHaven",
            "steps_title": "Guide étape par étape",
            "desc": "Le Minuteur est idéal pour suivre toute activité. Voici comment l'utiliser :",
            "steps": [
                "<b>Réglez le minuteur :</b> Choisissez la durée de votre session de travail.",
                "<b>Démarrez :</b> Cliquez sur <strong>Démarrer</strong> pour commencer.",
                "<b>Prenez des pauses :</b> Utilisez de courtes pauses entre les sessions."
            ],
            "back_btn": "Retour au Minuteur",
            "back_link": "timer-fr.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Conseils Minuteur — TimerHaven",
            "tips_title": "Conseils",
            "desc": "Maximisez votre productivité avec ces conseils :",
            "tips": [
                "<b>Utilisez pour les pauses :</b> Chronométrez vos périodes de repos.",
                "<b>Suivez les sessions :</b> Surveillez la durée de chaque tâche.",
                "<b>Redémarrez :</b> Réinitialisez entre les activités pour des enregistrements précis."
            ],
            "back_btn": "Retour au Minuteur",
            "back_link": "timer-fr.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {
            "minutes_label": "Minutos:",
            "seconds_label": "Segundos:",
            "start_btn": "Iniciar",
            "pause_btn": "Pausa",
            "reset_btn": "Reiniciar",
            "timeout_msg": "¡Tiempo!"
        },
        "main": {
            "title": "Temporizador de tareas — TimerHaven",
            "desc": "Sigue sesiones de trabajo, tareas de concentración y descansos. Aprende a usar el Temporizador, obtén consejos y FAQs.",
            "howto_link": "timer-how-to-es.html",
            "howto_btn": "Leer el artículo",
            "tips_link": "timer-tips-es.html",
            "tips_btn": "Leer el artículo",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>¿Puedo establecer duraciones personalizadas?</b> Sí, elige cualquier periodo.",
                "<b>¿Persiste el temporizador?</b> No, se reinicia al recargar la página.",
                "<b>¿Es gratis?</b> Sí, todas las herramientas TimerHaven son gratuitas."
            ],
            "back_main": "Volver al menú principal",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política</a>'
        },
        "howto": {
            "title": "Cómo usar el Temporizador — TimerHaven",
            "steps_title": "Guía paso a paso",
            "desc": "El Temporizador es ideal para rastrear cualquier actividad. Así es como se usa:",
            "steps": [
                "<b>Ajusta el temporizador:</b> Elige la duración de tu sesión de trabajo.",
                "<b>Inicia:</b> Haz clic en <strong>Iniciar</strong> para comenzar.",
                "<b>Toma descansos:</b> Usa descansos cortos entre sesiones."
            ],
            "back_btn": "Volver al Temporizador",
            "back_link": "timer-es.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Consejos Temporizador — TimerHaven",
            "tips_title": "Consejos principales",
            "desc": "Maximiza tu productividad con estos consejos:",
            "tips": [
                "<b>Úsalo para descansos:</b> Cronometra tus periodos de descanso.",
                "<b>Registra sesiones:</b> Controla cuánto dura cada tarea.",
                "<b>Empieza de nuevo:</b> Reinicia entre actividades para registros limpios."
            ],
            "back_btn": "Volver al Temporizador",
            "back_link": "timer-es.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {
            "minutes_label": "Minuten:",
            "seconds_label": "Sekunden:",
            "start_btn": "Start",
            "pause_btn": "Pause",
            "reset_btn": "Zurücksetzen",
            "timeout_msg": "Zeit ist um!"
        },
        "main": {
            "title": "Aufgaben-Timer — TimerHaven",
            "desc": "Verfolge Arbeitssitzungen, Fokusaufgaben und Pausen. Erfahren Sie, wie der Timer funktioniert, erhalten Sie Tipps und FAQs.",
            "howto_link": "timer-how-to-de.html",
            "howto_btn": "Artikel lesen",
            "tips_link": "timer-tips-de.html",
            "tips_btn": "Artikel lesen",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Kann ich benutzerdefinierte Dauer einstellen?</b> Ja, wählen Sie jede Zeitspanne.",
                "<b>Bleibt der Timer erhalten?</b> Nein, er setzt sich beim Neuladen zurück.",
                "<b>Ist das kostenlos?</b> Ja, alle TimerHaven-Tools sind kostenlos."
            ],
            "back_main": "Zurück zum Hauptmenü",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a>'
        },
        "howto": {
            "title": "So verwenden Sie den Timer — TimerHaven",
            "steps_title": "Schritt-für-Schritt-Anleitung",
            "desc": "Der Timer ist ideal zum Verfolgen beliebiger Aktivitäten. So verwenden Sie ihn:",
            "steps": [
                "<b>Timer einstellen:</b> Wählen Sie die Dauer Ihrer Arbeitssitzung.",
                "<b>Starten:</b> Klicken Sie auf <strong>Start</strong> zum Beginnen.",
                "<b>Pauser nehmen:</b> Verwenden Sie kurze Pausen zwischen Sitzungen."
            ],
            "back_btn": "Zurück zum Timer",
            "back_link": "timer-de.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Timer-Tipps — TimerHaven",
            "tips_title": "Top-Tipps",
            "desc": "Maximieren Sie Ihre Produktivität mit diesen Tipps:",
            "tips": [
                "<b>Für Pausen nutzen:</b> Zeiträume zur Erholung messen.",
                "<b>Sitzungen verfolgen:</b> Überwachen Sie die Dauer jeder Aufgabe.",
                "<b>Neu starten:</b> Zurücksetzen zwischen Aktivitäten für genaue Aufzeichnungen."
            ],
            "back_btn": "Zurück zum Timer",
            "back_link": "timer-de.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {
            "minutes_label": "Минуты:",
            "seconds_label": "Секунды:",
            "start_btn": "Старт",
            "pause_btn": "Пауза",
            "reset_btn": "Сброс",
            "timeout_msg": "Время вышло!"
        },
        "main": {
            "title": "Таймер задач — TimerHaven",
            "desc": "Отслеживайте рабочие сессии, фокус и перерывы. Узнайте, как пользоваться, получите советы и FAQs.",
            "howto_link": "timer-how-to-ru.html",
            "howto_btn": "Читать статью",
            "tips_link": "timer-tips-ru.html",
            "tips_btn": "Читать статью",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Могу ли я задать свою длительность?</b> Да, выберите любой период.",
                "<b>Сохранится ли таймер?</b> Нет, он сбрасывается при перезагрузке.",
                "<b>Это бесплатно?</b> Да, все инструменты TimerHaven бесплатны."
            ],
            "back_main": "Назад в главное меню",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика</a>'
        },
        "howto": {
            "title": "Как пользоваться таймером — TimerHaven",
            "steps_title": "Пошаговое руководство",
            "desc": "Таймер идеально подходит для отслеживания любой активности. Как им пользоваться:",
            "steps": [
                "<b>Установите таймер:</b> Выберите длительность рабочей сессии.",
                "<b>Запустите:</b> Нажмите <strong>Старт</strong> для начала.",
                "<b>Делайте паузы:</b> Используйте короткие перерывы между сессиями."
            ],
            "back_btn": "Вернуться к таймеру",
            "back_link": "timer-ru.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Советы Таймера — TimerHaven",
            "tips_title": "Лучшие советы",
            "desc": "Максимизируйте продуктивность с этими советами:",
            "tips": [
                "<b>Используйте для перерывов:</b> Засекайте время отдыха.",
                "<b>Отслеживайте сессии:</b> Контролируйте длительность задач.",
                "<b>Начинайте заново:</b> Сбрасывайте между активностями для точных записей."
            ],
            "back_btn": "Вернуться к таймеру",
            "back_link": "timer-ru.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {
            "minutes_label": "Λεπτά:",
            "seconds_label": "Δευτερόλεπτα:",
            "start_btn": "Έναρξη",
            "pause_btn": "Παύση",
            "reset_btn": "Επαναφορά",
            "timeout_msg": "Ο χρόνος τελείωσε!"
        },
        "main": {
            "title": "Χρονοδιακόπτης εργασίας — TimerHaven",
            "desc": "Παρακολουθήστε συνεδρίες εργασίας, εστίαση και διαλείμματα. Μάθετε πώς να χρησιμοποιείτε τον Χρονοδιακόπτη, λάβετε συμβουλές και FAQs.",
            "howto_link": "timer-how-to-el.html",
            "howto_btn": "Διαβάστε το άρθρο",
            "tips_link": "timer-tips-el.html",
            "tips_btn": "Διαβάστε το άρθρο",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Μπορώ να ορίσω προσαρμοσμένες διάρκειες;</b> Ναι, επιλέξτε οποιαδήποτε περίοδο.",
                "<b>Θα παραμείνει ο χρονοδιακόπτης;</b> Όχι, επανέρχεται μετά την επαναφόρτωση.",
                "<b>Είναι δωρεάν;</b> Ναι, όλα τα εργαλεία TimerHaven είναι δωρεάν."
            ],
            "back_main": "Επιστροφή στο κύριο μενού",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική</a>'
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε τον Χρονοδιακόπτη — TimerHaven",
            "steps_title": "Οδηγίες βήμα προς βήμα",
            "desc": "Ο Χρονοδιακόπτης είναι ιδανικός για παρακολούθηση δραστηριοτήτων. Πώς να τον χρησιμοποιήσετε:",
            "steps": [
                "<b>Ορίστε χρόνο:</b> Επιλέξτε διάρκεια της συνεδρίας εργασίας.",
                "<b>Εκκίνηση:</b> Πατήστε <strong>Έναρξη</strong> για να ξεκινήσετε.",
                "<b>Κάντε διαλείμματα:</b> Χρησιμοποιήστε σύντομα διαλείμματα μεταξύ συνεδριών."
            ],
            "back_btn": "Επιστροφή στον Χρονοδιακόπτη",
            "back_link": "timer-el.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Συμβουλές Χρονοδιακόπτη — TimerHaven",
            "tips_title": "Κορυφαίες συμβουλές",
            "desc": "Μεγιστοποιήστε την παραγωγικότητα με αυτές τις συμβουλές:",
            "tips": [
                "<b>Χρησιμοποιήστε για διαλείμματα:</b> Χρονίστε τους χρόνους ανάπαυσης.",
                "<b>Παρακολουθήστε συνεδρίες:</b> Παρακολουθήστε τη διάρκεια κάθε εργασίας.",
                "<b>Ξεκινήστε από την αρχή:</b> Επαναφορά μεταξύ δραστηριοτήτων για ακριβή εγγραφή."
            ],
            "back_btn": "Επιστροφή στον Χρονοδιακόπτη",
            "back_link": "timer-el.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {
            "minutes_label": "دقائق:",
            "seconds_label": "ثواني:",
            "start_btn": "ابدأ",
            "pause_btn": "إيقاف مؤقت",
            "reset_btn": "إعادة ضبط",
            "timeout_msg": "انتهى الوقت!"
        },
        "main": {
            "title": "مؤقت المهام — TimerHaven",
            "desc": "تتبع جلسات العمل، مهام التركيز، وفترات الاستراحة. تعلّم كيفية استخدام المؤقت واحصل على نصائح والأسئلة الشائعة.",
            "howto_link": "timer-how-to-ar.html",
            "howto_btn": "اقرأ المقالة",
            "tips_link": "timer-tips-ar.html",
            "tips_btn": "اقرأ المقالة",
            "faq_title": "الأسئلة الشائعة",
            "faq_items": [
                "<b>هل يمكنني تعيين مدد مخصصة؟</b> نعم، اختر أي فترة زمنية.",
                "<b>هل يبقى المؤقت محفوظًا؟</b> لا، يُعاد عند إعادة تحميل الصفحة.",
                "<b>هل هذا مجاني؟</b> نعم، جميع أدوات TimerHaven مجانية."
            ],
            "back_main": "العودة إلى القائمة الرئيسية",
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a>'
        },
        "howto": {
            "title": "كيفية استخدام المؤقت — TimerHaven",
            "steps_title": "دليل خطوة بخطوة",
            "desc": "المؤقت مثالي لتتبع أي نشاط. كيفية استخدامه:",
            "steps": [
                "<b>اضبط المؤقت:</b> اختر مدة جلسة العمل.",
                "<b>ابدأ:</b> اضغط <strong>ابدأ</strong> للبدء.",
                "<b>خذ استراحات:</b> استخدم استراحات قصيرة بين الجلسات."
            ],
            "back_btn": "العودة إلى المؤقت",
            "back_link": "timer-ar.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "نصائح المؤقت — TimerHaven",
            "tips_title": "أهم النصائح",
            "desc": "حسّن إنتاجيتك بهذه النصائح:",
            "tips": [
                "<b>استخدمه للفواصل:</b> اضبط أوقات الراحة.",
                "<b>تتبع الجلسات:</b> راقب مدة كل مهمة.",
                "<b>ابدأ من جديد:</b> أعد الضبط بين الأنشطة لسجلات دقيقة."
            ],
            "back_btn": "العودة إلى المؤقت",
            "back_link": "timer-ar.html",
            "footer": DEFAULT_COPYRIGHT
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

def js_string_literal(s: str) -> str:
    """Return a safely escaped JS double-quoted string literal (no surrounding quotes)."""
    if not isinstance(s, str):
        return ""
    # Replace backslashes then double-quotes and newlines
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

def generate_main_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]

    # localized main-card back label (main.back_main)
    back_label = main.get("back_main", "Back to Main Menu")

    # Prepare JS-safe timeout message
    timeout_msg = ui.get('timeout_msg', "Time's up!")
    timeout_js = js_string_literal(timeout_msg)

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
    .article-card, .tool-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); width:410px; padding:1.3rem; }}
    .article-card h2 {{ color:#185a9d; font-size:1.25rem; margin-bottom:.6rem; }}
    .tool-card h3 {{ color:#185a9d; font-size:1.35rem; margin-bottom:.5rem; }}
    .timer-display {{ font-size:2em; font-weight:700; text-align:center; margin:0.9rem 0; }}
    .timer-controls input {{ width:80px; display:inline-block; margin-left:.4rem; }}
    .timer-btns {{ margin-top:.5rem; display:flex; gap:.5rem; flex-wrap:wrap; }}
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
      <div class="article-card" aria-labelledby="howto-title">
        <div>
          <h2 id="howto-title"><i class="fa fa-hourglass-half"></i> {escape_allow_tags(data.get('howto',{}).get('title','How to Use Task Timer'))}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in data.get('howto',{}).get('steps', []))}
          </ol>
        </div>
        <a href="{main.get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <div class="tool-card" role="region" aria-label="Task Timer">
        <a href="index.html" class="d-block mb-2" style="text-decoration:none; color:#0d6efd; font-weight:600;">&larr; {escape_allow_tags(back_label)}</a>
        <h3><i class="fa fa-hourglass-half"></i> {escape_allow_tags(main.get('title','Task Timer'))}</h3>

        <div class="timer-section" aria-live="polite">
          <div class="timer-controls mb-2">
            <label style="font-weight:600;">{escape_allow_tags(ui.get('minutes_label','Minutes:'))}
              <input id="minutes" type="number" min="0" max="999" value="25" class="form-control" style="width:80px; display:inline-block; margin-left:.4rem;">
            </label>
            <label style="font-weight:600; margin-left:0.8rem;">{escape_allow_tags(ui.get('seconds_label','Seconds:'))}
              <input id="seconds" type="number" min="0" max="59" value="0" class="form-control" style="width:80px; display:inline-block; margin-left:.4rem;">
            </label>
          </div>

          <div id="timerDisplay" class="timer-display">25:00</div>

          <div class="timer-btns">
            <button id="startBtn" class="btn btn-success btn-small"><i class="fa fa-play"></i> {escape_allow_tags(ui.get('start_btn','Start'))}</button>
            <button id="pauseBtn" class="btn btn-secondary btn-small"><i class="fa fa-pause"></i> {escape_allow_tags(ui.get('pause_btn','Pause'))}</button>
            <button id="resetBtn" class="btn btn-danger btn-small"><i class="fa fa-refresh"></i> {escape_allow_tags(ui.get('reset_btn','Reset'))}</button>
          </div>

          <details class="faq-section" style="margin-top:1rem;">
            <summary style="font-weight:700; font-size:1rem;">{escape_allow_tags(main.get('faq_title'))}</summary>
            <ul style="padding-left:1.1rem; color:#374151;">
              {faq_html}
            </ul>
          </details>
        </div>
      </div>

      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {escape_allow_tags(data.get('tips',{}).get('title','Task Timer Productivity Tips'))}</h2>
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
        window.location.href = 'timer-' + v + '.html';
      }});
    }}

    // Timer logic (localized text inlined)
    var timer = null;
    var totalSeconds = 25*60;
    var running = false;

    function updateTimerDisplay() {{
      var min = Math.floor(totalSeconds/60);
      var sec = totalSeconds % 60;
      document.getElementById('timerDisplay').textContent = String(min).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
    }}

    function setTimerLengths() {{
      var min = parseInt(document.getElementById('minutes').value,10) || 0;
      var sec = parseInt(document.getElementById('seconds').value,10) || 0;
      totalSeconds = Math.max(0, min*60 + sec);
      updateTimerDisplay();
    }}

    document.getElementById('minutes').addEventListener('change', setTimerLengths);
    document.getElementById('seconds').addEventListener('change', setTimerLengths);

    document.getElementById('startBtn').addEventListener('click', function() {{
      if (running) return;
      running = true;
      timer = setInterval(function() {{
        if (totalSeconds > 0) {{
          totalSeconds--;
          updateTimerDisplay();
        }} else {{
          clearInterval(timer);
          running = false;
          try {{ alert("{timeout_js}"); }} catch(e){{}}
        }}
      }}, 1000);
    }});

    document.getElementById('pauseBtn').addEventListener('click', function() {{
      if (timer) clearInterval(timer);
      running = false;
    }});

    document.getElementById('resetBtn').addEventListener('click', function() {{
      if (timer) clearInterval(timer);
      running = false;
      setTimerLengths();
    }});

    // initialize
    setTimerLengths();
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
    back_link = section.get("back_link", f"timer-{code}.html")
    back_btn = escape_allow_tags(section.get("back_btn","Back to Task Timer"))

    if page_type == "howto":
        # localized heading
        steps_title = escape_allow_tags(section.get("steps_title", "Step-by-Step Guide"))
        steps_html = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in section.get("steps", []))
        extra = f"""
      <h3 class="section-title">{steps_title}</h3>
      <ol>
        {steps_html}
      </ol>
"""
    else:
        tips_title = escape_allow_tags(section.get("tips_title", "Top Tips"))
        tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", []))
        extra = f"""
      <h3 class="section-title">{tips_title}</h3>
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
  <title>Task Timer — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=timer-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'timer-en.html',
        'fr': 'timer-fr.html',
        'es': 'timer-es.html',
        'de': 'timer-de.html',
        'ru': 'timer-ru.html',
        'el': 'timer-el.html',
        'ar': 'timer-ar.html'
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
    <h1>Task Timer — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="timer-en.html">English</a></li>
      <li><a href="timer-fr.html">Français</a></li>
      <li><a href="timer-es.html">Español</a></li>
      <li><a href="timer-de.html">Deutsch</a></li>
      <li><a href="timer-ru.html">Русский</a></li>
      <li><a href="timer-el.html">Ελληνικά</a></li>
      <li><a href="timer-ar.html">العربية</a></li>
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
        data["howto"].setdefault("back_link", f"timer-{code}.html")
        data["tips"].setdefault("back_link", f"timer-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"timer-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"timer-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["howto"], "howto"))

        tips_path = os.path.join(OUTPUT_DIR, f"timer-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["tips"], "tips"))

    redirect_path = os.path.join(OUTPUT_DIR, "timer.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        with open("timer.html", "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('timer.html')}'.")

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)

if __name__ == "__main__":
    main()