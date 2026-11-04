#!/usr/bin/env python3
"""apply-adsense.py — put AdSense on TimerHaven, consent-gated.

State before this ran: of 731 pages exactly one (index-en.html) carried the
AdSense loader, and no page carried an ad unit at all. ads.txt has advertised
the publisher since day one, so the account was verified for a site that could
never earn: there was nothing to earn from.

What this adds, idempotently, to every content page:
  1. assets/css/consent.css + assets/js/consent.js  (the existing consent gate;
     without the stylesheet the banner renders unstyled)
  2. one in-content unit
  3. one footer unit

The units carry NO inline push(). consent.js pushes them once the AdSense
library it appends has loaded, which only happens after consent — so ad requests
cannot fire before consent.

Placement rules, chosen so ads never interrupt a tool:
  * in-content unit goes before the first <h2> that appears BEFORE <footer>.
    On a timer/stopwatch page the entire tool is above the first section, so the
    unit lands under the tool, above the explanatory copy.
  * footer unit goes immediately above <footer> (or before </body> if the page
    has no footer element).
  * if those two anchors are within 400 characters, only the footer unit is
    added — a page that short must not ship two stacked units.

Run: python scripts/apply-adsense.py [--dry-run] [--verbose]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DRY = '--dry-run' in sys.argv
VERBOSE = '--verbose' in sys.argv

CLIENT = 'ca-pub-0467059729557007'
SLOTS = {
    'in-article': '2835722251',
    'footer': '1522640584',
}

LABELS = {
    'ar': 'إعلان', 'de': 'Anzeige', 'el': 'Διαφήμιση', 'es': 'Anuncio',
    'fr': 'Publicité', 'ru': 'Реклама',
}

SKIP_DIRS = {
    'node_modules', '_site', '.git', '_attic', 'scripts', 'assets', 'images',
    'images2', 'Backup_20260222', 'Backup_20260222_Refined', '_SYNCAPP',
    'chrome_store_screenshots', 'YouTube experiments', 'chrome_extension',
    'timerhaven-extension', 'timerhaven-extension-v2', 'components', 'android',
    'ios', 'data', 'docs', 'api', 'newsletter',
}
# Pages that must not carry ads: legal/utility surfaces, and the marketing kit.
SKIP_FILES = {
    'contact.html', 'privacy.html', 'terms.html', '404.html', 'offline.html',
    'thank-you.html', 'premium.html', 'checkout.html', 'Promotion_Kit.html',
}

MIN_GAP = 400  # chars between the two anchors


def unit(kind, label):
    return (
        f'<div class="th-ad-slot" data-ad-placement="{kind}" '
        f'style="margin:24px auto;max-width:728px;min-height:90px;text-align:center;overflow:hidden">\n'
        f'<span class="th-ad-label" style="display:block;font-size:10px;letter-spacing:.1em;'
        f'text-transform:uppercase;opacity:.55;margin-bottom:4px">{label}</span>\n'
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{CLIENT}" '
        f'data-ad-slot="{SLOTS[kind]}" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
        f'</div>'
    )


def pages():
    out = []
    for dirpath, dirnames, filenames in os.walk('.'):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for f in filenames:
            if not f.endswith('.html') or f in SKIP_FILES:
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), '.').replace(os.sep, '/')
            if ' - Copy' in rel or '(backup' in rel.lower() or rel.startswith('backup'):
                continue
            out.append(rel)
    return sorted(out)


def is_redirect_stub(html):
    return 'http-equiv="refresh"' in html and 'Redirecting to' in html


def lang_label(html):
    m = re.search(r'<html[^>]*\blang=["\']([a-zA-Z-]+)', html)
    code = (m.group(1) if m else 'en').lower().split('-')[0]
    return LABELS.get(code, 'Advertisement')


def ensure_consent(html):
    """Add the consent stylesheet + script once, root-absolute so it works from any depth."""
    changed = False
    head_end = html.lower().find('</head>')
    if head_end < 0:
        return html, changed
    head = html[:head_end]
    add = ''
    if 'consent.css' not in head:
        add += '\n  <link rel="stylesheet" href="/assets/css/consent.css" media="print" onload="this.media=\'all\'">'
    if 'consent.js' not in head:
        add += '\n  <script src="/assets/js/consent.js" defer></script>'
    if add:
        html = head + add + html[head_end:]
        changed = True
    return html, changed


def protected(html):
    """Ranges that must never be split: script and style bodies.

    Several tool pages build markup inside JavaScript (template strings), and a
    <h2>/<footer> lookalike in there is not a real anchor. Inserting into one
    would break the tool, so any candidate inside these ranges is rejected.
    """
    return [(m.start(), m.end()) for m in
            re.finditer(r'<(script|style)\b[^>]*>.*?</\1\s*>', html, re.S | re.I)]


def inside(pos, ranges):
    return any(a <= pos < b for a, b in ranges)


def apply_units(html, label):
    changed = False
    low = html.lower()
    guard = protected(html)
    footer = low.find('<footer')
    if footer >= 0 and inside(footer, guard):
        footer = -1
    body_end = low.rfind('</body>')

    # footer unit
    if 'data-ad-placement="footer"' not in html:
        at = footer if footer >= 0 else body_end
        if at >= 0 and not inside(at, guard):
            html = html[:at] + unit('footer', label) + '\n' + html[at:]
            changed = True
            low = html.lower()
            footer = low.find('<footer')
            body_end = low.rfind('</body>')

    # in-content unit
    if 'data-ad-placement="in-article"' not in html:
        limit = footer if footer >= 0 else body_end
        h1 = low.find('<h1')
        h2 = -1
        for m in re.finditer(r'<h2[\s>]', html, re.I):
            if limit >= 0 and m.start() > limit:
                break
            if m.start() <= h1 or inside(m.start(), guard):
                continue
            h2 = m.start()
            break
        if h2 > 0:
            f2 = low.find('data-ad-placement="footer"')
            if f2 < 0 or f2 - h2 >= MIN_GAP:
                html = html[:h2] + unit('in-article', label) + '\n' + html[h2:]
                changed = True
    return html, changed


scanned = skipped = updated = already = 0
placements = {'in-article': 0, 'footer': 0}
examples = []

for rel in pages():
    scanned += 1
    html = open(rel, encoding='utf-8', errors='replace').read()
    if is_redirect_stub(html):
        skipped += 1
        continue
    before = html
    label = lang_label(html)
    html, _ = ensure_consent(html)
    html, _ = apply_units(html, label)
    if html == before:
        already += 1
        continue
    updated += 1
    for kind in ('in-article', 'footer'):
        placements[kind] += html.count(f'data-ad-placement="{kind}"') - before.count(f'data-ad-placement="{kind}"')
    if len(examples) < 5:
        examples.append(rel)
    if VERBOSE:
        print(f'  + {rel}')
    if not DRY:
        open(rel, 'w', encoding='utf-8', newline='').write(html)

print(f'{DRY and "[dry-run] " or ""}adsense wiring')
print(f'  pages scanned   : {scanned}')
print(f'  updated         : {updated}')
print(f'  already correct : {already}')
print(f'  skipped (stubs) : {skipped}')
print(f'  in-article units added : {placements["in-article"]}')
print(f'  footer units added     : {placements["footer"]}')
if examples:
    print(f'  e.g. {", ".join(examples)}')
