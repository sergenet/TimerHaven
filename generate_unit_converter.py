#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_unit_converter.py

Generates localized static HTML pages for the Unit Converter tool in 7 languages.

Small change: the main page's three card headings (left article card title,
tool-card heading, right article card title) no longer include the "— TimerHaven"
suffix. The full page <title> and article pages keep the complete titles
(including the brand) so SEO/title remains descriptive.

Usage:
  python generate_unit_converter.py
  python generate_unit_converter.py --root   # also write unit-converter.html into current dir
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "unit_converter_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

# Translations (same as before)
TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "type_length": "Length",
            "type_weight": "Weight",
            "type_temperature": "Temperature",
            "value_placeholder": "Value",
            "convert_btn": "Convert",
            "result_invalid": "Please enter a valid value.",
            "back_main": "Back to Main Menu"
        },
        "main": {
            "title": "Unit Converter — TimerHaven",
            "desc": "Convert length, weight, temperature, and more units. Learn how to use Unit Converter, get productivity tips, FAQs, and read expert articles.",
            "howto_link": "unit-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "unit-tips-en.html",
            "tips_btn": "Read Full Article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Are all units supported?</b> Most common units are included.",
                "<b>Is the conversion free?</b> Yes, use as much as you want.",
                "<b>Can I convert decimals?</b> Yes, decimal values are supported."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Unit Converter — TimerHaven",
            "steps_title": "Step-by-Step Guide",
            "desc": "The <strong>Unit Converter</strong> tool is perfect for quick and accurate conversions. Here’s how to use it:",
            "steps": [
                "<b>Enter your value:</b> Type the number you want to convert.",
                "<b>Select units:</b> Choose the units you wish to convert from and to.",
                "<b>Convert:</b> Click <strong>Convert</strong> to get your answer instantly.",
                "<b>Try different units:</b> Switch units as needed for different conversions."
            ],
            "back_btn": "Back to Unit Converter",
            "back_link": "unit-converter-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Unit Converter Tips — TimerHaven",
            "tips_title": "Top Tips",
            "desc": "Make your conversions easier and more accurate with these tips:",
            "tips": [
                "<b>Double-check units:</b> Make sure you’re converting the right types.",
                "<b>Switch directions:</b> Try converting both ways for accuracy.",
                "<b>Bookmark for quick access:</b> Save this page for instant conversions."
            ],
            "back_btn": "Back to Unit Converter",
            "back_link": "unit-converter-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {
            "type_length": "Longueur",
            "type_weight": "Poids",
            "type_temperature": "Température",
            "value_placeholder": "Valeur",
            "convert_btn": "Convertir",
            "result_invalid": "Veuillez entrer une valeur valide.",
            "back_main": "Retour au menu principal"
        },
        "main": {
            "title": "Convertisseur d'unités — TimerHaven",
            "desc": "Convertissez longueur, poids, température et plus. Apprenez à utiliser le Convertisseur d'unités, obtenez des conseils et articles.",
            "howto_link": "unit-how-to-fr.html",
            "howto_btn": "Lire l'article",
            "tips_link": "unit-tips-fr.html",
            "tips_btn": "Lire l'article",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Toutes les unités sont-elles prises en charge ?</b> La plupart des unités courantes sont incluses.",
                "<b>La conversion est-elle gratuite ?</b> Oui, utilisez-la autant que vous voulez.",
                "<b>Puis-je convertir des décimales ?</b> Oui, les valeurs décimales sont prises en charge."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique</a>'
        },
        "howto": {
            "title": "Comment utiliser le Convertisseur d'unités — TimerHaven",
            "steps_title": "Guide étape par étape",
            "desc": "L'outil <strong>Convertisseur d'unités</strong> est parfait pour des conversions rapides et précises. Voici comment l'utiliser :",
            "steps": [
                "<b>Entrez la valeur :</b> Tapez le nombre à convertir.",
                "<b>Sélectionnez les unités :</b> Choisissez les unités d'origine et de destination.",
                "<b>Convertir :</b> Cliquez sur <strong>Convertir</strong> pour obtenir la réponse immédiatement.",
                "<b>Essayez d'autres unités :</b> Changez les unités selon vos besoins."
            ],
            "back_btn": "Retour au Convertisseur",
            "back_link": "unit-converter-fr.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Conseils Convertisseur — TimerHaven",
            "tips_title": "Conseils",
            "desc": "Facilitez et améliorez vos conversions avec ces conseils :",
            "tips": [
                "<b>Vérifiez les unités :</b> Assurez-vous de convertir les bons types.",
                "<b>Inversez :</b> Essayez la conversion dans l'autre sens pour vérifier.",
                "<b>Mettez en favori :</b> Enregistrez cette page pour un accès rapide."
            ],
            "back_btn": "Retour au Convertisseur",
            "back_link": "unit-converter-fr.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {
            "type_length": "Longitud",
            "type_weight": "Peso",
            "type_temperature": "Temperatura",
            "value_placeholder": "Valor",
            "convert_btn": "Convertir",
            "result_invalid": "Por favor ingrese un valor válido.",
            "back_main": "Volver al menú principal"
        },
        "main": {
            "title": "Convertidor de unidades — TimerHaven",
            "desc": "Convierte longitud, peso, temperatura y más. Aprende a usar el Convertidor, obtén consejos y artículos.",
            "howto_link": "unit-how-to-es.html",
            "howto_btn": "Leer el artículo",
            "tips_link": "unit-tips-es.html",
            "tips_btn": "Leer el artículo",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>¿Se admiten todas las unidades?</b> Se incluyen las unidades comunes más usadas.",
                "<b>¿La conversión es gratuita?</b> Sí, úsala tanto como necesites.",
                "<b>¿Puedo convertir decimales?</b> Sí, se admiten valores decimales."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política</a>'
        },
        "howto": {
            "title": "Cómo usar el Convertidor — TimerHaven",
            "steps_title": "Guía paso a paso",
            "desc": "La herramienta <strong>Convertidor</strong> es perfecta para conversiones rápidas y precisas. Esto es cómo usarla:",
            "steps": [
                "<b>Ingrese su valor :</b> Escriba el número que desea convertir.",
                "<b>Selecciones las unidades :</b> Elija las unidades de origen y destino.",
                "<b>Convertir :</b> Haga clic en <strong>Convertir</strong> para obtener la respuesta inmediatamente.",
                "<b>Pruebe otras unidades :</b> Cambie unidades según sea necesario."
            ],
            "back_btn": "Volver al Convertidor",
            "back_link": "unit-converter-es.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Consejos Convertidor — TimerHaven",
            "tips_title": "Consejos principales",
            "desc": "Haz tus conversiones más fáciles y precisas con estos consejos:",
            "tips": [
                "<b>Verifica las unidades :</b> Asegúrate de convertir los tipos correctos.",
                "<b>Cambia de dirección :</b> Intenta convertir en ambas direcciones para comprobar.",
                "<b>Guarda en favoritos :</b> Guarda esta página para acceso rápido."
            ],
            "back_btn": "Volver al Convertidor",
            "back_link": "unit-converter-es.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {
            "type_length": "Länge",
            "type_weight": "Gewicht",
            "type_temperature": "Temperatur",
            "value_placeholder": "Wert",
            "convert_btn": "Konvertieren",
            "result_invalid": "Bitte geben Sie einen gültigen Wert ein.",
            "back_main": "Zurück zum Hauptmenü"
        },
        "main": {
            "title": "Einheitenumrechner — TimerHaven",
            "desc": "Konvertieren Sie Länge, Gewicht, Temperatur und mehr. Erfahren Sie, wie der Umrechner funktioniert, erhalten Sie Tipps und Artikel.",
            "howto_link": "unit-how-to-de.html",
            "howto_btn": "Artikel lesen",
            "tips_link": "unit-tips-de.html",
            "tips_btn": "Artikel lesen",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Werden alle Einheiten unterstützt?</b> Die gebräuchlichsten Einheiten sind enthalten.",
                "<b>Ist die Umrechnung kostenlos?</b> Ja, verwenden Sie sie so oft Sie möchten.",
                "<b>Kann ich Dezimalzahlen umrechnen?</b> Ja, Dezimalwerte werden unterstützt."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a>'
        },
        "howto": {
            "title": "So verwenden Sie den Einheitenumrechner — TimerHaven",
            "steps_title": "Schritt-für-Schritt-Anleitung",
            "desc": "Das Tool <strong>Einheitenumrechner</strong> ist ideal für schnelle und genaue Umrechnungen. So verwenden Sie es:",
            "steps": [
                "<b>Geben Sie Ihren Wert ein:</b> Tippen Sie die Zahl ein, die Sie umrechnen möchten.",
                "<b>Wählen Sie Einheiten:</b> Wählen Sie die Ausgangs- und Ziel-Einheiten.",
                "<b>Konvertieren:</b> Klicken Sie auf <strong>Konvertieren</strong>, um sofort das Ergebnis zu erhalten.",
                "<b>Andere Einheiten ausprobieren:</b> Wechseln Sie die Einheiten bei Bedarf."
            ],
            "back_btn": "Zurück zum Umrechner",
            "back_link": "unit-converter-de.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Tipps Einheitenumrechner — TimerHaven",
            "tips_title": "Top-Tipps",
            "desc": "Machen Sie Ihre Umrechnungen einfacher und genauer mit diesen Tipps:",
            "tips": [
                "<b>Einheiten überprüfen:</b> Stellen Sie sicher, dass Sie die richtigen Typen umrechnen.",
                "<b>Richtung wechseln:</b> Versuchen Sie die Umrechnung in beide Richtungen zur Kontrolle.",
                "<b>Lesezeichen setzen:</b> Speichern Sie diese Seite zum schnellen Zugriff."
            ],
            "back_btn": "Zurück zum Umrechner",
            "back_link": "unit-converter-de.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {
            "type_length": "Длина",
            "type_weight": "Вес",
            "type_temperature": "Температура",
            "value_placeholder": "Значение",
            "convert_btn": "Преобразовать",
            "result_invalid": "Пожалуйста, введите корректное значение.",
            "back_main": "Назад в главное меню"
        },
        "main": {
            "title": "Конвертер единиц — TimerHaven",
            "desc": "Конвертируйте длину, вес, температуру и другие единицы. Узнайте, как пользоваться конвертером, получите советы и статьи.",
            "howto_link": "unit-how-to-ru.html",
            "howto_btn": "Читать статью",
            "tips_link": "unit-tips-ru.html",
            "tips_btn": "Читать статью",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Поддерживаются ли все единицы?</b> Включены наиболее распространённые единицы.",
                "<b>Бесплатна ли конверсия?</b> Да, используйте её сколько нужно.",
                "<b>Можно ли конвертировать десятичные числа?</b> Да, десятичные значения поддерживаются."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика</a>'
        },
        "howto": {
            "title": "Как пользоваться конвертером — TimerHaven",
            "steps_title": "Пошаговое руководство",
            "desc": "Инструмент <strong>Конвертер единиц</strong> отлично подходит для быстрых и точных преобразований. Как его использовать:",
            "steps": [
                "<b>Введите значение:</b> Введите число для конвертации.",
                "<b>Выберите единицы:</b> Выберите исходную и целевую единицы.",
                "<b>Преобразовать:</b> Нажмите <strong>Преобразовать</strong>, чтобы сразу получить результат.",
                "<b>Попробуйте другие единицы:</b> Меняйте единицы по необходимости."
            ],
            "back_btn": "Вернуться к конвертеру",
            "back_link": "unit-converter-ru.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Советы Конвертера — TimerHaven",
            "tips_title": "Лучшие советы",
            "desc": "Упростите и улучшите точность ваших преобразований с этими советами:",
            "tips": [
                "<b>Проверяйте единицы:</b> Убедитесь, что вы конвертируете правильные типы.",
                "<b>Поменяйте направление:</b> Попробуйте обратную конверсию для проверки.",
                "<b>Добавьте в закладки:</b> Сохраните страницу для быстрого доступа."
            ],
            "back_btn": "Вернуться к конвертеру",
            "back_link": "unit-converter-ru.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {
            "type_length": "Μήκος",
            "type_weight": "Βάρος",
            "type_temperature": "Θερμοκρασία",
            "value_placeholder": "Τιμή",
            "convert_btn": "Μετατροπή",
            "result_invalid": "Εισαγάγετε μια έγκυρη τιμή, παρακαλώ.",
            "back_main": "Επιστροφή στο κύριο μενού"
        },
        "main": {
            "title": "Μετατροπέας μονάδων — TimerHaven",
            "desc": "Μετατρέψτε μήκος, βάρος, θερμοκρασία και άλλες μονάδες. Μάθετε πώς να χρησιμοποιείτε τον Μετατροπέα, λάβετε συμβουλές και άρθρα.",
            "howto_link": "unit-how-to-el.html",
            "howto_btn": "Διαβάστε το άρθρο",
            "tips_link": "unit-tips-el.html",
            "tips_btn": "Διαβάστε το άρθρο",
            "faq_title": "FAQs",
            "faq_items": [
                "<b>Υποστηρίζονται όλες οι μονάδες;</b> Περιλαμβάνονται οι πιο κοινές μονάδες.",
                "<b>Η μετατροπή είναι δωρεάν;</b> Ναι, χρησιμοποιήστε το όσο χρειαστείτε.",
                "<b>Μπορώ να μετατρέψω δεκαδικά;</b> Ναι, υποστηρίζονται δεκαδικές τιμές."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική</a>'
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε τον Μετατροπέα — TimerHaven",
            "steps_title": "Οδηγίες βήμα προς βήμα",
            "desc": "Το εργαλείο <strong>Μετατροπέας μονάδων</strong> είναι ιδανικό για γρήγορες και ακριβείς μετατροπές. Πώς να το χρησιμοποιήσετε:",
            "steps": [
                "<b>Εισάγετε την τιμή:</b> Πληκτρολογήστε τον αριθμό που θέλετε να μετατρέψετε.",
                "<b>Επιλέξτε μονάδες:</b> Επιλέξτε την αρχική και την προοριζόμενη μονάδα.",
                "<b>Μετατροπή:</b> Πατήστε <strong>Μετατροπή</strong> για άμεσο αποτέλεσμα.",
                "<b>Δοκιμάστε άλλες μονάδες:</b> Αλλάξτε μονάδες εάν χρειαστεί."
            ],
            "back_btn": "Επιστροφή στον Μετατροπέα",
            "back_link": "unit-converter-el.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Συμβουλές Μετατροπέα — TimerHaven",
            "tips_title": "Κορυφαίες συμβουλές",
            "desc": "Κάντε τις μετατροπές σας πιο εύκολες και ακριβείς με αυτές τις συμβουλές:",
            "tips": [
                "<b>Ελέγξτε τις μονάδες:</b> Βεβαιωθείτε ότι μετατρέπετε τους σωστούς τύπους.",
                "<b>Δοκιμάστε αντίστροφα:</b> Δοκιμάστε την αντίστροφη μετατροπή για επαλήθευση.",
                "<b>Προσθέστε σε σελιδοδείκτη:</b> Αποθηκεύστε τη σελίδα για γρήγορη πρόσβαση."
            ],
            "back_btn": "Επιστροφή στον Μετατροπέα",
            "back_link": "unit-converter-el.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {
            "type_length": "الطول",
            "type_weight": "الوزن",
            "type_temperature": "درجة الحرارة",
            "value_placeholder": "القيمة",
            "convert_btn": "تحويل",
            "result_invalid": "يرجى إدخال قيمة صالحة.",
            "back_main": "العودة إلى القائمة الرئيسية"
        },
        "main": {
            "title": "محول الوحدات — TimerHaven",
            "desc": "حوّل الطول والوزن ودرجة الحرارة والمزيد. تعلّم كيفية استخدام محول الوحدات، واحصل على نصائح ومقالات.",
            "howto_link": "unit-how-to-ar.html",
            "howto_btn": "اقرأ المقالة",
            "tips_link": "unit-tips-ar.html",
            "tips_btn": "اقرأ المقالة",
            "faq_title": "الأسئلة الشائعة",
            "faq_items": [
                "<b>هل تدعم جميع الوحدات؟</b> يتم تضمين الوحدات الشائعة.",
                "<b>هل التحويل مجاني؟</b> نعم، استخدمه بقدر ما تشاء.",
                "<b>هل يمكن تحويل الأعداد العشرية؟</b> نعم، يتم دعم القيم العشرية."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a>'
        },
        "howto": {
            "title": "كيفية استخدام محول الوحدات — TimerHaven",
            "steps_title": "دليل خطوة بخطوة",
            "desc": "أداة <strong>محول الوحدات</strong> ممتازة للتحويلات السريعة والدقيقة. كيفية استخدامها:",
            "steps": [
                "<b>أدخل القيمة:</b> اكتب الرقم الذي تريد تحويله.",
                "<b>اختر الوحدات:</b> اختر الوحدة الأصلية والوحدة المطلوبة.",
                "<b>تحويل:</b> اضغط <strong>تحويل</strong> للحصول على النتيجة فورًا.",
                "<b>جرب وحدات أخرى:</b> غيّر الوحدات حسب الحاجة."
            ],
            "back_btn": "العودة إلى المحول",
            "back_link": "unit-converter-ar.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "نصائح المحول — TimerHaven",
            "tips_title": "أهم النصائح",
            "desc": "اجعل تحويلاً أكثر سهولة ودقة بهذه النصائح:",
            "tips": [
                "<b>تحقق من الوحدات:</b> تأكد من تحويل أنواع الوحدات الصحيحة.",
                "<b>حاول الاتجاه المعاكس:</b> جرّب التحويل بالعكس للتحقق.",
                "<b>أضف إلى العلامات المرجعية:</b> احفظ الصفحة للوصول السريع."
            ],
            "back_btn": "العودة إلى المحول",
            "back_link": "unit-converter-ar.html",
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
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

def remove_brand_suffix(s: str) -> str:
    """
    Remove the '— TimerHaven' brand suffix from a string if present.
    This is used only for the three on-page cards so they are cleaner.
    """
    if not isinstance(s, str):
        return s
    # Remove common variants of the suffix used in translations
    for suffix in [" — TimerHaven", "— TimerHaven", " - TimerHaven", " – TimerHaven"]:
        if suffix in s:
            return s.replace(suffix, "").strip()
    return s

def generate_main_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]
    howto = data.get("howto", {})
    tips = data.get("tips", {})

    back_label = ui.get("back_main", main.get("back_main", "Back to Main Menu"))
    language_options = [
        ("en", "English"), ("fr", "Français"), ("es", "Español"),
        ("de", "Deutsch"), ("ru", "Русский"), ("el", "Ελληνικά"), ("ar", "العربية")
    ]
    options_html = "".join(
        f'<option value="{lang}"{" selected" if lang == code else ""}>{html.escape(name)}</option>'
        for lang, name in language_options
    )

    type_length = escape_allow_tags(ui.get("type_length", "Length"))
    type_weight = escape_allow_tags(ui.get("type_weight", "Weight"))
    type_temperature = escape_allow_tags(ui.get("type_temperature", "Temperature"))
    value_placeholder = escape_allow_tags(ui.get("value_placeholder", "Value"))
    convert_btn = escape_allow_tags(ui.get("convert_btn", "Convert"))

    faq_html = "\n".join(f"<li>{escape_allow_tags(item)}</li>" for item in main.get("faq_items", []))
    result_invalid_js = js_string_literal(ui.get("result_invalid", "Please enter a valid value."))

    # Card titles without the brand suffix
    howto_card_title = escape_allow_tags(remove_brand_suffix(howto.get("title", "How to Use Unit Converter")))
    tool_card_title = escape_allow_tags(remove_brand_suffix(main.get("title", "Unit Converter")))
    tips_card_title = escape_allow_tags(remove_brand_suffix(tips.get("title", "Unit Converter Productivity Tips")))

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
    .article-card, .tool-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); padding:1.3rem; }}
    .article-card {{ width:330px; min-width:200px; min-height:340px; height:340px; display:flex; flex-direction:column; justify-content:space-between; align-items:flex-start; }}
    .tool-card {{ width:410px; min-width:240px; min-height:330px; display:flex; flex-direction:column; }}
    .article-card h2 {{ color:#185a9d; font-size:1.25rem; margin-bottom:.6rem; }}
    .tool-card h3 {{ color:#185a9d; font-size:1.35rem; margin-bottom:.5rem; }}
    .converter-form {{ display:flex; gap:.5rem; margin-bottom:1rem; flex-wrap:wrap; align-items:center; }}
    .converter-result {{ font-weight:700; font-size:1.12em; margin-bottom:1rem; }}
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
      <!-- Left article card -->
      <div class="article-card" aria-labelledby="howto-title">
        <div>
          <h2 id="howto-title"><i class="fa fa-ruler-combined"></i> {howto_card_title}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in howto.get('steps', []))}
          </ol>
        </div>
        <a href="{main.get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <!-- Tool card -->
      <div class="tool-card" role="region" aria-label="Unit Converter">
        <details class="howto-mobile" id="howto-mobile">
          <summary><h4 style="color:#185a9d;display:inline;"><i class="fa fa-ruler-combined"></i> {howto_card_title}</h4></summary>
          <ol>
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in howto.get('steps', []))}
          </ol>
        </details>

        <a href="index.html" class="back-link">&larr; {escape_allow_tags(back_label)}</a>
        <h3><i class="fa fa-ruler-combined"></i> {tool_card_title}</h3>

        <div class="unit-section">
          <form class="converter-form" id="unitForm">
            <select id="typeSelect" class="form-select" style="max-width:140px;">
              <option value="length">{type_length}</option>
              <option value="weight">{type_weight}</option>
              <option value="temperature">{type_temperature}</option>
            </select>

            <input type="number" id="inputValue" class="form-control" placeholder="{value_placeholder}" style="max-width:100px;">

            <select id="fromUnit" class="form-select" style="max-width:120px;"></select>
            <span style="font-size:1.3em;">→</span>
            <select id="toUnit" class="form-select" style="max-width:120px;"></select>

            <button type="submit" class="btn btn-primary btn-sm">{convert_btn}</button>
          </form>

          <div id="unitResult" class="converter-result"></div>
        </div>

        <details class="faq-section">
          <summary>{escape_allow_tags(main.get('faq_title'))}</summary>
          <ul style="padding-left:1.1rem; color:#374151;">
            {faq_html}
          </ul>
        </details>

        <details class="tips-mobile" id="tips-mobile">
          <summary><h4 style="color:#185a9d;display:inline;"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {escape_allow_tags(tips.get('title','Tips'))}</h4></summary>
          <ul>
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in tips.get('tips', []))}
          </ul>
        </details>
      </div>

      <!-- Right article card -->
      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {tips_card_title}</h2>
          <ul style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in tips.get('tips', []))}
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
  // Unit types & conversion logic (kept as original)
  const unitTypes = {{
    length: {{
      units: {{ "Meter": 1, "Kilometer": 1000, "Centimeter": 0.01, "Millimeter": 0.001, "Mile": 1609.34, "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254 }},
      convert: (val, from, to) => val * unitTypes.length.units[from] / unitTypes.length.units[to]
    }},
    weight: {{
      units: {{ "Kilogram": 1, "Gram": 0.001, "Milligram": 0.000001, "Pound": 0.453592, "Ounce": 0.0283495 }},
      convert: (val, from, to) => val * unitTypes.weight.units[from] / unitTypes.weight.units[to]
    }},
    temperature: {{
      units: {{ "Celsius": "C", "Fahrenheit": "F", "Kelvin": "K" }},
      convert: (val, from, to) => {{
        if (from === to) return val;
        if (from === "Celsius" && to === "Fahrenheit") return val * 9/5 + 32;
        if (from === "Fahrenheit" && to === "Celsius") return (val - 32) * 5/9;
        if (from === "Celsius" && to === "Kelvin") return val + 273.15;
        if (from === "Kelvin" && to === "Celsius") return val - 273.15;
        if (from === "Fahrenheit" && to === "Kelvin") return (val - 32) * 5/9 + 273.15;
        if (from === "Kelvin" && to === "Fahrenheit") return (val - 273.15) * 9/5 + 32;
      }}
    }}
  }};

  function populateUnits(type) {{
    const from = document.getElementById('fromUnit');
    const to = document.getElementById('toUnit');
    from.innerHTML = to.innerHTML = '';
    Object.keys(unitTypes[type].units).forEach(u => {{
      from.innerHTML += `<option value="${{u}}">${{u}}</option>`;
      to.innerHTML += `<option value="${{u}}">${{u}}</option>`;
    }});
  }}

  document.getElementById('typeSelect').addEventListener('change', function() {{
    populateUnits(this.value);
  }});
  populateUnits('length');

  document.getElementById('unitForm').addEventListener('submit', function(e) {{
    e.preventDefault();
    const type = document.getElementById('typeSelect').value;
    const val = parseFloat(document.getElementById('inputValue').value);
    const from = document.getElementById('fromUnit').value;
    const to = document.getElementById('toUnit').value;
    const resultEl = document.getElementById('unitResult');
    if (isNaN(val)) {{
      resultEl.innerText = "{js_string_literal(TRANSLATIONS['en']['ui']['result_invalid'])}";
      return;
    }}
    let result = unitTypes[type].convert(val, from, to);
    resultEl.innerText = `${{val}} ${{from}} = ${{result}} ${{to}}`;
  }});

  // language selector redirect
  (function() {{
    var sel = document.getElementById('language-select-top');
    if (sel) {{
      sel.addEventListener('change', function() {{
        var v = this.value || 'en';
        window.location.href = 'unit-converter-' + v + '.html';
      }});
    }}
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
    title = escape_allow_tags(section.get("title", ""))
    desc = escape_allow_tags(section.get("desc", ""))
    back_link = section.get("back_link", f"unit-converter-{code}.html")
    back_btn = escape_allow_tags(section.get("back_btn", "Back to Unit Converter"))

    if page_type == "howto":
        heading = escape_allow_tags(section.get("steps_title", "Step-by-Step Guide"))
        body_list = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in section.get("steps", []))
        extra = f"""
      <h2>{heading}</h2>
      <ol>
        {body_list}
      </ol>
"""
    else:
        heading = escape_allow_tags(section.get("tips_title", "Top Tips"))
        body_list = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", []))
        extra = f"""
      <h2>{heading}</h2>
      <ul>
        {body_list}
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
    h2 {{ font-size:1.25rem; margin-top:1rem; margin-bottom:.6rem; }}
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
  <title>Unit Converter — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=unit-converter-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'unit-converter-en.html',
        'fr': 'unit-converter-fr.html',
        'es': 'unit-converter-es.html',
        'de': 'unit-converter-de.html',
        'ru': 'unit-converter-ru.html',
        'el': 'unit-converter-el.html',
        'ar': 'unit-converter-ar.html'
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
    <h1>Unit Converter — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="unit-converter-en.html">English</a></li>
      <li><a href="unit-converter-fr.html">Français</a></li>
      <li><a href="unit-converter-es.html">Español</a></li>
      <li><a href="unit-converter-de.html">Deutsch</a></li>
      <li><a href="unit-converter-ru.html">Русский</a></li>
      <li><a href="unit-converter-el.html">Ελληνικά</a></li>
      <li><a href="unit-converter-ar.html">العربية</a></li>
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
        data["howto"].setdefault("back_link", f"unit-converter-{code}.html")
        data["tips"].setdefault("back_link", f"unit-converter-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"unit-converter-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"unit-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["howto"], "howto"))

        tips_path = os.path.join(OUTPUT_DIR, f"unit-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["tips"], "tips"))

    redirect_path = os.path.join(OUTPUT_DIR, "unit-converter.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        with open("unit-converter.html", "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('unit-converter.html')}'.")

def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)

if __name__ == "__main__":
    main()