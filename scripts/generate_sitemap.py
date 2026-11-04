"""generate_sitemap.py — build sitemap.xml from the pages on disk.

The previous version was a hand-maintained allowlist: 7 root pages, 15 tools,
blog posts and a `tool_folder_map`. Anything a generator added later was simply
missing unless someone remembered to edit the list - 279 live pages were absent,
and all 7 task-timer tool pages were absent because they are published as
timer-<lang>.html. An allowlist that has to be updated by hand is a list that
will be wrong again.

This walks the tree instead and takes the grouping from _i18n_groups, the same
module the title and hreflang passes use, so the sitemap can never advertise a
canonical, a language set or a URL that the pages themselves disagree with.

Rules:
  - a page is listed only if it is indexable in its own right: not a redirect
    stub, not noindex, and self-canonical (aliases and consolidated duplicates
    stay out)
  - one <loc> per canonical URL, never both /xx/foo/ and /xx/foo/index.html
  - alternates come from the translation group, so they are reciprocal by
    construction
  - <lastmod> is the date the page's content last changed (git commit date),
    not the build date
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _i18n_groups as G

BASE = 'https://timerhaven.com'
OUT = os.path.join(G.ROOT, 'sitemap.xml')
TODAY = date.today().isoformat()
XHTML = '{http://www.w3.org/1999/xhtml}link'


def _git_dates():
    """{repo-relative path: date of last commit touching it}.

    mtime is unusable here: this tree is bulk-rewritten by sync and reformat
    scripts, so 422 of 436 URLs once claimed the same day. Understating recency
    is harmless; claiming every page changed is what gets lastmod ignored.
    """
    import subprocess
    dates = {}
    try:
        log = subprocess.run(
            ['git', '-C', G.ROOT, 'log', '--pretty=format:__%cs', '--name-only'],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180,
        ).stdout
        current = None
        for line in log.splitlines():
            line = line.strip().strip('"')
            if not line:
                continue
            if line.startswith('__'):
                current = line[2:]
                continue
            if current and line not in dates:      # log is newest-first
                dates[line.replace('/', os.sep)] = current
    except Exception:
        pass
    return dates


GIT_DATES = _git_dates()


def lastmod_for(rel):
    if rel in GIT_DATES:
        return GIT_DATES[rel]
    try:
        return date.fromtimestamp(os.path.getmtime(os.path.join(G.ROOT, rel))).isoformat()
    except Exception:
        return TODAY


def url_of(rel):
    """The URL the page advertises; canonical if present, else its own path."""
    return G.canonical_of(G.read(rel)) or G.url_of(rel)


def listed_pages():
    """{url: rel} for every page that belongs in the sitemap."""
    out = {}
    for rel in G.pages():
        html = G.read(rel)
        if G.is_stub(html) or G.is_noindex(html):
            continue
        url = url_of(rel)
        if not url:
            continue
        # An alias file positions another page; never mint a second <loc>.
        if G.url_of(rel) != url and url != G.url_of(rel).rstrip('/') + '/':
            continue
        out.setdefault(url, rel)
    return out


def main():
    groups = G.groups()
    url_to_group = {}
    for key, members in groups.items():
        for lang, rel in members.items():
            url_to_group[url_of(rel)] = key

    pages = listed_pages()

    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
    })

    alternates = 0
    for url in sorted(pages):
        rel = pages[url]
        node = ET.SubElement(urlset, 'url')
        ET.SubElement(node, 'loc').text = url
        ET.SubElement(node, 'lastmod').text = lastmod_for(rel)

        key = url_to_group.get(url)
        members = groups.get(key, {}) if key else {}
        if len(members) > 1:
            pairs = [(lang, url_of(m)) for lang, m in sorted(members.items())]
            en = [u for l, u in pairs if l == 'en']
            for lang, href in pairs:
                ET.SubElement(node, XHTML, {'rel': 'alternate', 'hreflang': lang, 'href': href})
                alternates += 1
            if en:
                ET.SubElement(node, XHTML, {'rel': 'alternate', 'hreflang': 'x-default', 'href': en[0]})
                alternates += 1

        ET.SubElement(node, 'priority').text = (
            '1.0' if url == BASE + '/' else '0.8' if ('/blog/' in url or '-en.html' in url) else '0.6')
        ET.SubElement(node, 'changefreq').text = 'weekly'

    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent='  ')
    xml_str = xml_str.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')
    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        fh.write(xml_str)

    print(f'sitemap.xml written: {len(pages)} URLs, {alternates} hreflang annotations')
    print(f'  indexable pages on disk: {len(G.pages())}')
    print(f'  excluded (alias / noindex / stub): {len(G.pages()) - len(pages)}')
    dates = {}
    for rel in pages.values():
        d = lastmod_for(rel)
        dates[d] = dates.get(d, 0) + 1
    top = sorted(dates.items(), reverse=True)[:3]
    print('  most common lastmod values:', ', '.join(f'{d} ({n})' for d, n in top))


if __name__ == '__main__':
    main()
