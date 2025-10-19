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

notes_content = {
    "en": {
        "title": "Notes — TimerHaven",
        "desc": "Take quick notes and organize your thoughts. Learn how to use Notes, get productivity tips, FAQs, and read expert articles.",
        "howto_title": "How to Use Notes",
        "howto_list": [
            "<b>Add a note:</b> Type and save your note.",
            "<b>Organize:</b> Edit, delete, or pin notes as needed.",
            "<b>Stay productive:</b> Use notes for ideas, reminders, and tasks."
        ],
        "howto_link": "notes-how-to-en.html",
        "howto_btn": "Read Full Article",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Back to Main Menu",
        "notes_title": "Notes",
        "note_input": "Type your note...",
        "add_note_btn": "Add Note",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>Are notes saved?</b> Yes, in your browser until you clear them.",
            "<b>Can I pin important notes?</b> Yes, use the pin feature if available.",
            "<b>Is there a limit?</b> No, add as many notes as you need."
        ],
        "tips_title": "Notes Productivity Tips",
        "tips_list": [
            "<b>Keep notes short:</b> Focus on key ideas and reminders.",
            "<b>Pin top items:</b> Mark important notes for quick access.",
            "<b>Review regularly:</b> Clear old notes to stay organized."
        ],
        "tips_link": "notes-tips-en.html",
        "tips_btn": "Read Full Article",
        "no_notes": "No notes yet.",
        "privacy": "Privacy Policy",
        "terms": "Terms",
        "contact": "Contact",
        "footer": "&copy; 2025 TimerHaven. All tools are free and privacy-friendly.",
    },
    "fr": {
        "title": "Notes — TimerHaven",
        "desc": "Prenez des notes rapides et organisez vos idées. Découvrez comment utiliser Notes, obtenez des conseils de productivité, des FAQs et lisez des articles d'experts.",
        "howto_title": "Comment utiliser les Notes",
        "howto_list": [
            "<b>Ajoutez une note :</b> Saisissez et enregistrez votre note.",
            "<b>Organisez :</b> Modifiez, supprimez ou épinglez les notes selon vos besoins.",
            "<b>Restez productif :</b> Utilisez les notes pour des idées, rappels et tâches."
        ],
        "howto_link": "notes-how-to-fr.html",
        "howto_btn": "Lire l'article complet",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Retour au menu principal",
        "notes_title": "Notes",
        "note_input": "Tapez votre note...",
        "add_note_btn": "Ajouter une note",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>Les notes sont-elles sauvegardées ?</b> Oui, dans votre navigateur jusqu’à suppression.",
            "<b>Peut-on épingler des notes importantes ?</b> Oui, utilisez l’option épingler si disponible.",
            "<b>Y a-t-il une limite ?</b> Non, ajoutez autant de notes que vous le souhaitez."
        ],
        "tips_title": "Conseils pour les Notes",
        "tips_list": [
            "<b>Soyez concis :</b> Des notes courtes et claires sont plus faciles à relire et à utiliser.",
            "<b>Épinglez les éléments importants :</b> Marquez les notes essentielles pour y accéder rapidement.",
            "<b>Supprimez régulièrement :</b> Gardez vos notes organisées en effaçant les anciennes."
        ],
        "tips_link": "notes-tips-fr.html",
        "tips_btn": "Lire l'article complet",
        "no_notes": "Aucune note pour le moment.",
        "privacy": "Politique de confidentialité",
        "terms": "Conditions",
        "contact": "Contact",
        "footer": "&copy; 2025 TimerHaven. Tous les outils sont gratuits et respectueux de la vie privée.",
    },
    "es": {
        "title": "Notas — TimerHaven",
        "desc": "Toma notas rápidas y organiza tus ideas. Aprende a usar Notas, encuentra consejos de productividad, FAQs y lee artículos de expertos.",
        "howto_title": "Cómo usar las Notas",
        "howto_list": [
            "<b>Agrega una nota:</b> Escribe y guarda tu nota.",
            "<b>Organiza:</b> Edita, elimina o fija notas según lo necesites.",
            "<b>Sé productivo:</b> Usa notas para ideas, recordatorios y tareas."
        ],
        "howto_link": "notes-how-to-es.html",
        "howto_btn": "Leer el artículo completo",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Volver al menú principal",
        "notes_title": "Notas",
        "note_input": "Escribe tu nota...",
        "add_note_btn": "Agregar nota",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>¿Se guardan las notas?</b> Sí, en tu navegador hasta que las elimines.",
            "<b>¿Puedo fijar notas importantes?</b> Sí, usa la función de fijar si está disponible.",
            "<b>¿Hay límite?</b> No, agrega tantas notas como quieras."
        ],
        "tips_title": "Consejos para las Notas",
        "tips_list": [
            "<b>Mantén notas cortas:</b> Enfócate en ideas y recordatorios clave.",
            "<b>Fija elementos importantes:</b> Marca notas esenciales para acceso rápido.",
            "<b>Elimina regularmente:</b> Borra notas antiguas para mantenerte organizado."
        ],
        "tips_link": "notes-tips-es.html",
        "tips_btn": "Leer el artículo completo",
        "no_notes": "No hay notas todavía.",
        "privacy": "Política de privacidad",
        "terms": "Términos",
        "contact": "Contacto",
        "footer": "&copy; 2025 TimerHaven. Todas las herramientas son gratuitas y respetuosas con la privacidad.",
    },
    "de": {
        "title": "Notizen — TimerHaven",
        "desc": "Machen Sie schnelle Notizen und organisieren Sie Ihre Gedanken. Lernen Sie, wie Sie Notizen verwenden, erhalten Sie Produktivitätstipps, FAQs und lesen Sie Expertenartikel.",
        "howto_title": "So nutzen Sie Notizen",
        "howto_list": [
            "<b>Notiz hinzufügen:</b> Schreiben und speichern Sie Ihre Notiz.",
            "<b>Organisieren:</b> Bearbeiten, löschen oder markieren Sie Notizen nach Bedarf.",
            "<b>Produktiv bleiben:</b> Nutzen Sie Notizen für Ideen, Erinnerungen und Aufgaben."
        ],
        "howto_link": "notes-how-to-de.html",
        "howto_btn": "Vollständigen Artikel lesen",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Zurück zum Hauptmenü",
        "notes_title": "Notizen",
        "note_input": "Notiz eingeben...",
        "add_note_btn": "Notiz hinzufügen",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>Werden Notizen gespeichert?</b> Ja, im Browser bis Sie sie löschen.",
            "<b>Können wichtige Notizen angepinnt werden?</b> Ja, verwenden Sie die Pin-Funktion, falls verfügbar.",
            "<b>Gibt es ein Limit?</b> Nein, Sie können beliebig viele Notizen hinzufügen."
        ],
        "tips_title": "Notizen Tipps",
        "tips_list": [
            "<b>Notizen kurz halten:</b> Fokussieren Sie auf Schlüsselideen und Erinnerungen.",
            "<b>Wichtige Elemente anpinnen:</b> Markieren Sie wichtige Notizen für schnellen Zugriff.",
            "<b>Regelmäßig überprüfen:</b> Entfernen Sie alte Notizen, um organisiert zu bleiben."
        ],
        "tips_link": "notes-tips-de.html",
        "tips_btn": "Vollständigen Artikel lesen",
        "no_notes": "Noch keine Notizen.",
        "privacy": "Datenschutz",
        "terms": "Nutzungsbedingungen",
        "contact": "Kontakt",
        "footer": "&copy; 2025 TimerHaven. Alle Tools sind kostenlos und datenschutzfreundlich.",
    },
    "ru": {
        "title": "Заметки — TimerHaven",
        "desc": "Делайте быстрые заметки и организуйте свои мысли. Узнайте, как использовать Заметки, получите советы по продуктивности, FAQs и читайте экспертные статьи.",
        "howto_title": "Как использовать Заметки",
        "howto_list": [
            "<b>Добавьте заметку:</b> Введите и сохраните свою заметку.",
            "<b>Организуйте:</b> Редактируйте, удаляйте или закрепляйте заметки по необходимости.",
            "<b>Оставайтесь продуктивным:</b> Используйте заметки для идей, напоминаний и задач."
        ],
        "howto_link": "notes-how-to-ru.html",
        "howto_btn": "Читать всю статью",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Назад в главное меню",
        "notes_title": "Заметки",
        "note_input": "Введите заметку...",
        "add_note_btn": "Добавить заметку",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>Заметки сохраняются?</b> Да, в вашем браузере до удаления.",
            "<b>Можно закреплять важные заметки?</b> Да, используйте функцию закрепления, если она доступна.",
            "<b>Есть лимит?</b> Нет, добавляйте сколько угодно заметок."
        ],
        "tips_title": "Советы по Заметкам",
        "tips_list": [
            "<b>Пишите коротко:</b> Сосредоточьтесь на ключевых идеях и напоминаниях.",
            "<b>Закрепляйте важные заметки:</b> Помечайте важные заметки для быстрого доступа.",
            "<b>Регулярно удаляйте:</b> Очищайте старые заметки для порядка."
        ],
        "tips_link": "notes-tips-ru.html",
        "tips_btn": "Читать всю статью",
        "no_notes": "Заметок пока нет.",
        "privacy": "Политика конфиденциальности",
        "terms": "Условия",
        "contact": "Контакт",
        "footer": "&copy; 2025 TimerHaven. Все инструменты бесплатны и заботятся о приватности.",
    },
    "el": {
        "title": "Σημειώσεις — TimerHaven",
        "desc": "Κάντε γρήγορες σημειώσεις και οργανώστε τις ιδέες σας. Μάθετε πώς να χρησιμοποιείτε τις Σημειώσεις, δείτε συμβουλές παραγωγικότητας, FAQs και διαβάστε άρθρα ειδικών.",
        "howto_title": "Πώς να χρησιμοποιήσετε τις Σημειώσεις",
        "howto_list": [
            "<b>Προσθέστε σημείωση:</b> Γράψτε και αποθηκεύστε τη σημείωσή σας.",
            "<b>Οργανώστε:</b> Επεξεργαστείτε, διαγράψτε ή καρφιτσώστε σημειώσεις όπως χρειάζεται.",
            "<b>Μείνετε παραγωγικοί:</b> Χρησιμοποιήστε σημειώσεις για ιδέες, υπενθυμίσεις και εργασίες."
        ],
        "howto_link": "notes-how-to-el.html",
        "howto_btn": "Διαβάστε ολόκληρο το άρθρο",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-left'></i> Επιστροφή στο κύριο μενού",
        "notes_title": "Σημειώσεις",
        "note_input": "Γράψτε τη σημείωσή σας...",
        "add_note_btn": "Προσθήκη σημείωσης",
        "faq_title": "FAQs",
        "faq_items": [
            "<b>Αποθηκεύονται οι σημειώσεις;</b> Ναι, στον browser μέχρι να διαγραφούν.",
            "<b>Μπορώ να καρφιτσώσω σημαντικές σημειώσεις;</b> Ναι, χρησιμοποιήστε τη δυνατότητα αν είναι διαθέσιμη.",
            "<b>Υπάρχει όριο;</b> Όχι, προσθέστε όσες σημειώσεις θέλετε."
        ],
        "tips_title": "Συμβουλές για τις Σημειώσεις",
        "tips_list": [
            "<b>Κρατήστε τις σημειώσεις σύντομες:</b> Εστιάστε σε βασικές ιδέες και υπενθυμίσεις.",
            "<b>Καρφιτσώστε σημαντικά στοιχεία:</b> Μαρκάρετε σημαντικές σημειώσεις για γρήγορη πρόσβαση.",
            "<b>Επαναξιολογήστε τακτικά:</b> Διαγράψτε παλιές σημειώσεις για να είστε οργανωμένοι."
        ],
        "tips_link": "notes-tips-el.html",
        "tips_btn": "Διαβάστε ολόκληρο το άρθρο",
        "no_notes": "Δεν υπάρχουν σημειώσεις ακόμα.",
        "privacy": "Πολιτική απορρήτου",
        "terms": "Όροι",
        "contact": "Επικοινωνία",
        "footer": "&copy; 2025 TimerHaven. Όλα τα εργαλεία είναι δωρεάν και φιλικά προς το απόρρητο.",
    },
    "ar": {
        "title": "الملاحظات — TimerHaven",
        "desc": "دوّن ملاحظات سريعة ونظم أفكارك. تعرّف كيف تستخدم الملاحظات، واحصل على نصائح الإنتاجية، الأسئلة الشائعة، واطّلع على مقالات الخبراء.",
        "howto_title": "كيفية استخدام الملاحظات",
        "howto_list": [
            "<b>أضف ملاحظة:</b> اكتب واحتفظ بملاحظتك.",
            "<b>نظم:</b> عدل أو احذف أو ثبّت الملاحظات حسب الحاجة.",
            "<b>كن منتجًا:</b> استخدم الملاحظات للأفكار والتذكيرات والمهام."
        ],
        "howto_link": "notes-how-to-ar.html",
        "howto_btn": "اقرأ المقال الكامل",
        "back_main_link": "index.html",
        "back_main": "<i class='fa fa-arrow-right'></i> العودة إلى القائمة الرئيسية",
        "notes_title": "الملاحظات",
        "note_input": "اكتب ملاحظتك...",
        "add_note_btn": "أضف ملاحظة",
        "faq_title": "الأسئلة الشائعة",
        "faq_items": [
            "<b>هل تحفظ الملاحظات؟</b> نعم، في المتصفح حتى يتم حذفها.",
            "<b>هل يمكن تثبيت الملاحظات المهمة؟</b> نعم، استخدم ميزة التثبيت إذا كانت متاحة.",
            "<b>هل هناك حد؟</b> لا، أضف عددًا غير محدود من الملاحظات."
        ],
        "tips_title": "نصائح حول الملاحظات",
        "tips_list": [
            "<b>اجعل الملاحظات قصيرة:</b> ركز على الأفكار والتذكيرات الأساسية.",
            "<b>ثبّت العناصر المهمة:</b> ميّز الملاحظات الهامة للوصول السريع.",
            "<b>راجع بانتظام:</b> احذف الملاحظات القديمة للبقاء منظمًا."
        ],
        "tips_link": "notes-tips-ar.html",
        "tips_btn": "اقرأ المقال الكامل",
        "no_notes": "لا توجد ملاحظات بعد.",
        "privacy": "سياسة الخصوصية",
        "terms": "الشروط",
        "contact": "اتصل بنا",
        "footer": "&copy; 2025 TimerHaven. جميع الأدوات مجانية وتحترم الخصوصية.",
    }
}

def html_language_selector(lang):
    return '''
<div style="margin:1em 0;">
  <select id="language-select" style="font-size:1em;">
    <option value="en">English</option>
    <option value="fr">Français</option>
    <option value="es">Español</option>
    <option value="de">Deutsch</option>
    <option value="ru">Русский</option>
    <option value="el">Ελληνικά</option>
    <option value="ar">العربية</option>
  </select>
</div>
<script>
(function() {
  var file = window.location.pathname;
  var langs = ['en','fr','es','de','ru','el','ar'];
  var current = '%s';
  for (var i=0; i<langs.length; i++) {
    if (file.indexOf('-'+langs[i]+'.html') !== -1) {
      current = langs[i];
      break;
    }
  }
  document.getElementById('language-select').value = current;
  document.getElementById('language-select').addEventListener('change', function() {
    window.location.href = 'notes-' + this.value + '.html';
  });
})();
</script>
''' % lang

def notes_main_html(lang, c):
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="UTF-8">
  <title>{c['title']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{c['desc']}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body {{ background: #f4f7fb; font-family: 'Montserrat', Arial, sans-serif; }}
    .main-container {{ max-width: 1200px; margin: 2em auto; display: flex; justify-content: center; align-items: center; min-height: 90vh; }}
    .center-row {{ display: flex; flex-direction: row; justify-content: center; align-items: flex-start; gap: 2em; width: 100%; }}
    .article-card {{ background: #fff; border-radius: 16px; box-shadow: 0 2px 12px #e0e7ef; width: 330px; min-width: 200px; min-height: 370px; height: auto; display: flex; flex-direction: column; justify-content: space-between; align-items: flex-start; padding: 2em 1.3em 1em 1.3em; text-align: left; overflow: hidden; box-sizing: border-box; }}
    .article-card h2 {{ font-size: 1.35em; font-weight: 700; margin-bottom: 0.4em; display: flex; align-items: center; gap: 0.3em; }}
    .article-card ul, .article-card ol {{ margin-left: 1em; font-size: 1em; margin-bottom: 0.2em; padding-right: 0.2em; word-break: break-word; }}
    .article-card .btn {{
      white-space: normal;
      word-break: break-word;
      font-size: 1em;
      padding: 0.4em 0.6em;
      min-width: 0;
      width: 100%;
      box-sizing: border-box;
      margin-top: 0.6em;
      border-radius: 8px;
      font-weight: 600;
    }}
    .tool-card {{ background: #fff; border-radius: 16px; box-shadow: 0 2px 12px #e0e7ef; width: 410px; min-width: 240px; min-height: 330px; display: flex; flex-direction: column; justify-content: flex-start; align-items: stretch; padding: 2em 1.5em 1em 1.5em; text-align: left; position: relative; z-index: 1; }}
    .tool-card h3 {{ font-size: 1.45em; font-weight: 700; margin-bottom: 0.1em; }}
    .back-link {{ display: inline-block; margin-bottom: 1em; color: #185a9d; text-decoration: none; font-weight: bold; font-size: 1em; }}
    .back-link:hover {{ text-decoration: underline; color: #43cea2; }}
    .faq-section {{ margin-top: 1.1em; margin-bottom: 0.3em; font-size: 1em; background: #f7fafc; border-radius: 8px; padding: 1em; box-shadow: 0 1px 4px #e0e7ef; }}
    .faq-section summary {{ font-weight: bold; font-size: 1.07em; cursor: pointer; margin-bottom: 0.5em; }}
    @media (max-width: 1100px) {{ .main-container{{padding:0 8px;}} .center-row{{gap:1em;}} .tool-card,.article-card{{width:97vw;max-width:540px;height:auto;}} }}
    @media (max-width: 800px) {{ .main-container{{padding:0;}} .center-row{{flex-direction:column;align-items:center;}} .tool-card,.article-card{{width:98vw;max-width:540px;height:auto;}} .article-card {{ display: none !important; }} }}
    details[open] summary::after {{ content: " ▲"; font-size: 0.9em; }}
    details summary {{ cursor: pointer; padding: 0.35em 0; font-weight: bold; font-size: 1.09em; }}
    details:not([open]) summary::after {{ content: " ▼"; font-size: 0.9em; }}
    .notes-form {{ margin-bottom: 1em; display: flex; gap: 0.5em; }}
    .notes-list {{ margin-bottom: 1em; }}
    .note-item {{ background: #f7fafc; border-radius: 7px; padding: 0.6em 0.8em; margin-bottom: 0.6em; display: flex; align-items: center; justify-content: space-between; }}
    .note-meta {{ font-size: 0.9em; color: #888; margin-right: 1em; }}
    .note-btn {{ font-size: 0.9em; margin-left: 0.6em; }}
    .note-pinned {{ font-weight: bold; color: #185a9d; margin-right: 0.6em; }}
  </style>
</head>
<body>
  {html_language_selector(lang)}
  <div class="main-container">
    <div class="center-row">
      <div class="article-card">
        <div>
          <h2 style="color:#185a9d;"><i class="fa fa-note-sticky"></i> {c['howto_title']}</h2>
          <ol>
            {''.join(f"<li>{step}</li>" for step in c['howto_list'])}
          </ol>
        </div>
        <a href="{c['howto_link']}" class="btn btn-outline-primary btn-sm" style="margin-bottom:0;">{c['howto_btn']}</a>
      </div>
      <div class="tool-card">
        <a href="{c['back_main_link']}" class="back-link">{c['back_main']}</a>
        <h3><i class="fa fa-note-sticky"></i> {c['notes_title']}</h3>
        <div class="notes-section">
          <form class="notes-form" id="notesForm">
            <input type="text" id="noteInput" class="form-control" placeholder="{c['note_input']}" style="max-width:180px;">
            <button type="submit" class="btn btn-success btn-sm">{c['add_note_btn']}</button>
          </form>
          <div id="notesList" class="notes-list"></div>
        </div>
        <details class="faq-section">
          <summary>{c['faq_title']}</summary>
          <ul style="padding-left: 1em;">
            {''.join(f"<li>{item}</li>" for item in c['faq_items'])}
          </ul>
        </details>
      </div>
      <div class="article-card">
        <div>
          <h2 style="color:#185a9d;"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {c['tips_title']}</h2>
          <ul>
            {''.join(f"<li>{tip}</li>" for tip in c['tips_list'])}
          </ul>
        </div>
        <a href="{c['tips_link']}" class="btn btn-outline-primary btn-sm" style="margin-bottom:0;">{c['tips_btn']}</a>
      </div>
    </div>
  </div>
  <script>
    let notes = JSON.parse(localStorage.getItem('notesData') || '[]');
    function saveNotes() {{ localStorage.setItem('notesData', JSON.stringify(notes)); }}
    function renderNotes() {{
      const list = document.getElementById('notesList');
      list.innerHTML = '';
      if (notes.length === 0) {{
        list.innerHTML = '<div style="color:#888;">{c['no_notes']}</div>';
        return;
      }}
      notes.forEach((note, idx) => {{
        const pinned = note.pinned ? '<span class="note-pinned"><i class="fa fa-thumbtack"></i></span>' : '';
        list.innerHTML += `
          <div class="note-item">
            ${{pinned}}
            <span>${{note.text}}</span>
            <span class="note-meta">${{note.date}}</span>
            <button class="btn btn-outline-${{note.pinned ? 'secondary' : 'info'}} btn-sm note-btn" onclick="pinNote(${{idx}})" title="Pin/unpin"><i class="fa fa-thumbtack"></i></button>
            <button class="btn btn-outline-danger btn-sm note-btn" onclick="deleteNote(${{idx}})"><i class="fa fa-trash"></i></button>
          </div>
        `;
      }});
    }}
    document.getElementById('notesForm').addEventListener('submit', function(e){{
      e.preventDefault();
      const text = document.getElementById('noteInput').value.trim();
      if (!text) return;
      notes.unshift({{ text, date: new Date().toLocaleString(), pinned: false }});
      saveNotes();
      document.getElementById('noteInput').value = "";
      renderNotes();
    }});
    window.deleteNote = function(idx){{
      notes.splice(idx, 1);
      saveNotes();
      renderNotes();
    }}
    window.pinNote = function(idx){{
      notes[idx].pinned = !notes[idx].pinned;
      if (notes[idx].pinned) {{
        const pinnedNote = notes.splice(idx, 1)[0];
        notes.unshift(pinnedNote);
      }}
      saveNotes();
      renderNotes();
    }}
    renderNotes();
  </script>
<footer>
  {c['footer']}<br>
  <a href="privacy.html">{c['privacy']}</a> &bull;
  <a href="terms.html">{c['terms']}</a> &bull;
  <a href="contact.html">{c['contact']}</a>
</footer>
</body>
</html>
"""

def main():
    os.makedirs("notes_pages", exist_ok=True)
    for lang, _ in LANGS:
        with open(f"notes_pages/notes-{lang}.html", "w", encoding="utf-8") as f:
            f.write(notes_main_html(lang, notes_content[lang]))
    print("All notes main pages generated in ./notes_pages")

if __name__ == "__main__":
    main()