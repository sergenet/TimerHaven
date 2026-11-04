#!/usr/bin/env python3
"""restore-english-pages.py — put the English text back on pages a locale run overwrote.

Why: the root "how-to" / "tips" / landing pages for calendar, countdown,
currency, focus-music, habit and meeting have no -en sibling, so the plain file
IS the English page. A locale generation run wrote another language's text into
those filenames: 17 now serve Arabic and 2 serve French, at English URLs.

The English originals are still in git (the overwrite was never committed), so
this restores the committed text instead of rewriting the content by hand.

Guards, because a blind checkout would be dangerous:
  * only files at the site root whose name has no -xx language suffix
  * only when the working copy is NOT Latin-dominant AND the committed blob IS
    Latin-dominant (i.e. the commit holds the English version)
  * the file's <title> must also be Latin in the commit, so a page whose title
    was translated but body left English is not silently reverted
Run: python scripts/restore-english-pages.py [--dry-run] [--rev HEAD]
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DRY = '--dry-run' in sys.argv
REV = sys.argv[sys.argv.index('--rev') + 1] if '--rev' in sys.argv else 'HEAD'

SUFFIX_RE = re.compile(r'-(ar|de|el|en|es|fr|ru)\.html$')
ARABIC = re.compile(r'[\u0600-\u06FF]')
CYRILLIC = re.compile(r'[\u0400-\u04FF]')
GREEK = re.compile(r'[\u0370-\u03FF]')
LATIN_WORD = re.compile(r'\b(the|and|with|your|this|that|from|for|you|how|use|tips)\b', re.I)


def body_text(html):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.S | re.I)
    return re.sub(r'<[^>]+>', ' ', h)


def profile(html):
    b = body_text(html)
    return {
        'arabic': len(ARABIC.findall(b)),
        'cyrillic': len(CYRILLIC.findall(b)),
        'greek': len(GREEK.findall(b)),
        'latin': len(re.findall(r'[A-Za-z]', b)),
        'en_words': len(LATIN_WORD.findall(b)),
    }


def is_english(p):
    """Latin-dominant prose with English function words present."""
    scripted = max(p['arabic'], p['cyrillic'], p['greek'])
    return p['latin'] > 200 and p['latin'] > scripted * 3 and p['en_words'] >= 5


def is_foreign(p):
    scripted = max(p['arabic'], p['cyrillic'], p['greek'])
    return scripted > p['latin']


def title_of(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def git_show(path):
    r = subprocess.run(['git', 'show', f'{REV}:{path}'], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode('utf-8', 'replace')


candidates = [f for f in sorted(os.listdir('.'))
              if f.endswith('.html') and not SUFFIX_RE.search(f)]

restored, skipped, no_history = [], [], []
for f in candidates:
    cur = open(f, encoding='utf-8', errors='replace').read()
    if not is_foreign(profile(cur)):
        continue
    base = f[:-5]
    if os.path.exists(base + '-en.html'):
        skipped.append((f, 'has an -en sibling, so this file is not the English page'))
        continue
    old = git_show(f)
    if old is None:
        no_history.append(f)
        continue
    po = profile(old)
    if not is_english(po) or not is_english(profile({'x': title_of(old)}) if False else po):
        skipped.append((f, f'{REV} version is not English (latin={po["latin"]}, ar={po["arabic"]})'))
        continue
    old_title = title_of(old)
    if max(len(ARABIC.findall(old_title)), len(CYRILLIC.findall(old_title)),
           len(GREEK.findall(old_title))) > len(re.findall(r'[A-Za-z]', old_title)):
        skipped.append((f, f'{REV} title is not English: {old_title[:40]!r}'))
        continue
    restored.append((f, len(cur), len(old), old_title[:58]))
    if not DRY:
        open(f, 'w', encoding='utf-8', newline='').write(old)

print(f'{DRY and "[dry-run] " or ""}restore English text where a locale run overwrote it')
print(f'  root pages checked        : {len(candidates)}')
print(f'  restored                  : {len(restored)}')
for f, a, b, t in restored:
    print(f'      {f:32s} {a} -> {b} bytes   {t!r}')
print(f'  skipped                   : {len(skipped)}')
for f, why in skipped:
    print(f'      {f:32s} {why}')
if no_history:
    print(f'  no {REV} history (left as-is): {len(no_history)}')
    for f in no_history:
        print(f'      {f}')
