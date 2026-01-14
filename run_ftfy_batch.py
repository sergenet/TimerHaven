# run_ftfy_batch.py
# Usage:
# 1) create remaining-bad-files.txt in the same folder (one full path per line),
# 2) install ftfy: python -m pip install --user ftfy
# 3) run: python run_ftfy_batch.py
#
# The script creates backups named "<original>.ftfy.bak" for each file it modifies.

import os
import shutil
import ftfy
import sys

BASE = os.path.abspath(os.path.dirname(__file__))
LISTFILE = os.path.join(BASE, "remaining-bad-files.txt")

if not os.path.exists(LISTFILE):
    print("Error: remaining-bad-files.txt not found in", BASE)
    sys.exit(2)

paths = []
with open(LISTFILE, "r", encoding="utf-8") as fh:
    for line in fh:
        p = line.strip()
        if not p:
            continue
        # Normalize path
        p = os.path.abspath(p)
        paths.append(p)

if not paths:
    print("No paths found in remaining-bad-files.txt")
    sys.exit(0)

fixed_count = 0
nochange_count = 0
error_count = 0

for p in paths:
    try:
        if not os.path.exists(p):
            print("MISSING:", p)
            error_count += 1
            continue
        # Safety check: ensure file is under BASE (avoid accidental system-wide edits)
        try:
            common = os.path.commonpath([BASE, p])
        except ValueError:
            common = None
        if common != BASE:
            print("SKIP (outside base):", p)
            error_count += 1
            continue

        raw_bytes = open(p, "rb").read()
        # decode using utf-8 with replacement (we're repairing mojibake in utf-8 text)
        raw = raw_bytes.decode("utf-8", "replace")
        fixed = ftfy.fix_text(raw)

        if fixed != raw:
            bak = p + ".ftfy.bak"
            shutil.copy2(p, bak)
            open(p, "w", encoding="utf-8").write(fixed)
            print("fixed:", p)
            fixed_count += 1
        else:
            print("no change:", p)
            nochange_count += 1

    except Exception as e:
        print("ERROR:", p, e)
        error_count += 1

print()
print("SUMMARY")
print("  total paths:", len(paths))
print("  fixed:", fixed_count)
print("  no change:", nochange_count)
print("  errors/missing/skipped:", error_count)