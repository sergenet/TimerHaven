import json

with open('meeting-tips-translations.json', encoding='utf-8') as f:
    translations = json.load(f)

with open('meeting-tips-template.html', encoding='utf-8') as f:
    template = f.read()

for lang, t in translations.items():
    dir_attr = ' dir="rtl"' if lang == "ar" else ''
    tips_html = "\n".join(f"<li>{tip}</li>" for tip in t['tips'])
    didyou_html = "\n".join(f"<li>{fact}</li>" for fact in t['didyouknow'])
    html = template.format(
        lang=lang,
        dir=dir_attr,
        title=t['title'],
        intro=t['intro'],
        tips=tips_html,
        didyou=didyou_html,
        back=t['back']
    )
    filename = f"meeting-tips-{lang}.html"
    with open(filename, "w", encoding="utf-8") as outf:
        outf.write(html)
    print(f"Generated {filename}")