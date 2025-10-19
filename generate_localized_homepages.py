import os

LANGS = [
    ("en", "English"),
    ("fr", "Français"),
    ("es", "Español"),
    ("de", "Deutsch"),
    ("ru", "Русский"),
    ("el", "Ελληνικά"),
    ("ar", "العربية"),
]

home_content = {
    "en": {
        "title": "TimerHaven — Free Productivity Tools",
        "heading": "Welcome to TimerHaven",
        "desc": "Free, privacy-friendly tools for your productivity.",
        "notes_tool": "Notes",
        "notes_link": "notes-en.html",
        "notes_desc": "Quick notes, lists, reminders.",
        "footer": "&copy; 2025 TimerHaven. All tools are free and privacy-friendly.<br><a href=\"privacy.html\">Privacy Policy</a> &bull; <a href=\"terms.html\">Terms</a> &bull; <a href=\"contact.html\">Contact</a>",
    },
    "fr": {
        "title": "TimerHaven — Outils de productivité gratuits",
        "heading": "Bienvenue sur TimerHaven",
        "desc": "Des outils gratuits, respectueux de la vie privée, pour votre productivité.",
        "notes_tool": "Notes",
        "notes_link": "notes-fr.html",
        "notes_desc": "Notes rapides, listes, rappels.",
        "footer": "&copy; 2025 TimerHaven. Tous les outils sont gratuits et respectent votre vie privée.<br><a href=\"privacy.html\">Politique de confidentialité</a> &bull; <a href=\"terms.html\">Conditions</a> &bull; <a href=\"contact.html\">Contact</a>",
    },
    "es": {
        "title": "TimerHaven — Herramientas de productividad gratis",
        "heading": "Bienvenido a TimerHaven",
        "desc": "Herramientas gratuitas y privadas para tu productividad.",
        "notes_tool": "Notas",
        "notes_link": "notes-es.html",
        "notes_desc": "Notas rápidas, listas, recordatorios.",
        "footer": "&copy; 2025 TimerHaven. Todas las herramientas son gratuitas y respetuosas con la privacidad.<br><a href=\"privacy.html\">Política de privacidad</a> &bull; <a href=\"terms.html\">Términos</a> &bull; <a href=\"contact.html\">Contacto</a>",
    },
    "de": {
        "title": "TimerHaven — Gratis Produktivitäts-Tools",
        "heading": "Willkommen bei TimerHaven",
        "desc": "Kostenlose, datenschutzfreundliche Tools für Ihre Produktivität.",
        "notes_tool": "Notizen",
        "notes_link": "notes-de.html",
        "notes_desc": "Schnelle Notizen, Listen, Erinnerungen.",
        "footer": "&copy; 2025 TimerHaven. Alle Tools sind kostenlos und datenschutzfreundlich.<br><a href=\"privacy.html\">Datenschutz</a> &bull; <a href=\"terms.html\">Nutzungsbedingungen</a> &bull; <a href=\"contact.html\">Kontakt</a>",
    },
    "ru": {
        "title": "TimerHaven — Бесплатные инструменты продуктивности",
        "heading": "Добро пожаловать в TimerHaven",
        "desc": "Бесплатные и приватные инструменты для вашей продуктивности.",
        "notes_tool": "Заметки",
        "notes_link": "notes-ru.html",
        "notes_desc": "Быстрые заметки, списки, напоминания.",
        "footer": "&copy; 2025 TimerHaven. Все инструменты бесплатны и приватны.<br><a href=\"privacy.html\">Политика конфиденциальности</a> &bull; <a href=\"terms.html\">Условия</a> &bull; <a href=\"contact.html\">Контакт</a>",
    },
    "el": {
        "title": "TimerHaven — Δωρεάν εργαλεία παραγωγικότητας",
        "heading": "Καλώς ήρθατε στο TimerHaven",
        "desc": "Δωρεάν, φιλικά προς το απόρρητο εργαλεία για την παραγωγικότητά σας.",
        "notes_tool": "Σημειώσεις",
        "notes_link": "notes-el.html",
        "notes_desc": "Γρήγορες σημειώσεις, λίστες, υπενθυμίσεις.",
        "footer": "&copy; 2025 TimerHaven. Όλα τα εργαλεία είναι δωρεάν και φιλικά προς το απόρρητο.<br><a href=\"privacy.html\">Πολιτική απορρήτου</a> &bull; <a href=\"terms.html\">Όροι</a> &bull; <a href=\"contact.html\">Επικοινωνία</a>",
    },
    "ar": {
        "title": "TimerHaven — أدوات الإنتاجية المجانية",
        "heading": "مرحبًا بك في TimerHaven",
        "desc": "أدوات مجانية وتحترم الخصوصية لزيادة إنتاجيتك.",
        "notes_tool": "الملاحظات",
        "notes_link": "notes-ar.html",
        "notes_desc": "ملاحظات سريعة، قوائم، تذكيرات.",
        "footer": "&copy; 2025 TimerHaven. جميع الأدوات مجانية وتحترم الخصوصية.<br><a href=\"privacy.html\">سياسة الخصوصية</a> &bull; <a href=\"terms.html\">الشروط</a> &bull; <a href=\"contact.html\">اتصل بنا</a>",
    }
}

def homepage_html(lang, c):
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="UTF-8">
  <title>{c['title']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{c['desc']}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background: #f4f7fb; font-family: 'Montserrat', Arial, sans-serif; }}
    .container {{ max-width: 700px; margin: 2em auto; background: #fff; border-radius: 14px; box-shadow: 0 2px 12px #e0e7ef; padding: 2em; text-align: center; }}
    .tool-card {{ background: #f7fafc; border-radius: 12px; box-shadow: 0 2px 8px #e0e7ef; margin: 1em auto; padding: 1.5em; max-width: 360px; text-align: left; }}
    .tool-link {{ font-size: 1.1em; font-weight: bold; color: #185a9d; text-decoration: none; display: inline-block; margin-bottom: 0.5em; }}
    .tool-link:hover {{ color: #43cea2; text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="container">
    <h1 style="color:#185a9d;">{c['heading']}</h1>
    <p style="font-size:1.15em;">{c['desc']}</p>
    <div class="tool-card">
      <a href="{c['notes_link']}" class="tool-link"><i class="fa fa-note-sticky"></i> {c['notes_tool']}</a>
      <div style="color:#333;">{c['notes_desc']}</div>
    </div>
    <!-- Add more tools here if needed -->
  </div>
<footer style="text-align:center;margin:2em 0 1em 0;">
  {c['footer']}
</footer>
</body>
</html>
"""

def main():
    outdir = "localized_homepages"
    os.makedirs(outdir, exist_ok=True)
    for lang, _ in LANGS:
        with open(f"{outdir}/index-{lang}.html", "w", encoding="utf-8") as f:
            f.write(homepage_html(lang, home_content[lang]))
    print(f"All localized homepage files generated in ./{outdir}/")

if __name__ == "__main__":
    main()