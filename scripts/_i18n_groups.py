"""_i18n_groups.py — one definition of "which page is which page, in which language".

TimerHaven carries two parallel localization schemes, and every SEO pass needs to
agree on how they map:

  A. root suffix files      timer-en.html, timer-es.html, ... (36 bases)
  B. locale directories     es/task-timer/index.html, de/blog/... (6 locales + en/)

Both exist and are live. They use different slugs for the same tool (task-timer
in the directories, timer in the suffix files), so a page clusters only with the
pages it is genuinely a translation of — the two schemes form separate clusters
rather than being force-merged on guesswork.

Everything else (title translation, hreflang clusters, sitemap alternates)
imports from here so the three can never drift apart.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = ['en', 'ar', 'de', 'el', 'es', 'fr', 'ru']
SPEC = LANGS[1:]  # locales that appear as a directory or a -xx suffix

SUFFIX_RE = re.compile(r'^(.*)-(ar|de|el|en|es|fr|ru)\.html$')

SKIP_DIRS = {
    'node_modules', '_site', '.git', '_attic', 'scripts', 'assets', 'images',
    'images2', 'Backup_20260222', 'Backup_20260222_Refined', '_SYNCAPP',
    'chrome_store_screenshots', 'YouTube experiments', 'chrome_extension',
    'timerhaven-extension', 'timerhaven-extension-v2', 'components', 'android',
    'ios', 'data', 'docs', 'api', 'newsletter',
}
# Pages that are not content: legal, utility, marketing, redirect stubs.
NON_CONTENT = {
    'contact.html', 'privacy.html', 'terms.html', '404.html', 'offline.html',
    'thank-you.html', 'premium.html', 'checkout.html', 'Promotion_Kit.html',
}

# Tool directory name -> root file stem, for the pages where the two schemes
# disagree. Only used to look up an already-translated title; clustering never
# crosses schemes.
FOLDER_TO_STEM = {
    'task-timer': 'timer',
    'pomodoro-timer': 'pomodoro',
    'calendar-planning': 'calendar',
    'clipboard-manager': 'clipboard-manager',
    'countdown': 'countdown',
    'currency': 'currency',
    'focus-music': 'focus-music',
    'habit-tracker': 'habit-tracker',
    'meeting-planner': 'meeting-planner',
    'notes': 'notes',
    'password-generator': 'password-generator',
    'stopwatch': 'stopwatch',
    'unit-converter': 'unit-converter',
    'weather': 'weather',
    'world-clock': 'world-clock',
}


def pages():
    """Every deployable HTML page, site-relative, forward slashes."""
    out = []
    root = ROOT
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, '/')
        if rel_dir == '.':
            rel_dir = ''
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for f in filenames:
            if not f.endswith('.html'):
                continue
            rel = f'{rel_dir}/{f}' if rel_dir else f
            if ' - Copy' in rel or '(backup' in rel.lower() or rel.startswith('backup'):
                continue
            out.append(rel)
    return sorted(out)


def lang_of(rel):
    head = rel.split('/')[0]
    if '/' in rel and head in SPEC:
        return head
    if '/' in rel and head == 'en':
        return 'en'
    m = SUFFIX_RE.match(rel) if '/' not in rel else None
    if m:
        return m.group(2)
    return 'en'


def group_key(rel):
    """Pages sharing a key are translations of one another."""
    if '/' in rel:
        first, rest = rel.split('/', 1)
        if first in SPEC or first == 'en':
            return rest
        return rel
    m = SUFFIX_RE.match(rel)
    if m:
        return m.group(1) + '.html'
    return rel


def is_english_member(rel):
    return lang_of(rel) == 'en'


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace') as fh:
        return fh.read()


def head_of(html):
    i = html.lower().find('</head>')
    return html if i < 0 else html[:i]


def title_of(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def url_of(rel):
    if rel == 'index.html':
        return 'https://timerhaven.com/'
    if rel.endswith('/index.html'):
        return 'https://timerhaven.com/' + rel[:-len('index.html')]
    return 'https://timerhaven.com/' + rel


def is_stub(html):
    return 'http-equiv="refresh"' in html and 'Redirecting to' in html


def is_noindex(html):
    m = re.search(r'<meta\s+name=["\']robots["\'][^>]*content=["\']([^"\']*)', head_of(html), re.I)
    return bool(m and 'noindex' in m.group(1).lower())


def canonical_of(html):
    m = re.search(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', head_of(html), re.I)
    return m.group(1).strip() if m else None


def is_self_canonical(rel, html):
    c = canonical_of(html)
    return c is not None and c.rstrip('/') == url_of(rel).rstrip('/')


def groups():
    """{key: {lang: rel}} for pages that are indexable in their own right."""
    out = {}
    for rel in pages():
        if rel in NON_CONTENT:
            continue
        html = read(rel)
        if is_stub(html) or is_noindex(html) or not is_self_canonical(rel, html):
            continue
        out.setdefault(group_key(rel), {})[lang_of(rel)] = rel
    return out


def translated_title_for(rel, html):
    """An already-translated title for `rel`, taken from a sibling page.

    Used where a locale directory page was built with an English <title>: the
    suffix scheme for the same tool and language already holds a real
    translation, so it is reused rather than machine-translated again.
    """
    lang = lang_of(rel)
    if lang == 'en':
        return None
    parts = rel.split('/')
    candidates = []
    if len(parts) >= 3 and parts[0] == lang:
        folder = parts[1]
        stem = FOLDER_TO_STEM.get(folder)
        if stem:
            candidates.append(f'{stem}-{lang}.html')
        # the tool's guide page in the same locale uses the same vocabulary
        for other in pages():
            if other.startswith(f'{lang}/{folder}/') and other != rel:
                candidates.append(other)
    elif '/' not in rel:
        m = SUFFIX_RE.match(rel)
        if m:
            candidates.append(f'{m.group(1)}-en.html')
    for cand in candidates:
        try:
            if not os.path.exists(os.path.join(ROOT, cand)):
                continue
            h = read(cand)
            t = title_of(h)
            if t and lang_of(cand) == lang and not t.lower().startswith(('task timer', 'timerhaven')):
                return t
        except Exception:
            continue
    return None
