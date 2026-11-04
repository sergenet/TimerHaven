#!/usr/bin/env python3
"""fix-foreign-redirects.py — retire the pages a locale run left in the wrong language.

After restore-english-pages.py put back the ten English originals that git still
held, nine root pages remained with no English source anywhere:

  * seven Arabic copies (five "-how" duplicates of an existing "-how-to" page,
    plus focus.html and habit.html, which are the Arabic text of
    focus-music-tips.html and habit-tips.html)
  * two French copies of the meeting-planner how-to, for which no English page
    was ever written

None of them is in the sitemap and only focus.html is linked from anywhere, so
the right fix is to send visitors and crawlers to the real page rather than to
invent translated content.

Two layers, because each covers a failure of the other:
  1. a 301 rule in .htaccess — what a browser and Google actually receive
  2. a stub file with a canonical to the target, noindex, and a meta refresh —
     so the page is still correct if the rewrite rules are ever lost or the
     site is served without .htaccess

Run: python scripts/fix-foreign-redirects.py [--dry-run]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DRY = '--dry-run' in sys.argv

# corrupted page -> the English page it is a translation of
MAP = {
    'calendar-how.html': 'calendar-how-to.html',
    'countdown-how.html': 'countdown-how-to.html',
    'currency-how.html': 'currency-how-to.html',
    'focus-music-how.html': 'focus-music-how-to.html',
    'habit-how.html': 'habit-how-to.html',
    'focus.html': 'focus-music-tips.html',
    'habit.html': 'habit-tips.html',
    # No English "how to use the meeting planner" page exists; the planner
    # itself carries the instructions, so that is where these now lead.
    'meeting-how-to.html': 'meeting-planner-en.html',
    'meeting-how.html': 'meeting-planner-en.html',
}

STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redirecting to {target} | TimerHaven</title>
<link rel="canonical" href="https://timerhaven.com/{target}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url=/{target}">
<script>location.replace('/{target}');</script>
</head>
<body style="font-family:system-ui,sans-serif;padding:40px;text-align:center">
<p>This page has moved to <a href="/{target}">/{target}</a>.</p>
</body>
</html>
"""

# ---- 1. stubs -------------------------------------------------------------
for src, target in MAP.items():
    if not os.path.exists(target):
        print(f'  ! {src}: target {target} does not exist, skipped')
        continue
    if not os.path.exists(src):
        print(f'  · {src}: already gone')
        continue
    if not DRY:
        with open(src, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(STUB.format(target=target))
    print(f'  {src:24s} -> {target}')

# ---- 2. .htaccess rules ---------------------------------------------------
ht = open('.htaccess', encoding='utf-8', errors='replace').read()
BEGIN = '# --- pages retired 2026-11-04 (foreign-language copies of an English page) ---'
if BEGIN in ht:
    print('\n  .htaccess already carries the retirement block, left alone')
else:
    lines = [BEGIN]
    for src, target in MAP.items():
        lines.append(f'Redirect 301 /{src} https://timerhaven.com/{target}')
    block = '\n'.join(lines) + '\n'
    # Append after the last existing Redirect line so all 301s stay together.
    idx = ht.rfind('\nRedirect 301 ')
    if idx >= 0:
        end = ht.find('\n', idx + 1)
        new = ht[:end + 1] + '\n' + block + ht[end + 1:]
    else:
        new = ht.rstrip('\n') + '\n\n' + block
    if not DRY:
        open('.htaccess', 'w', encoding='utf-8', newline='\n').write(new)
    print(f'\n  .htaccess: {len(MAP)} 301 rule(s) {"would be " if DRY else ""}added')
