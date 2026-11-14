#!/usr/bin/env python3
"""Generate the per-tool PWA assets for timerhaven.com.

Outputs:
  assets/icons/tool-<slug>-{192,512}.png   distinct icon per tool
  assets/icons/app-{192,512}.png           TimerHaven icon
  manifests/<slug>-<lang>.json             one installable app per tool + language
  manifests/home-<lang>.json               installable TimerHaven app

Then wires every tool page and home page to its manifest, the install stylesheet
and the install script. Safe to re-run: generated blocks are replaced, not
duplicated.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(ROOT, "assets", "icons")
MANIFEST_DIR = os.path.join(ROOT, "manifests")
LANGS = ["en", "de", "el", "es", "fr", "ru", "ar"]

BRAND = "#185a9d"

TOOLS = {
    "pomodoro": {
        "short": {"en": "Pomodoro", "de": "Pomodoro", "el": "Pomodoro", "es": "Pomodoro", "fr": "Pomodoro", "ru": "Pomodoro"},
        "names": {"en": "Pomodoro Timer", "de": "Pomodoro-Timer", "el": "Χρονόμετρο Pomodoro", "es": "Temporizador Pomodoro", "fr": "Minuteur Pomodoro", "ru": "Таймер Pomodoro"},
        "colors": ("#ef5350", "#b71c1c"),
    },
    "timer": {
        "short": {"en": "Task Timer", "de": "Aufgaben", "el": "Εργασίες", "es": "Tareas", "fr": "Tâches", "ru": "Задачи"},
        "names": {"en": "Task Timer", "de": "Aufgaben-Timer", "el": "Χρονόμετρο Εργασιών", "es": "Temporizador de tareas", "fr": "Minuteur de tâches", "ru": "Таймер задач"},
        "colors": ("#f59e0b", "#b45309"),
    },
    "countdown": {
        "short": {"en": "Countdown", "de": "Countdown", "el": "Αντίστροφη", "es": "Cuenta atrás", "fr": "Minuteur", "ru": "Таймер"},
        "names": {"en": "Countdown Timer", "de": "Countdown-Timer", "el": "Χρονόμετρο Αντίστροφης Μέτρησης", "es": "Temporizador de cuenta atrás", "fr": "Minuteur de compte à rebours", "ru": "Таймер обратного отсчёта"},
        "colors": ("#8b5cf6", "#5b21b6"),
    },
    "stopwatch": {
        "short": {"en": "Stopwatch", "de": "Stoppuhr", "el": "Χρονόμετρο", "es": "Cronómetro", "fr": "Chronomètre", "ru": "Секундомер"},
        "names": {"en": "Stopwatch", "de": "Stoppuhr", "el": "Χρονόμετρο", "es": "Cronómetro", "fr": "Chronomètre", "ru": "Секундомер"},
        "colors": ("#3b82f6", "#1e40af"),
    },
    "focus-music": {
        "short": {"en": "Focus Music", "de": "Fokus-Musik", "el": "Μουσική", "es": "Música", "fr": "Musique", "ru": "Музыка"},
        "names": {"en": "Focus Music", "de": "Fokus-Musik", "el": "Μουσική Συγκέντρωσης", "es": "Música para concentrarse", "fr": "Musique de concentration", "ru": "Музыка для фокуса"},
        "colors": ("#ec4899", "#9d174d"),
    },
    "habit-tracker": {
        "short": {"en": "Habits", "de": "Gewohnheiten", "el": "Συνήθειες", "es": "Hábitos", "fr": "Habitudes", "ru": "Привычки"},
        "names": {"en": "Habit Tracker", "de": "Gewohnheits-Tracker", "el": "Παρακολούθηση Συνηθειών", "es": "Seguimiento de hábitos", "fr": "Suivi des habitudes", "ru": "Трекер привычек"},
        "colors": ("#22c55e", "#15803d"),
    },
    "meeting-planner": {
        "short": {"en": "Meetings", "de": "Meetings", "el": "Συναντήσεις", "es": "Reuniones", "fr": "Réunions", "ru": "Встречи"},
        "names": {"en": "Meeting Planner", "de": "Meeting-Planer", "el": "Προγραμματισμός Συναντήσεων", "es": "Planificador de reuniones", "fr": "Planificateur de réunions", "ru": "Планировщик встреч"},
        "colors": ("#06b6d4", "#0e7490"),
    },
    "calendar": {
        "short": {"en": "Calendar", "de": "Kalender", "el": "Ημερολόγιο", "es": "Calendario", "fr": "Calendrier", "ru": "Календарь"},
        "names": {"en": "Calendar", "de": "Kalender", "el": "Ημερολόγιο", "es": "Calendario", "fr": "Calendrier", "ru": "Календарь"},
        "colors": ("#2563eb", "#1e3a8a"),
    },
    "notes": {
        "short": {"en": "Notes", "de": "Notizen", "el": "Σημειώσεις", "es": "Notas", "fr": "Notes", "ru": "Заметки"},
        "names": {"en": "Notes", "de": "Notizen", "el": "Σημειώσεις", "es": "Notas", "fr": "Notes", "ru": "Заметки"},
        "colors": ("#eab308", "#a16207"),
    },
    "world-clock": {
        "short": {"en": "World Clock", "de": "Weltzeit", "el": "Παγκόσμιο", "es": "Reloj mundial", "fr": "Horloge", "ru": "Мир. время"},
        "names": {"en": "World Clock", "de": "Weltzeituhr", "el": "Παγκόσμιο Ρολόι", "es": "Reloj mundial", "fr": "Horloge mondiale", "ru": "Мировое время"},
        "colors": ("#6366f1", "#3730a3"),
    },
    "password-generator": {
        "short": {"en": "Passwords", "de": "Passwörter", "el": "Κωδικοί", "es": "Contraseñas", "fr": "Mots de passe", "ru": "Пароли"},
        "names": {"en": "Password Generator", "de": "Passwort-Generator", "el": "Γεννήτρια Κωδικών", "es": "Generador de contraseñas", "fr": "Générateur de mots de passe", "ru": "Генератор паролей"},
        "colors": ("#64748b", "#334155"),
    },
    "unit-converter": {
        "short": {"en": "Units", "de": "Einheiten", "el": "Μονάδες", "es": "Unidades", "fr": "Unités", "ru": "Единицы"},
        "names": {"en": "Unit Converter", "de": "Einheitenrechner", "el": "Μετατροπέας Μονάδων", "es": "Conversor de unidades", "fr": "Convertisseur d'unités", "ru": "Конвертер единиц"},
        "colors": ("#14b8a6", "#0f766e"),
    },
    "currency": {
        "short": {"en": "Currency", "de": "Währung", "el": "Νομίσματα", "es": "Divisas", "fr": "Devises", "ru": "Валюты"},
        "names": {"en": "Currency Converter", "de": "Währungsrechner", "el": "Μετατροπέας Νομισμάτων", "es": "Conversor de divisas", "fr": "Convertisseur de devises", "ru": "Конвертер валют"},
        "colors": ("#16a34a", "#14532d"),
    },
    "clipboard-manager": {
        "short": {"en": "Clipboard", "de": "Zwischenablage", "el": "Πρόχειρο", "es": "Portapapeles", "fr": "Presse-papiers", "ru": "Буфер"},
        "names": {"en": "Clipboard Manager", "de": "Zwischenablage", "el": "Διαχειριστής Προχείρου", "es": "Portapapeles", "fr": "Presse-papiers", "ru": "Буфер обмена"},
        "colors": ("#d97706", "#92400e"),
    },
    "weather": {
        "short": {"en": "Weather", "de": "Wetter", "el": "Καιρός", "es": "Clima", "fr": "Météo", "ru": "Погода"},
        "names": {"en": "Weather", "de": "Wetter", "el": "Καιρός", "es": "Clima", "fr": "Météo", "ru": "Погода"},
        "colors": ("#0ea5e9", "#075985"),
    },
}

AR_NAMES = {
    "pomodoro": ("مؤقت بومودورو", "بومودورو"),
    "timer": ("مؤقت المهام", "المهام"),
    "countdown": ("مؤقت العد التنازلي", "عد تنازلي"),
    "stopwatch": ("ساعة إيقاف", "إيقاف"),
    "focus-music": ("موسيقى التركيز", "موسيقى"),
    "habit-tracker": ("متتبع العادات", "العادات"),
    "meeting-planner": ("مخطط الاجتماعات", "الاجتماعات"),
    "calendar": ("التقويم", "التقويم"),
    "notes": ("الملاحظات", "ملاحظات"),
    "world-clock": ("ساعة العالم", "العالم"),
    "password-generator": ("مولد كلمات المرور", "كلمات المرور"),
    "unit-converter": ("محول الوحدات", "الوحدات"),
    "currency": ("محول العملات", "العملات"),
    "clipboard-manager": ("مدير الحافظة", "الحافظة"),
    "weather": ("الطقس", "الطقس"),
}

DESC = {
    "ar": "{name} — أداة مجانية من TimerHaven. تفتح مباشرة وتعمل دون اتصال.",
    "en": "{name} — a free TimerHaven tool. Opens straight to {name}, works offline.",
    "de": "{name} – ein kostenloses TimerHaven-Tool. Öffnet direkt {name}, funktioniert offline.",
    "el": "{name} — δωρεάν εργαλείο του TimerHaven. Ανοίγει απευθείας, λειτουργεί εκτός σύνδεσης.",
    "es": "{name}: herramienta gratuita de TimerHaven. Se abre directamente y funciona sin conexión.",
    "fr": "{name} — outil gratuit de TimerHaven. S'ouvre directement et fonctionne hors ligne.",
    "ru": "{name} — бесплатный инструмент TimerHaven. Открывается сразу и работает офлайн.",
}

GLYPHS = {
    "pomodoro": """
      <circle cx="256" cy="276" r="118"/>
      <path d="M256 158c0-26 14-42 38-48"/>
      <path d="M256 158c-34-8-58 2-72 22 28 14 54 12 72-6"/>
      <path d="M256 158c18-18 44-20 72-6-14 20-38 30-72 22"/>""",
    "timer": """
      <circle cx="256" cy="272" r="118"/>
      <path d="M256 208v66l48 30"/>
      <path d="M214 120h84"/>
      <path d="M256 120v34"/>""",
    "countdown": """
      <path d="M186 148h140M186 372h140"/>
      <path d="M198 148c0 74 58 92 58 124 0 32-58 50-58 124"/>
      <path d="M314 148c0 74-58 92-58 124 0 32 58 50 58 124"/>""",
    "stopwatch": """
      <circle cx="256" cy="288" r="112"/>
      <path d="M256 288v-62"/>
      <path d="M256 176v-38"/>
      <path d="M226 138h60"/>
      <path d="M336 216l28-26"/>""",
    "focus-music": """
      <path d="M330 156v150a44 44 0 1 1-26-40"/>
      <path d="M330 156l-116 26"/>
      <path d="M214 182v150a44 44 0 1 1-26-40"/>""",
    "habit-tracker": """
      <circle cx="256" cy="270" r="116"/>
      <path d="M198 272l40 42 78-88"/>""",
    "meeting-planner": """
      <circle cx="196" cy="216" r="54"/>
      <path d="M120 372c0-46 34-76 76-76s76 30 76 76"/>
      <circle cx="336" cy="212" r="42"/>
      <path d="M296 372c4-40 30-64 62-64 30 0 54 22 62 56"/>""",
    "calendar": """
      <rect x="142" y="168" width="228" height="212" rx="24"/>
      <path d="M142 236h228"/>
      <path d="M196 140v48M316 140v48"/>
      <path d="M190 288h44M190 332h44M278 288h44"/>""",
    "notes": """
      <rect x="156" y="148" width="200" height="236" rx="20"/>
      <path d="M204 224h104M204 278h104M204 332h62"/>""",
    "world-clock": """
      <circle cx="256" cy="268" r="118"/>
      <ellipse cx="256" cy="268" rx="56" ry="118"/>
      <path d="M146 228h220M146 308h220"/>""",
    "password-generator": """
      <rect x="174" y="252" width="164" height="130" rx="24"/>
      <path d="M214 252v-34a42 42 0 0 1 84 0v34"/>
      <path d="M256 304v30"/>""",
    "unit-converter": """
      <path d="M148 206h196M306 172l40 34-40 34"/>
      <path d="M364 330H168M206 296l-40 34 40 34"/>""",
    "currency": """
      <circle cx="256" cy="268" r="116"/>
      <path d="M256 186v164"/>
      <path d="M298 218c0-22-20-32-42-32-24 0-42 12-42 32 0 38 84 24 84 62 0 20-18 32-42 32-22 0-42-10-42-32"/>""",
    "clipboard-manager": """
      <rect x="168" y="172" width="176" height="216" rx="20"/>
      <rect x="220" y="144" width="72" height="48" rx="16"/>
      <path d="M204 268h104M204 316h104M204 364h64"/>""",
    "weather": """
      <circle cx="192" cy="196" r="52"/>
      <path d="M192 118v-24M112 196H88M272 196h-24M136 140l-18-18M254 140l-16-16"/>
      <path d="M214 384h140a52 52 0 0 0 6-104 76 76 0 0 0-136-16 48 48 0 0 0-10 120z"/>""",
    "app": """
      <circle cx="256" cy="268" r="120"/>
      <path d="M256 200v68l52 32"/>
      <path d="M256 148v-22"/>""",
}


def svg(glyph, colors):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{colors[0]}"/><stop offset="1" stop-color="{colors[1]}"/>'
        '</linearGradient></defs>'
        '<rect width="512" height="512" fill="url(#g)"/>'
        '<g fill="none" stroke="#ffffff" stroke-width="26" stroke-linecap="round" '
        'stroke-linejoin="round" opacity="0.97">' + glyph + '</g></svg>'
    )


def render_icons():
    os.makedirs(ICON_DIR, exist_ok=True)
    jobs = [(slug, cfg["colors"]) for slug, cfg in TOOLS.items()]
    jobs.append(("app", ("#43cea2", "#185a9d")))
    for slug, colors in jobs:
        source = os.path.join(ICON_DIR, f".{slug}.svg")
        with open(source, "w", encoding="utf-8") as handle:
            handle.write(svg(GLYPHS[slug], colors))
        for size in (192, 512):
            target = os.path.join(ICON_DIR, f"{'tool-' if slug != 'app' else ''}{slug if slug != 'app' else 'app'}-{size}.png")
            subprocess.run(
                ["magick", source, "-resize", f"{size}x{size}", "-strip", target],
                check=True,
            )
        os.remove(source)
    print(f"icons: {len(jobs)} sets rendered")


def manifest(entry, lang, start_url, slug):
    if not entry:
        short = name = "TimerHaven"
    elif lang == "ar" and slug in AR_NAMES:
        name, short = AR_NAMES[slug]
    else:
        short = entry["short"][lang]
        name = entry["names"][lang]
    description = (DESC[lang].format(name=name) if entry
                   else "TimerHaven — timers, planners and focus tools in one app.")
    return {
        "id": f"/{slug if slug.startswith('home-') else slug + '-' + lang}/",
        "name": name,
        "short_name": short,
        "description": description,
        "lang": lang,
        "dir": "rtl" if lang == "ar" else "ltr",
        "start_url": start_url,
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "background_color": "#ffffff",
        "theme_color": BRAND,
        "categories": ["productivity", "utilities"],
        "icons": [
            {
                "src": f"/assets/icons/{'tool-' + slug if entry else 'app'}-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable",
            },
            {
                "src": f"/assets/icons/{'tool-' + slug if entry else 'app'}-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable",
            },
        ],
    }


def write_manifests():
    os.makedirs(MANIFEST_DIR, exist_ok=True)
    written = 0
    for slug, entry in TOOLS.items():
        for lang in LANGS:
            page = f"{slug}-{lang}.html"
            if not os.path.exists(os.path.join(ROOT, page)):
                continue
            data = manifest(entry, lang, f"/{page}", slug)
            path = os.path.join(MANIFEST_DIR, f"{slug}-{lang}.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2)
            written += 1
    home_langs = ["en", "de", "el", "es", "fr", "ru", "ar"]
    for lang in home_langs:
        page = "index.html" if lang == "en" else f"index-{lang}.html"
        if not os.path.exists(os.path.join(ROOT, page)):
            continue
        data = manifest(None, lang, f"/{page}", f"home-{lang}")
        data["name"] = "TimerHaven"
        with open(os.path.join(MANIFEST_DIR, f"home-{lang}.json"), "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
        written += 1
    print(f"manifests: {written} written")


def inject_targets():
    targets = []
    for slug in TOOLS:
        for lang in LANGS:
            page = f"{slug}-{lang}.html"
            if os.path.exists(os.path.join(ROOT, page)):
                targets.append((page, f"/manifests/{slug}-{lang}.json", slug, lang))
    # Language-detecting landing pages such as /pomodoro.html install the
    # English tool app, which is what that page shows by default.
    for slug in TOOLS:
        page = f"{slug}.html"
        if os.path.exists(os.path.join(ROOT, page)):
            targets.append((page, f"/manifests/{slug}-en.json", slug, "en"))
    for lang in ["en", "de", "el", "es", "fr", "ru", "ar"]:
        page = "index.html" if lang == "en" else f"index-{lang}.html"
        if os.path.exists(os.path.join(ROOT, page)):
            targets.append((page, f"/manifests/home-{lang}.json", "home", lang))
    return targets


HEAD_SNIPPET = (
    '<!-- th-pwa:begin -->\n'
    '  <link rel="manifest" href="{manifest}">\n'
    '  <meta name="theme-color" content="{brand}">\n'
    '  <link rel="apple-touch-icon" href="/assets/icons/app-192.png">\n'
    '  <link rel="stylesheet" href="/assets/css/install.css">\n'
    '  <!-- th-pwa:end -->'
)
BODY_SNIPPET = (
    '<!-- th-pwa:begin -->\n'
    '<script src="/assets/js/install.js" defer data-th-tool="{tool}" data-th-scheme="{manifest}"></script>\n'
    '<!-- th-pwa:end -->'
)


def inject():
    changed = 0
    for page, manifest_url, tool, _lang in inject_targets():
        path = os.path.join(ROOT, page)
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as handle:
            html = handle.read()
        original = html

        head_block = HEAD_SNIPPET.format(manifest=manifest_url, brand=BRAND)
        body_block = BODY_SNIPPET.format(tool=tool, manifest=manifest_url)

        # Replace earlier PWA blocks, then any stray manifest link.
        html = re.sub(r"<!-- th-pwa:begin -->.*?<!-- th-pwa:end -->", "", html, flags=re.S)
        html = re.sub(r'<link rel="manifest"[^>]*>\s*', "", html)
        html = re.sub(r'<link rel="stylesheet" href="/assets/css/install\.css">\s*', "", html)

        if "</head>" in html:
            html = html.replace("</head>", head_block + "\n</head>", 1)
        else:
            print(f"WARN no </head>: {page}", file=sys.stderr)
            continue

        if "</body>" in html:
            html = html.replace("</body>", body_block + "\n</body>", 1)
        else:
            html = html + "\n" + body_block + "\n"

        if html != original:
            with open(path, "w", encoding="utf-8", errors="surrogateescape") as handle:
                handle.write(html)
            changed += 1
    print(f"pages: {changed} updated")


if __name__ == "__main__":
    render_icons()
    write_manifests()
    inject()
