#!/usr/bin/env python3
"""fix-descriptions.py — give every indexable page a meta description.

245 of 709 indexable pages had none, so Google wrote its own snippet from
whatever it found first - often a nav label or a list of link text. The
description is not a ranking factor, but it is the only text a searcher reads
before deciding to click, and a page whose snippet is boilerplate loses the
click to a page that wrote one.

The description is built from the page's own opening prose, in the page's own
language, so it always matches what the page says. No translation is involved:
the text already exists on the page. Where a page has no prose at all (a short
tool page that is mostly buttons), a per-language template is used instead.

Run: python scripts/fix-descriptions.py [--dry-run] [--verbose]
"""
import html as html_mod
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

DRY = '--dry-run' in sys.argv
VERBOSE = '--verbose' in sys.argv
LIMIT = 155

DESC_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*>', re.I)
DESC_CONTENT_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', re.I)

# A page with no prose of its own gets this instead of an empty or boilerplate
# snippet. Keyed by language so the fallback reads naturally.
FALLBACK = {
    'en': '{title_no_brand} - free online tool and practical guide from TimerHaven.',
    'de': '{title_no_brand} - kostenloses Online-Tool und praktische Anleitung von TimerHaven.',
    'es': '{title_no_brand}: herramienta online gratuita y guía práctica de TimerHaven.',
    'fr': '{title_no_brand} : outil en ligne gratuit et guide pratique par TimerHaven.',
    'ru': '{title_no_brand} - бесплатный онлайн-инструмент и практическое руководство TimerHaven.',
    'el': '{title_no_brand} - δωρεάν διαδικτυακό εργαλείο και πρακτικός οδηγός από το TimerHaven.',
    'ar': '{title_no_brand} - أداة مجانية عبر الإنترنت ودليل عملي من TimerHaven.',
}


# Repo scaffolding, scheduled for removal from the web root - never summarised.
SKIP = {'Promotion_Kit.html'}


def clean_text(fragment):
    fragment = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<[^>]+>', ' ', fragment)
    text = html_mod.unescape(fragment)
    text = re.sub(r'\s+', ' ', text).strip()
    # Tag stripping leaves a space where an inline tag met punctuation:
    # <strong>Kalender</strong>-Tool became "Kalender -Tool".
    text = re.sub(r'\s+([,.;:!?»]|-(?=[^ ]))', r'\1', text)
    return text.strip()


def usable(text):
    """Reject text that is not a sentence about the page."""
    if 'file:///' in text or re.search(r'[A-Za-z]:\\', text):
        return False
    if not re.search(r'[a-z\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff\u0600-\u06ff]', text):
        return False
    return ' ' in text


def body_of(html):
    i = html.lower().find('<body')
    body = html[i:] if i >= 0 else html
    # Navigation, cookie banners and footers are never a good summary.
    for tag in ('nav', 'header', 'footer', 'aside'):
        body = re.sub(rf'<{tag}\b.*?</{tag}>', ' ', body, flags=re.S | re.I)
    return body


def candidates(html):
    body = body_of(html)
    out = []
    for m in re.findall(r'<p\b[^>]*>(.*?)</p>', body, re.S | re.I):
        t = clean_text(m)
        if len(t) >= 60 and usable(t):
            out.append(t)
    for m in re.findall(r'<li\b[^>]*>(.*?)</li>', body, re.S | re.I):
        t = clean_text(m)
        if len(t) >= 50 and usable(t):
            out.append(t)
    for m in re.findall(r'<h2\b[^>]*>(.*?)</h2>', body, re.S | re.I):
        t = clean_text(m)
        if len(t) >= 30 and usable(t):
            out.append(t)
    return out


def fit(text):
    """Trim to a sentence-ish 155 characters without cutting mid-word."""
    text = re.sub(r'\s+', ' ', text).strip()
    # A paragraph that introduces a list ends in a colon; a snippet that ends in
    # one reads like it was cut off.
    text = re.sub(r'\s*[:：]$', '', text)
    if len(text) <= LIMIT:
        return text
    cut = text[:LIMIT]
    # Prefer ending on a sentence boundary inside the limit.
    for mark in ('. ', '! ', '? ', '» ', ': '):
        pos = cut.rfind(mark)
        if pos >= 90:
            return cut[:pos + 1].strip()
    pos = cut.rfind(' ')
    return cut[:pos].rstrip(' ,;:-–—') + '…'


def title_no_brand(title):
    return re.sub(r'\s*[|—-]\s*TimerHaven\s*$', '', title).strip() or title


def main():
    written = templated = trimmed = 0
    samples = []
    for rel in G.pages():
        html = G.read(rel)
        if G.is_stub(html) or G.is_noindex(html) or rel in SKIP:
            continue
        head = G.head_of(html)
        existing = DESC_CONTENT_RE.search(head)
        if existing and existing.group(1).strip():
            # Present but too long to survive a search result: Google cuts it
            # around 160 characters and the tail is never read anyway.
            current = html_mod.unescape(existing.group(1))
            if len(current) > 160:
                short = fit(current)
                if short and short != current:
                    attr = html_mod.escape(short, quote=True)
                    new = html.replace(existing.group(0),
                                       f'<meta name="description" content="{attr}">', 1)
                    trimmed += 1
                    if not DRY:
                        with open(os.path.join(G.ROOT, rel), 'w', encoding='utf-8', newline='') as fh:
                            fh.write(new)
            continue
        title = G.title_of(html)
        picked = next((c for c in candidates(html)), None)
        if picked:
            desc = fit(picked)
        else:
            lang = G.lang_of(rel)
            desc = fit(FALLBACK.get(lang, FALLBACK['en']).format(title_no_brand=title_no_brand(title)))
            templated += 1
        if not desc:
            continue
        attr = html_mod.escape(desc, quote=True)
        tag = f'<meta name="description" content="{attr}">'
        new = html
        if existing:            # present but empty
            new = new.replace(existing.group(0), tag, 1)
        else:
            m = re.search(r'<title[^>]*>.*?</title>', head, re.S | re.I)
            if m:
                new = html[:m.end()] + '\n' + tag + html[m.end():]
            else:
                i = html.lower().find('</head>')
                new = html[:i] + tag + '\n' + html[i:]
        if new == html:
            continue
        written += 1
        if len(samples) < 6:
            samples.append((rel, desc))
        if VERBOSE:
            print(f'  + {rel}')
        if not DRY:
            with open(os.path.join(G.ROOT, rel), 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)

    print(f'{"[dry-run] " if DRY else ""}descriptions added: {written}')
    print(f'  from page prose : {written - templated}')
    print(f'  from template   : {templated}')
    print(f'  over-long trimmed: {trimmed}')
    for rel, desc in samples:
        print(f'    {rel}\n      {desc}')


if __name__ == '__main__':
    main()
