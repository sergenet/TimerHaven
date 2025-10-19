import json

required_keys = [
    "tool_title", "tool_desc", "back_menu", "label_language", "language_options",
    "label_name", "placeholder_name", "label_city", "placeholder_city", "city_options",
    "button_add", "label_date", "label_time", "button_show_times", "faq_title", "faqs"
]

with open('meeting-planner-translations.json', encoding='utf-8') as f:
    translations = json.load(f)

with open('meeting-planner-template.html', encoding='utf-8') as f:
    template = f.read()

print("Languages found in JSON:", list(translations.keys()))

for lang, t in translations.items():
    print(f"\nProcessing: {lang}")
    print("Available keys:", list(t.keys()))

    # Check for missing keys
    missing = [k for k in required_keys if k not in t]
    if missing:
        print(f"ERROR: Language '{lang}' is missing keys: {missing}")
        continue

    dir_attr = ' dir="rtl"' if lang == "ar" else ''
    html = template.format(
        lang=lang,
        dir=dir_attr,
        tool_title=t['tool_title'],
        tool_desc=t['tool_desc'],
        back_menu=t['back_menu'],
        label_language=t['label_language'],
        language_options=t['language_options'],
        label_name=t['label_name'],
        placeholder_name=t['placeholder_name'],
        label_city=t['label_city'],
        placeholder_city=t['placeholder_city'],
        city_options=t['city_options'],
        button_add=t['button_add'],
        label_date=t['label_date'],
        label_time=t['label_time'],
        button_show_times=t['button_show_times'],
        faq_title=t['faq_title'],
        faqs=t['faqs']
    )
    filename = f"meeting-planner-{lang}.html"
    with open(filename, "w", encoding="utf-8") as outf:
        outf.write(html)
    print(f"Generated {filename}")