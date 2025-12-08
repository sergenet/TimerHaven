#!/usr/bin/env python3
"""
update_read_guide_style.py

Purpose:
- Ensure every localized calendar HTML file in a folder uses a boxed "Read full guide" button style.
- Adds a small .read-guide CSS rule in the document <head> if not already present.
- Ensures the Read button has the 'read-guide' class and reasonable attributes (target/_blank, rel="noopener").
- Dry-run by default; use --apply to overwrite files.
- By default does NOT create backups; pass --backup to enable .bak files.

Usage (example):
  Dry-run:
    python update_read_guide_style.py --folder "C:\TimerHavenWebsite\calendar-other-langs"

  Apply changes:
    python update_read_guide_style.py --folder "C:\TimerHavenWebsite\calendar-other-langs" --apply

  Apply with backups:
    python update_read_guide_style.py --folder "C:\TimerHavenWebsite\calendar-other-langs" --apply --backup

Dependencies:
  pip install beautifulsoup4 lxml
"""
import argparse
import os
import re
from bs4 import BeautifulSoup

READ_GUIDE_CSS = """
/* read-guide: consistent boxed CTA used across tools */
.read-guide {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  width: auto;
  align-self: flex-start;
  margin: .35rem 0 .8rem 0;
  padding: .45rem .9rem;
  border-radius: 8px;
  background: #007bff;
  color: #fff !important;
  text-decoration: none;
  font-weight: 700;
  font-size: .95rem;
  border: none;
  box-sizing: border-box;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.read-guide:hover { filter: brightness(.95); text-decoration: none; }
"""

def has_read_guide_css(soup):
    """Return True if any <style> contains .read-guide rule already (simple substring check)."""
    for style in soup.find_all('style'):
        if style.string and '.read-guide' in style.string:
            return True
    return False

def ensure_css_in_head(soup):
    """Add READ_GUIDE_CSS into a new <style> tag in <head> if missing."""
    if has_read_guide_css(soup):
        return False, "css_present"
    head = soup.head
    if not head:
        # create head if missing
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    style_tag = soup.new_tag('style')
    style_tag.string = READ_GUIDE_CSS
    head.append(style_tag)
    return True, "css_added"

def ensure_button_attrs_and_class(soup):
    """
    Find the read-guide anchor and ensure:
      - it has class 'read-guide'
      - it has id 'read-guide-btn' (if missing, not mandatory)
      - it has target="_blank" and rel includes "noopener"
    Returns tuple (changed_bool, description)
    """
    changed = False
    desc = []
    # Prefer id first
    anchors = []
    a = soup.find(id='read-guide-btn')
    if a:
        anchors.append(a)
    # Also include anchors with class read-guide or text like 'Read full guide' in any language (best-effort)
    anchors += [el for el in soup.find_all('a') if el not in anchors and ('read-guide' in ' '.join(el.get('class') or []))]
    # Fallback: anchors that look like guide links by href pattern containing '/calendar-planning/'.
    anchors += [el for el in soup.find_all('a') if el not in anchors and el.get('href') and '/calendar-planning/' in el.get('href')]

    # Deduplicate
    anchors = list(dict.fromkeys(anchors))

    if not anchors:
        return False, "no-read-guide-anchor-found"

    for el in anchors:
        before = str(el)
        classes = set(el.get('class') or [])
        if 'read-guide' not in classes:
            classes.add('read-guide')
            el['class'] = list(classes)
            changed = True
            desc.append("added class")
        # ensure id exists (optional)
        if not el.get('id'):
            el['id'] = 'read-guide-btn'
            changed = True
            desc.append("added id")
        # ensure target and rel
        if el.get('target') != '_blank':
            el['target'] = '_blank'
            changed = True
            desc.append("set target=_blank")
        rel = el.get('rel') or ''
        if 'noopener' not in rel:
            # preserve existing rel values
            new_rel = (rel + ' noopener').strip()
            el['rel'] = new_rel
            changed = True
            desc.append("set rel")
    return changed, '; '.join(desc) or "no-change"

def process_file(path, apply=False, backup=False):
    fn = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {fn}: {e}"

    try:
        soup = BeautifulSoup(src, 'lxml')
    except Exception as e:
        return False, f"ERROR parsing {fn}: {e}"

    file_changed = False
    notes = []

    css_changed, css_note = ensure_css_in_head(soup)
    if css_changed:
        file_changed = True
        notes.append(css_note)

    btn_changed, btn_note = ensure_button_attrs_and_class(soup)
    if btn_changed:
        file_changed = True
        notes.append(btn_note)
    elif btn_note == "no-read-guide-anchor-found":
        notes.append(btn_note)

    if file_changed and apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {fn}: " + '; '.join(notes)
        except Exception as e:
            return False, f"ERROR writing {fn}: {e}"
    elif file_changed:
        return True, f"DRY-RUN: {fn}: " + '; '.join(notes)
    else:
        return False, f"NO-CHANGE: {fn}: " + '; '.join(notes)

def main():
    p = argparse.ArgumentParser(description="Ensure boxed Read full guide button style for localized calendar pages.")
    p.add_argument('--folder','-f', required=True, help="Folder with localized html files")
    p.add_argument('--apply', action='store_true', help="Actually overwrite files")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before overwriting")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    files = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])
    if not files:
        print("No .html files found in folder")
        return

    print(f"{'APPLY' if args.apply else 'DRY-RUN'} -> scanning {len(files)} files in: {folder}\n")
    for fpath in files:
        ok, msg = process_file(fpath, apply=args.apply, backup=args.backup)
        print(msg)
    print("\nDone.")

if __name__ == '__main__':
    main()