#!/usr/bin/env python3
# C:\TimerHavenWebsite\restore_dryrun.py
# Dry-run: list .ftfy.bak backups under ar and say whether we'd restore each original
# (we "would restore" when original is missing or contains <20 Arabic letters).
#
# Usage:
#   python C:\TimerHavenWebsite\restore_dryrun.py

import os, re

BASE = r"C:\TimerHavenWebsite\ar"
bak_paths = []
for root, _, files in os.walk(BASE):
    for fn in files:
        if fn.lower().endswith(".ftfy.bak"):
            bak_paths.append(os.path.join(root, fn))

if not bak_paths:
    print("No .ftfy.bak files found under", BASE)
    raise SystemExit(0)

arab_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')

for bak in sorted(bak_paths):
    orig = bak[:-len(".ftfy.bak")]
    if not os.path.exists(orig):
        print("WILL RESTORE (original missing):", orig)
        print("  bak:", bak)
        continue
    try:
        text = open(orig, "rb").read().decode("utf-8", "replace")
    except Exception as e:
        print("ERROR reading original:", orig, e)
        continue
    count = len(arab_re.findall(text))
    if count < 20:
        print(f"WILL RESTORE: {orig}  (arabic_count={count})")
        print("  bak:", bak)
    else:
        print(f"SKIP:         {orig}  (arabic_count={count})")
print("\nDone. This was a dry-run (no files changed).")