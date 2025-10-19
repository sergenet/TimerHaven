import json

with open('meeting-howto-translations.json', encoding='utf-8') as f:
    translations = json.load(f)

with open('meeting-howto-template.html', encoding='utf-8') as f:
    template = f.read()

for lang, t in translations.items():
    dir_attr = ' dir="rtl"' if lang == "ar" else ''
    steps_html = "\n".join(f"<li>{step}</li>" for step in t['steps'])
    faqs_html = "\n".join(f"<li>{faq}</li>" for faq in t['faqs'])
    tips_html = "\n".join(f"<li>{tip}</li>" for tip in t['tips'])
    html = template.format(
        lang=lang,
        dir=dir_attr,
        title=t['title'],
        intro=t['intro'],
        steps=steps_html,
        faqs=faqs_html,
        tips=tips_html,
        back=t['back']
    )
    filename = f"meeting-how-to-{lang}.html"
    with open(filename, "w", encoding="utf-8") as outf:
        outf.write(html)
    print(f"Generated {filename}")