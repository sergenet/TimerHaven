import os
import json

base_dir = r"C:\TimerHavenWebsite\timerhaven-extension\_locales"

translations = {
    "en": {
        "extName": {"message": "TimerHaven Productivity Hub"},
        "extDesc": {"message": "Quick access to your favorite timers, stopwatches, and productivity tools from TimerHaven."},
        "timer": {"message": "Timer"},
        "stopwatch": {"message": "Stopwatch"},
        "pomodoro": {"message": "Pomodoro"},
        "clips": {"message": "Clips"},
        "launchBtn": {"message": "Launch Web Tools"}
    },
    "es": {
        "extName": {"message": "Centro de Productividad TimerHaven"},
        "extDesc": {"message": "Acceso rápido a tus temporizadores, cronómetros y herramientas de productividad favoritas de TimerHaven."},
        "timer": {"message": "Temporizador"},
        "stopwatch": {"message": "Cronómetro"},
        "pomodoro": {"message": "Pomodoro"},
        "clips": {"message": "Clips"},
        "launchBtn": {"message": "Abrir herramientas web"}
    },
    "fr": {
        "extName": {"message": "Centre de Productivité TimerHaven"},
        "extDesc": {"message": "Accès rapide à vos minuteurs, chronomètres et outils de productivité préférés de TimerHaven."},
        "timer": {"message": "Minuteur"},
        "stopwatch": {"message": "Chronomètre"},
        "pomodoro": {"message": "Pomodoro"},
        "clips": {"message": "Presse-papiers"},
        "launchBtn": {"message": "Lancer les outils web"}
    },
    "de": {
        "extName": {"message": "TimerHaven Produktivitäts-Hub"},
        "extDesc": {"message": "Schneller Zugriff auf Ihre Lieblings-Timer, Stoppuhren und Produktivitäts-Tools von TimerHaven."},
        "timer": {"message": "Timer"},
        "stopwatch": {"message": "Stoppuhr"},
        "pomodoro": {"message": "Pomodoro"},
        "clips": {"message": "Ablagen"},
        "launchBtn": {"message": "Web-Tools starten"}
    },
    "ru": {
        "extName": {"message": "Центр продуктивности TimerHaven"},
        "extDesc": {"message": "Быстрый доступ к вашим любимым таймерам, секундомерам и инструментам продуктивности от TimerHaven."},
        "timer": {"message": "Таймер"},
        "stopwatch": {"message": "Секундомер"},
        "pomodoro": {"message": "Помодоро"},
        "clips": {"message": "Буфер"},
        "launchBtn": {"message": "Запустить веб-инструменты"}
    },
    "el": {
        "extName": {"message": "Κέντρο Παραγωγικότητας TimerHaven"},
        "extDesc": {"message": "Γρήγορη πρόσβαση στα αγαπημένα σας χρονόμετρα, χρονόμετρα αντίστροφης μέτρησης και εργαλεία παραγωγικότητας από το TimerHaven."},
        "timer": {"message": "Χρονόμετρο"},
        "stopwatch": {"message": "Χρονόμετρο"},
        "pomodoro": {"message": "Pomodoro"},
        "clips": {"message": "Πρόχειρο"},
        "launchBtn": {"message": "Εκκίνηση εργαλείων ιστού"}
    },
    "ar": {
        "extName": {"message": "مركز إنتاجية TimerHaven"},
        "extDesc": {"message": "وصول سريع إلى المؤقتات المفضلة لديك وساعات الإيقاف وأدوات الإنتاجية من TimerHaven."},
        "timer": {"message": "المؤقت"},
        "stopwatch": {"message": "ساعة التوقيف"},
        "pomodoro": {"message": "بومودورو"},
        "clips": {"message": "قصاصات"},
        "launchBtn": {"message": "إطلاق أدوات الويب"}
    }
}

os.makedirs(base_dir, exist_ok=True)

for lang, messages in translations.items():
    lang_dir = os.path.join(base_dir, lang)
    os.makedirs(lang_dir, exist_ok=True)
    file_path = os.path.join(lang_dir, 'messages.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

print("Generated _locales directory structure and messages.json files successfully.")
