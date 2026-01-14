# run_list_mojibake.py
# Save as C:\TimerHavenWebsite\run_list_mojibake.py and run:
#    python C:\TimerHavenWebsite\run_list_mojibake.py
#
# It prints each HTML file path that contains mojibake tokens (Ã, Â, â).

import os
import re
base = r"C:\TimerHavenWebsite"
pattern = re.compile(r"[ÃÂâ]")

matches = []
for root, _, files in os.walk(base):
    for fn in files:
        if not fn.lower().endswith(".html"):
            continue
        # skip our known test file patterns to reduce noise
        if fn.endswith(".ftfy.test.html") or fn.endswith(".repaired.test.html") or fn.endswith(".ftfy.bak"):
            continue
        path = os.path.join(root, fn)
        try:
            # read in binary then decode utf-8 replace to match what we fixed earlier
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