try:  # local credentials file, never committed
    from _secrets import FTP_PASS
except ImportError:  # fall back to the environment
    import os
    FTP_PASS = os.environ.get('TH_FTP_PASS', '')
"""Give each translated homepage its own language-specific title and description.

The translated index pages were inheriting the English <title>, so all of them
competed for one search result. This fetches the live copy of each page, swaps
the title/description/social tags for translated text, and uploads it back
byte-for-byte identical apart from those tags.
"""

import ftplib
import io
import re
import urllib.request

HOST = "ftp.timerhaven.com"
USER = "contact@timerhaven.com"
PASSWORD = FTP_PASS
ORIGIN = "https://timerhaven.com"

ENGLISH_TITLE = "TimerHaven | Free Productivity Tools, Clocks, & Timers"
ENGLISH_DESC = (
    "TimerHaven offers free world clocks, countdown timers, alarms, stopwatches, "
    "Pomodoro, weather, and currency tools. Boost your productivity with TimerHaven!"
)
ENGLISH_SOCIAL = "Master your focus with TimerHaven's free productivity tools."

LOCALES = {
    "fr": {
        "title": "TimerHaven | Minuteurs, horloges et outils de productivité gratuits",
        "desc": "TimerHaven réunit horloges mondiales, minuteurs, alarmes, chronomètres, Pomodoro, météo et devises, gratuitement. Gagnez en concentration sans créer de compte.",
        "social": "Concentrez-vous avec les outils de productivité gratuits de TimerHaven.",
    },
    "es": {
        "title": "TimerHaven | Temporizadores, relojes y herramientas de productividad gratis",
        "desc": "TimerHaven reúne relojes mundiales, temporizadores, alarmas, cronómetros, Pomodoro, clima y divisas, gratis. Mejora tu concentración sin crear una cuenta.",
        "social": "Concéntrate con las herramientas de productividad gratuitas de TimerHaven.",
    },
    "de": {
        "title": "TimerHaven | Kostenlose Timer, Weltuhren und Produktivitätstools",
        "desc": "TimerHaven bündelt Weltuhren, Timer, Alarme, Stoppuhren, Pomodoro, Wetter und Währungen kostenlos. Mehr Fokus, ohne ein Konto anzulegen.",
        "social": "Mehr Fokus mit den kostenlosen Produktivitätstools von TimerHaven.",
    },
    "ru": {
        "title": "TimerHaven | Бесплатные таймеры, мировые часы и инструменты продуктивности",
        "desc": "TimerHaven объединяет мировые часы, таймеры, будильники, секундомеры, Помодоро, погоду и валюты бесплатно. Больше собранности без регистрации.",
        "social": "Собранность с бесплатными инструментами продуктивности TimerHaven.",
    },
    "el": {
        "title": "TimerHaven | Δωρεάν χρονόμετρα, παγκόσμια ρολόγια και εργαλεία παραγωγικότητας",
        "desc": "Το TimerHaven συγκεντρώνει παγκόσμια ρολόγια, χρονόμετρα, ξυπνητήρια, Πομόδορο, καιρό και νομίσματα δωρεάν. Περισσότερη συγκέντρωση χωρίς λογαριασμό.",
        "social": "Περισσότερη συγκέντρωση με τα δωρεάν εργαλεία παραγωγικότητας του TimerHaven.",
    },
    "ar": {
        "title": "TimerHaven | مؤقتات وساعات عالمية وأدوات إنتاجية مجانية",
        "desc": "يجمع TimerHaven الساعات العالمية والمؤقتات والمنبهات وساعات الإيقاف وبومودورو والطقس والعملات مجانًا. زد تركيزك دون إنشاء حساب.",
        "social": "زد تركيزك مع أدوات الإنتاجية المجانية من TimerHaven.",
    },
}


def escape(value):
    return value.replace("&", "&amp;").replace('"', "&quot;")


def patch(html, locale):
    text = LOCALES[locale]
    html = re.sub(
        r"<title id=\"page-title\">[^<]*</title>",
        f'<title id="page-title">{escape(text["title"])}</title>',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="description"\s+content="[^"]*"\s*/?>',
        f'<meta name="description" content="{escape(text["desc"])}">',
        html,
        count=1,
    )
    for attr in ("property=\"og:title\"", "name=\"twitter:title\""):
        html = html.replace(
            f'<meta {attr} content="{ENGLISH_TITLE}">',
            f'<meta {attr} content="{escape(text["title"])}">',
        )
    for attr in ("property=\"og:description\"", "name=\"twitter:description\""):
        html = html.replace(
            f'<meta {attr} content="{ENGLISH_SOCIAL}">',
            f'<meta {attr} content="{escape(text["social"])}">',
        )
    return html


def main():
    ftp = ftplib.FTP(HOST, timeout=60)
    ftp.login(USER, PASSWORD)
    ftp.set_pasv(True)
    try:
        for locale, text in LOCALES.items():
            name = f"index-{locale}.html"
            with urllib.request.urlopen(f"{ORIGIN}/{name}", timeout=30) as response:
                original = response.read().decode("utf-8")

            updated = patch(original, locale)
            if updated == original:
                print(f"{name}: no change made — check the tag patterns")
                continue

            # Prove the title is gone from the English set before uploading.
            still_english = ENGLISH_TITLE in updated
            ftp.storbinary(f"STOR {name}", io.BytesIO(updated.encode("utf-8")))
            print(f"{name}: uploaded ({len(updated)} bytes), english title remains: {still_english}")
    finally:
        ftp.quit()


if __name__ == "__main__":
    main()
