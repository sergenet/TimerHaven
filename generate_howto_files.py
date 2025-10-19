import json

# Load translations
with open('meeting-howto-translations.json', encoding='utf-8') as f:
    translations = json.load(f)

# HTML template with placeholders
template = """
<!DOCTYPE html>
<html lang="{lang}"{dir}>
<head>
  <meta charset="UTF-8">
  <title>{title} — TimerHaven</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Step-by-step instructions for Meeting Planner.">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background: #f4f7fb; font-family: 'Montserrat', Arial, sans-serif; }}
    .container {{ max-width: 700px; margin: 2em auto; background: #fff; border-radius: 14px; box-shadow: 0 2px 12px #e0e7ef; padding: 2em; }}
    h1 {{ color: #185a9d; font-size: 2em; margin-bottom: 0.8em; }}
    h2 {{ font-size: 1.35em; margin-top: 2em; }}
    ul, ol {{ margin-left: 1.4em; }}
    .back-link {{ display: inline-block; margin-bottom: 1em; color: #007bff; text-decoration: none; font-weight: bold; }}
    .back-link:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="container">
    <a href="meeting-planner.html" class="back-link"><i class="fa fa-arrow-left"></i> {back}</a>
    <h1><i class="fa fa-users"></i> {title}</h1>
    <p>{intro}</p>
    <h2>Step-by-Step Guide</h2>
    <ol>
      {steps}
    </ol>
    <h2>FAQs</h2>
    <ul>
      {faqs}
    </ul>
    <h2>Tips for Success</h2>
    <ul>
      {tips}
    </ul>
    <p>
      <a href="meeting-planner.html" class="btn btn-outline-primary btn-sm mt-3">{back}</a>
    </p>
  </div>
<footer>
  &copy; 2025 TimerHaven.
</footer>
</body>
</html>
"""

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
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {filename}")