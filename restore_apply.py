# C:\TimerHavenWebsite\restore_apply.py
# Usage:
#   python C:\TimerHavenWebsite\restore_apply.py
#
# This will copy each *.ftfy.bak under C:\TimerHavenWebsite\ar
# back to its original filename ONLY when the current original
# file contains fewer than 20 Arabic letters (same logic as the dry-run).
# Backups are kept intact (we copy, not move).

import os, re, shutil

BASE = r"C:\TimerHavenWebsite\ar"
arab_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')

restored = 0
skipped = 0
errors = []

for root, _, files in os.walk(BASE):
    for fn in files:
        if not fn.lower().endswith(".ftfy.bak"):
            continue
        bak = os.path.join(root, fn)
        orig = bak[:-len(".ftfy.bak")]
        try:
            if not os.path.exists(orig):
                # original missing -> restore
                shutil.copy2(bak, orig)
                print("restored (original missing):", orig)
                restored += 1
                continue
            # read original as utf-8 (replace)
            text = open(orig, "rb").read().decode("utf-8", "replace")
            count = len(arab_re.findall(text))
            if count < 20:
                shutil.copy2(bak, orig)
                print(f"restored: {orig}  (was arabic_count={count})")
                restored += 1
            else:
                print(f"kept:    {orig}  (arabic_count={count})")
                skipped += 1
        except Exception as e:
            errors.append((orig, str(e)))
            print("ERROR for", orig, e)

print("\nDone. Restored:", restored, "Skipped:", skipped, "Errors:", len(errors))
if errors:
    for o,e in errors[:20]:
        print("ERR:", o, e)