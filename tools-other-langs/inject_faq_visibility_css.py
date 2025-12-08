#!/usr/bin/env python3
"""
Inject small CSS to ensure FAQ is visible and card has spacing to avoid overlap.
Idempotent: checks for marker before injecting.

Usage:
  python inject_faq_visibility_css.py --folder "C:\TimerHavenWebsite\tools-other-langs"    # dry-run prints DRY-RUN lines
  python inject_faq_visibility_css.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup
  python inject_faq_visibility_css.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file countdown-de.html --apply --backup
"""
import argparse, os, sys
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: faq visibility fix */"
CSS = f"""
{MARKER}
.faq-section, .faq, details {{
  display: block !important;
  position: relative !important;
  z-index: 999 !important;
  margin-bottom: 1.2rem !important;
}}
.tool-card, .article-card {{
  margin-bottom: 3.2rem !important;
  position: relative !important;
  z-index: 1 !important;
}}
footer {{ z-index:0 !important; position: relative !important; }}
@media (max-width:900px) {{
  .tool-card {{ margin-bottom: 4rem !important; }}
}}
"""

def already_injected(soup):
    for s in soup.find_all('style'):
        if s.string and MARKER in s.string:
            return True
    return False

def inject_into_head(soup):
    head = soup.head
    if not head:
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    style = soup.new_tag('style')
    style.string = CSS
    head.append(style)

def process(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        src = open(path, 'r', encoding='utf-8').read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, 'lxml')
    if already_injected(soup):
        return False, f"NO-CHANGE: {name} (css already present)"
    if apply:
        if backup:
            open(path + '.bak','w', encoding='utf-8').write(src)
        inject_into_head(soup)
        open(path, 'w', encoding='utf-8').write(str(soup))
        return True, f"APPLIED: {name} (injected faq css)"
    else:
        # dry-run, but report if .faq-section exists and if likely problem
        has_faq = bool(soup.select_one('.faq-section') or soup.find_all('details'))
        return True, f"DRY-RUN: {name}: has_faq={has_faq}"
        
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--folder','-f', required=True)
    p.add_argument('--file')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--backup', action='store_true')
    args = p.parse_args()
    folder = args.folder
    if not os.path.isdir(folder):
        print("ERROR: folder not found"); sys.exit(1)
    targets = []
    if args.file:
        targets = [os.path.join(folder, args.file)]
    else:
        targets = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])
    for t in targets:
        ok, msg = process(t, apply=args.apply, backup=args.backup)
        print(msg)

if __name__ == '__main__':
    main()