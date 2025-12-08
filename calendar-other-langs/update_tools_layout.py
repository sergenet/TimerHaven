#!/usr/bin/env python3
"""
update_tools_layout.py

Purpose:
- Inject a small CSS block + boxed CTA into HTML tool pages so they use a single,
  centered card layout (matching the FR screenshot).
- Idempotent: will not inject the same CSS twice (uses a marker).
- Dry-run by default; use --apply to write files. Use --backup to create .bak copies.

Usage examples (run from any folder where Python is available):
  Dry-run:
    python update_tools_layout.py --folder "C:/path/to/new-tools-folder"

  Apply with backups (recommended):
    python update_tools_layout.py --folder "C:/path/to/new-tools-folder" --apply --backup

Notes:
- Requires: beautifulsoup4, lxml
  Install with: pip install beautifulsoup4 lxml
- The script will report DRY-RUN lines for files that would change.
"""
import argparse
import os
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: enforce single-card layout and CTA */"

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
.article-card {{
  display: none !important;
}}
.read-guide {{
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: .35rem 0 .8rem 0 !important;
  padding: .45rem .9rem !important;
  border-radius: 8px !important;
  background: #007bff !important;
  color: #fff !important;
  text-decoration: none !important;
  font-weight: 700 !important;
  font-size: .95rem !important;
  border: none !important;
  box-sizing: border-box !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
}}
.read-guide:hover {{ filter: brightness(.95); text-decoration: none; }}
@media (max-width: 800px) {{
  .main-container {{ padding: 0 8px !important; }}
  .tool-card {{ max-width: 97vw !important; }}
}}
"""

def already_injected(soup):
    for s in soup.find_all('style'):
        if s.string and MARKER in s.string:
            return True
    return False

def inject_css_head(soup):
    if already_injected(soup):
        return False
    head = soup.head
    if head is None:
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    style_tag = soup.new_tag('style')
    style_tag.string = INJECT_CSS
    head.append(style_tag)
    return True

def ensure_read_guide_anchor(soup):
    changed = False
    anchors = []
    # prefer explicit id
    a = soup.find(id='read-guide-btn')
    if a:
        anchors.append(a)
    # anchors linking to likely guide pages (best-effort)
    anchors += [el for el in soup.find_all('a') if el.get('href') and ('/calendar-planning/' in el.get('href') or 'guide' in el.get('href'))]
    # anchors already with read-guide class
    anchors += [el for el in soup.find_all('a') if 'read-guide' in ' '.join(el.get('class') or [])]
    # dedupe while preserving order
    seen = set()
    unique = []
    for el in anchors:
        ident = str(el)
        if ident not in seen:
            unique.append(el)
            seen.add(ident)
    for el in unique:
        classes = set(el.get('class') or [])
        if 'read-guide' not in classes:
            classes.add('read-guide')
            el['class'] = list(classes)
            changed = True
        if el.get('target') != '_blank':
            el['target'] = '_blank'
            changed = True
        rel = el.get('rel') or ''
        if 'noopener' not in rel:
            el['rel'] = (rel + ' noopener').strip()
            changed = True
    return changed

def process_file(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"

    soup = BeautifulSoup(src, 'lxml')
    changed = False
    notes = []

    if inject_css_head(soup):
        changed = True
        notes.append("css_injected")
    if ensure_read_guide_anchor(soup):
        changed = True
        notes.append("read-guide-ensured")

    if changed and apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: " + ";".join(notes)
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    elif changed:
        return True, f"DRY-RUN: {name}: " + ";".join(notes)
    else:
        return False, f"NO-CHANGE: {name}"

def main():
    p = argparse.ArgumentParser(description="Apply single-card layout + boxed CTA to tool HTML files.")
    p.add_argument('--folder', '-f', required=True, help="Folder with HTML files (Windows path OK)")
    p.add_argument('--apply', action='store_true', help="Actually overwrite files")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before writing")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    files = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])
    if not files:
        print("No .html files found in folder")
        return

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode} -> scanning {len(files)} files in: {folder}\n")
    for pth in files:
        ok, msg = process_file(pth, apply=args.apply, backup=args.backup)
        print(msg)
    print("\nDone.")

if __name__ == '__main__':
    main()