# C:\TimerHavenWebsite\scan_ar_content_check.py
# Usage:
#   python C:\TimerHavenWebsite\scan_ar_content_check.py
#
# Scans C:\TimerHavenWebsite\ar for .html files and reports:
#  - files that contain very few Arabic letters (likely missing content)
#  - files that contain common English placeholder strings like "Read Full Article"
#
# This script is read-only and does not modify any files.

import os, re
BASE = r"C:\TimerHavenWebsite\ar"
arabic_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
placeholder_re = re.compile(r'Read Full|Read full|Read Full Article|Read full article|Read full guide', re.I)

results = []
for root, _, files in os.walk(BASE):
    for fn in files:
        if not fn.lower().endswith(".html"):
            continue
        path = os.path.join(root, fn)
        try:
            text = open(path, "rb").read().decode("utf-8", "replace")
        except Exception as e:
            results.append((path, "ERROR", str(e)))
            continue
        arabic_count = len(arabic_re.findall(text))
        has_placeholder = bool(placeholder_re.search(text))
        # Report files with very few Arabic characters OR that contain English placeholder text
        if arabic_count < 20 or has_placeholder:
            tag = "PLACEHOLDER" if has_placeholder else "LOW_ARABIC"
            results.append((path, arabic_count, tag))

if not results:
    print("No low-arabic / placeholder files found under", BASE)
else:
    for p,c,tag in results:
        print(f"{p}  -> {tag}  arabic_count={c}")
    print("\nTOTAL:", len(results))