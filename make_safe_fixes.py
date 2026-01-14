# make_safe_fixes.py
# Save to C:\TimerHavenWebsite\make_safe_fixes.py
# Usage: python C:\TimerHavenWebsite\make_safe_fixes.py
#
# Produces C:\TimerHavenWebsite\fixes-to-apply.safe.txt containing:
# - entries where best_tag != 'utf8' (we will use best_tag)
# - OR entries where best_tag == 'utf8' but tokens==0
#
# This reduces risk of applying utf8 to files that still display mojibake.

import os, re, sys
BASE = r"C:\TimerHavenWebsite"
REPORT = os.path.join(BASE, "ar", "candidates", "report.txt")
OUT = os.path.join(BASE, "fixes-to-apply.safe.txt")
if not os.path.exists(REPORT):
    print("Report not found:", REPORT); sys.exit(2)

pattern = re.compile(r"^(?P<rel>.+?)\s+->\s+best:\s+(?P<tag>[\w_]+)\s+\(tokens=(?P<t>\d+)\)")
lines = open(REPORT, "r", encoding="utf-8").read().splitlines()
out = []
for ln in lines:
    m = pattern.match(ln)
    if not m:
        continue
    rel = m.group("rel").strip()
    tag = m.group("tag").strip()
    toks = int(m.group("t"))
    orig = os.path.normpath(os.path.join(BASE, "ar", rel))
    if not os.path.exists(orig):
        print("Skipping missing original (report):", orig)
        continue
    # Include when best_tag != utf8 (we'll use that tag),
    # or when best_tag == utf8 but token count is zero (safe)
    if tag.lower() != "utf8" or toks == 0:
        out.append(f"{orig}|{tag}")

with open(OUT, "w", encoding="utf-8") as fh:
    for ln in out:
        fh.write(ln + "\n")
print("Wrote", len(out), "entries to", OUT)
print("Open the file and review it before applying with apply_fix_selected.py")