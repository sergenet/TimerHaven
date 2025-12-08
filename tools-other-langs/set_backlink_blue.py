#!/usr/bin/env python3
"""
set_backlink_blue.py

Idempotently add a small CSS rule to make the "back to main menu" link blue
(and bold) across a folder of HTML files.

Usage (dry-run by default):
  python set_backlink_blue.py --folder "C:\TimerHavenWebsite\tools-other-langs"

Apply changes (with optional backups):
  python set_backlink_blue.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup

Options:
  --color   CSS color to use (default: #0d6efd, Bootstrap primary blue)
  --weight  CSS font-weight (default: 700)
  --file    Single filename (relative to folder) to modify
"""
import argparse
import os
from bs4 import BeautifulSoup

MARKER = "/* timerhaven: backlink color */"

def already_injected(soup, marker=MARKER):
    for s in soup.find_all('style'):
        if s.string and marker in s.string:
            return True
    return False

def make_style_tag(color, weight):
    css = f"""{MARKER}
.back-link {{
  color: {color} !important;
  font-weight: {weight} !important;
  text-decoration: none !important;
}}
.back-link:hover {{ text-decoration: underline !important; }}
"""
    return css

def process_file(path, apply=False, backup=False, color="#0d6efd", weight="700"):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"

    soup = BeautifulSoup(src, 'lxml')
    if already_injected(soup):
        return False, f"NO-CHANGE: {name} (backlink color already set)"

    head = soup.head
    if not head:
        # create head if missing
        head = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    style_tag = soup.new_tag('style')
    style_tag.string = make_style_tag(color, weight)
    head.append(style_tag)

    if apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: backlink color set to {color}"
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would add backlink color {color}"

def main():
    p = argparse.ArgumentParser(description="Set back-link color in HTML files.")
    p.add_argument('--folder','-f', required=True, help="Folder with HTML files")
    p.add_argument('--file', help="Optional single filename (relative to folder)")
    p.add_argument('--apply', action='store_true', help="Write changes")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before writing")
    p.add_argument('--color', default="#0d6efd", help="CSS color for back-link (default: #0d6efd)")
    p.add_argument('--weight', default="700", help="CSS font-weight for back-link (default: 700)")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    if args.file:
        files = [os.path.join(folder, args.file)]
    else:
        files = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])

    for pth in files:
        ok, msg = process_file(pth, apply=args.apply, backup=args.backup, color=args.color, weight=args.weight)
        print(msg)

if __name__ == '__main__':
    main()