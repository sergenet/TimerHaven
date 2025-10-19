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

tips_article = {
    "en": {
        "title": "Notes Productivity Tips — TimerHaven",
        "back_btn": "Back to Notes",
        "back_link": "notes-en.html",
        "h1": "Notes Productivity Tips",
        "desc": "Make your notes more useful with these practical tips:",
        "tips_title": "Top Tips",
        "tips": [
            "<b>Be concise:</b> Short, clear notes are easier to review and act on.",
            "<b>Delete often:</b> Keep your note list focused and relevant.",
            "<b>Use for tasks:</b> Write quick to-dos, reminders, or ideas.",
            "<b>Organize:</b> Use separate notes for different topics."
        ],
        "did_title": "Did You Know?",
        "did": [
            "Notes are not saved after refresh—use for quick thoughts.",
            "You can add as many notes as you like."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Privacy Policy</a> &bull; <a href=\"terms.html\">Terms</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "fr": {
        "title": "Conseils pour les Notes — TimerHaven",
        "back_btn": "Retour aux Notes",
        "back_link": "notes-fr.html",
        "h1": "Conseils pour les Notes",
        "desc": "Rendez vos notes plus utiles grâce à ces conseils pratiques :",
        "tips_title": "Conseils principaux",
        "tips": [
            "<b>Soyez concis :</b> Des notes courtes et claires sont plus faciles à relire et à utiliser.",
            "<b>Supprimez régulièrement :</b> Gardez votre liste de notes ciblée et pertinente.",
            "<b>Utilisez pour les tâches :</b> Notez rapidement vos tâches, rappels ou idées.",
            "<b>Organisez :</b> Créez des notes distinctes pour chaque sujet."
        ],
        "did_title": "Le saviez-vous ?",
        "did": [
            "Les notes ne sont pas enregistrées après actualisation : utilisez-les pour des idées rapides.",
            "Vous pouvez ajouter autant de notes que vous le souhaitez."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Politique de confidentialité</a> &bull; <a href=\"terms.html\">Conditions</a> &bull; <a href=\"contact.html\">Contact</a>"
    },
    "es": {
        "title": "Consejos para las Notas — TimerHaven",
        "back_btn": "Volver a Notas",
        "back_link": "notes-es.html",
        "h1": "Consejos para las Notas",
        "desc": "Haz que tus notas sean más útiles con estos consejos prácticos:",
        "tips_title": "Consejos principales",
        "tips": [
            "<b>Sé conciso:</b> Las notas cortas y claras son más fáciles de revisar y aplicar.",
            "<b>Elimina frecuentemente:</b> Mantén tu lista de notas enfocada y relevante.",
            "<b>Úsalas para tareas:</b> Escribe tareas rápidas, recordatorios o ideas.",
            "<b>Organiza:</b> Utiliza notas separadas para distintos temas."
        ],
        "did_title": "¿Lo sabías?",
        "did": [
            "Las notas no se guardan tras refrescar: úsalas para ideas rápidas.",
            "Puedes añadir tantas notas como desees."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Política de privacidad</a> &bull; <a href=\"terms.html\">Términos</a> &bull; <a href=\"contact.html\">Contacto</a>"
    },
    "de": {
        "title": "Notizen Tipps — TimerHaven",
        "back_btn": "Zurück zu Notizen",
        "back_link": "notes-de.html",
        "h1": "Notizen Tipps",
        "desc": "Machen Sie Ihre Notizen mit diesen praktischen Tipps noch nützlicher:",
        "tips_title": "Top-Tipps",
        "tips": [
            "<b>Kurz und prägnant:</b> Kurze, klare Notizen sind leichter zu überprüfen und umzusetzen.",
            "<b>Regelmäßig löschen:</b> Halten Sie Ihre Notizenliste fokussiert und relevant.",
            "<b>Für Aufgaben nutzen:</b> Schreiben Sie schnelle To-dos, Erinnerungen oder Ideen auf.",
            "<b>Organisieren:</b> Verwenden Sie separate Notizen für verschiedene Themen."
        ],
        "did_title": "Wussten Sie schon?",
        "did": [
            "Notizen werden nach dem Aktualisieren nicht gespeichert – nutzen Sie sie für schnelle Gedanken.",
            "Sie können beliebig viele Notizen hinzufügen."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Datenschutz</a> &bull; <a href=\"terms.html\">Nutzungsbedingungen</a> &bull; <a href=\"contact.html\">Kontakt</a>"
    },
    "ru": {
        "title": "Советы по Заметкам — TimerHaven",
        "back_btn": "Назад к заметкам",
        "back_link": "notes-ru.html",
        "h1": "Советы по Заметкам",
        "desc": "Сделайте свои заметки более полезными с помощью этих практических советов:",
        "tips_title": "Главные советы",
        "tips": [
            "<b>Будьте лаконичны:</b> Краткие, ясные заметки проще просматривать и выполнять.",
            "<b>Удаляйте лишнее:</b> Держите список заметок актуальным и полезным.",
            "<b>Для задач:</b> Записывайте быстрые дела, напоминания или идеи.",
            "<b>Организуйте:</b> Используйте отдельные заметки для разных тем."
        ],
        "did_title": "Знаете ли вы?",
        "did": [
            "Заметки не сохраняются после обновления — используйте их для быстрых мыслей.",
            "Вы можете добавлять сколько угодно заметок."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Политика конфиденциальности</a> &bull; <a href=\"terms.html\">Условия</a> &bull; <a href=\"contact.html\">Контакт</a>"
    },
    "el": {
        "title": "Συμβουλές για τις Σημειώσεις — TimerHaven",
        "back_btn": "Επιστροφή στις Σημειώσεις",
        "back_link": "notes-el.html",
        "h1": "Συμβουλές για τις Σημειώσεις",
        "desc": "Κάντε τις σημειώσεις σας πιο χρήσιμες με αυτές τις πρακτικές συμβουλές:",
        "tips_title": "Κορυφαίες συμβουλές",
        "tips": [
            "<b>Να είστε συνοπτικοί:</b> Σύντομες, σαφείς σημειώσεις είναι πιο εύκολες στην ανασκόπηση και δράση.",
            "<b>Διαγράψτε συχνά:</b> Κρατήστε τη λίστα σημειώσεων εστιασμένη και σχετική.",
            "<b>Χρησιμοποιήστε για εργασίες:</b> Γράψτε σύντομες υπενθυμίσεις, ιδέες ή να κάνετε λίστες.",
            "<b>Οργανώστε:</b> Χρησιμοποιήστε ξεχωριστές σημειώσεις για διαφορετικά θέματα."
        ],
        "did_title": "Το ξέρατε;",
        "did": [
            "Οι σημειώσεις δεν αποθηκεύονται μετά την ανανέωση — χρησιμοποιήστε τις για γρήγορες σκέψεις.",
            "Μπορείτε να προσθέσετε όσες σημειώσεις θέλετε."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">Πολιτική απορρήτου</a> &bull; <a href=\"terms.html\">Όροι</a> &bull; <a href=\"contact.html\">Επικοινωνία</a>"
    },
    "ar": {
        "title": "نصائح حول الملاحظات — TimerHaven",
        "back_btn": "العودة إلى الملاحظات",
        "back_link": "notes-ar.html",
        "h1": "نصائح حول الملاحظات",
        "desc": "اجعل ملاحظاتك أكثر فائدة مع هذه النصائح العملية:",
        "tips_title": "أفضل النصائح",
        "tips": [
            "<b>كن موجزًا:</b> الملاحظات القصيرة والواضحة أسهل في المراجعة والتنفيذ.",
            "<b>احذف باستمرار:</b> حافظ على قائمة ملاحظاتك مركزة وذات صلة.",
            "<b>استخدمها للمهام:</b> اكتب قوائم سريعة أو أفكار أو تذكيرات.",
            "<b>نظمها:</b> استخدم ملاحظات منفصلة لمواضيع مختلفة."
        ],
        "did_title": "هل تعلم؟",
        "did": [
            "الملاحظات لا تحفظ بعد تحديث الصفحة—استخدمها للأفكار السريعة.",
            "يمكنك إضافة عدد غير محدود من الملاحظات."
        ],
        "footer": "&copy; 2025 TimerHaven.<br><a href=\"privacy.html\">سياسة الخصوصية</a> &bull; <a href=\"terms.html\">الشروط</a> &bull; <a href=\"contact.html\">اتصل بنا</a>"
    }
}

def html_tips_article(lang, c):
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
        with open(f"notes_articles/notes-tips-{lang}.html", "w", encoding="utf-8") as f:
            f.write(html_tips_article(lang, tips_article[lang]))
    print("All notes tips pages generated in ./notes_articles")

if __name__ == "__main__":
    main()