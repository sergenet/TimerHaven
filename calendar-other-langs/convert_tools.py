#!/usr/bin/env python3
"""
convert_tools.py

Purpose:
- For calendar localized HTML files in a folder, ensure each file has a "Read full guide" button
  that points to: https://timerhaven.com/{lang}/calendar-planning/calendar-planning-index.html
- If how-to/tips sections exist outside the main tool card, attempt to move them inside the tool card.
- Preserve scripts and other content. Default: dry-run (report only). Use --apply to overwrite files.
- No backups by default (per user request).

Usage examples:
  Dry run (report only):
    python convert_tools.py --folder "C:\timerhavenwebsite\calendar-other-langs" --tool calendar

  Apply changes:
    python convert_tools.py --folder "C:\timerhavenwebsite\calendar-other-langs" --tool calendar --apply

Dependencies:
  pip install beautifulsoup4 lxml
"""
import argparse
import os
import re
from bs4 import BeautifulSoup

# Mapping of a few button texts by language (fallback to English)
GUIDE_TEXT = {
    'en': 'Read full guide',
    'fr': 'Lire le guide complet',
    'es': 'Leer guía completa',
    'de': 'Vollständigen Leitfaden lesen',
    'ru': 'Прочитать полное руководство',
    'el': 'Διαβάστε τον πλήρη οδηγό',
    'ar': 'اقرأ الدليل الكامل'
}

def detect_lang_from_filename(filename):
    # look for suffix like -fr.html or -en.html
    m = re.search(r'-([a-z]{2})\.html?$', filename, re.I)
    if m:
        return m.group(1).lower()
    return None

def detect_lang_from_html(soup):
    html = soup.find('html')
    if html and html.has_attr('lang'):
        return html['lang'].split('-')[0].lower()
    return None

def build_guide_url(lang):
    if not lang:
        lang = 'en'
    return f"https://timerhaven.com/{lang}/calendar-planning/calendar-planning-index.html"

def ensure_read_guide(soup, lang):
    """
    Returns (changed:boolean, desc:str)
    Ensures an element with id 'read-guide-btn' exists and points to guide URL.
    If missing, create and insert after #tool-title or into first .tool-card.
    """
    changed = False
    desc = []
    guide_url = build_guide_url(lang)
    btn = soup.find(id='read-guide-btn')
    # prefer element with class 'read-guide' also if id missing
    if not btn:
        btn = soup.find('a', class_='read-guide')
    if btn:
        # update href and text if necessary
        old_href = btn.get('href', '')
        if old_href != guide_url:
            btn['href'] = guide_url
            changed = True
            desc.append(f"updated href -> {guide_url}")
        # set text based on language mapping
        wanted_text = GUIDE_TEXT.get(lang, GUIDE_TEXT['en'])
        if (btn.text or '').strip() != wanted_text:
            btn.string = wanted_text
            changed = True
            desc.append("updated button text")
        # ensure attributes
        if btn.get('target') != '_blank' or 'noopener' not in (btn.get('rel') or ''):
            btn['target'] = '_blank'
            btn['rel'] = 'noopener'
            changed = True
            desc.append("ensured target/_blank and rel")
        return changed, '; '.join(desc) or "no changes needed"
    # Create button and insert it
    # preferred insertion points: after element with id 'tool-title'; else inside first element with class 'tool-card';
    tool_title = soup.find(id='tool-title')
    tool_card = None
    if tool_title:
        # insert after the tool_title element
        new_btn = soup.new_tag('a', id='read-guide-btn', href=guide_url, role='button', target='_blank', rel='noopener')
        new_btn['class'] = 'read-guide'
        new_btn.string = GUIDE_TEXT.get(lang, GUIDE_TEXT['en'])
        # insert after the element (as a sibling)
        tool_title.insert_after(new_btn)
        changed = True
        desc.append("inserted button after #tool-title")
    else:
        # find first .tool-card or element with aria-labelledby="tool-title"
        tool_card = soup.find(class_='tool-card') or soup.find(attrs={'aria-labelledby': 'tool-title'}) or soup.find('main') or soup.body
        if tool_card:
            new_btn = soup.new_tag('a', id='read-guide-btn', href=guide_url, role='button', target='_blank', rel='noopener')
            new_btn['class'] = 'read-guide'
            new_btn.string = GUIDE_TEXT.get(lang, GUIDE_TEXT['en'])
            # Insert near the top of tool_card (before first child)
            if tool_card.contents:
                tool_card.insert(1, new_btn)  # after possible back-link at 0
            else:
                tool_card.append(new_btn)
            changed = True
            desc.append("inserted button inside tool-card")
        else:
            # last resort: append to body
            new_btn = soup.new_tag('a', id='read-guide-btn', href=guide_url, role='button', target='_blank', rel='noopener')
            new_btn['class'] = 'read-guide'
            new_btn.string = GUIDE_TEXT.get(lang, GUIDE_TEXT['en'])
            soup.body.append(new_btn)
            changed = True
            desc.append("appended button to <body>")
    return changed, '; '.join(desc)

def move_sections_into_toolcard(soup):
    """
    Try to move howto/tips/article sections into the main tool card if they exist elsewhere.
    Returns (changed, desc).
    """
    changed = False
    desc = []
    # Candidate ids we care about
    groups = [
        ('howto-title', 'howto-steps', 'howto-section', 'howto-mobile', 'howto-mobile-steps'),
        ('tips-title', 'tips-list', 'tips-section', 'tips-mobile', 'tips-mobile-list'),
    ]
    # locate tool_card target
    tool_card = soup.find(class_='tool-card') or soup.find(attrs={'aria-labelledby':'tool-title'})
    if not tool_card:
        return False, "no tool-card found"
    for group in groups:
        # find if any element from group exists and is not already inside tool_card
        for idname in group:
            el = soup.find(id=idname)
            if el and tool_card not in el.find_parents():
                # move this element into tool_card (append near end)
                tool_card.append(el.extract())
                changed = True
                desc.append(f"moved #{idname} into tool-card")
    return changed, '; '.join(desc)

def process_file(path, apply=False):
    filename = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        return False, f"ERROR reading {filename}: {e}"

    soup = BeautifulSoup(html, 'lxml')

    # detect language
    lang = detect_lang_from_filename(filename) or detect_lang_from_html(soup) or 'en'
    changed_any = False
    changes = []

    # Ensure read guide button
    changed, desc = ensure_read_guide(soup, lang)
    if changed:
        changed_any = True
        changes.append(f"read-guide: {desc}")

    # Move howto/tips into tool-card if needed
    moved, mdesc = move_sections_into_toolcard(soup)
    if moved:
        changed_any = True
        changes.append(f"moved-sections: {mdesc}")

    # If applying, write file back
    if changed_any and apply:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {filename}: " + '; '.join(changes)
        except Exception as e:
            return False, f"ERROR writing {filename}: {e}"
    elif changed_any:
        return True, f"DRY-RUN: {filename}: " + '; '.join(changes)
    else:
        return False, f"NO-CHANGE: {filename}"

def main():
    parser = argparse.ArgumentParser(description="Convert localized calendar pages: add Read full guide and adjust layout.")
    parser.add_argument('--folder', '-f', required=False, default=r"C:\timerhavenwebsite\calendar-other-langs",
                        help="Folder containing localized calendar HTML files (default as provided).")
    parser.add_argument('--tool', '-t', choices=['calendar'], default='calendar', help="Tool to process (calendar)")
    parser.add_argument('--apply', action='store_true', help="Actually overwrite files. Default: dry-run (report only).")
    args = parser.parse_args()

    folder = args.folder
    apply = args.apply

    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    html_files = [os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')]
    if not html_files:
        print(f"No .html files found in {folder}")
        return

    print(f"{'APPLYING' if apply else 'DRY-RUN'} -> scanning {len(html_files)} files in: {folder}\n")
    for path in html_files:
        ok, msg = process_file(path, apply=apply)
        print(msg)

    print("\nDone. Notes:")
    print("- Dry-run shows what would be changed. Use --apply to write changes.")
    print("- No backups are created by this script. Make local backups before running with --apply if you want a copy.")

if __name__ == '__main__':
    main()