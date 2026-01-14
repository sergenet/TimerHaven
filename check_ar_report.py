# check_ar_report.py
# Save to C:\TimerHavenWebsite\check_ar_report.py
# Usage: python C:\TimerHavenWebsite\check_ar_report.py
#
# Prints files from ar/candidates/report.txt where the best tag is NOT 'utf8'
# so you can open those candidate HTML files and confirm the best tag visually.

import os, re, sys
BASE = r"C:\TimerHavenWebsite"
REPORT = os.path.join(BASE, "ar", "candidates", "report.txt")
if not os.path.exists(REPORT):
    print("Report not found:", REPORT)
    sys.exit(2)

pattern = re.compile(r"^(?P<rel>.+?)\s+->\s+best:\s+(?P<tag>[\w_]+)\s+\(tokens=(?P<t>\d+)\)")
lines = open(REPORT, "r", encoding="utf-8").read().splitlines()
found = []
for ln in lines:
    m = pattern.match(ln)
    if not m:
        continue
    rel = m.group("rel")
    tag = m.group("tag")
    toks = int(m.group("t"))
    if tag.lower() != "utf8":
        found.append((rel, tag, toks))

if not found:
    print("All best-tags are utf8 (or no report candidates).")
else:
    print("Files whose best tag != utf8 (inspect these candidates):\n")
    for rel, tag, toks in found:
        orig = os.path.normpath(os.path.join(BASE, "ar", rel))
        cand = os.path.normpath(os.path.join(BASE, "ar", "candidates", rel + "." + tag + ".html"))
        print(f"{rel}  -> best: {tag}  tokens={toks}")
        print(f"  orig: {orig}")
        print(f"  candidate: {cand}\n")
    print("Open candidate paths above in your browser to verify the rendering.")