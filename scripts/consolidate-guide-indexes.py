#!/usr/bin/env python3
"""consolidate-guide-indexes.py — one URL per tool guide.

Five guide folders contain two copies of the same page:

    el/notes/index.html            + el/notes/notes-index.html
    el/pomodoro-timer/index.html   + el/pomodoro-timer/pomodoro-index.html
    el|es|ru/task-timer/index.html + .../task-timer-index.html

The `-index.html` copy is the one every locale uses, and the one the sitemap
generator emits, so it is the canonical URL. The bare directory form is only
served by `DirectoryIndex index.html` in those five folders - which is why
`/el/notes/` carried an hreflang cluster naming `/en/notes/`, `/fr/notes/` and
four more URLs that 404: no other locale has an index.html in a guide folder.

Each alias becomes a redirect stub (the convention already used for the retired
-how pages), plus an .htaccess 301 so the redirect happens before the body is
ever served. After this, `_i18n_groups.pages()` skips the aliases as stubs and
every advertised hreflang URL resolves to a page that advertises it back.

Run: python scripts/consolidate-guide-indexes.py [--dry-run]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

DRY = '--dry-run' in sys.argv
BASE = 'https://timerhaven.com'

STUB = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redirecting to {name} | TimerHaven</title>
<link rel="canonical" href="{base}{path}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={path}">
<script>location.replace('{path}');</script>
</head>
<body style="font-family:system-ui,sans-serif;padding:40px;text-align:center">
<p>This page has moved to <a href="{path}">{path}</a>.</p>
</body>
</html>
"""

# Tools whose folder name differs from the root file stem (see _i18n_groups).
def aliases():
    """[(alias rel, canonical rel)] for guide folders holding both copies."""
    found = []
    for lang in G.LANGS:
        for folder in sorted(set(G.FOLDER_TO_STEM)):
            d = os.path.join(G.ROOT, lang, folder)
            if not os.path.isdir(d):
                continue
            files = {f for f in os.listdir(d) if f.endswith('.html')}
            alias = 'index.html'
            if alias not in files:
                continue
            # The guide page is not always named after its folder
            # (el/pomodoro-timer holds pomodoro-index.html).
            candidates = [f for f in files if f.endswith('-index.html') and f != alias]
            canon = f'{folder}-index.html'
            if canon not in candidates:
                if len(candidates) != 1:
                    print(f'  ! {lang}/{folder}: ambiguous guide page {sorted(candidates)} - skipped')
                    continue
                canon = candidates[0]
            found.append((f'{lang}/{folder}/{alias}', f'{lang}/{folder}/{canon}'))
    return found


def htaccess_rules(pairs):
    """Anchored rules for /el/notes/ and /el/notes/index.html only.

    mod_alias `Redirect` matches by prefix, so `Redirect 301 /el/notes/` would
    also catch `/el/notes/notes-index.html` and send the canonical page to
    itself. RedirectMatch anchored to the optional index.html is exact.
    """
    lines = []
    for alias_rel, canon_rel in pairs:
        folder_path = '/' + alias_rel[:-len('index.html')]        # /el/notes/
        to_url = f'{BASE}/{canon_rel}'
        lines.append(f'RedirectMatch 301 ^{re.escape(folder_path)}(?:index\\.html)?$ {to_url}')
    return lines


def main():
    pairs = aliases()
    print(f'guide aliases found: {len(pairs)}')

    for alias_rel, canon_rel in pairs:
        path = '/' + canon_rel
        lang = canon_rel.split('/')[0]
        body = STUB.format(lang=lang, name=canon_rel.split('/')[-1],
                           base=BASE, path=path)
        if not DRY:
            with open(os.path.join(G.ROOT, alias_rel), 'w', encoding='utf-8', newline='') as fh:
                fh.write(body)
        print(f'  stub  {alias_rel}  ->  {path}')

    # The es task-timer copy had its canonical pointed at the directory URL by an
    # earlier pass; with the alias retired its own URL is canonical again.
    revert = 'es/task-timer/task-timer-index.html'
    html = G.read(revert)
    self_url = f'{BASE}/{revert}'
    fixed = re.sub(r'(<link\s+rel=["\']canonical["\'][^>]*href=["\'])[^"\']*(["\'])',
                   lambda m: m.group(1) + self_url + m.group(2), html, count=1, flags=re.I)
    if fixed != html:
        if not DRY:
            with open(os.path.join(G.ROOT, revert), 'w', encoding='utf-8', newline='') as fh:
                fh.write(fixed)
        print(f'  canon {revert}  ->  {self_url}')

    # .htaccess 301s, appended once under their own heading.
    ht_path = os.path.join(G.ROOT, '.htaccess')
    text = open(ht_path, encoding='utf-8', errors='replace').read()
    # Rewrite the whole managed block so an earlier (prefix-matching) version
    # cannot survive alongside the anchored one.
    text = re.sub(r'# --- guide directory aliases[^\n]*\n(?:Redirect[^\n]*\n)*\n?', '', text)
    wanted = htaccess_rules(pairs)
    heading = '# --- guide directory aliases (301 to the -index page) ---'
    block = '\n'.join([heading] + wanted) + '\n\n'
    marker = '# --- PHASE 12: PERFORMANCE EXCELLENCE ---'
    if marker in text:
        text = text.replace(marker, block + marker, 1)
    else:
        text = text.rstrip('\n') + '\n\n' + block
    if not DRY:
        with open(ht_path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    print(f'  .htaccess: {len(wanted)} anchored redirect(s) written')


if __name__ == '__main__':
    main()
