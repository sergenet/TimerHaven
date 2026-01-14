# apply_best_for_ar.py
# Usage:
# 1) Ensure you already ran scan_ar_candidates.py so:
#    C:\TimerHavenWebsite\ar\candidates\report.txt exists.
# 2) Save this file to C:\TimerHavenWebsite\apply_best_for_ar.py
# 3) Run: python C:\TimerHavenWebsite\apply_best_for_ar.py
#
# What it does:
# - parses the report.txt written by scan_ar_candidates.py
# - for each original file, chooses the 'best' candidate tag and writes a line to
#   C:\TimerHavenWebsite\fixes-to-apply.txt in the form:
#     C:\TimerHavenWebsite\ar\<relative-path>|<tag>
# - DOES NOT MODIFY original files. You must run apply_fix_selected.py afterwards.

import os, re, sys
BASE = r"C:\TimerHavenWebsite"
AR_BASE = os.path.join(BASE, "ar")
REPORT = os.path.join(AR_BASE, "candidates", "report.txt")
OUT = os.path.join(BASE, "fixes-to-apply.txt")

if not os.path.exists(REPORT):
    print("Report not found:", REPORT)
    sys.exit(2)

lines = open(REPORT, "r", encoding="utf-8").read().splitlines()
out_lines = []
pattern = re.compile(r"^(?P<rel>.+?)\s+->\s+best:\s+(?P<tag>[\w_]+)\s+\(tokens=(?P<t>\d+)\)")

for ln in lines:
    m = pattern.match(ln)
    if not m:
        continue
    rel = m.group("rel").strip()
    tag = m.group("tag").strip()
    tokens = int(m.group("t"))
    # If tokens are high you might want to inspect that file manually before fixing.
    orig = os.path.join(AR_BASE, rel)
    # normalize path
    orig = os.path.normpath(orig)
    if not os.path.exists(orig):
        print("Skipping (missing):", orig)
        continue
    # Only select candidates where tag is meaningful (not 'utf8' if it still has tokens)
    out_lines.append(f"{orig}|{tag}")

# Write tentative fixes file but do not overwrite an existing one without prompt
if os.path.exists(OUT):
    print("Existing fixes-to-apply.txt found at", OUT)
    print("It will be overwritten. If you want to preserve it, move it first.")
with open(OUT, "w", encoding="utf-8") as fh:
    for ln in out_lines:
        fh.write(ln + "\n")

print("Wrote", len(out_lines), "entries to", OUT)
print("IMPORTANT: Inspect the file before applying changes. Example first 20 lines:")
for ln in out_lines[:20]:
    print(" ", ln)
print("\nWhen ready, run: python C:\\TimerHavenWebsite\\apply_fix_selected.py")