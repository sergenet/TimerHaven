#!/usr/bin/env python3
"""
remove_language_indicator_strict.py

Aggressively remove language-selector UI that appears in the top-left of pages.

- Dry-run by default: reports which files contain candidate language elements.
- Use --apply to actually remove them and write files.
- Use --backup to create .bak before writing.

Heuristics used:
- Remove any select element that is NOT inside .tool-card/.article-card (common top-left select).
- Remove elements matching common language-select selectors (.language-indicator, .language-select, #language-select, etc).
- Remove small top-level elements (div, span, p, button, a) whose visible text is a short language name (e.g. "Français", "English", "Deutsch", etc.) and which are not inside .tool-card.
- Inject a safe CSS fallback to hide any remaining language indicator selectors.

Run a dry-run first and review results before using --apply.

Usage:
  Dry-run (folder):
    python remove_language_indicator_strict.py --folder "C:\TimerHavenWebsite\tools-other-langs"

  Dry-run single file:
    python remove_language_indicator_strict.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file clipboard-manager-fr.html

  Apply with backups:
    python remove_language_indicator_strict.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup
"""
import argparse
import os
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: remove language indicator (strict) */"
INJECT_CSS = f"""
{MARKER}
.language-indicator, select.language-indicator, .language-select, #language-select,
select#language, select#lang, select[name="lang"], select[name="language"],
div.language-indicator, .lang-selector, .lang-select {{
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
  width: 0 !important;
  opacity: 0 !important;
}}
/* fallback: hide any select that appears as a direct child of body */
body > select {{ display: none !important; }}
"""

# Short language name tokens (lowercase) used to find tiny language labels
LANG_TOKENS = [
    "français", "francais", "english", "deutsch", "español", "espanol", "русский", "рус",
    "ελληνικά", "ελληνικα", "العربية", "العربي", "中文", "日本語", "italiano", "português",
    "portugues", "nederlands", "polski", "svenska", "한국어"
]

def is_inside_tool_card(el):
    for p in el.parents:
        if not getattr(p, 'get', None):
            continue
        cls = " ".join(p.get("class") or [])
        if 'tool-card' in cls or 'article-card' in cls or 'center-row' in cls:
            return True
    return False

def already_injected(soup):
    for s in soup.find_all('style'):
        if s.string and MARKER in s.string:
            return True
    return False

def inject_css_head(soup):
    if already_injected(soup):
        return False
    head = soup.head
    if not head:
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    style_tag = soup.new_tag('style')
    style_tag.string = INJECT_CSS
    head.append(style_tag)
    return True

def find_candidates(soup):
    found = []

    # 1) explicit selectors
    selectors = [
        'select.language-indicator', '.language-indicator', '.language-select', '#language-select',
        'select#language', 'select#lang', 'select[name="lang"]', 'select[name="language"]',
        'div.language-indicator', '.lang-selector', '.lang-select', 'form.language-selector'
    ]
    for sel in selectors:
        for el in soup.select(sel):
            if el not in found:
                found.append(el)

    # 2) selects that are top-level (not inside tool-card)
    if soup.body:
        for sel in soup.body.find_all('select', recursive=False):
            if not is_inside_tool_card(sel) and sel not in found:
                found.append(sel)

    # 3) small elements near top-level whose text matches a language token
    #    target only elements that are not inside the tool card
    for tag in ['div','span','p','a','button','label']:
        for el in soup.find_all(tag):
            if is_inside_tool_card(el):
                continue
            text = (el.get_text() or "").strip()
            if not text:
                continue
            t = text.lower()
            if len(t) > 40:
                continue
            # if any token is present as whole word or exact label
            for tok in LANG_TOKENS:
                if tok in t:
                    if el not in found:
                        found.append(el)
                    break

    # dedupe and return
    unique = []
    seen = set()
    for el in found:
        ident = str(el)[:240]
        if ident not in seen:
            unique.append(el)
            seen.add(ident)
    return unique

def process_file(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, 'lxml')

    candidates = find_candidates(soup)
    css_injected = inject_css_head(soup)
    notes = []
    changed = False

    if candidates:
        notes.append(f"found-{len(candidates)}-lang-el")
        if apply:
            for el in candidates:
                try:
                    el.extract()
                except Exception:
                    pass
            notes.append("removed-elements")
            changed = True
    else:
        notes.append("no-lang-el-found")

    if css_injected:
        notes.append("css-injected")
        changed = True
    else:
        notes.append("css-already-present")

    if not changed:
        return False, f"NO-CHANGE: {name}: " + ";".join(notes)

    if apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: " + ";".join(notes)
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would " + ";".join(notes)

def main():
    p = argparse.ArgumentParser(description="Remove language indicator UI from tool pages (aggressive).")
    p.add_argument('--folder','-f', required=True, help="Folder with HTML files")
    p.add_argument('--file', help="Optional single filename (relative to folder)")
    p.add_argument('--apply', action='store_true', help="Write changes")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before writing")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    if args.file:
        targets = [os.path.join(folder, args.file)]
    else:
        targets = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])

    for t in targets:
        ok, msg = process_file(t, apply=args.apply, backup=args.backup)
        print(msg)

if __name__ == '__main__':
    main()