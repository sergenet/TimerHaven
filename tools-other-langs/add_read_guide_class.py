#!/usr/bin/env python3
"""
add_read_guide_class.py

- Dry-run by default: reports which files would be changed.
- Use --apply to write changes.
- Use --backup to create .bak copies before writing.
- Optionally use --file to target a single filename (relative to folder).
"""
import argparse
import os
from bs4 import BeautifulSoup

def matches_cta(el):
    # match common CTA anchors:
    # - anchors with class "cta"
    # - anchors whose text contains "read" and "guide" (best-effort, case-insensitive)
    txt = (el.get_text() or "").strip().lower()
    classes = " ".join(el.get("class") or []).lower()
    href = (el.get("href") or "").lower()
    if "cta" in classes:
        return True
    if "read" in txt and "guide" in txt:
        return True
    # also match anchors that include 'index' and the tool name (best-effort)
    if href.endswith("-index.html") or href.endswith("/index.html"):
        return True
    return False

def process(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, 'lxml')
    changed = False
    notes = []
    anchors = soup.find_all('a')
    touched = []
    for a in anchors:
        if matches_cta(a):
            classes = set(a.get('class') or [])
            if 'read-guide' not in classes:
                classes.add('read-guide')
                a['class'] = list(classes)
                changed = True
                touched.append('add-class')
            if a.get('target') != '_blank':
                a['target'] = '_blank'
                changed = True
                touched.append('target')
            rel = a.get('rel') or ''
            rel_parts = set(rel.split()) if rel else set()
            if 'noopener' not in rel_parts:
                rel_parts.add('noopener')
                a['rel'] = " ".join(sorted(rel_parts))
                changed = True
                touched.append('rel')
    if changed and apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: touched=" + ",".join(sorted(set(touched)))
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    elif changed:
        return True, f"DRY-RUN: {name}: would touch=" + ",".join(sorted(set(touched)))
    else:
        return False, f"NO-CHANGE: {name}"

def main():
    p = argparse.ArgumentParser(description="Add read-guide class + target/rel to CTA anchors.")
    p.add_argument('--folder','-f', required=True, help="Folder with HTML files")
    p.add_argument('--apply', action='store_true', help="Actually overwrite files")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before writing")
    p.add_argument('--file', help="Optional single filename (relative to folder) to process")
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
        ok, msg = process(pth, apply=args.apply, backup=args.backup)
        print(msg)

if __name__ == '__main__':
    main()