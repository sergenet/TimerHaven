#!/usr/bin/env python3
"""
Small idempotent fixer for countdown-de.html to ensure 'Sekunden' is present.

Usage:
  python fix_de_countdown_text.py --folder "C:\TimerHavenWebsite\tools-other-langs" --file countdown-de.html   # dry-run
  python fix_de_countdown_text.py --folder ... --file countdown-de.html --apply --backup
"""
import argparse, os, sys
from bs4 import BeautifulSoup

def process(path, apply=False, backup=False):
    name = os.path.basename(path)
    try:
        src = open(path,'r',encoding='utf-8').read()
    except Exception as e:
        return False, f"ERROR reading {name}: {e}"
    soup = BeautifulSoup(src, 'lxml')
    # heuristic: find label/button/input that contains 'Sekunde' and ensure plural where needed
    changed = False
    notes = []
    for el in soup.find_all(text=True):
        t = str(el)
        if "Sekunde</" in t or ">Sekunde" in t or "Sekunde " in t or "Sekunde," in t:
            # if 'Sekunde' appears but not 'Sekunden' and context indicates plural label, we will replace whole word
            if "Sekunden" not in t:
                new = t.replace("Sekunde", "Sekunden")
                el.replace_with(new)
                changed = True
                notes.append("replaced-Sekunde->Sekunden")
    if not changed:
        return False, f"NO-CHANGE: {name}"
    if apply:
        if backup:
            open(path + '.bak','w',encoding='utf-8').write(src)
        open(path,'w',encoding='utf-8').write(str(soup))
        return True, f"APPLIED: {name}: " + ",".join(notes)
    else:
        return True, f"DRY-RUN: {name}: would " + ",".join(notes)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--folder','-f', required=True)
    p.add_argument('--file', required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--backup', action='store_true')
    args = p.parse_args()
    path = os.path.join(args.folder, args.file)
    if not os.path.isfile(path):
        print("ERROR file not found", path); sys.exit(1)
    ok, msg = process(path, apply=args.apply, backup=args.backup)
    print(msg)

if __name__ == '__main__':
    main()