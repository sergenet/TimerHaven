#!/usr/bin/env python3
"""apply-hreflang.py — reciprocal hreflang across TimerHaven's translations.

Measured state: of 731 pages, six carried any hreflang at all. The site
publishes the same tool in seven languages, with no annotation telling Google
they are translations of one page — so the variants competed with each other and
the strongest one absorbed the rest.

hreflang is reciprocal by definition: a cluster only counts when every URL in it
names the others. So the cluster is written to every member of a group at once,
from one grouping (scripts/_i18n_groups.py) that the sitemap generator also uses.

A page joins a cluster only if it is indexable in its own right — self-canonical,
not noindex, not a redirect stub. Alias files and consolidated duplicates are
therefore never advertised.

Run: python scripts/apply-hreflang.py [--dry-run] [--verbose]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

DRY = '--dry-run' in sys.argv
VERBOSE = '--verbose' in sys.argv

ALT_RE = re.compile(
    r'<link[^>]*rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
    re.I)
ALT_ANY_RE = re.compile(r'<link[^>]*\bhreflang=["\'][^"\']+["\'][^>]*>', re.I)


def cluster_for(members):
    """[(hreflang, url)] for a group, English last so x-default can follow it."""
    pairs = []
    for lang in ('ar', 'de', 'el', 'es', 'fr', 'ru', 'en'):
        if lang in members:
            pairs.append((lang, G.url_of(members[lang])))
    en = members.get('en')
    if en:
        pairs.append(('x-default', G.url_of(en)))
    return pairs


def block(pairs, indent='  '):
    return '\n'.join(
        f'{indent}<link rel="alternate" hreflang="{lang}" href="{href}">'
        for lang, href in pairs)


def strip_existing(html):
    out = ALT_ANY_RE.sub('', html)
    return re.sub(r'\n[ \t]*\n(?=\s*(?:<meta|<link|<script|<style|</head))', '\n', out)


groups = G.groups()
multi = {k: v for k, v in groups.items() if len(v) > 1}

updated = already = 0
sizes = {}
examples = []

for key, members in multi.items():
    pairs = cluster_for(members)
    sizes[len(pairs)] = sizes.get(len(pairs), 0) + 1
    for lang, rel in members.items():
        html = G.read(rel)
        new_html = strip_existing(html)
        i = new_html.lower().find('</head>')
        if i < 0:
            continue
        head = new_html[:i]
        # already exactly this cluster?
        have = sorted(ALT_RE.findall(head))
        want = sorted(pairs)
        if have == want:
            already += 1
            continue
        b = block(pairs)
        new_html = head.rstrip() + '\n' + b + '\n' + new_html[i:]
        if new_html == html:
            already += 1
            continue
        updated += 1
        if len(examples) < 5:
            examples.append((rel, len(pairs)))
        if VERBOSE:
            print(f'  + {rel} ({len(pairs)} languages)')
        if not DRY:
            with open(os.path.join(G.ROOT, rel), 'w', encoding='utf-8', newline='') as fh:
                fh.write(new_html)

print(f'{DRY and "[dry-run] " or ""}hreflang clusters')
print(f'  translation groups (2+ languages): {len(multi)}')
print(f'  pages updated                   : {updated}')
print(f'  already correct                 : {already}')
print('  cluster sizes (alternates per group):', dict(sorted(sizes.items())))
for rel, n in examples:
    print(f'    e.g. {rel}  ({n} languages)')

singles = [k for k, v in groups.items() if len(v) == 1]
if singles:
    print(f'  groups with a single language (left without a cluster): {len(singles)}')
