#!/usr/bin/env python3
"""
normalize_layout_into_card.py

Purpose:
- Ensure each tool page uses the same structure (like the en pages):
  [back link]
  [tool title]
  [read-guide CTA]
  [tool content...]

- Dry-run by default. Use --apply to write files. Use --backup to create .bak copies.

Usage:
  Dry-run:
    python normalize_layout_into_card.py --folder "C:\TimerHavenWebsite\tools-other-langs"

  Apply (with backups):
    python normalize_layout_into_card.py --folder "C:\TimerHavenWebsite\tools-other-langs" --apply --backup

Notes:
- Requires beautifulsoup4 and lxml (you already installed these).
"""
import argparse
import os
from bs4 import BeautifulSoup

# Phrases to detect "back to main menu" in multiple languages (case-insensitive)
BACK_TEXT_KEYWORDS = [
    "back to main", "back to", "retour au menu", "zurück zum", "volver al menu",
    "volver al menú", "volver al menú principal", "volver al menú", "voltar ao menu",
    "главное меню", "القائمة الرئيسية", "رجوع", "戻る", "トップに戻る", "返回主菜单"
]

def text_contains_any(text, keywords):
    t = (text or "").strip().lower()
    return any(k in t for k in keywords)

def find_back_link(soup):
    # prefer explicit class or id
    el = soup.select_one('a.back-link, a#back-to-main, a[href*="main-menu"], a[href="index.html"]')
    if el:
        return el
    # fallback: find anchors whose text contains a back/menu keyword or starts with an arrow
    for a in soup.find_all('a'):
        txt = (a.get_text() or "").strip()
        if txt.startswith('←') or txt.startswith('←') or text_contains_any(txt, BACK_TEXT_KEYWORDS):
            return a
    return None

def find_title_heading(soup):
    # prefer headings already inside a .tool-card
    for sel in ['.tool-card h1', '.tool-card h2', '.tool-card h3', '.article-card h1', '.article-card h2', '.article-card h3']:
        h = soup.select_one(sel)
        if h:
            return h
    # fallback: first h1/h2/h3 in document
    for tag in ['h1','h2','h3']:
        h = soup.find(tag)
        if h:
            return h
    return None

def find_read_guide_anchor(soup):
    # find anchor already with read-guide class first
    a = soup.select_one('a.read-guide')
    if a:
        return a
    # other heuristics (class cta or text contains read+guide, or index links)
    for a in soup.find_all('a'):
        classes = " ".join(a.get('class') or [])
        txt = (a.get_text() or "").strip().lower()
        href = (a.get('href') or "").lower()
        if 'cta' in classes or ('read' in txt and 'guide' in txt) or href.endswith('-index.html') or href.endswith('/index.html'):
            return a
    return None

def is_inside_tool_card(el):
    if el is None:
        return False
    for p in el.parents:
        if not getattr(p, 'get', None):
            continue
        cls = " ".join(p.get("class") or [])
        if 'tool-card' in cls or 'article-card' in cls:
            return True
    return False

def dest_tool_card(soup):
    return soup.select_one('.tool-card') or soup.select_one('.article-card') or soup.select_one('.center-row .col') or soup.body or soup

def normalize_anchor_attrs(a):
    if a is None:
        return
    classes = set(a.get('class') or [])
    classes.add('read-guide')
    a['class'] = list(classes)
    if a.get('target') != '_blank':
        a['target'] = '_blank'
    rel = a.get('rel')
    if rel:
        rel_parts = set(rel if isinstance(rel, list) else str(rel).split())
    else:
        rel_parts = set()
    rel_parts.add('noopener')
    a['rel'] = " ".join(sorted(rel_parts))

def move_element_after(target, element):
    # insert element (already extracted) after target
    if target and target.parent:
        target.insert_after(element)
    else:
        # fallback: append to dest
        dd = dest_tool_card(element.find_parent() or element)
        dd.append(element)

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

    dest = dest_tool_card(soup)
    if dest is None:
        return False, f"NO-DEST: {name}"

    back = find_back_link(soup)
    title = find_title_heading(soup)
    cta = find_read_guide_anchor(soup)

    # ensure back link is at top of dest
    if back:
        if not is_inside_tool_card(back) or back.find_parent() != dest:
            # move it to be the first child of dest
            back.extract()
            # place at top
            dest.insert(0, back)
            changed = True
            notes.append("moved-back")
    # ensure title is directly under back (or top of dest)
    if title:
        if not is_inside_tool_card(title):
            # move title inside dest after back if back exists else at top
            title.extract()
            if back and back.parent == dest:
                back.insert_after(title)
            else:
                dest.insert(0, title)
            changed = True
            notes.append("moved-title")
        else:
            # if inside but not right after back, reposition it to be after back
            if back and title.parent == dest:
                # check order
                # if title precedes back, or not immediately after back, move it
                elems = [c for c in dest.children if getattr(c, 'name', None)]
                try:
                    idx_back = next(i for i,c in enumerate(elems) if c is back)
                    idx_title = next(i for i,c in enumerate(elems) if c is title)
                    if idx_title != idx_back + 1:
                        title.extract()
                        back.insert_after(title)
                        changed = True
                        notes.append("repositioned-title")
                except StopIteration:
                    pass

    # ensure CTA is normalized and placed directly after title
    if cta:
        normalize_anchor_attrs(cta)
        if not is_inside_tool_card(cta) or (title and cta.find_parent() != dest):
            # move cta after title
            cta.extract()
            wrapper = soup.new_tag('p')
            wrapper['style'] = "margin-top:1rem;"
            wrapper.append(cta)
            if title and (title.parent == dest):
                title.insert_after(wrapper)
            else:
                # if no title, place after back or at top
                if back and back.parent == dest:
                    back.insert_after(wrapper)
                else:
                    dest.insert(0, wrapper)
            changed = True
            notes.append("moved-cta")
    else:
        notes.append("no-cta-found")

    if not changed:
        return False, f"NO-CHANGE: {name}"

    if apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: " + ";".join(notes)
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would " + ";".join(notes)

def main():
    p = argparse.ArgumentParser(description="Normalize tool page layout so all content sits inside the card.")
    p.add_argument('--folder','-f', required=True, help="Folder with HTML files")
    p.add_argument('--file', help="Optional single filename to process")
    p.add_argument('--apply', action='store_true', help="Write changes")
    p.add_argument('--backup', action='store_true', help="Create .bak backups before writing")
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
        ok, msg = process_file(pth, apply=args.apply, backup=args.backup)
        print(msg)

if __name__=='__main__':
    main()