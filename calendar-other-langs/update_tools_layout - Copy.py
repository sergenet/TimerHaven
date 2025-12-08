#!/usr/bin/env python3
"""
update_tools_layout.py

Purpose:
- Make all tool pages in a folder use the same single-centered card size/layout
  as your French calendar screenshot.
- The script inserts a small CSS block into each HTML file's <head> (if not already present)
  which:
    - forces a single centered column layout (.center-row -> column)
    - sets .tool-card max-width and padding to match the FR screenshot
    - hides the side article cards (.article-card) so the page displays a single centered card
    - ensures the boxed .read-guide CTA style is present
- Non-destructive by default (dry-run). Use --apply to overwrite files.
- Optional --backup will write .bak copies before modifying files.

Usage:
  Dry run (report only):
    python update_tools_layout.py --folder "C:/TimerHavenWebsite/calendar-other-langs"

  Apply changes (overwrite files):
    python update_tools_layout.py --folder "C:/TimerHavenWebsite/calendar-other-langs" --apply

  Apply with backups:
    python update_tools_layout.py --folder "C:/TimerHavenWebsite/calendar-other-langs" --apply --backup

Dependencies:
  pip install beautifulsoup4 lxml
"""
import argparse
import os
from bs4 import BeautifulSoup, Comment

# Marker to detect we've already added this block
MARKER = "/* timerhaven: enforce single-card layout and CTA */"

# CSS to inject (matches FR layout + boxed CTA)
INJECT_CSS = f"""
{MARKER}
.main-container {{
  max-width: 520px !important;
  margin: 2rem auto !important;
  padding: 0 12px !important;
  box-sizing: border-box;
}}
.center-row {{
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 0 !important;
}}
.tool-card, .article-card {{
  background: #fff !important;
  border-radius: 16px !important;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
  width: 100% !important;
  max-width: 520px !important;
  padding: 1.6rem 1.3rem !important;
  box-sizing: border-box !important;
  margin: 0 0 1.2rem 0 !important;
}}
/* hide side article cards so only the centered tool-card remains visible */
.article-card {{
  display: none !important;
}}
/* Read-guide boxed CTA consistent style (same as calendar) */
.read-guide {{
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
}}
.read-guide:hover {{ filter: brightness(.95); text-decoration: none; }}
@media (max-width: 800px) {{
  .main-container {{ padding: 0 8px !important; }}
  .tool-card {{ max-width: 97vw !important; }}
}}
"""

def already_injected(soup):
    # Look for a style tag containing our marker
    for s in soup.find_all('style'):
        if s.string and MARKER in s.string:
            return True
    return False

def ensure_style_head(soup):
    """Insert the INJECT_CSS into a <style> tag inside <head>, if not present."""
    if already_injected(soup):
        return False, "already_present"
    head = soup.head
    if head is None:
        # create head if missing
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    style_tag = soup.new_tag('style')
    style_tag.string = INJECT_CSS
    head.append(style_tag)
    return True, "css_injected"

def ensure_read_guide_anchor_class(soup):
    """
    Add the 'read-guide' class to existing guide anchors (best-effort).
    We search for:
      - id='read-guide-btn'
      - anchors linking to calendar-planning (guide) or anchors that already have 'read-guide'
    """
    changed = False
    anchors = []
    # prefer id
    a = soup.find(id='read-guide-btn')
    if a:
        anchors.append(a)
    # anchors with href pointing to calendar-planning (help guides) - best-effort across tools too
    anchors += [el for el in soup.find_all('a') if el.get('href') and '/calendar-planning/' in el.get('href')]
    # anchors already with read-guide class
    anchors += [el for el in soup.find_all('a') if 'read-guide' in ' '.join(el.get('class') or [])]
    # dedupe
    anchors = list(dict.fromkeys(anchors))
    for el in anchors:
        classes = set(el.get('class') or [])
        if 'read-guide' not in classes:
            classes.add('read-guide')
            el['class'] = list(classes)
            changed = True
        # enforce target/rel
        if el.get('target') != '_blank':
            el['target'] = '_blank'
            changed = True
        rel = el.get('rel') or ''
        if 'noopener' not in rel:
            el['rel'] = (rel + ' noopener').strip()
            changed = True
    return changed, "read-guide-ensured" if changed else "read-guide-nochange"

def process_file(path, apply=False, backup=False):
    fn = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {fn}: {e}"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')

    changed = False
    notes = []

    css_changed, css_note = ensure_style_head(soup)
    if css_changed:
        changed = True
        notes.append(css_note)

    btn_changed, btn_note = ensure_read_guide_anchor_class(soup)
    if btn_changed:
        changed = True
        notes.append(btn_note)

    if changed and apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {fn}: " + '; '.join(notes)
        except Exception as e:
            return False, f"ERROR writing {fn}: {e}"
    elif changed:
        return True, f"DRY-RUN: {fn}: " + '; '.join(notes)
    else:
        return False, f"NO-CHANGE: {fn}"

def main():
    p = argparse.ArgumentParser(description="Enforce single-centered tool-card layout and boxed CTA across tool pages.")
    p.add_argument('--folder','-f', required=True, help="Folder with tool HTML files to process")
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
    print("\nDone. Notes:")
    print("- Dry-run shows what would be changed. Use --apply to write changes.")
    print("- If you choose --backup the script will write .bak copies before modifying files.")

if __name__ == '__main__':
    main()