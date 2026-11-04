#!/usr/bin/env python3
"""fix-canonicals.py — give every page exactly one correct self-canonical.

Measured state: 274 of 731 pages carried no canonical at all, so Google was free
to pick any of the near-duplicate URLs as the representative — which for a site
with seven language variants of every page is how you get a French page ranking
for an English query's slot, or nothing ranking at all.

Rules:
  * a page's canonical is the URL it is actually served at
  * a directory index (foo/index.html) canonicalises to foo/, matching what the
    server serves and what the six existing correct canonicals already said
  * a root file that has an -en sibling is a legacy alias: .htaccess 301s some of
    them to the -en URL and the rest are live duplicates of it, so all of them
    point their canonical at the -en page rather than at themselves
  * redirect stubs are skipped — they already carry a canonical for their target
  * a canonical pointing at a path that does not exist is rewritten, because a
    dangling canonical de-indexes the page that declares it

Run: python scripts/fix-canonicals.py [--dry-run]
"""
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DRY = '--dry-run' in sys.argv

SITE = 'https://timerhaven.com'
SUFFIX_RE = re.compile(r'-(ar|de|el|en|es|fr|ru)\.html$')
CANON_RE = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', re.I)
CANON_TAG_RE = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*>', re.I)

SKIP_DIRS = {
    'node_modules', '_site', '.git', '_attic', 'scripts', 'assets', 'images',
    'images2', 'Backup_20260222', 'Backup_20260222_Refined', '_SYNCAPP',
    'chrome_store_screenshots', 'YouTube experiments', 'chrome_extension',
    'timerhaven-extension', 'timerhaven-extension-v2', 'components', 'android',
    'ios', 'data', 'docs', 'api',
}


def pages():
    out = []
    for dirpath, dirnames, filenames in os.walk('.'):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for f in filenames:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), '.').replace(os.sep, '/')
            if ' - Copy' in rel or '(backup' in rel.lower() or rel.startswith('backup'):
                continue
            out.append(rel)
    return sorted(out)


def url_of(rel):
    if rel == 'index.html':
        return SITE + '/'
    if rel.endswith('/index.html'):
        return SITE + '/' + rel[:-len('index.html')]
    return SITE + '/' + rel


def disk_of(url):
    p = url.replace(SITE + '/', '')
    if p == '':
        return 'index.html'
    if p.endswith('/'):
        return p + 'index.html'
    return p


def target_for(rel):
    """The canonical this page should declare."""
    if '/' not in rel:
        base = rel[:-5]
        if not SUFFIX_RE.search(rel) and os.path.exists(base + '-en.html'):
            return f'{SITE}/{base}-en.html'
    return url_of(rel)


def main():
    stats = collections.Counter()
    areas = collections.Counter()
    samples = collections.defaultdict(list)

    for rel in pages():
        html = open(rel, encoding='utf-8', errors='replace').read()
        if 'http-equiv="refresh"' in html and 'Redirecting to' in html:
            stats['skipped_stub'] += 1
            continue
        want = target_for(rel)
        m = CANON_RE.search(html)
        cur = m.group(1).strip() if m else None

        if cur is None:
            stats['added'] += 1
            areas[rel.split('/')[0] if '/' in rel else '(root)'] += 1
            if len(samples['added']) < 6:
                samples['added'].append((rel, want))
            if not DRY:
                head_end = html.lower().find('</head>')
                if head_end < 0:
                    stats['no_head'] += 1
                    continue
                tag = f'\n  <link rel="canonical" href="{want}" />'
                open(rel, 'w', encoding='utf-8', newline='').write(
                    html[:head_end] + tag + html[head_end:])
            continue

        if cur.rstrip('/') == want.rstrip('/'):
            stats['already_correct'] += 1
            continue

        dangling = not os.path.exists(disk_of(cur))
        stats['dangling_rewritten' if dangling else 'mismatch_rewritten'] += 1
        areas[rel.split('/')[0] if '/' in rel else '(root)'] += 1
        if len(samples['rewritten']) < 8:
            samples['rewritten'].append((rel, cur, want, dangling))
        if not DRY:
            new = html[:m.start()] + m.group(0).replace(cur, want, 1) + html[m.end():]
            open(rel, 'w', encoding='utf-8', newline='').write(new)

    print(f'{DRY and "[dry-run] " or ""}canonicals')
    print(f'  added (page had none)        : {stats["added"]}')
    print(f'  rewritten (dangling target)  : {stats["dangling_rewritten"]}')
    print(f'  rewritten (not this page)    : {stats["mismatch_rewritten"]}')
    print(f'  already correct              : {stats["already_correct"]}')
    print(f'  skipped (redirect stubs)     : {stats["skipped_stub"]}')
    if stats['no_head']:
        print(f'  could not insert (no </head>) : {stats["no_head"]}')
    print('  by area:', dict(areas.most_common(8)))
    for rel, want in samples['added']:
        print(f'    + {rel:44s} -> {want}')
    for rel, cur, want, dangling in samples['rewritten']:
        flag = 'DANGLING' if dangling else 'MISMATCH'
        print(f'    ~ {rel}\n        was {cur}   [{flag}]\n        now {want}')


if __name__ == '__main__':
    main()
