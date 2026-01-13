# run_list_live_mojibake.py
# Usage:
#   python C:\TimerHavenWebsite\run_list_live_mojibake.py
#
# Prints HTML file paths that contain mojibake tokens (Ã, Â, â)
# but ignores directories whose path contains "archive-" or "removed-by-ftfy".

import os
import re
base = r"C:\TimerHavenWebsite"
pattern = re.compile(r"[ÃÂâ]")

def is_live_path(path):
    low = path.lower()
    if "archive-" in low or "removed-by-ftfy" in low:
        return False
    return True

matches = []
for root, _, files in os.walk(base):
    # skip archive/removed directories right away
    if not is_live_path(root):
        continue
    for fn in files:
        if not fn.lower().endswith(".html"):
            continue
        path = os.path.join(root, fn)
        try:
            bs = open(path, "rb").read()
            text = bs.decode("utf-8", "replace")
        except Exception as e:
            print("ERROR reading:", path, e)
            continue
        if pattern.search(text):
            matches.append(path)

if not matches:
    print("NO_MATCHES")
else:
    for p in matches:
        print(p)
    print()
    print("TOTAL:", len(matches))