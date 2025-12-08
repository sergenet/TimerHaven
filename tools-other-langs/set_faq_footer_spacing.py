#!/usr/bin/env python3
"""
set_faq_footer_spacing.py

Injects a small CSS fix to prevent FAQ content from overlapping the footer.

Usage (dry-run):
  python set_faq_footer_spacing.py --folder "C:\TimerHavenWebsite\tools-other-langs"

Apply with backups:
  python set_faq_footer_spacing.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup

Options:
  --file  single filename (relative to folder) to process
"""
import argparse
import os
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: faq spacing fix */"
INJECT_CSS = f"""
{MARKER}
.tool-card, .article-card {{
  margin-bottom: 2.8rem !important; /* ensure card has breathing room above footer */
  position: relative !important;
  z-index: 1 !important;
}}
.faq-section, .clips-list, .faq {{
  position: relative !important;
  z-index: 2 !important; /* ensure FAQ content appears above footer if near */
  margin-bottom: 1.2rem !important;
}}
footer {{
  position: relative !important;
  z-index: 0 !important;
  padding-top: 1.0rem !important;
}}
.main-container {{
  padding-bottom: 2.4rem !important;
}}
@media (max-width: 900px) {{
  .tool-card, .article-card {{ margin-bottom: 3.6rem !important; }}
  .main-container {{ padding-bottom: 3.2rem !important; }}
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

def process_file(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, 'lxml')
    injected = inject_css_head(soup)
    if not injected:
        return False, f"NO-CHANGE: {name} (css already present)"
    if apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: injected faq spacing css"
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would inject faq spacing css"

def main():
    p = argparse.ArgumentParser(description="Inject CSS to prevent FAQ overlap with footer.")
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