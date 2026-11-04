#!/usr/bin/env python3
"""consolidate-thin-duplicates.py — retire pages that are copies of another page.

Measured: nine root pages (`notes-how.html`, `timer-how.html`, `world-how.html`,
...) are byte-identical in body text to their `-how-to-en.html` twin, and each is
self-canonical. Google therefore holds two copies of every one of them, both
eligible for the same query, and neither is credited as the original.

The `-how-to-en.html` page is the survivor: it is the one the site already links
to, the one the other languages cluster with, and the one in the sitemap. The
copy keeps its URL but stops positioning itself: canonical moves to the survivor
and the server 301s it there.

The check is deliberately strict - identical normalised body text, not "similar"
- so it cannot merge two pages that merely share a title.

Run: python scripts/consolidate-thin-duplicates.py [--dry-run]
"""
import difflib
import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

DRY = '--dry-run' in sys.argv
BASE = 'https://timerhaven.com'
SIM_FLOOR = 0.99


def body_text(html):
    h = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', '', html, flags=re.S | re.I)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = re.sub(r'&[a-z#0-9]+;', ' ', h)
    return re.sub(r'\s+', ' ', h).strip()


def find_pairs():
    """[(loser rel, winner url)] for self-canonical pages that duplicate another."""
    by_title = collections.defaultdict(list)
    cache = {}
    for rel in G.pages():
        html = G.read(rel)
        cache[rel] = html
        if G.is_stub(html) or G.is_noindex(html) or not G.is_self_canonical(rel, html):
            continue
        by_title[G.title_of(html)].append(rel)

    pairs = []
    for title, rels in by_title.items():
        if len(rels) < 2:
            continue
        texts = {r: body_text(cache[r]) for r in rels}
        # Survivor: an -en page if the group has one, else the longest text.
        winner = next((r for r in rels if r.endswith('-en.html')), None) \
            or max(rels, key=lambda r: len(texts[r]))
        for rel in rels:
            if rel == winner:
                continue
            if difflib.SequenceMatcher(None, texts[rel], texts[winner]).ratio() >= SIM_FLOOR:
                pairs.append((rel, G.url_of(winner)))
    return pairs


def main():
    pairs = find_pairs()
    print(f'thin duplicates found: {len(pairs)}')

    for rel, winner in pairs:
        html = G.read(rel)
        new = re.sub(r'(<link\s+rel=["\']canonical["\'][^>]*href=["\'])[^"\']*(["\'])',
                     lambda m: m.group(1) + winner + m.group(2), html, count=1, flags=re.I)
        if new == html:
            print(f'  ! {rel}: no canonical tag to rewrite')
            continue
        if not DRY:
            with open(os.path.join(G.ROOT, rel), 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)
        print(f'  canon {rel:<28} -> {winner.replace(BASE, "")}')

    # 301s, anchored so they only ever match the exact retired URL.
    ht_path = os.path.join(G.ROOT, '.htaccess')
    text = open(ht_path, encoding='utf-8', errors='replace').read()
    text = re.sub(r'# --- thin duplicates[^\n]*\n(?:RedirectMatch[^\n]*\n)*\n?', '', text)
    rules = [f'RedirectMatch 301 ^{re.escape("/" + rel)}$ {winner}' for rel, winner in pairs]
    heading = '# --- thin duplicates (301 to the page that survives) ---'
    block = '\n'.join([heading] + rules) + '\n\n'
    marker = '# --- PHASE 12: PERFORMANCE EXCELLENCE ---'
    text = text.replace(marker, block + marker, 1) if marker in text \
        else text.rstrip('\n') + '\n\n' + block
    if not DRY:
        with open(ht_path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    print(f'  .htaccess: {len(rules)} anchored redirect(s) written')


if __name__ == '__main__':
    main()
