#!/usr/bin/env python3
"""Write the Play Store listing copy for the six site languages.

Layout matches the fastlane convention so the files can be pasted into the Play
Console (or uploaded with supply) without reformatting:

    fastlane/metadata/android/<locale>/title.txt
    fastlane/metadata/android/<locale>/short_description.txt
    fastlane/metadata/android/<locale>/full_description.txt
"""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "fastlane", "metadata", "android")

LISTINGS = {
    "de": {
        "title": "TimerHaven: Timer & Fokus",
        "short": "Pomodoro, Countdown, Weltzeit, Notizen u. mehr: 15 kostenlose Tools in 1 App.",
        "full": """TimerHaven bündelt 15 Produktivitätswerkzeuge in einer App – ohne Konto, ohne Abo.

POMODORO & TIMER
• Pomodoro-Timer mit einstellbaren Arbeits- und Pausenintervallen
• Countdown-Timer für Küche, Prüfungen und Deadlines
• Stoppuhr mit Rundenzeiten
• Aufgaben-Timer für fokussierte Arbeitsblöcke

PLANUNG & FOKUS
• Kalender mit Notizen zu jedem Tag
• Gewohnheits-Tracker für deine täglichen Routinen
• Besprechungsplaner für mehrere Zeitzonen
• Fokus-Musik für konzentriertes Arbeiten
• Notizen mit automatischer Speicherung

ALLTAG
• Weltzeituhr für mehrere Städte
• Währungsumrechner
• Einheitenrechner
• Passwort-Generator
• Zwischenablage-Verlauf
• Wetter für deinen Standort

WAS NEU IST
• Hefte einzelne Tools als eigene Symbole auf den Startbildschirm – der Timer, den du nutzt, ohne die anderen 14.
• Neu: Pomodoro-Widget. Starte und pausiere eine Sitzung direkt vom Startbildschirm, und der Countdown läuft weiter, wenn die App geschlossen ist.
• Der Pomodoro-Timer läuft als Benachrichtigung weiter, damit du die Sitzung nicht aus den Augen verlierst.

Alle Tools funktionieren kostenlos. Die App finanziert sich über Werbung; ein einmaliger Kauf entfernt sie dauerhaft.

TimerHaven ist privat by design: keine Anmeldung, kein Profil, keine Weitergabe deiner Notizen.""",
    },
    "el": {
        "title": "TimerHaven: Χρονόμετρα",
        "short": "Pomodoro, αντίστροφη μέτρηση, παγκόσμιο ρολόι, σημειώσεις: 15 δωρεάν εργαλεία.",
        "full": """Το TimerHaven συγκεντρώνει 15 εργαλεία παραγωγικότητας σε μία εφαρμογή — χωρίς λογαριασμό και χωρίς συνδρομή.

POMODORO ΚΑΙ ΧΡΟΝΟΜΕΤΡΑ
• Χρονόμετρο Pomodoro με προσαρμόσιμα διαστήματα εργασίας και διαλείμματος
• Αντίστροφη μέτρηση για μαγείρεμα, εξετάσεις και προθεσμίες
• Χρονόμετρο με γύρους
• Χρονόμετρο εργασιών για συγκεντρωμένη δουλειά

ΟΡΓΑΝΩΣΗ ΚΑΙ ΣΥΓΚΕΝΤΡΩΣΗ
• Ημερολόγιο με σημειώσεις για κάθε ημέρα
• Παρακολούθηση συνηθειών
• Προγραμματισμός συναντήσεων σε πολλές ζώνες ώρας
• Μουσική συγκέντρωσης
• Σημειώσεις με αυτόματη αποθήκευση

ΚΑΘΗΜΕΡΙΝΑ
• Παγκόσμιο ρολόι
• Μετατροπέας νομισμάτων
• Μετατροπέας μονάδων
• Γεννήτρια κωδικών
• Ιστορικό προχείρου
• Καιρός για την περιοχή σου

ΤΙ ΝΕΟ ΥΠΑΡΧΕΙ
• Καρφίτσωσε μεμονωμένα εργαλεία στην αρχική οθόνη ως δικά τους εικονίδια — το χρονόμετρο που χρησιμοποιείς, χωρίς τα άλλα 14.
• Νέο widget Pomodoro: ξεκίνα ή παύσε μια συνεδρία από την αρχική οθόνη και η αντίστροφη μέτρηση συνεχίζεται με την εφαρμογή κλειστή.
• Ο χρονομετρητής Pomodoro συνεχίζει στην ειδοποίηση, ώστε να μη χάνεις τη συνεδρία.

Όλα τα εργαλεία είναι δωρεάν. Η εφαρμογή υποστηρίζεται από διαφημίσεις· μία αγορά τις αφαιρεί οριστικά.

Το TimerHaven σέβεται τα προσωπικά σου δεδομένα: χωρίς σύνδεση, χωρίς προφίλ, χωρίς κοινοποίηση των σημειώσεών σου.""",
    },
    "es": {
        "title": "TimerHaven: Temporizadores",
        "short": "Pomodoro, cuenta atrás, reloj mundial, notas y más: 15 herramientas gratis.",
        "full": """TimerHaven reúne 15 herramientas de productividad en una sola app, sin cuenta y sin suscripción.

POMODORO Y TEMPORIZADORES
• Temporizador Pomodoro con intervalos de trabajo y descanso personalizables
• Cuenta atrás para cocina, exámenes y entregas
• Cronómetro con vueltas
• Temporizador de tareas para bloques de concentración

ORGANIZACIÓN Y CONCENTRACIÓN
• Calendario con notas para cada día
• Seguimiento de hábitos
• Planificador de reuniones en varias zonas horarias
• Música para concentrarse
• Notas con guardado automático

DÍA A DÍA
• Reloj mundial
• Conversor de divisas
• Conversor de unidades
• Generador de contraseñas
• Historial del portapapeles
• Clima de tu ubicación

NOVEDADES
• Ancla herramientas sueltas a tu pantalla de inicio como iconos propios: el temporizador que usas, sin los otros 14.
• Nuevo widget de Pomodoro: inicia o pausa una sesión desde la pantalla de inicio y la cuenta atrás sigue con la app cerrada.
• El temporizador Pomodoro continúa en la notificación para que no pierdas la sesión.

Todas las herramientas son gratis. La app se financia con anuncios; una compra única los elimina para siempre.

TimerHaven es privado por diseño: sin registro, sin perfil y sin compartir tus notas.""",
    },
    "fr": {
        "title": "TimerHaven : minuteurs",
        "short": "Pomodoro, compte à rebours, horloge mondiale, notes : 15 outils gratuits.",
        "full": """TimerHaven réunit 15 outils de productivité dans une seule application, sans compte ni abonnement.

POMODORO ET MINUTEURS
• Minuteur Pomodoro avec durées de travail et de pause personnalisables
• Compte à rebours pour la cuisine, les examens et les échéances
• Chronomètre avec temps intermédiaires
• Minuteur de tâches pour les blocs de concentration

ORGANISATION ET CONCENTRATION
• Calendrier avec des notes pour chaque jour
• Suivi des habitudes
• Planificateur de réunions sur plusieurs fuseaux horaires
• Musique de concentration
• Notes enregistrées automatiquement

AU QUOTIDIEN
• Horloge mondiale
• Convertisseur de devises
• Convertisseur d'unités
• Générateur de mots de passe
• Historique du presse-papiers
• Météo de votre position

NOUVEAUTÉS
• Épinglez un outil sur votre écran d'accueil avec sa propre icône : le minuteur que vous utilisez, sans les 14 autres.
• Nouveau widget Pomodoro : lancez ou mettez en pause une session depuis l'écran d'accueil, le compte à rebours continue application fermée.
• Le minuteur Pomodoro reste visible dans la notification pour ne pas perdre le fil.

Tous les outils sont gratuits. L'application est financée par la publicité ; un achat unique les supprime définitivement.

TimerHaven respecte votre vie privée : pas d'inscription, pas de profil, vos notes restent chez vous.""",
    },
    "ru": {
        "title": "TimerHaven: таймеры",
        "short": "Pomodoro, таймер, мировое время, заметки и ещё 11 инструментов — бесплатно.",
        "full": """TimerHaven собирает 15 инструментов продуктивности в одном приложении — без аккаунта и подписки.

POMODORO И ТАЙМЕРЫ
• Таймер Pomodoro с настраиваемыми интервалами работы и отдыха
• Таймер обратного отсчёта для кухни, экзаменов и дедлайнов
• Секундомер с кругами
• Таймер задач для блоков концентрации

ПЛАНИРОВАНИЕ И ФОКУС
• Календарь с заметками на каждый день
• Трекер привычек
• Планировщик встреч в разных часовых поясах
• Музыка для концентрации
• Заметки с автосохранением

НА КАЖДЫЙ ДЕНЬ
• Мировое время
• Конвертер валют
• Конвертер единиц
• Генератор паролей
• История буфера обмена
• Погода для вашего местоположения

ЧТО НОВОГО
• Закрепляйте отдельные инструменты на главном экране как собственные значки: нужный таймер без остальных 14.
• Новый виджет Pomodoro: запускайте и приостанавливайте сессию с главного экрана — отсчёт продолжается при закрытом приложении.
• Таймер Pomodoro остаётся в уведомлении, чтобы сессия не потерялась.

Все инструменты бесплатны. Приложение живёт за счёт рекламы; разовая покупка убирает её навсегда.

TimerHaven уважает приватность: без регистрации, без профиля, заметки остаются у вас.""",
    },
    "ar": {
        "title": "TimerHaven: مؤقتات",
        "short": "بومودورو وعد تنازلي وساعة عالمية وملاحظات و11 أداة أخرى مجانًا.",
        "full": """يجمع TimerHaven خمس عشرة أداة إنتاجية في تطبيق واحد، دون حساب أو اشتراك.

بومودورو والمؤقتات
• مؤقت بومودورو بمدد عمل وراحة قابلة للتعديل
• مؤقت العد التنازلي للمطبخ والاختبارات والمواعيد النهائية
• ساعة إيقاف مع دورات
• مؤقت المهام لجلسات التركيز

التنظيم والتركيز
• تقويم مع ملاحظات لكل يوم
• متتبع العادات
• مخطط الاجتماعات عبر مناطق زمنية متعددة
• موسيقى التركيز
• ملاحظات تُحفظ تلقائيًا

الاستخدام اليومي
• ساعة العالم
• محول العملات
• محول الوحدات
• مولد كلمات المرور
• سجل الحافظة
• الطقس لموقعك

ما الجديد
• ثبّت أي أداة على الشاشة الرئيسية بأيقونة خاصة: المؤقت الذي تستخدمه دون الأدوات الأربع عشرة الأخرى.
• واجهة بومودورو جديدة: ابدأ الجلسة أو أوقفها من الشاشة الرئيسية، ويستمر العد حتى مع إغلاق التطبيق.
• يستمر مؤقت بومودورو في الإشعار حتى لا تفقد جلستك.

كل الأدوات مجانية. يعتمد التطبيق على الإعلانات، وشراء واحد يزيلها نهائيًا.

يحترم TimerHaven خصوصيتك: دون تسجيل أو ملف شخصي، وتبقى ملاحظاتك لديك.""",
    },
}

LIMITS = {"title": 30, "short_description": 80, "full_description": 4000}

failures = []
for locale, data in LISTINGS.items():
    folder = os.path.join(OUT, locale)
    os.makedirs(folder, exist_ok=True)
    for name, key in (
        ("title", "title"),
        ("short_description", "short"),
        ("full_description", "full"),
    ):
        text = data[key].strip()
        if len(text) > LIMITS[name]:
            failures.append(f"{locale}/{name}: {len(text)} chars over {LIMITS[name]}")
        with io.open(os.path.join(folder, name + ".txt"), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
    print(f"{locale}: title {len(data['title'])}, short {len(data['short'])}, full {len(data['full'])}")

if failures:
    raise SystemExit("over limit: " + "; ".join(failures))
print("all listings within Play limits")
