#!/usr/bin/env python3
"""fix-untranslated-titles.py — a translated page should not be titled in English.

Four locale pages were left with the bare English product name as their <title>
("Task Timer — TimerHaven"), so a Spanish, Greek or Russian searcher saw English
above a translated snippet — the same snippet-vs-title mismatch that costs the
click even when the page ranks.

No translation is generated here. The same tool is already published in the same
language under the suffix scheme (timer-es.html, timer-el.html, timer-ru.html),
so those titles are reused: they are human-reviewed, on-brand, and already the
words that language's visitors see elsewhere on the site.

Run: python scripts/fix-untranslated-titles.py [--dry-run]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

DRY = '--dry-run' in sys.argv
BARE = re.compile(r'(Task )?Timer\s*[\u2013\u2014-]\s*TimerHaven')

fixed = 0
for rel in G.pages():
    if rel in G.NON_CONTENT:
        continue
    lang = G.lang_of(rel)
    if lang == 'en':
        continue
    html = G.read(rel)
    if G.is_stub(html):
        continue
    title = G.title_of(html)
    if not BARE.fullmatch(title):
        continue
    replacement = G.translated_title_for(rel, html)
    if not replacement:
        print(f'  ! {rel}: no translated source found, left alone')
        continue
    new_html = re.sub(r'(<title[^>]*>)(.*?)(</title>)',
                      lambda m: m.group(1) + replacement + m.group(3),
                      html, count=1, flags=re.S | re.I)
    if new_html == html:
        print(f'  ! {rel}: title not replaced')
        continue
    if not DRY:
        with open(os.path.join(G.ROOT, rel), 'w', encoding='utf-8', newline='') as fh:
            fh.write(new_html)
    fixed += 1
    print(f'  {rel:38s} {title!r}')
    print(f'      -> {replacement!r}')

print(f'{DRY and "[dry-run] " or ""}retitled {fixed} page(s)')
