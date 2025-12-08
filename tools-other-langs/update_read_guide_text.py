#!/usr/bin/env python3
"""
update_read_guide_text.py

- Dry-run by default: reports files where CTA text would be changed.
- Use --apply to write changes.
- Use --backup to create .bak copies before writing.

Behavior:
- Detects page language via <html lang="xx">, falling back to filename suffix (e.g. -de.html).
- Finds CTA anchors (class "read-guide" / "cta" / text contains "read" and "guide" / index links).
- Replaces anchor text with a language-appropriate phrase.
"""
import argparse
import os
from bs4 import BeautifulSoup

# translation mapping (edit any phrase if you'd prefer different wording)
TRANSLATIONS = {
    "en": "Read full guide",
    "de": "Vollständige Anleitung lesen",
    "es": "Leer la guía completa",
    "fr": "Lire le guide complet",
    "ru": "Читать полное руководство",
    "el": "Διαβάστε τον πλήρη οδηγό",
    "ar": "اقرأ الدليل الكامل",
}

def detect_lang(soup, path):
    # prefer <html lang="...">
    html = soup.find('html')
    if html and html.get('lang'):
        return html.get('lang').lower().split('-')[0]
    # fallback: try filename suffix like name-de.html
    name = os.path.basename(path).lower()
    parts = name.rsplit('-', 1)
    if len(parts) == 2 and parts[1].endswith('.html'):
        code = parts[1].replace('.html','')
        if code in TRANSLATIONS:
            return code
    return "en"

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

def process_file(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"

    soup = BeautifulSoup(src, 'lxml')
    lang = detect_lang(soup, path)
    new_text = TRANSLATIONS.get(lang, TRANSLATIONS['en'])

    changed = False
    notes = []
    for a in soup.find_all('a'):
        if looks_like_cta(a):
            current = (a.get_text() or "").strip()
            if current != new_text:
                a.string = new_text
                changed = True
                notes.append(f"set-text({lang})")
    if not changed:
        return False, f"NO-CHANGE: {name}"

    if apply:
        try:
            if backup:
                with open(path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"APPLIED: {name}: " + ",".join(notes)
        except Exception as e:
            return False, f"ERROR writing {name}: {e}"
    else:
        return True, f"DRY-RUN: {name}: would " + ",".join(notes)

def main():
    p = argparse.ArgumentParser(description="Set localized 'Read full guide' CTA text.")
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
        files = [os.path.join(folder, args.file)]
    else:
        files = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])

    for pth in files:
        ok, msg = process_file(pth, apply=args.apply, backup=args.backup)
        print(msg)

if __name__ == '__main__':
    main()