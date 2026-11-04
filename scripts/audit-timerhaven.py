#!/usr/bin/env python3
"""audit-timerhaven.py — read-only audit of the TimerHaven tree.

Reports, with counts and samples:
  * which pages are in / out of the sitemap
  * canonical correctness (missing, cross-host, pointing elsewhere)
  * noindex pages (and whether any are wrongly submitted)
  * duplicate titles and duplicate meta descriptions
  * title / description length
  * AdSense loader and fixed-unit coverage
  * hreflang clusters on the localized trees
  * internal link targets that do not exist on disk
Run: python scripts/audit-timerhaven.py
"""
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKIP_DIRS = {'node_modules', '_site', '.git', '_attic', 'scripts', 'assets',
             'images', 'images2', 'Backup_20260222', 'Backup_20260222_Refined',
             '_SYNCAPP', 'chrome_store_screenshots', 'YouTube experiments'}

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']*)', re.I)
CANON_RE = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', re.I)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*content=["\']([^"\']*)', re.I)
ALT_RE = re.compile(r'<link[^>]*rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)', re.I)
HREF_RE = re.compile(r'<a\s[^>]*href=["\']([^"\'#][^"\']*)["\']', re.I)


def pages():
    out = []
    for dirpath, dirnames, filenames in os.walk('.'):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for f in filenames:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), '.').replace('\\', '/')
            if ' - Copy' in rel or '(backup' in rel.lower() or rel.startswith('backup'):
                continue
            out.append(rel)
    return sorted(out)


def head_of(html):
    i = html.lower().find('</head>')
    return html if i < 0 else html[:i]


def main():
    sm = open('sitemap.xml', encoding='utf-8').read()
    sm_urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    sm_set = set(sm_urls)
    hosts = collections.Counter(re.match(r'(https?://[^/]+)', u).group(1) for u in sm_urls)
    print(f'sitemap: {len(sm_urls)} urls, hosts={dict(hosts)}')

    all_pages = pages()
    print(f'html pages on disk (deployable tree): {len(all_pages)}\n')

    titles = collections.defaultdict(list)
    descs = collections.defaultdict(list)
    no_canon, bad_canon, noindexed, in_sm_noindex = [], [], [], []
    long_title, long_desc, no_desc = [], [], []
    no_ads, ads_loader_only, ads_with_units = [], [], []
    hreflang_pages = 0
    missing_targets = collections.Counter()
    in_sitemap = 0

    for rel in all_pages:
        html = open(rel, encoding='utf-8', errors='replace').read()
        head = head_of(html)

        t = TITLE_RE.search(head)
        title = re.sub(r'\s+', ' ', t.group(1)).strip() if t else ''
        titles[title].append(rel)
        if len(title) > 60:
            long_title.append((len(title), rel))

        d = DESC_RE.search(head)
        desc = re.sub(r'\s+', ' ', d.group(1)).strip() if d else ''
        if not desc:
            no_desc.append(rel)
        else:
            descs[desc].append(rel)
            if len(desc) > 160:
                long_desc.append((len(desc), rel))

        c = CANON_RE.search(head)
        expected = 'https://timerhaven.com/' + ('' if rel == 'index.html' else rel)
        if not c:
            no_canon.append(rel)
        else:
            href = c.group(1).strip()
            if rel in sm_set:
                in_sitemap += 1
            if href.rstrip('/') != expected.rstrip('/'):
                bad_canon.append((rel, href))

        r = ROBOTS_RE.search(head)
        if r and 'noindex' in r.group(1).lower():
            noindexed.append(rel)
            if expected in sm_set:
                in_sm_noindex.append(rel)

        n_loader = html.count('pagead2.googlesyndication.com')
        n_units = html.count('adsbygoogle')
        if n_loader == 0:
            no_ads.append(rel)
        elif n_units <= 1:
            ads_loader_only.append(rel)
        else:
            ads_with_units.append(rel)

        if ALT_RE.search(head):
            hreflang_pages += 1

        for href in HREF_RE.findall(html):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
                continue
            p = href.split('?')[0].split('#')[0].lstrip('/')
            if not p:
                continue
            base = os.path.dirname(rel)
            for cand in (os.path.normpath(os.path.join(base, p)), p):
                if os.path.isfile(cand) or os.path.isdir(cand):
                    break
            else:
                if p.endswith('.html') or '/' not in p:
                    missing_targets[p] += 1

    def section(name, items, show=0):
        print(f'{name}: {len(items)}')
        for it in (items if show else items[:show]) if show else []:
            print('   ', it)

    print('=== sitemap coverage ===')
    print(f'  pages that are in the sitemap (by expected url): {in_sitemap} / {len(all_pages)}')
    on_disk_urls = {'https://timerhaven.com/' + ('' if r == 'index.html' else r) for r in all_pages}
    missing_from_sm = sorted(on_disk_urls - sm_set)
    print(f'  on disk but NOT in sitemap: {len(missing_from_sm)}')
    for u in missing_from_sm[:12]:
        print('      ', u)
    print(f'  in sitemap but no file on disk: {len(sm_set - on_disk_urls)}')
    for u in sorted(sm_set - on_disk_urls)[:12]:
        print('      ', u)

    print('\n=== canonicals ===')
    print(f'  missing            : {len(no_canon)}')
    for x in no_canon[:8]:
        print('      ', x)
    print(f'  not self-referencing: {len(bad_canon)}')
    for rel, href in bad_canon[:12]:
        print(f'       {rel}\n         -> {href}')

    print('\n=== indexability ===')
    print(f'  pages carrying noindex: {len(noindexed)}')
    print(f'  noindex pages submitted in sitemap: {len(in_sm_noindex)}')
    for x in in_sm_noindex[:8]:
        print('      ', x)

    print('\n=== titles ===')
    dup_t = {k: v for k, v in titles.items() if len(v) > 1 and k}
    print(f'  unique titles: {len(titles)}   duplicated title strings: {len(dup_t)}')
    worst = sorted(dup_t.items(), key=lambda kv: -len(kv[1]))[:8]
    for k, v in worst:
        print(f'    x{len(v):2d}  {k[:74]!r}')
        for r in v[:4]:
            print('           ', r)
    print(f'  titles over 60 chars: {len(long_title)}')
    for n, r in sorted(long_title, reverse=True)[:6]:
        print(f'      {n:3d}  {r}')
    empty_t = titles.get('', [])
    if empty_t:
        print(f'  pages with NO title: {len(empty_t)}  e.g. {empty_t[:5]}')

    print('\n=== descriptions ===')
    dup_d = {k: v for k, v in descs.items() if len(v) > 1}
    print(f'  missing: {len(no_desc)}   duplicated: {len(dup_d)}')
    for k, v in sorted(dup_d.items(), key=lambda kv: -len(kv[1]))[:5]:
        print(f'    x{len(v):2d}  {k[:70]!r}  e.g. {v[0]}')
    print(f'  over 160 chars: {len(long_desc)}')

    print('\n=== adsense ===')
    print(f'  no loader at all     : {len(no_ads)}')
    for x in no_ads[:10]:
        print('      ', x)
    print(f'  loader but no units  : {len(ads_loader_only)}')
    for x in ads_loader_only[:10]:
        print('      ', x)
    print(f'  loader + units       : {len(ads_with_units)}')

    print(f'\n=== hreflang ===\n  pages with a cluster: {hreflang_pages}')

    print(f'\n=== internal links ===\n  distinct missing targets: {len(missing_targets)}')
    for p, n in missing_targets.most_common(12):
        print(f'    x{n:3d}  {p}')


if __name__ == '__main__':
    main()
