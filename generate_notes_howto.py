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

howto_article = {
    "en": {
        "title": "How to Use Notes — TimerHaven",
        "back_btn": "Back to Notes",
        "back_link": "notes-en.html",
        "h1": "How to Use Notes",
        "desc": "The <b>Notes</b> tool is designed for quick ideas, lists, and reminders. Here’s how to use it:",
        "steps_title": "Step-by-step Guide",
        "steps": [
            "<b>Add a note:</b> Type your text in the input box.",
            "<b>Save the note:</b> Click <b>Add Note</b> to add it to your list.",
            "<b>View notes:</b> All notes appear in the list below the form.",
            "<b>Delete notes:</b> Remove notes you no longer need."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Are notes saved after refresh?</b> Yes, until you clear your browser storage.",
            "<b>Can I add multiple notes?</b> Yes, as many as you wish.",
            "<b>Can I edit a note?</b> Not yet—delete and add a new note to update."
        ],
        "tips_title": "Tips for Success",
        "tips": [
            "Use short notes for quick ideas or tasks.",
            "Delete old notes to stay organized.",
            "Use notes for reminders, lists, or important points."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Privacy Policy</a> &bull; <a href=\"terms.html\">Terms</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "fr": {
        "title": "Comment utiliser les Notes — TimerHaven",
        "back_btn": "Retour aux Notes",
        "back_link": "notes-fr.html",
        "h1": "Comment utiliser les Notes",
        "desc": "L’outil <strong>Notes</strong> est conçu pour les idées rapides, les rappels et les listes. Voici comment l’utiliser :",
        "steps_title": "Guide étape par étape",
        "steps": [
            "<b>Écrivez votre note :</b> Saisissez votre texte dans la boîte prévue à cet effet.",
            "<b>Ajoutez la note :</b> Cliquez sur <strong>Ajouter une note</strong> pour l’enregistrer dans la liste.",
            "<b>Affichez vos notes :</b> Toutes vos notes apparaissent dans la liste sous le formulaire.",
            "<b>Supprimez les notes :</b> Retirez les notes inutiles grâce au bouton de suppression."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Les notes sont-elles sauvegardées après actualisation ?</b> Non, elles sont temporaires et locales au navigateur.",
            "<b>Puis-je ajouter plusieurs notes ?</b> Oui, autant que vous le souhaitez.",
            "<b>Puis-je modifier une note ?</b> Pas encore—supprimez et recréez-la pour la mettre à jour."
        ],
        "tips_title": "Conseils pour réussir",
        "tips": [
            "Utilisez des notes courtes pour des idées ou tâches rapides.",
            "Supprimez régulièrement les anciennes notes pour rester organisé.",
            "Utilisez les notes pour des rappels, des listes ou des points importants."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Politique de confidentialité</a> &bull; <a href=\"terms.html\">Conditions</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "es": {
        "title": "Cómo usar las Notas — TimerHaven",
        "back_btn": "Volver a Notas",
        "back_link": "notes-es.html",
        "h1": "Cómo usar las Notas",
        "desc": "La herramienta <strong>Notas</strong> está diseñada para pensamientos rápidos, recordatorios y listas. Así se utiliza:",
        "steps_title": "Guía paso a paso",
        "steps": [
            "<b>Escribe tu nota:</b> Ingresa tu texto en el campo correspondiente.",
            "<b>Agrega la nota:</b> Haz clic en <strong>Agregar Nota</strong> para guardarla en tu lista.",
            "<b>Visualiza las notas:</b> Todas tus notas aparecen en la lista debajo del formulario.",
            "<b>Elimina las notas:</b> Borra las notas que ya no necesites usando el botón de eliminar."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>¿Se guardan las notas tras refrescar?</b> No, son temporales y locales al navegador.",
            "<b>¿Puedo agregar varias notas?</b> Sí, tantas como desees.",
            "<b>¿Puedo editar notas?</b> Aún no—elimina y vuelve a añadir para actualizar."
        ],
        "tips_title": "Consejos para el éxito",
        "tips": [
            "Utiliza notas cortas para ideas o tareas rápidas.",
            "Elimina notas regularmente para mantenerte organizado.",
            "Utiliza las notas para recordatorios, listas o puntos importantes."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Política de privacidad</a> &bull; <a href=\"terms.html\">Términos</a> &bull; <a href=\"contact.html\">Contacto</a>"
    },
    "de": {
        "title": "So nutzen Sie Notizen — TimerHaven",
        "back_btn": "Zurück zu Notizen",
        "back_link": "notes-de.html",
        "h1": "So nutzen Sie Notizen",
        "desc": "Das <strong>Notizen</strong>-Tool eignet sich für schnelle Gedanken, Erinnerungen und Listen. So funktioniert es:",
        "steps_title": "Schritt-für-Schritt-Anleitung",
        "steps": [
            "<b>Notiz eingeben:</b> Tragen Sie Ihren Text in das vorgesehene Feld ein.",
            "<b>Notiz hinzufügen:</b> Klicken Sie auf <strong>Notiz hinzufügen</strong>, um sie zu speichern.",
            "<b>Notizen anzeigen:</b> Alle Ihre Notizen erscheinen in der Liste unterhalb des Formulars.",
            "<b>Notizen löschen:</b> Entfernen Sie nicht mehr benötigte Notizen mit dem Löschen-Button."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Werden Notizen nach dem Aktualisieren gespeichert?</b> Nein, sie sind temporär und nur lokal im Browser.",
            "<b>Kann ich mehrere Notizen hinzufügen?</b> Ja, so viele Sie möchten.",
            "<b>Kann ich Notizen bearbeiten?</b> Noch nicht—löschen und neu hinzufügen zum Aktualisieren."
        ],
        "tips_title": "Tipps für den Erfolg",
        "tips": [
            "Verwenden Sie kurze Notizen für schnelle Ideen oder Aufgaben.",
            "Löschen Sie regelmäßig alte Notizen, um organisiert zu bleiben.",
            "Nutzen Sie Notizen für Erinnerungen, Listen oder wichtige Punkte."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Datenschutz</a> &bull; <a href=\"terms.html\">Nutzungsbedingungen</a> &bull; <a href=\"contact.html\">Kontakt</a>"
    },
    "ru": {
        "title": "Как использовать Заметки — TimerHaven",
        "back_btn": "Назад к заметкам",
        "back_link": "notes-ru.html",
        "h1": "Как использовать Заметки",
        "desc": "Инструмент <strong>Заметки</strong> предназначен для быстрых мыслей, напоминаний и списков. Вот как им пользоваться:",
        "steps_title": "Пошаговое руководство",
        "steps": [
            "<b>Введите заметку:</b> Введите текст в соответствующее поле.",
            "<b>Добавьте заметку:</b> Нажмите <strong>Добавить заметку</strong> для сохранения.",
            "<b>Просмотрите заметки:</b> Все заметки появятся в списке под формой.",
            "<b>Удалите заметки:</b> Удаляйте ненужные заметки с помощью кнопки удаления."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Сохраняются ли заметки после обновления?</b> Нет, они временные и локальные для браузера.",
            "<b>Можно ли добавить несколько заметок?</b> Да, сколько угодно.",
            "<b>Можно ли редактировать заметки?</b> Пока нет—удалите и добавьте снова для обновления."
        ],
        "tips_title": "Советы для успеха",
        "tips": [
            "Используйте короткие заметки для идей или быстрых задач.",
            "Регулярно удаляйте старые заметки для порядка.",
            "Используйте заметки для напоминаний, списков или важных моментов."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Политика конфиденциальности</a> &bull; <a href=\"terms.html\">Условия</a> &bull; <a href=\"contact.html\">Контакт</a>"
    },
    "el": {
        "title": "Πώς να χρησιμοποιήσετε τις Σημειώσεις — TimerHaven",
        "back_btn": "Επιστροφή στις Σημειώσεις",
        "back_link": "notes-el.html",
        "h1": "Πώς να χρησιμοποιήσετε τις Σημειώσεις",
        "desc": "Το εργαλείο <strong>Σημειώσεις</strong> είναι σχεδιασμένο για γρήγορες σκέψεις, υπενθυμίσεις και λίστες. Δείτε πώς να το χρησιμοποιήσετε:",
        "steps_title": "Βήμα προς βήμα οδηγός",
        "steps": [
            "<b>Γράψτε τη σημείωσή σας:</b> Εισάγετε το κείμενό σας στο κατάλληλο πεδίο.",
            "<b>Προσθέστε τη σημείωση:</b> Πατήστε <strong>Προσθήκη σημείωσης</strong> για να την αποθηκεύσετε.",
            "<b>Δείτε τις σημειώσεις:</b> Όλες οι σημειώσεις εμφανίζονται στη λίστα κάτω από τη φόρμα.",
            "<b>Διαγράψτε σημειώσεις:</b> Αφαιρέστε τις σημειώσεις που δεν χρειάζεστε με το κουμπί διαγραφής."
        ],
        "faq_title": "FAQs",
        "faqs": [
            "<b>Αποθηκεύονται οι σημειώσεις μετά την ανανέωση;</b> Όχι, είναι προσωρινές και μόνο στον browser.",
            "<b>Μπορώ να προσθέσω πολλές σημειώσεις;</b> Ναι, όσες θέλετε.",
            "<b>Μπορώ να επεξεργαστώ σημείωση;</b> Όχι ακόμα—διαγράψτε και προσθέστε ξανά για να ενημερώσετε."
        ],
        "tips_title": "Συμβουλές επιτυχίας",
        "tips": [
            "Χρησιμοποιήστε σύντομες σημειώσεις για γρήγορες ιδέες ή εργασίες.",
            "Διαγράψτε συχνά παλιές σημειώσεις για να είστε οργανωμένοι.",
            "Χρησιμοποιήστε σημειώσεις για υπενθυμίσεις, λίστες ή σημαντικά σημεία."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Πολιτική απορρήτου</a> &bull; <a href=\"terms.html\">Όροι</a> &bull; <a href=\"contact.html\">Επικοινωνία</a>"
    },
    "ar": {
        "title": "كيفية استخدام الملاحظات — TimerHaven",
        "back_btn": "العودة إلى الملاحظات",
        "back_link": "notes-ar.html",
        "h1": "كيفية استخدام الملاحظات",
        "desc": "أداة <strong>الملاحظات</strong> مصممة للأفكار السريعة والتذكيرات والقوائم. إليك كيفية استخدامها:",
        "steps_title": "دليل خطوة بخطوة",
        "steps": [
            "<b>اكتب ملاحظتك:</b> أدخل النص في الحقل المخصص.",
            "<b>أضف الملاحظة:</b> اضغط على <strong>إضافة ملاحظة</strong> لحفظها في قائمتك.",
            "<b>عرض الملاحظات:</b> تظهر جميع الملاحظات في القائمة أسفل النموذج.",
            "<b>حذف الملاحظات:</b> احذف الملاحظات غير المرغوب فيها باستخدام زر الحذف."
        ],
        "faq_title": "الأسئلة الشائعة",
        "faqs": [
            "<b>هل تحفظ الملاحظات بعد تحديث الصفحة؟</b> لا، فهي مؤقتة ومحلية في المتصفح.",
            "<b>هل يمكنني إضافة عدة ملاحظات؟</b> نعم، عدد غير محدود.",
            "<b>هل يمكنني تعديل الملاحظة؟</b> ليس بعد—احذف وأعد الإضافة للتحديث."
        ],
        "tips_title": "نصائح للنجاح",
        "tips": [
            "استخدم ملاحظات قصيرة لأفكار أو مهام سريعة.",
            "احذف الملاحظات القديمة بانتظام للبقاء منظمًا.",
            "استخدم الملاحظات للتذكيرات أو القوائم أو النقاط الهامة."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">سياسة الخصوصية</a> &bull; <a href=\"terms.html\">الشروط</a> &bull; <a href=\"contact.html\">اتصل بنا</a>"
    }
}

def html_howto_article(lang, c):
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
    <a href="{c['back_link']}" class="btn btn-outline-primary btn-sm" style="font-weight:bold;margin-bottom:1em;">{c['back_btn']}</a>
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
    <a href="{c['back_link']}" class="btn btn-outline-primary btn-sm mt-3">{c['back_btn']}</a>
  </div>
<footer style="text-align:center;margin:2em 0 1em 0;">
  {c['footer']}
</footer>
</body>
</html>
"""

def main():
    os.makedirs("notes_articles", exist_ok=True)
    for lang, _ in LANGS:
        with open(f"notes_articles/notes-how-to-{lang}.html", "w", encoding="utf-8") as f:
            f.write(html_howto_article(lang, howto_article[lang]))
    print("All notes how-to pages generated in ./notes_articles")

if __name__ == "__main__":
    main()