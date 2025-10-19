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

howto = {
    "en": {
        "title": "How to Use Notes — TimerHaven",
        "back": "Back to Notes",
        "back_icon": "arrow-left",
        "back_link": "notes-en.html",
        "h1": "How to Use Notes",
        "desc": "The <b>Notes</b> tool is designed for quick ideas, lists, and reminders. Here’s how to use it:",
        "steps_title": "Step-by-step Guide",
        "steps": [
            "<b>Add a note:</b> Type your text in the input box.",
            "<b>Save the note:</b> Click <b>Add Note</b> to add it to your list.",
            "<b>View notes:</b> All notes appear in the list below the form.",
            "<b>Delete notes:</b> Remove notes you no longer need.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Are notes saved after refresh?</b> Yes, until you clear your browser storage.",
            "<b>Can I add multiple notes?</b> Yes, as many as you wish.",
            "<b>Can I edit a note?</b> Not yet—delete and add a new note to update.",
        ],
        "tips_title": "Tips for Success",
        "tips": [
            "Use short notes for quick ideas or tasks.",
            "Delete old notes to stay organized.",
            "Use notes for reminders, lists, or important points.",
        ],
        "btn": "Back to Notes",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Privacy Policy</a> &bull; <a href=\"terms.html\">Terms</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "fr": {
        "title": "Comment utiliser les Notes — TimerHaven",
        "back": "Retour aux Notes",
        "back_icon": "arrow-left",
        "back_link": "notes-fr.html",
        "h1": "Comment utiliser les Notes",
        "desc": "L’outil <strong>Notes</strong> est conçu pour les idées rapides, les rappels et les listes. Voici comment l’utiliser :",
        "steps_title": "Guide étape par étape",
        "steps": [
            "<b>Écrivez votre note :</b> Saisissez votre texte dans la boîte prévue à cet effet.",
            "<b>Ajoutez la note :</b> Cliquez sur <strong>Ajouter une note</strong> pour l’enregistrer dans la liste.",
            "<b>Affichez vos notes :</b> Toutes vos notes apparaissent dans la liste sous le formulaire.",
            "<b>Supprimez les notes :</b> Retirez les notes inutiles grâce au bouton de suppression.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Les notes sont-elles sauvegardées après actualisation ?</b> Non, elles sont temporaires et locales au navigateur.",
            "<b>Puis-je ajouter plusieurs notes ?</b> Oui, autant que vous le souhaitez.",
            "<b>Puis-je modifier une note ?</b> Pas encore—supprimez et recréez-la pour la mettre à jour.",
        ],
        "tips_title": "Conseils pour réussir",
        "tips": [
            "Utilisez des notes courtes pour des idées ou tâches rapides.",
            "Supprimez régulièrement les anciennes notes pour rester organisé.",
            "Utilisez les notes pour des rappels, des listes ou des points importants.",
        ],
        "btn": "Retour aux Notes",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Politique de confidentialité</a> &bull; <a href=\"terms.html\">Conditions</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "es": {
        "title": "Cómo usar las Notas — TimerHaven",
        "back": "Volver a Notas",
        "back_icon": "arrow-left",
        "back_link": "notes-es.html",
        "h1": "Cómo usar las Notas",
        "desc": "La herramienta <strong>Notas</strong> está diseñada para pensamientos rápidos, recordatorios y listas. Así se utiliza:",
        "steps_title": "Guía paso a paso",
        "steps": [
            "<b>Escribe tu nota:</b> Ingresa tu texto en el campo correspondiente.",
            "<b>Agrega la nota:</b> Haz clic en <strong>Agregar Nota</strong> para guardarla en tu lista.",
            "<b>Visualiza las notas:</b> Todas tus notas aparecen en la lista debajo del formulario.",
            "<b>Elimina las notas:</b> Borra las notas que ya no necesites usando el botón de eliminar.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>¿Se guardan las notas tras refrescar?</b> No, son temporales y locales al navegador.",
            "<b>¿Puedo agregar varias notas?</b> Sí, tantas como desees.",
            "<b>¿Puedo editar notas?</b> Aún no—elimina y vuelve a añadir para actualizar.",
        ],
        "tips_title": "Consejos para el éxito",
        "tips": [
            "Utiliza notas cortas para ideas o tareas rápidas.",
            "Elimina notas regularmente para mantenerte organizado.",
            "Utiliza las notas para recordatorios, listas o puntos importantes.",
        ],
        "btn": "Volver a Notas",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Política de privacidad</a> &bull; <a href=\"terms.html\">Términos</a> &bull; <a href=\"contact.html\">Contacto</a>"
    },
    "de": {
        "title": "So nutzen Sie Notizen — TimerHaven",
        "back": "Zurück zu Notizen",
        "back_icon": "arrow-left",
        "back_link": "notes-de.html",
        "h1": "So nutzen Sie Notizen",
        "desc": "Das <strong>Notizen</strong>-Tool eignet sich für schnelle Gedanken, Erinnerungen und Listen. So funktioniert es:",
        "steps_title": "Schritt-für-Schritt-Anleitung",
        "steps": [
            "<b>Notiz eingeben:</b> Tragen Sie Ihren Text in das vorgesehene Feld ein.",
            "<b>Notiz hinzufügen:</b> Klicken Sie auf <strong>Notiz hinzufügen</strong>, um sie zu speichern.",
            "<b>Notizen anzeigen:</b> Alle Ihre Notizen erscheinen in der Liste unterhalb des Formulars.",
            "<b>Notizen löschen:</b> Entfernen Sie nicht mehr benötigte Notizen mit dem Löschen-Button.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Werden Notizen nach dem Aktualisieren gespeichert?</b> Nein, sie sind temporär und nur lokal im Browser.",
            "<b>Kann ich mehrere Notizen hinzufügen?</b> Ja, so viele Sie möchten.",
            "<b>Kann ich Notizen bearbeiten?</b> Noch nicht—löschen und neu hinzufügen zum Aktualisieren.",
        ],
        "tips_title": "Tipps für den Erfolg",
        "tips": [
            "Verwenden Sie kurze Notizen für schnelle Ideen oder Aufgaben.",
            "Löschen Sie regelmäßig alte Notizen, um organisiert zu bleiben.",
            "Nutzen Sie Notizen für Erinnerungen, Listen oder wichtige Punkte.",
        ],
        "btn": "Zurück zu Notizen",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Datenschutz</a> &bull; <a href=\"terms.html\">Nutzungsbedingungen</a> &bull; <a href=\"contact.html\">Kontakt</a>"
    },
    "ru": {
        "title": "Как использовать Заметки — TimerHaven",
        "back": "Назад к заметкам",
        "back_icon": "arrow-left",
        "back_link": "notes-ru.html",
        "h1": "Как использовать Заметки",
        "desc": "Инструмент <strong>Заметки</strong> предназначен для быстрых мыслей, напоминаний и списков. Вот как им пользоваться:",
        "steps_title": "Пошаговое руководство",
        "steps": [
            "<b>Введите заметку:</b> Введите текст в соответствующее поле.",
            "<b>Добавьте заметку:</b> Нажмите <strong>Добавить заметку</strong> для сохранения.",
            "<b>Просмотрите заметки:</b> Все заметки появятся в списке под формой.",
            "<b>Удалите заметки:</b> Удаляйте ненужные заметки с помощью кнопки удаления.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Сохраняются ли заметки после обновления?</b> Нет, они временные и локальные для браузера.",
            "<b>Можно ли добавить несколько заметок?</b> Да, сколько угодно.",
            "<b>Можно ли редактировать заметки?</b> Пока нет—удалите и добавьте снова для обновления.",
        ],
        "tips_title": "Советы для успеха",
        "tips": [
            "Используйте короткие заметки для идей или быстрых задач.",
            "Регулярно удаляйте старые заметки для порядка.",
            "Используйте заметки для напоминаний, списков или важных моментов.",
        ],
        "btn": "Назад к заметкам",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Политика конфиденциальности</a> &bull; <a href=\"terms.html\">Условия</a> &bull; <a href=\"contact.html\">Контакт</a>"
    },
    "el": {
        "title": "Πώς να χρησιμοποιήσετε τις Σημειώσεις — TimerHaven",
        "back": "Επιστροφή στις Σημειώσεις",
        "back_icon": "arrow-left",
        "back_link": "notes-el.html",
        "h1": "Πώς να χρησιμοποιήσετε τις Σημειώσεις",
        "desc": "Το εργαλείο <strong>Σημειώσεις</strong> είναι σχεδιασμένο για γρήγορες σκέψεις, υπενθυμίσεις και λίστες. Δείτε πώς να το χρησιμοποιήσετε:",
        "steps_title": "Βήμα προς βήμα οδηγός",
        "steps": [
            "<b>Γράψτε τη σημείωσή σας:</b> Εισάγετε το κείμενό σας στο κατάλληλο πεδίο.",
            "<b>Προσθέστε τη σημείωση:</b> Πατήστε <strong>Προσθήκη σημείωσης</strong> για να την αποθηκεύσετε.",
            "<b>Δείτε τις σημειώσεις:</b> Όλες οι σημειώσεις εμφανίζονται στη λίστα κάτω από τη φόρμα.",
            "<b>Διαγράψτε σημειώσεις:</b> Αφαιρέστε τις σημειώσεις που δεν χρειάζεστε με το κουμπί διαγραφής.",
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Αποθηκεύονται οι σημειώσεις μετά την ανανέωση;</b> Όχι, είναι προσωρινές και μόνο στον browser.",
            "<b>Μπορώ να προσθέσω πολλές σημειώσεις;</b> Ναι, όσες θέλετε.",
            "<b>Μπορώ να επεξεργαστώ σημείωση;</b> Όχι ακόμα—διαγράψτε και προσθέστε ξανά για να ενημερώσετε.",
        ],
        "tips_title": "Συμβουλές επιτυχίας",
        "tips": [
            "Χρησιμοποιήστε σύντομες σημειώσεις για γρήγορες ιδέες ή εργασίες.",
            "Διαγράψτε συχνά παλιές σημειώσεις για να είστε οργανωμένοι.",
            "Χρησιμοποιήστε σημειώσεις για υπενθυμίσεις, λίστες ή σημαντικά σημεία.",
        ],
        "btn": "Επιστροφή στις Σημειώσεις",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Πολιτική απορρήτου</a> &bull; <a href=\"terms.html\">Όροι</a> &bull; <a href=\"contact.html\">Επικοινωνία</a>"
    },
    "ar": {
        "title": "كيفية استخدام الملاحظات — TimerHaven",
        "back": "العودة إلى الملاحظات",
        "back_icon": "arrow-right",
        "back_link": "notes-ar.html",
        "h1": "كيفية استخدام الملاحظات",
        "desc": "أداة <strong>الملاحظات</strong> مصممة للأفكار السريعة والتذكيرات والقوائم. إليك كيفية استخدامها:",
        "steps_title": "دليل خطوة بخطوة",
        "steps": [
            "<b>اكتب ملاحظتك:</b> أدخل النص في الحقل المخصص.",
            "<b>أضف الملاحظة:</b> اضغط على <strong>إضافة ملاحظة</strong> لحفظها في قائمتك.",
            "<b>عرض الملاحظات:</b> تظهر جميع الملاحظات في القائمة أسفل النموذج.",
            "<b>حذف الملاحظات:</b> احذف الملاحظات غير المرغوب فيها باستخدام زر الحذف.",
        ],
        "faq_title": "الأسئلة الشائعة",
        "faqs": [
            "<b>هل تحفظ الملاحظات بعد تحديث الصفحة؟</b> لا، فهي مؤقتة ومحلية في المتصفح.",
            "<b>هل يمكنني إضافة عدة ملاحظات؟</b> نعم، عدد غير محدود.",
            "<b>هل يمكنني تعديل الملاحظة؟</b> ليس بعد—احذف وأعد الإضافة للتحديث.",
        ],
        "tips_title": "نصائح للنجاح",
        "tips": [
            "استخدم ملاحظات قصيرة لأفكار أو مهام سريعة.",
            "احذف الملاحظات القديمة بانتظام للبقاء منظمًا.",
            "استخدم الملاحظات للتذكيرات أو القوائم أو النقاط الهامة.",
        ],
        "btn": "العودة إلى الملاحظات",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">سياسة الخصوصية</a> &bull; <a href=\"terms.html\">الشروط</a> &bull; <a href=\"contact.html\">اتصل بنا</a>"
    }
}

tips = {
    "en": {
        "title": "Notes Productivity Tips — TimerHaven",
        "back": "Back to Notes",
        "back_icon": "arrow-left",
        "back_link": "notes-en.html",
        "h1": "Notes Productivity Tips",
        "desc": "Make your notes more useful with these practical tips:",
        "tips_title": "Top Tips",
        "tips": [
            "<b>Be concise:</b> Short, clear notes are easier to review and act on.",
            "<b>Delete often:</b> Keep your note list focused and relevant.",
            "<b>Use for tasks:</b> Write quick to-dos, reminders, or ideas.",
            "<b>Organize:</b> Use separate notes for different topics.",
        ],
        "did_title": "Did You Know?",
        "did": [
            "Notes are not saved after refresh—use for quick thoughts.",
            "You can add as many notes as you like.",
        ],
        "btn": "Back to Notes",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Privacy Policy</a> &bull; <a href=\"terms.html\">Terms</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "fr": {
        "title": "Conseils pour les Notes — TimerHaven",
        "back": "Retour aux Notes",
        "back_icon": "arrow-left",
        "back_link": "notes-fr.html",
        "h1": "Conseils pour les Notes",
        "desc": "Rendez vos notes plus utiles grâce à ces conseils pratiques :",
        "tips_title": "Conseils principaux",
        "tips": [
            "<b>Soyez concis :</b> Des notes courtes et claires sont plus faciles à relire et à utiliser.",
            "<b>Supprimez régulièrement :</b> Gardez votre liste de notes ciblée et pertinente.",
            "<b>Utilisez pour les tâches :</b> Notez rapidement vos tâches, rappels ou idées.",
            "<b>Organisez :</b> Créez des notes distinctes pour chaque sujet.",
        ],
        "did_title": "Le saviez-vous ?",
        "did": [
            "Les notes ne sont pas enregistrées après actualisation : utilisez-les pour des idées rapides.",
            "Vous pouvez ajouter autant de notes que vous le souhaitez.",
        ],
        "btn": "Retour aux Notes",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Politique de confidentialité</a> &bull; <a href=\"terms.html\">Conditions</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "es": {
        "title": "Consejos para las Notas — TimerHaven",
        "back": "Volver a Notas",
        "back_icon": "arrow-left",
        "back_link": "notes-es.html",
        "h1": "Consejos para las Notas",
        "desc": "Haz que tus notas sean más útiles con estos consejos prácticos:",
        "tips_title": "Consejos principales",
        "tips": [
            "<b>Sé conciso:</b> Las notas cortas y claras son más fáciles de revisar y aplicar.",
            "<b>Elimina frecuentemente:</b> Mantén tu lista de notas enfocada y relevante.",
            "<b>Úsalas para tareas:</b> Escribe tareas rápidas, recordatorios o ideas.",
            "<b>Organiza:</b> Utiliza notas separadas para distintos temas.",
        ],
        "did_title": "¿Lo sabías?",
        "did": [
            "Las notas no se guardan tras refrescar: úsalas para ideas rápidas.",
            "Puedes añadir tantas notas como desees.",
        ],
        "btn": "Volver a Notas",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Política de privacidad</a> &bull; <a href=\"terms.html\">Términos</a> &bull; <a href=\"contact.html\">Contacto</a>"
    },
    "de": {
        "title": "Notizen Tipps — TimerHaven",
        "back": "Zurück zu Notizen",
        "back_icon": "arrow-left",
        "back_link": "notes-de.html",
        "h1": "Notizen Tipps",
        "desc": "Machen Sie Ihre Notizen mit diesen praktischen Tipps noch nützlicher:",
        "tips_title": "Top-Tipps",
        "tips": [
            "<b>Kurz und prägnant:</b> Kurze, klare Notizen sind leichter zu überprüfen und umzusetzen.",
            "<b>Regelmäßig löschen:</b> Halten Sie Ihre Notizenliste fokussiert und relevant.",
            "<b>Für Aufgaben nutzen:</b> Schreiben Sie schnelle To-dos, Erinnerungen oder Ideen auf.",
            "<b>Organisieren:</b> Verwenden Sie separate Notizen für verschiedene Themen.",
        ],
        "did_title": "Wussten Sie schon?",
        "did": [
            "Notizen werden nach dem Aktualisieren nicht gespeichert – nutzen Sie sie für schnelle Gedanken.",
            "Sie können beliebig viele Notizen hinzufügen.",
        ],
        "btn": "Zurück zu Notizen",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Datenschutz</a> &bull; <a href=\"terms.html\">Nutzungsbedingungen</a> &bull; <a href=\"contact.html\">Kontakt</a>"
    },
    "ru": {
        "title": "Советы по Заметкам — TimerHaven",
        "back": "Назад к заметкам",
        "back_icon": "arrow-left",
        "back_link": "notes-ru.html",
        "h1": "Советы по Заметкам",
        "desc": "Сделайте свои заметки более полезными с помощью этих практических советов:",
        "tips_title": "Главные советы",
        "tips": [
            "<b>Будьте лаконичны:</b> Краткие, ясные заметки проще просматривать и выполнять.",
            "<b>Удаляйте лишнее:</b> Держите список заметок актуальным и полезным.",
            "<b>Для задач:</b> Записывайте быстрые дела, напоминания или идеи.",
            "<b>Организуйте:</b> Используйте отдельные заметки для разных тем.",
        ],
        "did_title": "Знаете ли вы?",
        "did": [
            "Заметки не сохраняются после обновления — используйте их для быстрых мыслей.",
            "Вы можете добавлять сколько угодно заметок.",
        ],
        "btn": "Назад к заметкам",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Политика конфиденциальности</a> &bull; <a href=\"terms.html\">Условия</a> &bull; <a href=\"contact.html\">Контакт</a>"
    },
    "el": {
        "title": "Συμβουλές για τις Σημειώσεις — TimerHaven",
        "back": "Επιστροφή στις Σημειώσεις",
        "back_icon": "arrow-left",
        "back_link": "notes-el.html",
        "h1": "Συμβουλές για τις Σημειώσεις",
        "desc": "Κάντε τις σημειώσεις σας πιο χρήσιμες με αυτές τις πρακτικές συμβουλές:",
        "tips_title": "Κορυφαίες συμβουλές",
        "tips": [
            "<b>Να είστε συνοπτικοί:</b> Σύντομες, σαφείς σημειώσεις είναι πιο εύκολες στην ανασκόπηση και δράση.",
            "<b>Διαγράψτε συχνά:</b> Κρατήστε τη λίστα σημειώσεων εστιασμένη και σχετική.",
            "<b>Χρησιμοποιήστε για εργασίες:</b> Γράψτε σύντομες υπενθυμίσεις, ιδέες ή να κάνετε λίστες.",
            "<b>Οργανώστε:</b> Χρησιμοποιήστε ξεχωριστές σημειώσεις για διαφορετικά θέματα.",
        ],
        "did_title": "Το ξέρατε;",
        "did": [
            "Οι σημειώσεις δεν αποθηκεύονται μετά την ανανέωση — χρησιμοποιήστε τις για γρήγορες σκέψεις.",
            "Μπορείτε να προσθέσετε όσες σημειώσεις θέλετε.",
        ],
        "btn": "Επιστροφή στις Σημειώσεις",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Πολιτική απορρήτου</a> &bull; <a href=\"terms.html\">Όροι</a> &bull; <a href=\"contact.html\">Επικοινωνία</a>"
    },
    "ar": {
        "title": "نصائح حول الملاحظات — TimerHaven",
        "back": "العودة إلى الملاحظات",
        "back_icon": "arrow-right",
        "back_link": "notes-ar.html",
        "h1": "نصائح حول الملاحظات",
        "desc": "اجعل ملاحظاتك أكثر فائدة مع هذه النصائح العملية:",
        "tips_title": "أفضل النصائح",
        "tips": [
            "<b>كن موجزًا:</b> الملاحظات القصيرة والواضحة أسهل في المراجعة والتنفيذ.",
            "<b>احذف باستمرار:</b> حافظ على قائمة ملاحظاتك مركزة وذات صلة.",
            "<b>استخدمها للمهام:</b> اكتب قوائم سريعة أو أفكار أو تذكيرات.",
            "<b>نظمها:</b> استخدم ملاحظات منفصلة لمواضيع مختلفة.",
        ],
        "did_title": "هل تعلم؟",
        "did": [
            "الملاحظات لا تحفظ بعد تحديث الصفحة—استخدمها للأفكار السريعة.",
            "يمكنك إضافة عدد غير محدود من الملاحظات.",
        ],
        "btn": "العودة إلى الملاحظات",
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">سياسة الخصوصية</a> &bull; <a href=\"terms.html\">الشروط</a> &bull; <a href=\"contact.html\">اتصل بنا</a>"
    }
}

def html_howto(lang, c):
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="UTF-8">
  <title>{c['title']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container" style="max-width:700px;margin:2em auto;background:#fff;border-radius:14px;box-shadow:0 2px 12px #e0e7ef;padding:2em;">
    <a href="{c['back_link']}" class="back-link" style="color:#185a9d;font-weight:bold;"><i class="fa fa-{c['back_icon']}"></i> {c['back']}</a>
    <h1><i class="fa fa-note-sticky"></i> {c['h1']}</h1>
    <p>{c['desc']}</p>
    <h2>{c['steps_title']}</h2>
    <ol>
      {''.join(f"<li>{step}</li>" for step in c['steps'])}
    </ol>
    <h2>{c['faq_title']}</h2>
    <ul>
      {''.join(f"<li>{faq}</li>" for faq in c['faqs'])}
    </ul>
    <h2>{c['tips_title']}</h2>
    <ul>
      {''.join(f"<li>{tip}</li>" for tip in c['tips'])}
    </ul>
    <a href="{c['back_link']}" class="btn btn-outline-primary btn-sm mt-3">{c['btn']}</a>
  </div>
<footer style="text-align:center;margin:2em 0 1em 0;">
  {c['footer']}
</footer>
</body>
</html>
"""

def html_tips(lang, c):
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="UTF-8">
  <title>{c['title']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container" style="max-width:700px;margin:2em auto;background:#fff;border-radius:14px;box-shadow:0 2px 12px #e0e7ef;padding:2em;">
    <a href="{c['back_link']}" class="back-link" style="color:#185a9d;font-weight:bold;"><i class="fa fa-{c['back_icon']}"></i> {c['back']}</a>
    <h1><i class="fa fa-lightbulb"></i> {c['h1']}</h1>
    <p>{c['desc']}</p>
    <h2>{c['tips_title']}</h2>
    <ul>
      {''.join(f"<li>{tip}</li>" for tip in c['tips'])}
    </ul>
    <h2>{c['did_title']}</h2>
    <ul>
      {''.join(f"<li>{d}</li>" for d in c['did'])}
    </ul>
    <a href="{c['back_link']}" class="btn btn-outline-primary btn-sm mt-3">{c['btn']}</a>
  </div>
<footer style="text-align:center;margin:2em 0 1em 0;">
  {c['footer']}
</footer>
</body>
</html>
"""

def main():
    outdir = "notes_articles"
    os.makedirs(outdir, exist_ok=True)
    for lang, _ in LANGS:
        with open(f"{outdir}/notes-how-to-{lang}.html", "w", encoding="utf-8") as f:
            f.write(html_howto(lang, howto[lang]))
        with open(f"{outdir}/notes-tips-{lang}.html", "w", encoding="utf-8") as f:
            f.write(html_tips(lang, tips[lang]))
    print(f"All how-to and tips files generated in ./{outdir}/")

if __name__ == "__main__":
    main()