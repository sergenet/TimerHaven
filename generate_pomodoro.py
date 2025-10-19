#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pomodoro.py

Generates static HTML pages for the "Pomodoro Timer" tool in 7 languages:
 - Main Tool Pages:      pomodoro-xx.html
 - How-to Article Pages: pomodoro-how-to-xx.html
 - Tips Article Pages:   pomodoro-tips-xx.html
 - A redirect landing page: pomodoro.html (in output folder)

Output folder (default): ./pomodoro_pages

Usage:
  python generate_pomodoro.py            # writes files to ./pomodoro_pages
  python generate_pomodoro.py --root     # also writes pomodoro.html into current dir
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "pomodoro_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

# Translations for 7 languages (en, fr, es, de, ru, el, ar)
TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "work_label": "Work (min):",
            "break_label": "Break (min):",
            "start_btn": "Start",
            "pause_btn": "Pause",
            "reset_btn": "Reset",
            "status_work": "Work",
            "status_break": "Break",
            "completed_cycles": "Completed cycles:"
        },
        "main": {
            "title": "Pomodoro Timer — TimerHaven",
            "desc": "Boost focus with the Pomodoro technique. Learn how to use Pomodoro Timer, get productivity tips, FAQs, and read expert articles.",
            "howto_link": "pomodoro-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "pomodoro-tips-en.html",
            "tips_btn": "Read Full Article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>What is Pomodoro?</b> A productivity technique using timed focus/break cycles.",
                "<b>Can I adjust the timer?</b> Yes — set durations to fit your workflow.",
                "<b>Does this save sessions?</b> No — sessions reset after page reload."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Pomodoro Timer — TimerHaven",
            "desc": "The Pomodoro Technique helps you stay productive and focused by breaking work into short intervals, with regular breaks for rest.",
            "steps_title": "Step-by-Step",
            "steps": [
                "<b>Set timer:</b> Choose your work duration and break length.",
                "<b>Start session:</b> Click <strong>Start</strong> to begin focused work.",
                "<b>Take breaks:</b> When the timer ends, take a short break, then repeat.",
                "<b>Repeat cycles:</b> After several Pomodoros, take a longer break."
            ],
            "back_btn": "Back to Pomodoro Timer",
            "back_link": "pomodoro-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Pomodoro Productivity Tips — TimerHaven",
            "desc": "Make the most of Pomodoro with these practical tips.",
            "tips_title": "Top Tips",
            "tips": [
                "<b>Don’t skip breaks:</b> Regular rests keep you energized.",
                "<b>Track sessions:</b> See how many Pomodoros you complete daily.",
                "<b>Customize lengths:</b> Adjust timer for tasks that suit you."
            ],
            "back_btn": "Back to Pomodoro Timer",
            "back_link": "pomodoro-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {
            "work_label": "Travail (min):",
            "break_label": "Pause (min):",
            "start_btn": "Démarrer",
            "pause_btn": "Pause",
            "reset_btn": "Réinitialiser",
            "status_work": "Travail",
            "status_break": "Pause",
            "completed_cycles": "Cycles terminés:"
        },
        "main": {
            "title": "Minuteur Pomodoro — TimerHaven",
            "desc": "Améliorez votre concentration avec la technique Pomodoro. Apprenez à utiliser le Minuteur Pomodoro, obtenez des conseils, FAQs et articles.",
            "howto_link": "pomodoro-how-to-fr.html",
            "howto_btn": "Lire l'article",
            "tips_link": "pomodoro-tips-fr.html",
            "tips_btn": "Lire l'article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Qu'est-ce que Pomodoro ?</b> Une technique de productivité basée sur des cycles travail/pause.",
                "<b>Puis-je ajuster le minuteur ?</b> Oui — adaptez les durées à votre flux de travail.",
                "<b>Les sessions sont-elles sauvegardées ?</b> Non — les sessions sont réinitialisées au rechargement."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique de confidentialité</a> &bull; <a href="terms.html">Conditions</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "Comment utiliser le Minuteur Pomodoro — TimerHaven",
            "desc": "La technique Pomodoro vous aide à rester productif en alternant périodes de travail et pauses.",
            "steps_title": "Étapes",
            "steps": [
                "<b>Réglez le minuteur :</b> Choisissez la durée de travail et de pause.",
                "<b>Démarrez :</b> Cliquez sur <strong>Démarrer</strong> pour commencer.",
                "<b>Prenez des pauses :</b> Quand le minuteur s'arrête, faites une courte pause, puis recommencez.",
                "<b>Répétez :</b> Après plusieurs Pomodoros, prenez une pause plus longue."
            ],
            "back_btn": "Retour au Minuteur Pomodoro",
            "back_link": "pomodoro-fr.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Conseils Pomodoro — TimerHaven",
            "desc": "Optimisez Pomodoro avec ces conseils pratiques.",
            "tips_title": "Conseils",
            "tips": [
                "<b>Ne sautez pas les pauses :</b> Elles rechargent votre énergie.",
                "<b>Suivez vos sessions :</b> Notez vos Pomodoros quotidiens.",
                "<b>Personnalisez :</b> Ajustez les durées selon vos tâches."
            ],
            "back_btn": "Retour au Minuteur Pomodoro",
            "back_link": "pomodoro-fr.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {
            "work_label": "Trabajo (min):",
            "break_label": "Descanso (min):",
            "start_btn": "Iniciar",
            "pause_btn": "Pausa",
            "reset_btn": "Reiniciar",
            "status_work": "Trabajo",
            "status_break": "Descanso",
            "completed_cycles": "Ciclos completados:"
        },
        "main": {
            "title": "Temporizador Pomodoro — TimerHaven",
            "desc": "Mejora el enfoque con la técnica Pomodoro. Aprende a usar el Temporizador Pomodoro, obtén consejos, FAQs y artículos.",
            "howto_link": "pomodoro-how-to-es.html",
            "howto_btn": "Leer el artículo",
            "tips_link": "pomodoro-tips-es.html",
            "tips_btn": "Leer el artículo",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>¿Qué es Pomodoro?</b> Una técnica de productividad con ciclos trabajo/descanso.",
                "<b>¿Puedo ajustar el temporizador?</b> Sí — ajusta las duraciones a tu ritmo.",
                "<b>¿Se guardan las sesiones?</b> No — se reinician al recargar la página."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política de privacidad</a> &bull; <a href="terms.html">Términos</a> &bull; <a href="contact.html">Contacto</a>'
        },
        "howto": {
            "title": "Cómo usar el Temporizador Pomodoro — TimerHaven",
            "desc": "Pomodoro te ayuda a mantener la productividad dividiendo el trabajo en intervalos con descansos.",
            "steps_title": "Pasos",
            "steps": [
                "<b>Ajusta el temporizador:</b> Elige duración de trabajo y descanso.",
                "<b>Inicia sesión:</b> Haz clic en <strong>Iniciar</strong> para comenzar.",
                "<b>Toma descansos:</b> Al terminar el temporizador, descansa brevemente y repite.",
                "<b>Repite ciclos:</b> Tras varios Pomodoros toma un descanso largo."
            ],
            "back_btn": "Volver al Temporizador Pomodoro",
            "back_link": "pomodoro-es.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Consejos Pomodoro — TimerHaven",
            "desc": "Saca el máximo provecho a Pomodoro con estos consejos.",
            "tips_title": "Consejos",
            "tips": [
                "<b>No saltes descansos:</b> Mantienen tu energía.",
                "<b>Registra sesiones:</b> Controla tus Pomodoros diarios.",
                "<b>Personaliza:</b> Ajusta duraciones para cada tarea."
            ],
            "back_btn": "Volver al Temporizador Pomodoro",
            "back_link": "pomodoro-es.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {
            "work_label": "Arbeit (min):",
            "break_label": "Pause (min):",
            "start_btn": "Start",
            "pause_btn": "Pause",
            "reset_btn": "Zurücksetzen",
            "status_work": "Arbeit",
            "status_break": "Pause",
            "completed_cycles": "Abgeschlossene Zyklen:"
        },
        "main": {
            "title": "Pomodoro-Timer — TimerHaven",
            "desc": "Steigern Sie Ihre Konzentration mit der Pomodoro-Technik. Erfahren Sie, wie der Pomodoro-Timer funktioniert, erhalten Sie Tipps und FAQs.",
            "howto_link": "pomodoro-how-to-de.html",
            "howto_btn": "Artikel lesen",
            "tips_link": "pomodoro-tips-de.html",
            "tips_btn": "Artikel lesen",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Was ist Pomodoro?</b> Eine Produktivitätstechnik mit Fokus-/Pausenzyklen.",
                "<b>Kann ich den Timer anpassen?</b> Ja — passen Sie die Dauer an Ihre Arbeit an.",
                "<b>Werden Sitzungen gespeichert?</b> Nein — sie werden nach dem Neuladen zurückgesetzt."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a> &bull; <a href="terms.html">Nutzungsbedingungen</a> &bull; <a href="contact.html">Kontakt</a>'
        },
        "howto": {
            "title": "So verwenden Sie den Pomodoro-Timer — TimerHaven",
            "desc": "Die Pomodoro-Technik teilt Arbeit in kurze Intervalle mit Pausen zur Erholung.",
            "steps_title": "Schritte",
            "steps": [
                "<b>Timer einstellen:</b> Wählen Sie Arbeits- und Pausenzeiten.",
                "<b>Sitzung starten:</b> Klicken Sie auf <strong>Start</strong>.",
                "<b>Pausen einlegen:</b> Wenn der Timer endet, machen Sie eine kurze Pause.",
                "<b>Zyklen wiederholen:</b> Nach mehreren Pomodoros längere Pause einlegen."
            ],
            "back_btn": "Zurück zum Pomodoro-Timer",
            "back_link": "pomodoro-de.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Pomodoro-Tipps — TimerHaven",
            "desc": "Verbessern Sie Ihre Pomodoro-Gewohnheiten mit diesen Tipps.",
            "tips_title": "Tipps",
            "tips": [
                "<b>Keine Pausen überspringen:</b> Sie erhalten Energie zurück.",
                "<b>Sitzungen verfolgen:</b> Notieren Sie Ihre täglichen Pomodoros.",
                "<b>Längen anpassen:</b> Stellen Sie Zeiten passend zur Aufgabe ein."
            ],
            "back_btn": "Zurück zum Pomodoro-Timer",
            "back_link": "pomodoro-de.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {
            "work_label": "Работа (мин):",
            "break_label": "Перерыв (мин):",
            "start_btn": "Старт",
            "pause_btn": "Пауза",
            "reset_btn": "Сброс",
            "status_work": "Работа",
            "status_break": "Перерыв",
            "completed_cycles": "Завершённые циклы:"
        },
        "main": {
            "title": "Таймер Помодоро — TimerHaven",
            "desc": "Повышайте концентрацию с помощью техники Помодоро. Узнайте, как пользоваться, получите советы и FAQs.",
            "howto_link": "pomodoro-how-to-ru.html",
            "howto_btn": "Читать статью",
            "tips_link": "pomodoro-tips-ru.html",
            "tips_btn": "Читать статью",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Что такое Помодоро?</b> Метод продуктивности с циклами работы и отдыха.",
                "<b>Можно ли настроить таймер?</b> Да — подстройте длительности под себя.",
                "<b>Сохраняются ли сессии?</b> Нет — после перезагрузки всё сбрасывается."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика конфиденциальности</a> &bull; <a href="terms.html">Условия</a> &bull; <a href="contact.html">Контакт</a>'
        },
        "howto": {
            "title": "Как пользоваться Таймером Помодоро — TimerHaven",
            "desc": "Техника Помодоро разбивает работу на короткие интервалы с перерывами для восстановления.",
            "steps_title": "Шаги",
            "steps": [
                "<b>Установите таймер:</b> Выберите длительность работы и перерыва.",
                "<b>Начните сессию:</b> Нажмите <strong>Старт</strong> для начала.",
                "<b>Делайте перерывы:</b> По окончании таймера сделайте короткий перерыв.",
                "<b>Повторяйте циклы:</b> После нескольких Помодоро сделайте длинный перерыв."
            ],
            "back_btn": "Вернуться к Таймеру Помодоро",
            "back_link": "pomodoro-ru.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Советы Помодоро — TimerHaven",
            "desc": "Улучшите практику Помодоро этими советами.",
            "tips_title": "Советы",
            "tips": [
                "<b>Не пропускайте перерывы:</b> Они восстанавливают энергию.",
                "<b>Отслеживайте сессии:</b> Записывайте Pomodoro за день.",
                "<b>Настраивайте длительности:</b> Подберите под свои задачи."
            ],
            "back_btn": "Вернуться к Таймеру Помодоро",
            "back_link": "pomodoro-ru.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {
            "work_label": "Εργασία (λεπ):",
            "break_label": "Διάλειμμα (λεπ):",
            "start_btn": "Έναρξη",
            "pause_btn": "Παύση",
            "reset_btn": "Επαναφορά",
            "status_work": "Εργασία",
            "status_break": "Διάλειμμα",
            "completed_cycles": "Ολοκληρωμένοι κύκλοι:"
        },
        "main": {
            "title": "Χρονόμετρο Pomodoro — TimerHaven",
            "desc": "Ενισχύστε τη συγκέντρωσή σας με την τεχνική Pomodoro. Μάθετε πώς λειτουργεί, συμβουλές και FAQs.",
            "howto_link": "pomodoro-how-to-el.html",
            "howto_btn": "Διαβάστε το άρθρο",
            "tips_link": "pomodoro-tips-el.html",
            "tips_btn": "Διαβάστε το άρθρο",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Τι είναι το Pomodoro;</b> Μια τεχνική παραγωγικότητας με κύκλους εργασίας/διαλείμματος.",
                "<b>Μπορώ να ρυθμίσω τον χρονοδιακόπτη;</b> Ναι — προσαρμόστε τις διάρκειες.",
                "<b>Αποθηκεύονται οι συνεδρίες;</b> Όχι — επαναφέρονται κατά το ανανέωμα της σελίδας."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική απορρήτου</a> &bull; <a href="terms.html">Όροι</a> &bull; <a href="contact.html">Επικοινωνία</a>'
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε το Pomodoro — TimerHaven",
            "desc": "Η τεχνική Pomodoro χωρίζει την εργασία σε σύντομα διαστήματα με διαλείμματα.",
            "steps_title": "Βήματα",
            "steps": [
                "<b>Ορίστε χρόνο:</b> Επιλέξτε διάρκεια εργασίας και διάλειμμα.",
                "<b>Ξεκινήστε:</b> Πατήστε <strong>Έναρξη</strong> για να ξεκινήσει.",
                "<b>Κάντε διαλείμματα:</b> Όταν τελειώσει ο χρόνος, κάντε σύντομο διάλειμμα.",
                "<b>Επαναλάβετε:</b> Μετά από μερικά Pomodoros, κάντε μεγαλύτερο διάλειμμα."
            ],
            "back_btn": "Επιστροφή στο Pomodoro",
            "back_link": "pomodoro-el.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Συμβουλές Pomodoro — TimerHaven",
            "desc": "Βελτιώστε την τεχνική Pomodoro με αυτές τις συμβουλές.",
            "tips_title": "Συμβουλές",
            "tips": [
                "<b>Μην παραλείπετε διαλείμματα:</b> Διατηρούν την ενέργεια.",
                "<b>Παρακολουθήστε συνεδρίες:</b> Καταγράψτε τα Pomodoros σας.",
                "<b>Προσαρμόστε διάρκειες:</b> Επιλέξτε κατάλληλες ρυθμίσεις για εργασίες."
            ],
            "back_btn": "Επιστροφή στο Pomodoro",
            "back_link": "pomodoro-el.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {
            "work_label": "العمل (دقائق):",
            "break_label": "استراحة (دقائق):",
            "start_btn": "ابدأ",
            "pause_btn": "إيقاف مؤقت",
            "reset_btn": "إعادة ضبط",
            "status_work": "عمل",
            "status_break": "استراحة",
            "completed_cycles": "الدورات المكتملة:"
        },
        "main": {
            "title": "مؤقت بومودورو — TimerHaven",
            "desc": "زد تركيزك باستخدام تقنية بومودورو. تعلّم كيفية استخدام المؤقت، واحصل على نصائح، والأسئلة الشائعة.",
            "howto_link": "pomodoro-how-to-ar.html",
            "howto_btn": "اقرأ المقالة",
            "tips_link": "pomodoro-tips-ar.html",
            "tips_btn": "اقرأ المقالة",
            "faq_title": "الأسئلة الشائعة",
            "faq_items": [
                "<b>ما هو بومودورو؟</b> تقنية إنتاجية تعتمد دورات عمل/استراحة.",
                "<b>هل يمكن تعديل المؤقت؟</b> نعم — عدِّل المدد حسب حاجتك.",
                "<b>هل تُحفظ الجلسات؟</b> لا — تُعاد عند إعادة تحميل الصفحة."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a> &bull; <a href="terms.html">الشروط</a> &bull; <a href="contact.html">اتصل بنا</a>'
        },
        "howto": {
            "title": "كيفية استخدام مؤقت بومودورو — TimerHaven",
            "desc": "تقنية تقسم العمل إلى فترات قصيرة مع استراحات للراحة.",
            "steps_title": "خطوات",
            "steps": [
                "<b>اضبط المؤقت:</b> اختر مدة العمل والاستراحة.",
                "<b>ابدأ الجلسة:</b> اضغط <strong>ابدأ</strong> للبدء.",
                "<b>خذ استراحات:</b> عند انتهاء الوقت خذ استراحة قصيرة ثم كرر.",
                "<b>كرر الدورات:</b> بعد عدة دورات خذ استراحة أطول."
            ],
            "back_btn": "العودة إلى مؤقت بومودورو",
            "back_link": "pomodoro-ar.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "نصائح بومودورو — TimerHaven",
            "desc": "حسّن استخدام بومودورو بهذه النصائح العملية.",
            "tips_title": "نصائح",
            "tips": [
                "<b>لا تتجاوز الاستراحات:</b> تساعد على استعادة النشاط.",
                "<b>سجل الجلسات:</b> تابع عدد الجلسات يوميًا.",
                "<b>خصص المدد:</b> اضبطها حسب نوع المهام."
            ],
            "back_btn": "العودة إلى مؤقت بومودورو",
            "back_link": "pomodoro-ar.html",
            "footer": DEFAULT_COPYRIGHT
        }
    }
}

# Allowed inline tags for translation strings
ALLOWED_INLINE_TAGS = {"b", "strong", "a", "br"}

def escape_allow_tags(s: str) -> str:
    """Escape but allow a small set of inline tags present in translations."""
    if not isinstance(s, str):
        return ""
    esc = html.escape(s, quote=True)
    for tag in ALLOWED_INLINE_TAGS:
        esc = esc.replace(html.escape(f"<{tag}>"), f"<{tag}>")
        esc = esc.replace(html.escape(f"</{tag}>"), f"</{tag}>")
        esc = esc.replace(html.escape(f"<{tag} "), f"<{tag} ")
    return esc

def generate_main_tool_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]

    # MAIN CARD: fixed, non-localized back label per request
    back_label = "Back to Main Menu"

    faq_items_html = "".join(f"<li>{escape_allow_tags(item)}</li>\n" for item in main.get("faq_items", []))
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
    .form-inline {{ display:flex; gap:.6rem; align-items:center; flex-wrap:wrap; }}
    .pomodoro-display {{ font-weight:700; font-size:1.25rem; margin-top:.5rem; margin-bottom:.5rem; }}
    .controls-row {{ display:flex; gap:.5rem; align-items:center; flex-wrap:wrap; margin-top:.5rem; }}
    .toggles {{ margin-top:.6rem; display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center; }}
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
          <h2 id="howto-title"><i class="fa fa-apple-whole"></i> {escape_allow_tags(data['howto'].get('title','How to Use Pomodoro'))}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in data['howto'].get('steps', []))}
          </ol>
        </div>
        <a href="{data['main'].get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <div class="tool-card" role="region" aria-label="Pomodoro timer">
        <!-- Fixed main-card back label: "Back to Main Menu" -->
        <a href="index.html" class="d-block mb-2" style="text-decoration:none; color:#0d6efd; font-weight:600;">&larr; {escape_allow_tags(back_label)}</a>
        <h3><i class="fa fa-apple-whole"></i> {escape_allow_tags(main.get('title','Pomodoro Timer'))}</h3>

        <div class="pomodoro-section" aria-live="polite">
          <div class="form-inline mb-2">
            <label style="font-weight:600;">{escape_allow_tags(ui.get('work_label','Work (min):'))}
              <input id="workLength" type="number" min="1" max="60" value="25" class="form-control" style="width:80px; margin-left:.3rem;">
            </label>
            <label style="font-weight:600;">{escape_allow_tags(ui.get('break_label','Break (min):'))}
              <input id="breakLength" type="number" min="1" max="30" value="5" class="form-control" style="width:80px; margin-left:.3rem;">
            </label>
          </div>

          <div id="pomodoroStatus" style="font-weight:600; margin-bottom:.25rem;">{escape_allow_tags(ui.get('status_work','Work'))}</div>
          <div id="pomodoroDisplay" class="pomodoro-display">25:00</div>

          <div class="controls-row">
            <button id="startBtn" class="btn btn-success btn-small"><i class="fa fa-play"></i> {escape_allow_tags(ui.get('start_btn','Start'))}</button>
            <button id="pauseBtn" class="btn btn-secondary btn-small"><i class="fa fa-pause"></i> {escape_allow_tags(ui.get('pause_btn','Pause'))}</button>
            <button id="resetBtn" class="btn btn-danger btn-small"><i class="fa fa-refresh"></i> {escape_allow_tags(ui.get('reset_btn','Reset'))}</button>
          </div>

          <div id="pomodoroCycle" style="margin-top:.5rem; color:#185a9d; font-weight:600;">{escape_allow_tags(ui.get('completed_cycles','Completed cycles:'))} 0</div>

          <div class="toggles" aria-hidden="false" style="margin-top:.5rem;">
            <label style="display:flex; align-items:center; gap:.35rem;"><input type="checkbox" id="beepToggle"> Beep on end</label>
            <label style="display:flex; align-items:center; gap:.35rem;"><input type="checkbox" id="notifyToggle"> Desktop notification</label>
            <label style="display:flex; align-items:center; gap:.35rem;"><input type="checkbox" id="autoStartToggle"> Auto-start next period</label>
          </div>

          <details class="faq-section" style="margin-top:1rem;">
            <summary style="font-weight:700; font-size:1rem;">{escape_allow_tags(main.get('faq_title'))}</summary>
            <ul style="padding-left:1.1rem; color:#374151;">
              {faq_items_html}
            </ul>
          </details>
        </div>
      </div>

      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {escape_allow_tags(data['tips'].get('title','Pomodoro Tips'))}</h2>
          <ul style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in data['tips'].get('tips', []))}
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
        window.location.href = 'pomodoro-' + v + '.html';
      }});
    }}

    // Pomodoro logic (simple)
    var timer = null;
    var running = false;
    var isWork = true;
    var timeLeft = 25*60;
    var cycleCount = 0;

    function updateDisplay() {{
      var min = Math.floor(timeLeft/60);
      var sec = timeLeft % 60;
      document.getElementById('pomodoroDisplay').textContent = String(min).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
      document.getElementById('pomodoroStatus').textContent = isWork ? "{escape_allow_tags(ui.get('status_work','Work'))}" : "{escape_allow_tags(ui.get('status_break','Break'))}";
      document.getElementById('pomodoroCycle').textContent = "{escape_allow_tags(ui.get('completed_cycles','Completed cycles:'))} " + cycleCount;
    }}

    function setLengths() {{
      if (isWork) {{
        timeLeft = parseInt(document.getElementById('workLength').value,10) * 60;
      }} else {{
        timeLeft = parseInt(document.getElementById('breakLength').value,10) * 60;
      }}
      updateDisplay();
    }}

    document.getElementById('workLength').addEventListener('change', setLengths);
    document.getElementById('breakLength').addEventListener('change', setLengths);

    document.getElementById('startBtn').addEventListener('click', function(){{
      if (running) return;
      running = true;
      timer = setInterval(function(){{
        if (timeLeft > 0) {{
          timeLeft--;
          updateDisplay();
        }} else {{
          clearInterval(timer);
          running = false;
          if (isWork) cycleCount++;
          isWork = !isWork;
          setLengths();
        }}
      }}, 1000);
    }});

    document.getElementById('pauseBtn').addEventListener('click', function(){{
      if (timer) clearInterval(timer);
      running = false;
    }});

    document.getElementById('resetBtn').addEventListener('click', function(){{
      if (timer) clearInterval(timer);
      running = false;
      cycleCount = 0;
      isWork = true;
      setLengths();
    }});

    setLengths();
  }})();
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js"></script>
</body>
</html>
"""
    return html_out

def generate_article_template(code: str, data_section: Dict, page_type: str) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    section = data_section
    back_link = section.get("back_link", f"pomodoro-{code}.html")
    back_btn = section.get("back_btn", "Back to Pomodoro Timer")

    if page_type == "howto":
        steps_html = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in section.get("steps", []))
        faqs_html = "\n".join(f"<li>{escape_allow_tags(f)}</li>" for f in section.get("faqs", [])) if section.get("faqs") else ""
        tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", [])) if section.get("tips") else ""
        extra = f"""
      <div>
        <h3 class="section-title">{escape_allow_tags(section.get('steps_title','Step-by-Step'))}</h3>
        <ul>
          {steps_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">{escape_allow_tags(section.get('faq_title','FAQs'))}</h3>
        <ul>
          {faqs_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">{escape_allow_tags(section.get('tips_title','Tips'))}</h3>
        <ul>
          {tips_html}
        </ul>
      </div>
"""
    else:
        tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", []))
        did_html = "\n".join(f"<li>{escape_allow_tags(d)}</li>" for d in section.get("did", [])) if section.get("did") else ""
        extra = f"""
      <div>
        <h3 class="section-title">{escape_allow_tags(section.get('tips_title','Top Tips'))}</h3>
        <ul>
          {tips_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">{escape_allow_tags(section.get('did_title','Did You Know?'))}</h3>
        <ul>
          {did_html}
        </ul>
      </div>
"""

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape_allow_tags(section.get('title',''))}</title>
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
    <a class="back-link" href="{back_link}">&larr; {escape_allow_tags(back_btn)}</a>

    <div class="article-card">
      <h1 class="title">{escape_allow_tags(section.get('title',''))}</h1>
      <p class="lead">{escape_allow_tags(section.get('desc',''))}</p>

      {extra}

      <a class="btn btn-outline-primary back-bottom" href="{back_link}">{escape_allow_tags(back_btn)}</a>
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
  <title>Pomodoro Timer — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=pomodoro-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'pomodoro-en.html',
        'fr': 'pomodoro-fr.html',
        'es': 'pomodoro-es.html',
        'de': 'pomodoro-de.html',
        'ru': 'pomodoro-ru.html',
        'el': 'pomodoro-el.html',
        'ar': 'pomodoro-ar.html'
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
    <h1>Pomodoro Timer — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="pomodoro-en.html">English</a></li>
      <li><a href="pomodoro-fr.html">Français</a></li>
      <li><a href="pomodoro-es.html">Español</a></li>
      <li><a href="pomodoro-de.html">Deutsch</a></li>
      <li><a href="pomodoro-ru.html">Русский</a></li>
      <li><a href="pomodoro-el.html">Ελληνικά</a></li>
      <li><a href="pomodoro-ar.html">العربية</a></li>
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
        data["howto"].setdefault("back_link", f"pomodoro-{code}.html")
        data["tips"].setdefault("back_link", f"pomodoro-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"pomodoro-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_tool_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"pomodoro-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_article_template(code, data["howto"], "howto"))

        tips_path = os.path.join(OUTPUT_DIR, f"pomodoro-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_article_template(code, data["tips"], "tips"))

    redirect_path = os.path.join(OUTPUT_DIR, "pomodoro.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        with open("pomodoro.html", "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('pomodoro.html')}'.")

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)

if __name__ == "__main__":
    main()