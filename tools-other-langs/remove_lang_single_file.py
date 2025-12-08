#!/usr/bin/env python3
"""
remove_lang_single_file.py

Targeted removal of a language selector from a single HTML file.

- Dry-run by default: reports found candidate elements and does NOT modify the file.
- Use --apply to remove the element(s) and write the file.
- Use --backup to create path/to/file.html.bak before overwriting.

Heuristics:
- Remove select elements that are not inside .tool-card/.article-card
- Remove small top-level elements whose text looks like a language label (e.g. "Français")
- Inject a small CSS marker to hide any leftover language selector

Usage (dry-run):
  python remove_lang_single_file.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file "clipboard-manager-fr.html"

Apply with backup:
  python remove_lang_single_file.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file "clipboard-manager-fr.html" --apply --backup
"""
import argparse
import os
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: remove single-file language indicator */"
INJECT_CSS = f"""
{MARKER}
.language-indicator, select.language-indicator, .language-select, #language-select,
select#language, select#lang, select[name="lang"], select[name="language"], .lang-selector {{
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
  width: 0 !important;
  opacity: 0 !important;
}}
body > select {{ display: none !important; }} /* fallback */
"""

LANG_TOKENS = ["français","francais","english","deutsch","español","espanol","русский","ελληνικά","العربية","中文","日本語"]

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

    # selects outside tool-card
    for sel in soup.find_all('select'):
        if not is_inside_tool_card(sel):
            found.append(sel)

    # small text elements (not inside tool card) that match language tokens
    for tag in ['div','span','p','a','button','label']:
        for el in soup.find_all(tag):
            if is_inside_tool_card(el):
                continue
            text = (el.get_text() or "").strip()
            if not text or len(text) > 40:
                continue
            low = text.lower()
            for tok in LANG_TOKENS:
                if tok in low:
                    found.append(el)
                    break

    # dedupe by string repr
    unique = []
    seen = set()
    for el in found:
        ident = str(el)[:300]
        if ident not in seen:
            unique.append(el)
            seen.add(ident)
    return unique

def process(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"

    soup = BeautifulSoup(src, 'lxml')
    candidates = find_candidates(soup)
    css_added = inject_css_head(soup)

    if not candidates and not css_added:
        return False, f"NO-CHANGE: {name} (no candidates and css already present)"

    report = []
    if candidates:
        report.append(f"found-{len(candidates)}-candidates")
    else:
        report.append("no-candidates-found")

    if apply:
        if backup:
            with open(path + ".bak", "w", encoding='utf-8') as bf:
                bf.write(src)
        # remove candidates
        for el in candidates:
            try:
                el.extract()
            except Exception:
                pass
        # write file
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            report.append("APPLIED")
            return True, f"{name}: " + ";".join(report)
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: " + ";".join(report)

def main():
    p = argparse.ArgumentParser(description="Remove lang selector from a single HTML file")
    p.add_argument('--folder','-f', required=True, help="Folder with HTML files")
    p.add_argument('--file','-F', required=True, help="Single filename to process (relative to folder)")
    p.add_argument('--apply', action='store_true', help="Write changes")
    p.add_argument('--backup', action='store_true', help="Backup original file to .bak")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return
    path = os.path.join(folder, args.file)
    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}")
        return

    ok, msg = process(path, apply=args.apply, backup=args.backup)
    print(msg)

if __name__ == '__main__':
    main()