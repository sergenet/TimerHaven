"""Assemble blog/how-long-should-a-break-be.html.

The head is taken verbatim from an existing article (flow-state-guide.html) so the
new page inherits the identical CSS, fonts, analytics and icon setup; only the
per-page fields are swapped. The body comes from scripts/break_body.html.

Run: python scripts/build_break_article.py
"""
import json
import os
import re
import sys

TEMPLATE = "flow-state-guide.html"
OUT = "how-long-should-a-break-be.html"
BODY = os.path.join("scripts", "break_body.html")

SLUG = "how-long-should-a-break-be"
URL = f"https://timerhaven.com/blog/{SLUG}.html"
TITLE = "How Long Should a Break Be? The Science of Rest | TimerHaven"
HEADLINE = "How Long Should a Break Be?"
DESCRIPTION = (
    "How long should a break be? The research points to 5-15 minutes after a 50-90 minute "
    "block of work. Here is the science of break length, and how to time breaks you will "
    "actually take."
)
OG_DESCRIPTION = (
    "The research-backed answer to how long a break should be, why phone breaks do not "
    "restore you, and how to time breaks that you will actually take."
)
DATE = "2026-10-28"
IMAGE = "https://timerhaven.com/images/blog/break-length-featured.webp"

FAQ = [
    (
        "Is a 15-minute break too long?",
        "For deep work, no. Fifteen minutes is close to ideal after a 50 to 90 minute block: long "
        "enough to disengage, short enough to re-enter without losing the thread. Problems start past "
        "roughly 30 minutes, where the cost of getting back into the task outweighs the recovery.",
    ),
    (
        "Should I time my breaks or take them when I feel tired?",
        "Time them. Feeling tired is a lagging signal - by the time you notice it, you have already been "
        "working below your best. A timer takes the break before fatigue, which is when it costs least.",
    ),
    (
        "Do breaks break your focus?",
        "Only bad ones. A break spent on a screen, or one long enough to lose context, costs momentum. A "
        "short break spent moving, looking outside or talking to someone restores the attention the next "
        "block needs.",
    ),
    (
        "How many breaks should I take in a day?",
        "For a focused eight-hour day, six to nine short breaks is typical - roughly one per hour of work, "
        "with a longer one mid-morning or after lunch.",
    ),
]


def swap(text, pattern, replacement, label):
    new, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if n != 1:
        sys.exit(f"FAILED to replace {label!r} in template")
    return new


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    blog = os.path.join(root, "blog")

    template = open(os.path.join(blog, TEMPLATE), encoding="utf-8", errors="strict").read()
    head = template.split("<body>", 1)[0]

    head = swap(head, r"<title>.*?</title>", f"<title>{TITLE}</title>", "title")
    head = swap(head, r'<meta name="description"\s*content=".*?">',
                f'<meta name="description"\n        content="{DESCRIPTION}">', "description")
    head = swap(head, r'<meta name="datePublished" content="[^"]*">',
                f'<meta name="datePublished" content="{DATE}">\n'
                f'    <meta name="dateModified" content="{DATE}">', "datePublished")
    head = swap(head, r'<link rel="canonical" href="[^"]*" />',
                f'<link rel="canonical" href="{URL}" />', "canonical")
    head = swap(head, r'(<link rel="alternate"[^>]*>\s*){1,12}',
                f'<link rel="alternate" href="{URL}" hreflang="en" />\n'
                f'  <link rel="alternate" href="{URL}" hreflang="x-default" />\n    ',
                "hreflang block")

    # JSON-LD BlogPosting fields
    head = swap(head, r'"headline": "[^"]*"', f'"headline": {json.dumps(HEADLINE)}', "schema headline")
    head = swap(head, r'"description": "[^"]*"', f'"description": {json.dumps(DESCRIPTION)}', "schema description")
    head = swap(head, r'"datePublished": "[^"]*"', f'"datePublished": "{DATE}"', "schema date")
    head = swap(head, r'("datePublished": "[^"]*",)', r'\1\n      "dateModified": "' + DATE + '",',
                "schema dateModified")
    head = swap(head, r'"image": "https://timerhaven\.com/images/blog/[^"]*"',
                f'"image": "{IMAGE}"', "schema image")

    # Open Graph / Twitter
    head = swap(head, r'<meta property="og:title" content="[^"]*">',
                f'<meta property="og:title" content="{TITLE}">', "og:title")
    head = swap(head, r'<meta property="og:description"\s*content="[^"]*">',
                f'<meta property="og:description"\n        content="{OG_DESCRIPTION}">', "og:description")
    head = swap(head, r'<meta property="og:image" content="[^"]*">',
                f'<meta property="og:image" content="{IMAGE}">', "og:image")
    head = swap(head, r'<meta property="og:url" content="[^"]*">',
                f'<meta property="og:url" content="{URL}">', "og:url")
    head = swap(head, r'<meta name="twitter:image" content="[^"]*">',
                f'<meta name="twitter:image" content="{IMAGE}">', "twitter:image")

    # FAQ block, appended to the head so it does not disturb the template
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQ
        ],
    }
    faq_markup = (
        '  <script type="application/ld+json">\n'
        + json.dumps(faq_ld, indent=2, ensure_ascii=False)
        + "\n  </script>\n"
    )
    # The template has no explicit </head>; insert before the body instead.
    if "</head>" in head:
        head = head.replace("</head>", faq_markup + "</head>")
    else:
        head = head + faq_markup

    body = open(BODY, encoding="utf-8").read()
    doc = head + "<body>\n" + body

    out_path = os.path.join(blog, OUT)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
