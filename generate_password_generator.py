#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_password_generator.py

Generates static HTML pages for a "Password Generator" tool in 7 languages:
 - Main Tool Pages:      password-generator-xx.html
 - How-to Article Pages: password-how-to-xx.html
 - Tips Article Pages:   password-tips-xx.html
Output folder (default): ./password_generator

This version:
 - Uses the localized "back" label for the main card's back link (so non-English pages show translated text)
 - Restyles the language selector/dropdown to better match the site's tools
 - Adds a Clear button for the generated password (id="clearBtn")
 - Keeps everything else intact (RTL for Arabic, localized links, article styling)
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "password_generator"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "length_label": "Password Length:",
            "include_upper": "Uppercase",
            "include_lower": "Lowercase",
            "include_numbers": "Digits",
            "include_symbols": "Symbols",
            "generate_btn": "Generate",
            "copy_btn": "Copy",
            "clear_btn": "Clear",
            "password_placeholder": "Your generated password appears here"
        },
        "main": {
            "title": "Password Generator — TimerHaven",
            "desc": "Create secure, random passwords instantly. Learn how to use Password Generator, get productivity tips, FAQs, and read expert articles.",
            "howto_link": "password-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "password-tips-en.html",
            "tips_btn": "Read Full Article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Are passwords saved?</b> No — passwords are generated locally and not stored by this page.",
                "<b>Is this secure?</b> Passwords are created using randomization; always keep them private.",
                "<b>Can I copy to clipboard?</b> Yes — use the \"Copy\" button next to the generated password."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Password Generator — TimerHaven",
            "desc": "The Password Generator tool creates strong, random passwords you can use for any account. Follow these simple steps:",
            "steps": [
                "<b>Choose options:</b> Pick a length and which character types to include (uppercase, numbers, symbols).",
                "<b>Generate:</b> Click <strong>Generate</strong> to create a new password instantly.",
                "<b>Copy:</b> Click <strong>Copy</strong> to copy the password to your clipboard.",
                "<b>Use a manager:</b> Store passwords in a password manager for safe keeping."
            ],
            "back_btn": "Back to Password Generator",
            "back_link": "password-generator-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Password Tips — TimerHaven",
            "desc": "Make your passwords stronger with these practical tips.",
            "tips": [
                "<b>Use long passwords:</b> Aim for 12+ characters.",
                "<b>Mix character types:</b> Combine upper, lower, numbers, and symbols.",
                "<b>Don’t reuse passwords:</b> Use different passwords for different services.",
                "<b>Use a password manager:</b> It generates and stores passwords securely."
            ],
            "back_btn": "Back to Password Generator",
            "back_link": "password-generator-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {
            "length_label": "Longueur du mot de passe:",
            "include_upper": "Majuscules",
            "include_lower": "Minuscules",
            "include_numbers": "Chiffres",
            "include_symbols": "Symboles",
            "generate_btn": "Générer",
            "copy_btn": "Copier",
            "clear_btn": "Effacer",
            "password_placeholder": "Votre mot de passe généré apparaîtra ici"
        },
        "main": {
            "title": "Générateur de mots de passe — TimerHaven",
            "desc": "Créez des mots de passe sécurisés et aléatoires instantanément. Apprenez à utiliser le Générateur, obtenez des conseils et consultez les FAQs.",
            "howto_link": "password-how-to-fr.html",
            "howto_btn": "Lire l'article",
            "tips_link": "password-tips-fr.html",
            "tips_btn": "Lire l'article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Les mots de passe sont-ils sauvegardés ?</b> Non — ils sont générés localement et ne sont pas stockés.",
                "<b>Est-ce sécurisé ?</b> Les mots de passe sont créés aléatoirement ; conservez-les privés.",
                "<b>Puis-je copier ?</b> Oui — utilisez le bouton « Copier »."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique de confidentialité</a> &bull; <a href="terms.html">Conditions</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "Comment utiliser le Générateur de mots de passe — TimerHaven",
            "desc": "L’outil crée des mots de passe forts et aléatoires. Suivez ces étapes :",
            "steps": [
                "<b>Choisissez les options :</b> Longueur et types de caractères (majuscule, chiffres, symboles).",
                "<b>Générez :</b> Cliquez sur <strong>Générer</strong> pour créer un mot de passe.",
                "<b>Copiez :</b> Cliquez sur <strong>Copier</strong> pour le copier.",
                "<b>Stockez :</b> Utilisez un gestionnaire de mots de passe sécurisé."
            ],
            "back_btn": "Retour au Générateur de mots de passe",
            "back_link": "password-generator-fr.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Conseils sur les mots de passe — TimerHaven",
            "desc": "Renforcez vos mots de passe avec ces conseils.",
            "tips": [
                "<b>Utilisez des mots de passe longs :</b> Visez 12+ caractères.",
                "<b>Mélangez les types :</b> Majuscules, minuscules, chiffres et symboles.",
                "<b>Ne réutilisez pas :</b> Utilisez un mot de passe différent par service.",
                "<b>Utilisez un gestionnaire :</b> Pour génération et stockage sécurisé."
            ],
            "back_btn": "Retour au Générateur de mots de passe",
            "back_link": "password-generator-fr.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {
            "length_label": "Longitud de la contraseña:",
            "include_upper": "Mayúsculas",
            "include_lower": "Minúsculas",
            "include_numbers": "Números",
            "include_symbols": "Símbolos",
            "generate_btn": "Generar",
            "copy_btn": "Copiar",
            "clear_btn": "Borrar",
            "password_placeholder": "Su contraseña generada aparecerá aquí"
        },
        "main": {
            "title": "Generador de Contraseñas — TimerHaven",
            "desc": "Crea contraseñas seguras y aleatorias al instante. Aprende a usar el Generador y consulta consejos y FAQs.",
            "howto_link": "password-how-to-es.html",
            "howto_btn": "Leer el artículo",
            "tips_link": "password-tips-es.html",
            "tips_btn": "Leer el artículo",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>¿Se guardan las contraseñas?</b> No — se generan localmente y no se almacenan.",
                "<b>¿Es seguro?</b> Se crean de forma aleatoria; manténgalas privadas.",
                "<b>¿Puedo copiar?</b> Sí — use el botón \"Copiar\"."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política de privacidad</a> &bull; <a href="terms.html">Términos</a> &bull; <a href="contact.html">Contacto</a>'
        },
        "howto": {
            "title": "Cómo usar el Generador de Contraseñas — TimerHaven",
            "desc": "La herramienta crea contraseñas fuertes y aleatorias. Siga estos pasos:",
            "steps": [
                "<b>Elija opciones:</b> Longitud y tipos de caracteres (mayúsculas, números, símbolos).",
                "<b>Genere:</b> Haga clic en <strong>Generar</strong> para crear una contraseña.",
                "<b>Copie:</b> Haga clic en <strong>Copiar</strong> para copiarla.",
                "<b>Guarde:</b> Use un gestor de contraseñas seguro."
            ],
            "back_btn": "Volver al Generador de Contraseñas",
            "back_link": "password-generator-es.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Consejos sobre contraseñas — TimerHaven",
            "desc": "Fortalezca sus contraseñas con estos consejos.",
            "tips": [
                "<b>Use contraseñas largas:</b> Apunte a 12+ caracteres.",
                "<b>Mezcle tipos de caracteres:</b> Mayúsculas, minúsculas, números y símbolos.",
                "<b>No reutilice:</b> Use contraseñas diferentes por servicio.",
                "<b>Use un gestor:</b> Para generarlas y almacenarlas con seguridad."
            ],
            "back_btn": "Volver al Generador de Contraseñas",
            "back_link": "password-generator-es.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {
            "length_label": "Länge des Passworts:",
            "include_upper": "Großbuchstaben",
            "include_lower": "Kleinbuchstaben",
            "include_numbers": "Zahlen",
            "include_symbols": "Symbole",
            "generate_btn": "Generieren",
            "copy_btn": "Kopieren",
            "clear_btn": "Löschen",
            "password_placeholder": "Ihr generiertes Passwort erscheint hier"
        },
        "main": {
            "title": "Passwort-Generator — TimerHaven",
            "desc": "Sofort sichere, zufällige Passwörter erstellen. Erfahren Sie, wie Sie den Generator nutzen und lesen Sie Tipps und FAQs.",
            "howto_link": "password-how-to-de.html",
            "howto_btn": "Artikel lesen",
            "tips_link": "password-tips-de.html",
            "tips_btn": "Artikel lesen",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Werden Passwörter gespeichert?</b> Nein — lokal generiert und nicht gespeichert.",
                "<b>Ist das sicher?</b> Ja — zufällig erzeugt; halten Sie sie privat.",
                "<b>Kann ich kopieren?</b> Ja — nutzen Sie die Schaltfläche \"Kopieren\"."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a> &bull; <a href="terms.html">Nutzungsbedingungen</a> &bull; <a href="contact.html">Kontakt</a>'
        },
        "howto": {
            "title": "So verwenden Sie den Passwort-Generator — TimerHaven",
            "desc": "Das Tool erstellt starke, zufällige Passwörter. So verwenden Sie es:",
            "steps": [
                "<b>Optionen einstellen:</b> Länge und Zeichenarten wählen (Groß-/Kleinbuchstaben, Zahlen, Symbole).",
                "<b>Generieren:</b> Klicken Sie auf <strong>Generieren</strong>.",
                "<b>Kopieren:</b> Klicken Sie auf <strong>Kopieren</strong> zum Kopieren.",
                "<b>Sichern:</b> Verwenden Sie einen Passwort-Manager."
            ],
            "back_btn": "Zurück zum Passwort-Generator",
            "back_link": "password-generator-de.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Passwort-Tipps — TimerHaven",
            "desc": "Stärken Sie Ihre Passwörter mit diesen Empfehlungen.",
            "tips": [
                "<b>Nutzen Sie lange Passwörter:</b> 12+ Zeichen anstreben.",
                "<b>Mischen Sie Zeichen:</b> Groß-/Kleinbuchstaben, Zahlen, Symbole.",
                "<b>Keine Wiederverwendung:</b> Für jeden Dienst einzigartig.",
                "<b>Passwort-Manager:</b> Für sichere Speicherung und Autofill."
            ],
            "back_btn": "Zurück zum Passwort-Generator",
            "back_link": "password-generator-de.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {
            "length_label": "Длина пароля:",
            "include_upper": "Заглавные",
            "include_lower": "Прописные",
            "include_numbers": "Цифры",
            "include_symbols": "Символы",
            "generate_btn": "Сгенерировать",
            "copy_btn": "Копировать",
            "clear_btn": "Очистить",
            "password_placeholder": "Здесь появится сгенерированный пароль"
        },
        "main": {
            "title": "Генератор паролей — TimerHaven",
            "desc": "Создавайте надежные случайные пароли мгновенно. Узнайте, как использовать инструмент, читайте советы и FAQs.",
            "howto_link": "password-how-to-ru.html",
            "howto_btn": "Читать статью",
            "tips_link": "password-tips-ru.html",
            "tips_btn": "Читать статью",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Сохраняются ли пароли?</b> Нет — генерируются локально и не хранятся.",
                "<b>Это безопасно?</b> Да — создаются случайно; держите их в секрете.",
                "<b>Можно ли копировать?</b> Да — используйте кнопку «Копировать»."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика конфиденциальности</a> &bull; <a href="terms.html">Условия</a> &bull; <a href="contact.html">Контакт</a>'
        },
        "howto": {
            "title": "Как пользоваться Генератором паролей — TimerHaven",
            "desc": "Инструмент создает сильные случайные пароли. Следуйте этим шагам:",
            "steps": [
                "<b>Выберите параметры:</b> Длину и типы символов (заглавные, цифры, символы).",
                "<b>Сгенерируйте:</b> Нажмите <strong>Сгенерировать</strong>.",
                "<b>Скопируйте:</b> Нажмите <strong>Копировать</strong> для копирования.",
                "<b>Сохраните:</b> Используйте менеджер паролей."
            ],
            "back_btn": "Вернуться к Генератору паролей",
            "back_link": "password-generator-ru.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Советы по паролям — TimerHaven",
            "desc": "Укрепите свои пароли с помощью этих советов.",
            "tips": [
                "<b>Используйте длинные пароли:</b> Стремитесь к 12+ символам.",
                "<b>Смешивайте символы:</b> Заглавные, строчные, цифры и символы.",
                "<b>Не повторяйте:</b> Уникальные пароли для каждого сервиса.",
                "<b>Менеджеры паролей:</b> Для безопасного хранения и автозаполнения."
            ],
            "back_btn": "Вернуться к Генератору паролей",
            "back_link": "password-generator-ru.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {
            "length_label": "Μήκος κωδικού:",
            "include_upper": "Κεφαλαία",
            "include_lower": "Πεζά",
            "include_numbers": "Αριθμοί",
            "include_symbols": "Σύμβολα",
            "generate_btn": "Δημιουργία",
            "copy_btn": "Αντιγραφή",
            "clear_btn": "Καθαρισμός",
            "password_placeholder": "Εδώ θα εμφανιστεί ο παραγόμενος κωδικός"
        },
        "main": {
            "title": "Γεννήτρια Κωδικών — TimerHaven",
            "desc": "Δημιουργήστε ασφαλείς, τυχαίους κωδικούς άμεσα. Μάθετε πώς να τη χρησιμοποιείτε και δείτε συμβουλές και FAQs.",
            "howto_link": "password-how-to-el.html",
            "howto_btn": "Διαβάστε το άρθρο",
            "tips_link": "password-tips-el.html",
            "tips_btn": "Διαβάστε το άρθρο",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Αποθηκεύονται;</b> Όχι — δημιουργούνται τοπικά και δεν αποθηκεύονται.",
                "<b>Είναι ασφαλές;</b> Ναι — δημιουργούνται τυχαία· κρατήστε τα ιδιωτικά.",
                "<b>Μπορώ να αντιγράψω;</b> Ναι — χρησιμοποιήστε το κουμπί «Αντιγραφή»."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική απορρήτου</a> &bull; <a href="terms.html">Όροι</a> &bull; <a href="contact.html">Επικοινωνία</a>'
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε τη Γεννήτρια Κωδικών — TimerHaven",
            "desc": "Το εργαλείο δημιουργεί ισχυρούς, τυχαίους κωδικούς. Ακολουθήστε αυτά τα βήματα:",
            "steps": [
                "<b>Επιλέξτε επιλογές:</b> Μήκος και τύπους χαρακτήρων (κεφαλαία, αριθμοί, σύμβολα).",
                "<b>Δημιουργία:</b> Κάντε κλικ στο <strong>Δημιουργία</strong>.",
                "<b>Αντιγραφή:</b> Κάντε κλικ στο <strong>Αντιγραφή</strong> για αντιγραφή.",
                "<b>Αποθήκευση:</b> Χρησιμοποιήστε διαχειριστή κωδικών."
            ],
            "back_btn": "Επιστροφή στη Γεννήτρια Κωδικών",
            "back_link": "password-generator-el.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Συμβουλές για κωδικούς — TimerHaven",
            "desc": "Ενισχύστε τους κωδικούς σας με αυτές τις πρακτικές συμβουλές.",
            "tips": [
                "<b>Μήκος:</b> Στοχεύστε 12+ χαρακτήρες.",
                "<b>Μίξη:</b> Κεφαλαία, πεζά, αριθμοί και σύμβολα.",
                "<b>Μην επαναχρησιμοποιείτε:</b> Μοναδικοί κωδικοί για κάθε υπηρεσία.",
                "<b>Χρησιμοποιήστε διαχειριστή:</b> Για ασφαλή αποθήκευση και αυτόματη εισαγωγή."
            ],
            "back_btn": "Επιστροφή στη Γεννήτρια Κωδικών",
            "back_link": "password-generator-el.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {
            "length_label": "الطول:",
            "include_upper": "حروف كبيرة",
            "include_lower": "حروف صغيرة",
            "include_numbers": "أرقام",
            "include_symbols": "رموز",
            "generate_btn": "إنشاء",
            "copy_btn": "نسخ",
            "clear_btn": "مسح",
            "password_placeholder": "سيظهر هنا كلمة المرور المُنشأة"
        },
        "main": {
            "title": "مولد كلمات المرور — TimerHaven",
            "desc": "قم بإنشاء كلمات مرور آمنة وعشوائية على الفور. تعرّف على كيفية استخدام الأداة واطّلع على النصائح والأسئلة الشائعة.",
            "howto_link": "password-how-to-ar.html",
            "howto_btn": "اقرأ المقالة",
            "tips_link": "password-tips-ar.html",
            "tips_btn": "اقرأ المقالة",
            "faq_title": "الأسئلة الشائعة",
            "faq_items": [
                "<b>هل تُحفظ كلمات المرور؟</b> لا — تُنشأ محليًا ولا تُخزن على هذه الصفحة.",
                "<b>هل هذا آمن؟</b> نعم — تُولَّد كلمات المرور عشوائيًا؛ احتفظ بها خاصة.",
                "<b>هل يمكن نسخها؟</b> نعم — استخدم زر \"نسخ\"."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a> &bull; <a href="terms.html">الشروط</a> &bull; <a href="contact.html">اتصل بنا</a>'
        },
        "howto": {
            "title": "كيفية استخدام مولد كلمات المرور — TimerHaven",
            "desc": "تُنشئ الأداة كلمات مرور قوية وعشوائية. اتبع هذه الخطوات:",
            "steps": [
                "<b>اختر الخيارات:</b> الطول وأنواع الأحرف (حروف كبيرة، أرقام، رموز).",
                "<b>انشئ:</b> اضغط <strong>إنشاء</strong> للحصول على كلمة مرور.",
                "<b>انسخ:</b> اضغط <strong>نسخ</strong> لنسخها للحافظة.",
                "<b>احفظها:</b> استخدم مدير كلمات المرور للتخزين الآمن."
            ],
            "back_btn": "العودة إلى مولد كلمات المرور",
            "back_link": "password-generator-ar.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "نصائح كلمات المرور — TimerHaven",
            "desc": "عزّز كلمات المرور عبر هذه النصائح العملية.",
            "tips": [
                "<b>استخدم أطوالًا طويلة:</b> استهدف 12 حرفًا أو أكثر.",
                "<b>ادمج أنواع الأحرف:</b> كبيرة، صغيرة، أرقام، ورموز.",
                "<b>لا تُعد الاستخدام:</b> كلمات مرور فريدة لكل خدمة.",
                "<b>استخدم مدير كلمات مرور:</b> للتخزين الآمن والملء التلقائي."
            ],
            "back_btn": "العودة إلى مولد كلمات المرور",
            "back_link": "password-generator-ar.html",
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

def generate_main_tool_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]

    # Use the localized "back" label from data['howto']['back_btn'] (falls back to English)
    back_label = data.get("howto", {}).get("back_btn", data.get("main",{}).get("back_btn", "Back to Main Menu"))

    faq_html = "\n".join(f"<li>{escape_allow_tags(item)}</li>" for item in main.get("faq_items", []))

    language_options = [
        ("en", "English"),
        ("fr", "Français"),
        ("es", "Español"),
        ("de", "Deutsch"),
        ("ru", "Русский"),
        ("el", "Ελληνικά"),
        ("ar", "العربية")
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
    body {{ background:#f4f7fb; font-family: 'Montserrat', Arial, sans-serif; color: #0b2545; }}
    .page-wrap {{ max-width:1200px; margin: 2rem auto; padding: 0 1rem; }}
    .top-row {{ display:flex; justify-content:flex-end; gap:.5rem; margin-bottom:.6rem; }}
    /* Updated language selector styling to match site: blue accent, subtle border, rounded */
    .language-select {{
      width: 220px;
      border-radius: 10px;
      padding: .28rem .6rem;
      border: 1px solid rgba(13,110,253,0.25);
      background: #ffffff;
      color: #0d6efd;
      box-shadow: 0 1px 0 rgba(13,110,253,0.04) inset;
      appearance: none;
    }}
    .center-row {{ display:flex; gap:1.6rem; justify-content:center; align-items:flex-start; }}
    .article-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); width:330px; padding:1.3rem; display:flex; flex-direction:column; justify-content:space-between; }}
    .article-card h2 {{ color:#185a9d; font-size:1.25rem; margin-bottom:.6rem; }}
    .tool-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); width:420px; padding:1.3rem; }}
    .tool-card h3 {{ color:#185a9d; font-size:1.35rem; margin-bottom:.5rem; }}
    .password-form {{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; margin-bottom:.75rem; }}
    .password-result {{ font-size:1.15rem; font-weight:600; min-height:1.5rem; margin-bottom:.5rem; }}
    .faq-section {{ margin-top:1rem; background:#f7fafc; border-radius:8px; padding:1rem; }}
    footer.site {{ text-align:center; margin-top:1.5rem; color:#6b7280; }}
    @media (max-width:900px) {{
      .center-row{{flex-direction:column;align-items:center;}}
      .article-card, .tool-card{{width:98%; max-width:540px;}}
    }}
    /* ensure select text color remains visible on dark backgrounds in other samplings */
    select.language-select option {{ color:#0b2545; }}
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
          <h2 id="howto-title"><i class="fa fa-key"></i> {escape_allow_tags(data['howto'].get('title', 'How to Use'))}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in data['howto'].get('steps', []))}
          </ol>
        </div>
        <a href="{main.get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.4rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <div class="tool-card" role="region" aria-label="Password generator">
        <!-- Use localized back label from translations -->
        <a href="index.html" class="d-block mb-2" style="text-decoration:none; color:#0d6efd; font-weight:600;">&larr; {escape_allow_tags(back_label)}</a>
        <h3><i class="fa fa-key"></i> {escape_allow_tags(main.get('title','Password Generator'))}</h3>

        <div class="password-section">
          <form id="passwordForm" class="password-form" aria-label="Password generator form" onsubmit="return false;">
            <label style="font-weight:600;">{escape_allow_tags(ui.get('length_label','Password Length:'))}</label>
            <input id="pwLength" type="number" min="4" max="128" value="16" class="form-control" style="max-width:90px;">
            <label><input id="pwUpper" type="checkbox" checked> {escape_allow_tags(ui.get('include_upper'))}</label>
            <label><input id="pwLower" type="checkbox" checked> {escape_allow_tags(ui.get('include_lower'))}</label>
            <label><input id="pwDigits" type="checkbox" checked> {escape_allow_tags(ui.get('include_numbers'))}</label>
            <label><input id="pwSymbols" type="checkbox"> {escape_allow_tags(ui.get('include_symbols'))}</label>
            <button id="generateBtn" class="btn btn-success btn-sm" type="button">{escape_allow_tags(ui.get('generate_btn'))}</button>
            <button id="copyBtn" class="btn btn-outline-secondary btn-sm" type="button" style="display:none;">{escape_allow_tags(ui.get('copy_btn'))}</button>
            <button id="clearBtn" class="btn btn-outline-danger btn-sm" type="button" style="display:none; margin-left:6px;">{escape_allow_tags(ui.get('clear_btn','Clear'))}</button>
          </form>

          <div id="pwResult" class="password-result" aria-live="polite"></div>
        </div>

        <details class="faq-section" style="margin-top:.8rem;">
          <summary style="font-weight:700; font-size:1rem;">{escape_allow_tags(main.get('faq_title'))}</summary>
          <ul style="padding-left:1.1rem; color:#374151;">
            {faq_html}
          </ul>
        </details>
      </div>

      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {escape_allow_tags(data['tips'].get('title','Tips'))}</h2>
          <ul style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in data['tips'].get('tips', []))}
          </ul>
        </div>
        <a href="{main.get('tips_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.4rem;">{escape_allow_tags(main.get('tips_btn'))}</a>
      </div>
    </div>

    <footer class="site" style="text-align:center; margin-top:1.5rem; color:#6b7280;">
      {main.get('footer')}
    </footer>
  </div>

  <script>
  (function() {{
    var sel = document.getElementById('language-select-top');
    if (sel) {{
      sel.addEventListener('change', function() {{
        var v = this.value || 'en';
        window.location.href = 'password-generator-' + v + '.html';
      }});
    }}

    function randInt(max) {{ return Math.floor(Math.random() * max); }}
    function generatePassword(length, upper, lower, digits, symbols) {{
      var low = 'abcdefghijklmnopqrstuvwxyz';
      var up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      var nums = '0123456789';
      var syms = '!@#$%^&*()-_=+[]{{}};:,.<>?/|`~';
      var chars = '';
      if (lower) chars += low;
      if (upper) chars += up;
      if (digits) chars += nums;
      if (symbols) chars += syms;
      if (!chars) return '';
      var out = '';
      for (var i=0;i<length;i++) out += chars.charAt(randInt(chars.length));
      return out;
    }}

    var genBtn = document.getElementById('generateBtn');
    var copyBtn = document.getElementById('copyBtn');
    var clearBtn = document.getElementById('clearBtn');
    var pwResult = document.getElementById('pwResult');

    function doGenerate() {{
      var length = parseInt(document.getElementById('pwLength').value) || 16;
      length = Math.max(1, Math.min(128, length));
      var upper = document.getElementById('pwUpper').checked;
      var lower = document.getElementById('pwLower').checked;
      var digits = document.getElementById('pwDigits').checked;
      var symbols = document.getElementById('pwSymbols').checked;
      var pw = generatePassword(length, upper, lower, digits, symbols);
      pwResult.textContent = pw;
      if (pw) {{
        copyBtn.style.display = 'inline-block';
        clearBtn.style.display = 'inline-block';
      }} else {{
        copyBtn.style.display = 'none';
        clearBtn.style.display = 'none';
      }}
    }}

    if (genBtn) genBtn.addEventListener('click', doGenerate);

    if (copyBtn) copyBtn.addEventListener('click', function() {{
      var t = pwResult.textContent || '';
      if (!t) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(t).then(function(){{
          var old = copyBtn.textContent;
          copyBtn.textContent = old + ' ✓';
          setTimeout(function() {{ copyBtn.textContent = old; }}, 1000);
        }}, function(){{ alert('Could not copy to clipboard.'); }});
      }} else {{
        var ta = document.createElement('textarea');
        ta.value = t;
        document.body.appendChild(ta);
        ta.select();
        try {{ document.execCommand('copy'); }} catch(e) {{ alert('Could not copy to clipboard.'); }}
        document.body.removeChild(ta);
      }}
    }});

    if (clearBtn) clearBtn.addEventListener('click', function() {{
      pwResult.textContent = '';
      copyBtn.style.display = 'none';
      clearBtn.style.display = 'none';
    }});

    // initial generate
    if (genBtn) genBtn.click();
  }})();
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js"></script>
</body>
</html>
"""
    return html_out

def generate_howto_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    how = data["howto"]
    steps_html = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in how.get("steps", []))
    faqs_html = "\n".join(f"<li>{escape_allow_tags(f)}</li>" for f in how.get("faqs", []))
    tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in how.get("tips", []))

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape_allow_tags(how.get('title','How to'))}</title>
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
    <a class="back-link" href="{how.get('back_link','password-generator-en.html')}">&larr; {escape_allow_tags(how.get('back_btn','Back to Tool'))}</a>

    <div class="article-card">
      <h1 class="title">{escape_allow_tags(how.get('title','How to Use'))}</h1>
      <p class="lead">{escape_allow_tags(how.get('desc',''))}</p>

      <div>
        <h3 class="section-title">Step-by-Step Guide</h3>
        <ul>
          {steps_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">FAQs</h3>
        <ul>
          {faqs_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">Security Tips</h3>
        <ul>
          {tips_html}
        </ul>
      </div>

      <a class="btn btn-outline-primary back-bottom" href="{how.get('back_link','password-generator-en.html')}">{escape_allow_tags(how.get('back_btn','Back to Tool'))}</a>
    </div>

    <footer class="site">{how.get('footer','')}</footer>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return html_out

def generate_tips_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    tips = data["tips"]
    tips_html = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in tips.get("tips", []))
    did_html = "\n".join(f"<li>{escape_allow_tags(d)}</li>" for d in tips.get("did", []))

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape_allow_tags(tips.get('title','Tips'))}</title>
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
    ul {{ color:#374151; padding-left:1.2rem; }}
    .back-bottom {{ margin-top:1.25rem; display:inline-block; }}
    footer.site {{ color:#6b7280; margin-top:1.5rem; text-align:center; }}
    @media (max-width:900px) {{ .page {{ margin:1rem auto; }} .article-card {{ padding:1rem; }} h1.title {{ font-size:1.6rem; }} }}
  </style>
</head>
<body>
  <div class="page">
    <a class="back-link" href="{tips.get('back_link','password-generator-en.html')}">&larr; {escape_allow_tags(tips.get('back_btn','Back to Tool'))}</a>

    <div class="article-card">
      <h1 class="title">{escape_allow_tags(tips.get('title','Password Tips'))}</h1>
      <p class="lead">{escape_allow_tags(tips.get('desc',''))}</p>

      <div>
        <h3 class="section-title">{escape_allow_tags(tips.get('tips_title','Top Tips'))}</h3>
        <ul>
          {tips_html}
        </ul>
      </div>

      <div>
        <h3 class="section-title">{escape_allow_tags(tips.get('did_title','Did You Know?'))}</h3>
        <ul>
          {did_html}
        </ul>
      </div>

      <a class="btn btn-outline-primary back-bottom" href="{tips.get('back_link','password-generator-en.html')}">{escape_allow_tags(tips.get('back_btn','Back to Tool'))}</a>
    </div>

    <footer class="site">{tips.get('footer','')}</footer>
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
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Password Generator — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=password-generator-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'password-generator-en.html',
        'fr': 'password-generator-fr.html',
        'es': 'password-generator-es.html',
        'de': 'password-generator-de.html',
        'ru': 'password-generator-ru.html',
        'el': 'password-generator-el.html',
        'ar': 'password-generator-ar.html'
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
    <h1>Password Generator — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="password-generator-en.html">English</a></li>
      <li><a href="password-generator-fr.html">Français</a></li>
      <li><a href="password-generator-es.html">Español</a></li>
      <li><a href="password-generator-de.html">Deutsch</a></li>
      <li><a href="password-generator-ru.html">Русский</a></li>
      <li><a href="password-generator-el.html">Ελληνικά</a></li>
      <li><a href="password-generator-ar.html">العربية</a></li>
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
        data["howto"].setdefault("back_link", f"password-generator-{code}.html")
        data["tips"].setdefault("back_link", f"password-generator-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"password-generator-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_tool_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"password-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_howto_html(code, data))

        tips_path = os.path.join(OUTPUT_DIR, f"password-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_tips_html(code, data))

    redirect_path = os.path.join(OUTPUT_DIR, "password-generator.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        root_redirect = "password-generator.html"
        with open(root_redirect, "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('password-generator.html')}'.")

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)

if __name__ == "__main__":
    main()