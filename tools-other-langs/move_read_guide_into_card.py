#!/usr/bin/env python3
"""
Move 'Read full guide' CTA into the .tool-card area for tool pages.

- Dry-run by default (reports what it WOULD change).
- Use --apply to write changes.
- Use --backup to create .bak copies before writing.

Usage:
  Dry-run for a folder:
    python move_read_guide_into_card.py --folder "C:\TimerHavenWebsite\tools-other-langs"

  Apply with backups:
    python move_read_guide_into_card.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup

  Operate on a single file:
    python move_read_guide_into_card.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file "clipboard-manager-de.html" --apply --backup
"""
import argparse
import os
from bs4 import BeautifulSoup

def looks_like_cta(a):
    txt = (a.get_text() or "").strip().lower()
    classes = " ".join(a.get("class") or []).lower()
    href = (a.get("href") or "").lower()
    if "read-guide" in classes or "cta" in classes:
        return True
    if "read" in txt and "guide" in txt:
        return True
    if href.endswith("-index.html") or href.endswith("/index.html"):
        return True
    return False

def is_inside_tool_card(a):
    for p in a.parents:
        cls = " ".join(p.get("class") or [])
        if "tool-card" in cls or "article-card" in cls:
            return True
    return False

def normalize_anchor(a):
    classes = set(a.get("class") or [])
    classes.add("read-guide")
    a['class'] = list(classes)
    if a.get("target") != "_blank":
        a['target'] = "_blank"
    rel = a.get("rel")
    if rel:
        if isinstance(rel, list):
            rel_parts = set(rel)
        else:
            rel_parts = set(str(rel).split())
    else:
        rel_parts = set()
    rel_parts.add("noopener")
    a['rel'] = " ".join(sorted(rel_parts))

def move_into_tool(soup, a):
    # Find a destination tool-card
    dest = soup.select_one(".tool-card") or soup.select_one(".article-card") or soup.select_one(".center-row .col")
    if not dest:
        dest = soup.body or soup
    # Normalize anchor attributes
    normalize_anchor(a)
    # Create wrapper <p> for spacing (match earlier scripts)
    wrapper = soup.new_tag("p")
    wrapper['style'] = "margin-top:1rem;"
    # Remove anchor from current location and insert
    a.extract()
    wrapper.append(a)
    # Insert after first heading in dest (h1/h2/h3) if present, else at top of dest
    header = dest.find(['h1','h2','h3'])
    if header:
        header.insert_after(wrapper)
    else:
        dest.insert(0, wrapper)

def process_path(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, "lxml")
    anchors = soup.find_all('a')
    cta = None
    for a in anchors:
        if looks_like_cta(a):
            cta = a
            break
    if not cta:
        return False, f"NO-CTA: {name}"
    if is_inside_tool_card(cta):
        return False, f"ALREADY-IN-TOOL: {name}"
    # perform move
    move_into_tool(soup, cta)
    if apply:
        try:
            if backup:
                with open(path + ".bak", 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: moved CTA into tool-card"
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would move CTA into tool-card"

def main():
    p = argparse.ArgumentParser(description="Move Read guide CTA into tool card")
    p.add_argument("--folder", "-f", required=True, help="Folder with HTML files")
    p.add_argument("--apply", action="store_true", help="Write changes")
    p.add_argument("--backup", action="store_true", help="Create .bak backups before writing")
    p.add_argument("--file", help="Optional single filename (relative to folder)")
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"ERROR: folder not found: {folder}")
        return

    targets = []
    if args.file:
        targets = [os.path.join(folder, args.file)]
    else:
        targets = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])

    for t in targets:
        ok, msg = process_path(t, apply=args.apply, backup=args.backup)
        print(msg)

if __name__ == '__main__':
    main()