#!/usr/bin/env python3
"""Generate store.config.json from one source of truth for the App Store listing.

Editing the listing copy happens here and only here. The generated
store.config.json is what `eas metadata:push` uploads to App Store Connect, and
it is committed so the repo always shows exactly what the stores should serve.

Why store.config.json instead of fastlane folders: this app ships through EAS,
so `eas metadata:push` is the publish route (it validates the same limits Apple
enforces before it sends anything). The rest of store.config.json — categories,
advisory answers, the version — is preserved untouched; only `apple.info` is
rewritten, because that is the part this script owns.

Run: python tools/write_store_listings.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "store.config.json")

# App Store Connect language codes, in the order the script writes them.
# ar-SA and el are the codes App Store Connect uses for Arabic and Greek.
LISTINGS = {
    "en-US": {
        "title": "TimerHaven: Focus & Timers",
        "subtitle": "15 tools, offline and private",
        "description": """TimerHaven puts 15 productivity tools in one app — no account, no ads, no subscription.

POMODORO & TIMERS
• Pomodoro timer with adjustable work and break intervals
• Countdown timer for the kitchen, exams and deadlines
• Stopwatch with laps
• Task timer for focused work blocks

PLANNING & FOCUS
• Calendar with a note for every day
• Habit tracker for your daily routines
• Meeting planner across time zones
• Focus music for deep work
• Notes that save as you type

EVERYDAY
• World clock for many cities
• Currency converter
• Unit converter
• Password generator
• Clipboard history
• Weather for where you are

WORKS OFFLINE
Every tool runs on your device, so timers, notes and habits keep working with no connection at all.

PRIVATE BY DESIGN
No sign-up and no profile. Your notes, habits and calendar stay on your device, and nothing is tracked.

FIFTEEN TOOLS, ONE APP
Pomodoro, countdown, stopwatch, task timer, calendar, habits, meeting planner, focus music, notes, world clock, currency, units, passwords, clipboard, weather.

Free, with every feature included.""",
        "keywords": [
            "pomodoro", "countdown", "stopwatch", "interval", "study",
            "adhd", "productivity", "flow", "habit", "clock",
            "alarm", "task", "lap", "rest",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "de-DE": {
        "title": "TimerHaven: Timer & Fokus",
        "subtitle": "15 Tools, offline, ohne Konto",
        "description": """TimerHaven bündelt 15 Produktivitätswerkzeuge in einer App – ohne Konto, ohne Werbung, ohne Abo.

POMODORO & TIMER
• Pomodoro-Timer mit einstellbaren Arbeits- und Pausenzeiten
• Countdown für Küche, Prüfungen und Deadlines
• Stoppuhr mit Rundenzeiten
• Aufgaben-Timer für konzentrierte Arbeitsblöcke

PLANUNG & FOKUS
• Kalender mit einer Notiz zu jedem Tag
• Gewohnheits-Tracker für deine täglichen Routinen
• Besprechungsplaner über mehrere Zeitzonen
• Fokus-Musik für konzentriertes Arbeiten
• Notizen, die beim Tippen speichern

ALLTAG
• Weltzeituhr für viele Städte
• Währungsumrechner
• Einheitenrechner
• Passwort-Generator
• Zwischenablage-Verlauf
• Wetter für deinen Standort

FUNKTIONIERT OFFLINE
Alle Werkzeuge laufen auf deinem Gerät – Timer, Notizen und Gewohnheiten funktionieren auch ohne Verbindung.

PRIVAT DURCH KONZEPT
Keine Anmeldung, kein Profil. Notizen, Gewohnheiten und Kalender bleiben auf deinem Gerät, und nichts wird getrackt.

FÜNFZEHN WERKZEUGE, EINE APP
Pomodoro, Countdown, Stoppuhr, Aufgaben-Timer, Kalender, Gewohnheiten, Besprechungsplaner, Fokus-Musik, Notizen, Weltzeituhr, Währung, Einheiten, Passwörter, Zwischenablage, Wetter.

Kostenlos, mit allen Funktionen.""",
        "keywords": [
            "pomodoro", "timer", "countdown", "stoppuhr", "weltzeituhr",
            "gewohnheiten", "notizen", "fokus",
        ],
        # There is no localized contact page; the English one is the only live one.
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/de/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "es-ES": {
        "title": "TimerHaven: Temporizadores",
        "subtitle": "15 herramientas, sin cuenta",
        "description": """TimerHaven reúne 15 herramientas de productividad en una sola app: sin cuenta, sin anuncios y sin suscripción.

POMODORO Y TEMPORIZADORES
• Temporizador Pomodoro con intervalos de trabajo y descanso ajustables
• Cuenta atrás para la cocina, exámenes y entregas
• Cronómetro con vueltas
• Temporizador de tareas para bloques de concentración

ORGANIZACIÓN Y CONCENTRACIÓN
• Calendario con una nota para cada día
• Seguimiento de hábitos para tus rutinas
• Planificador de reuniones en varias zonas horarias
• Música para concentrarte
• Notas que se guardan mientras escribes

DÍA A DÍA
• Reloj mundial de muchas ciudades
• Conversor de divisas
• Conversor de unidades
• Generador de contraseñas
• Historial del portapapeles
• Clima de tu ubicación

FUNCIONA SIN CONEXIÓN
Todas las herramientas se ejecutan en tu dispositivo: los temporizadores, las notas y los hábitos siguen funcionando sin conexión.

PRIVADA POR DISEÑO
Sin registro y sin perfil. Tus notas, hábitos y calendario se quedan en tu dispositivo y no se rastrea nada.

QUINCE HERRAMIENTAS, UNA APP
Pomodoro, cuenta atrás, cronómetro, temporizador de tareas, calendario, hábitos, planificador de reuniones, música, notas, reloj mundial, divisas, unidades, contraseñas, portapapeles, clima.

Gratis, con todas las funciones incluidas.""",
        "keywords": [
            "pomodoro", "temporizador", "cuenta atrás", "cronómetro",
            "reloj mundial", "hábitos", "notas",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/es/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "fr-FR": {
        "title": "TimerHaven : minuteurs",
        "subtitle": "15 outils, sans compte",
        "description": """TimerHaven réunit 15 outils de productivité dans une seule application — sans compte, sans publicité, sans abonnement.

POMODORO ET MINUTEURS
• Minuteur Pomodoro avec intervalles de travail et de pause réglables
• Compte à rebours pour la cuisine, les examens et les échéances
• Chronomètre avec temps au tour
• Minuteur de tâches pour les sessions de travail concentré

ORGANISATION ET CONCENTRATION
• Calendrier avec une note pour chaque jour
• Suivi des habitudes pour votre routine quotidienne
• Planificateur de réunions sur plusieurs fuseaux horaires
• Musique de concentration pour le travail en profondeur
• Prise de notes enregistrée au fur et à mesure de la saisie

AU QUOTIDIEN
• Horloge mondiale pour de nombreuses villes
• Convertisseur de devises
• Convertisseur d'unités
• Générateur de mots de passe
• Historique du presse-papiers
• Météo pour votre position

FONCTIONNE HORS LIGNE
Tous les outils fonctionnent sur votre appareil — minuteurs, notes et habitudes restent utilisables sans connexion.

CONÇU POUR LA CONFIDENTIALITÉ
Aucune inscription, aucun profil. Vos notes, habitudes et calendrier restent sur votre appareil ; rien n'est suivi.

QUINZE OUTILS, UNE APPLICATION
Pomodoro, compte à rebours, chronomètre, minuteur de tâches, calendrier, habitudes, planificateur de réunions, musique, notes, horloge mondiale, devises, unités, mots de passe, presse-papiers, météo.

Gratuit, avec toutes les fonctionnalités incluses.""",
        "keywords": [
            "pomodoro", "minuteur", "compte à rebours", "chronomètre",
            "horloge mondiale", "habitudes", "notes",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/fr/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "ru": {
        "title": "TimerHaven: таймеры",
        "subtitle": "15 инструментов без аккаунта",
        "description": """TimerHaven объединяет 15 инструментов продуктивности в одном приложении — без учетной записи, без рекламы и без подписки.

ПОМОДОРО И ТАЙМЕРЫ
• Таймер Помодоро с настройкой интервалов работы и отдыха
• Таймер обратного отсчета для кухни, экзаменов и дедлайнов
• Секундомер с кругами
• Таймер задач для сфокусированной работы

ПЛАНИРОВАНИЕ И ФОКУС
• Календарь с заметкой на каждый день
• Трекер привычек для ежедневной рутины
• Планировщик встреч для разных часовых поясов
• Фоновая музыка для глубокой концентрации
• Заметки, которые сохраняются сразу при вводе

НА КАЖДЫЙ ДЕНЬ
• Мировое время для множества городов
• Конвертер валют
• Конвертер единиц
• Генератор паролей
• История буфера обмена
• Погода для вашего местоположения

РАБОТАЕТ ОФЛАЙН
Все инструменты запускаются на вашем устройстве, поэтому таймеры, заметки и привычки работают без интернета.

КОНФИДЕНЦИАЛЬНОСТЬ
Без регистрации и профилей. Ваши заметки, привычки и календарь остаются только на вашем устройстве, ничего не отслеживается.

15 ИНСТРУМЕНТОВ В ОДНОМ ПРИЛОЖЕНИИ
Помодоро, обратный отсчет, секундомер, таймер задач, календарь, привычки, планировщик встреч, музыка, заметки, мировое время, валюты, единицы, пароли, буфер обмена, погода.

Бесплатно, со всеми включенными функциями.""",
        "keywords": [
            "помодоро", "таймер", "секундомер", "мировое время",
            "привычки", "заметки", "фокус",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/ru/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "ar-SA": {
        "title": "TimerHaven: مؤقتات",
        "subtitle": "15 أداة دون حساب",
        "description": """يجمع TimerHaven خمس عشرة أداة إنتاجية في تطبيق واحد — دون حساب أو إعلانات أو اشتراك.

بومودورو والمؤقتات
• مؤقت بومودورو بمدد عمل وراحة قابلة للتعديل
• مؤقت عد تنازلي للمطبخ والاختبارات والمواعيد النهائية
• ساعة إيقاف مع الدورات
• مؤقت المهام لجلسات التركيز

التنظيم والتركيز
• تقويم مع ملاحظة لكل يوم
• متتبع العادات لروتينك اليومي
• مخطط اجتماعات عبر مناطق زمنية متعددة
• موسيقى التركيز للعمل العميق
• ملاحظات تُحفظ أثناء الكتابة

الاستخدام اليومي
• ساعة عالمية لمدن كثيرة
• محول العملات
• محول الوحدات
• مولد كلمات المرور
• سجل الحافظة
• الطقس لموقعك

يعمل دون اتصال
كل الأدوات تعمل على جهازك، لذا تستمر المؤقتات والملاحظات والعادات في العمل بلا اتصال.

خصوصية بالتصميم
دون تسجيل ودون ملف شخصي. تبقى ملاحظاتك وعاداتك وتقويمك على جهازك، ولا يتم تتبع أي شيء.

خمس عشرة أداة في تطبيق واحد
بومودورو، عد تنازلي، ساعة إيقاف، مؤقت مهام، تقويم، عادات، مخطط اجتماعات، موسيقى، ملاحظات، ساعة عالمية، عملات، وحدات، كلمات مرور، حافظة، طقس.

مجاني، وكل الميزات مشمولة.""",
        "keywords": [
            "بومودورو", "مؤقت", "ساعة إيقاف", "ساعة عالمية",
            "عادات", "ملاحظات", "تركيز",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/ar/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
    "el": {
        "title": "TimerHaven: Χρονόμετρα",
        "subtitle": "15 εργαλεία χωρίς λογαριασμό",
        "description": """Το TimerHaven συγκεντρώνει 15 εργαλεία παραγωγικότητας σε μία εφαρμογή — χωρίς λογαριασμό, διαφημίσεις ή συνδρομή.

POMODORO ΚΑΙ ΧΡΟΝΟΜΕΤΡΑ
• Χρονόμετρο Pomodoro με ρυθμιζόμενα διαστήματα εργασίας και διαλείμματος
• Αντίστροφη μέτρηση για κουζίνα, εξετάσεις και προθεσμίες
• Χρονόμετρο με γύρους
• Χρονόμετρο εργασιών για συγκεντρωμένη δουλειά

ΟΡΓΑΝΩΣΗ ΚΑΙ ΣΥΓΚΕΝΤΡΩΣΗ
• Ημερολόγιο με σημείωση για κάθε ημέρα
• Παρακολούθηση συνηθειών για την καθημερινή σου ρουτίνα
• Προγραμματισμός συναντήσεων σε ζώνες ώρας
• Μουσική συγκέντρωσης
• Σημειώσεις που αποθηκεύονται καθώς γράφεις

ΚΑΘΗΜΕΡΙΝΑ
• Παγκόσμιο ρολόι για πολλές πόλεις
• Μετατροπέας νομισμάτων
• Μετατροπέας μονάδων
• Γεννήτρια κωδικών
• Ιστορικό προχείρου
• Καιρός για την περιοχή σου

ΛΕΙΤΟΥΡΓΕΙ ΧΩΡΙΣ ΣΥΝΔΕΣΗ
Όλα τα εργαλεία εκτελούνται στη συσκευή σου, οπότε χρονόμετρα, σημειώσεις και συνήθειες δουλεύουν και χωρίς σύνδεση.

ΙΔΙΩΤΙΚΟΤΗΤΑ ΕΞ ΑΡΧΗΣ
Χωρίς εγγραφή και χωρίς προφίλ. Οι σημειώσεις, οι συνήθειες και το ημερολόγιό σου μένουν στη συσκευή σου και τίποτα δεν παρακολουθείται.

ΔΕΚΑΠΕΝΤΕ ΕΡΓΑΛΕΙΑ, ΜΙΑ ΕΦΑΡΜΟΓΗ
Pomodoro, αντίστροφη μέτρηση, χρονόμετρο, χρονόμετρο εργασιών, ημερολόγιο, συνήθειες, προγραμματισμός συναντήσεων, μουσική, σημειώσεις, παγκόσμιο ρολόι, νομίσματα, μονάδες, κωδικοί, πρόχειρο, καιρός.

Δωρεάν, με όλες τις λειτουργίες.""",
        "keywords": [
            "πομοντόρο", "χρονόμετρο", "αντίστροφη μέτρηση",
            "παγκόσμιο ρολόι", "συνήθειες", "σημειώσεις",
        ],
        "supportUrl": "https://timerhaven.com/contact.html",
        "marketingUrl": "https://timerhaven.com/el/",
        "privacyPolicyUrl": "https://timerhaven.com/app-privacy.html",
    },
}

# Apple's documented maxima. Keywords are a list on disk but Apple joins them
# with commas into one 100-character field, which is the limit that matters.
LIMITS = {"title": 30, "subtitle": 30, "description": 4000, "promoText": 170}
KEYWORDS_TOTAL = 100
KEYWORD_ITEM = 100
URL_FIELDS = ("marketingUrl", "supportUrl", "privacyPolicyUrl")

# Copy that belongs to the other store must never reach this file.
FORBIDDEN = ("android", "google play", "play store", "widget", "home screen shortcut")


def validate(locale, data):
    """Return the problems with one locale's copy; empty means it is publishable."""
    problems = []
    for field, limit in LIMITS.items():
        if field not in data:
            continue
        text = data[field]
        if text != text.strip():
            problems.append("%s/%s: leading or trailing whitespace" % (locale, field))
        if len(text) > limit:
            problems.append("%s/%s: %d chars over %d" % (locale, field, len(text), limit))
    for field in ("title", "subtitle", "description"):
        if not data.get(field):
            problems.append("%s/%s: missing" % (locale, field))

    keywords = data.get("keywords") or []
    if not keywords:
        problems.append("%s/keywords: missing" % locale)
    seen = set()
    for word in keywords:
        if not word or word != word.strip():
            problems.append("%s/keywords: empty or padded item %r" % (locale, word))
            continue
        if len(word) > KEYWORD_ITEM:
            problems.append("%s/keywords: %r over %d chars" % (locale, word, KEYWORD_ITEM))
        if word.lower() in seen:
            problems.append("%s/keywords: duplicate %r" % (locale, word))
        seen.add(word.lower())
    joined = len(",".join(keywords))
    if joined > KEYWORDS_TOTAL:
        problems.append("%s/keywords: %d chars over %d" % (locale, joined, KEYWORDS_TOTAL))

    haystack = " ".join([data.get("title", ""), data.get("subtitle", ""),
                         data.get("description", "")]).lower()
    for phrase in FORBIDDEN:
        if phrase in haystack:
            problems.append("%s: copy mentions %r, which belongs to the Play listing"
                            % (locale, phrase))
    return problems


def main():
    failures = []
    info = {}
    for locale, data in LISTINGS.items():
        failures.extend(validate(locale, data))
        info[locale] = {key: value for key, value in data.items() if value}
        print("%-6s title %d, subtitle %d, description %d, keywords %d"
              % (locale, len(data["title"]), len(data["subtitle"]),
                 len(data["description"]), len(",".join(data["keywords"]))))

    if failures:
        raise SystemExit("over limit: " + "; ".join(failures))

    config = {}
    if os.path.exists(CONFIG):
        with io.open(CONFIG, encoding="utf-8") as handle:
            try:
                config = json.load(handle)
            except ValueError as error:
                raise SystemExit("%s is not valid JSON (%s); fix or remove it first"
                                 % (os.path.basename(CONFIG), error))
    config["configVersion"] = config.get("configVersion", 0)
    apple = config.setdefault("apple", {})
    # Categories, advisory answers and the version are owned by the store, not
    # by this script, so they survive the rewrite untouched.
    apple["info"] = info

    with io.open(CONFIG, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print("wrote %s: %d locales within App Store limits"
          % (os.path.basename(CONFIG), len(info)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
