#!/usr/bin/env python3
"""
remove_side_cards.py

Purpose:
- Scan HTML files in a folder and remove empty aside article cards (left/right placeholders)
  that remain after converting localized tool pages to the single centered layout.

Behavior:
- Dry-run by default: reports files and the specific aside elements that would be removed.
- Use --apply to overwrite the files and remove the detected elements.
- By default does NOT create backups. If you want backups, run with --backup to create .bak copies.

Usage:
  Dry-run:
    python remove_side_cards.py --folder "C:\timerhavenwebsite\calendar-other-langs"

  Apply changes:
    python remove_side_cards.py --folder "C:\timerhavenwebsite\calendar-other-langs" --apply

  With backup:
    python remove_side_cards.py --folder "C:\timerhavenwebsite\calendar-other-langs" --apply --backup

Dependencies:
  pip install beautifulsoup4 lxml
"""
import argparse
import os
from bs4 import BeautifulSoup, Comment

def is_element_empty(el):
    """
    Consider element empty if:
    - No non-whitespace text in itself or descendants (excluding script/style/comments)
    - No child tags except empty ones
    """
    # Remove comments for checking
    for c in el.find_all(text=lambda text: isinstance(text, Comment)):
        c.extract()

    # If there is any <img>, <svg>, or non-empty child other than scripts/styles, treat as non-empty
    for tag in el.find_all():
        if tag.name in ('script', 'style'):
            continue
        # If tag has meaningful text
        if tag.string and tag.string.strip():
            return False
        # If tag has attributes that indicate content (e.g., images)
        if tag.name in ('img','svg','iframe','object'):
            return False
        # If has children that are not empty, will be caught when iterating
    # Finally check textual content
    txt = el.get_text(separator='').strip()
    if txt:
        return False
    # If no meaningful text and no non-decorative tags found -> empty
    return True

def find_empty_asides(soup):
    """
    Return list of aside elements that look like left/right article cards and are empty.
    Criteria:
     - tag.name == 'aside' AND (class contains 'article-card' OR id is 'left-card'/'right-card')
    """
    results = []
    asides = soup.find_all('aside')
    for a in asides:
        cls = ' '.join(a.get('class') or [])
        aid = a.get('id','')
        if 'article-card' in cls or 'article' in cls or aid in ('left-card','right-card'):
            if is_element_empty(a):
                results.append(a)
    return results

def process_file(path, apply=False, backup=False):
    fn = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {fn}: {e}"

    soup = BeautifulSoup(src, 'lxml')
    empty_asides = find_empty_asides(soup)
    if not empty_asides:
        return False, f"NO-CHANGE: {fn}"

    removed_ids = []
    for a in empty_asides:
        # record id/class info for report
        info = f"id='{a.get('id','')}' class='{ ' '.join(a.get('class') or []) }'"
        removed_ids.append(info)
        # Remove element from tree
        a.extract()

    if apply:
        try:
            if backup:
                bak = path + '.bak'
                with open(bak, 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {fn}: removed asides -> {', '.join(removed_ids)}"
        except Exception as e:
            return False, f"ERROR writing {fn}: {e}"
    else:
        return True, f"DRY-RUN: {fn}: would remove asides -> {', '.join(removed_ids)}"

def main():
    p = argparse.ArgumentParser(description="Remove empty aside article-cards (left/right placeholders).")
    p.add_argument('--folder','-f', required=True, help="Folder with localized html files")
    p.add_argument('--apply', action='store_true', help="Actually overwrite files")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before overwriting")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    files = [os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')]
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