# C:\TimerHavenWebsite\show_decodes_for_file.py
# Usage:
#   python C:\TimerHavenWebsite\show_decodes_for_file.py "C:\full\path\to\file.html"
#
# Prints byte-length, first 4 bytes, and first-400-char previews decoded several ways
# (utf-8, cp1252, cp1256, iso-8859-1, utf-16, rt_from_1252, rt_from_1256, utf8_ftfy)
# so we can pick the correct conversion.

import sys, os
from collections import OrderedDict

if len(sys.argv) < 2:
    print("Usage: python show_decodes_for_file.py <full-path-to-html>")
    sys.exit(2)

path = sys.argv[1]
if not os.path.exists(path):
    print("Missing file:", path); sys.exit(2)

b = open(path, "rb").read()
print("FILE:", path)
print("BYTES LENGTH:", len(b))
if len(b) >= 4:
    print("FIRST 4 BYTES:", " ".join(str(x) for x in b[0:4]))
else:
    print("SHORT FILE (<4 bytes)")

def preview(s, n=400):
    s2 = s.replace("\r","").replace("\n","\n")
    return s2[:n].replace("\n", "\\n")

def token_count(s):
    return s.count("Ã") + s.count("Â") + s.count("â") + s.count("\uFFFD")

candidates = OrderedDict()

# utf-8 (replace)
try:
    candidates["utf8"] = b.decode("utf-8", "replace")
except Exception as e:
    candidates["utf8"] = str(e)

# cp1256 (Arabic windows)
try:
    candidates["cp1256"] = b.decode("cp1256", "replace")
except Exception as e:
    candidates["cp1256"] = str(e)

# cp1252
try:
    candidates["cp1252"] = b.decode("cp1252", "replace")
except Exception as e:
    candidates["cp1252"] = str(e)

# iso-8859-1
try:
    candidates["iso8859"] = b.decode("iso-8859-1", "replace")
except Exception as e:
    candidates["iso8859"] = str(e)

# utf-16 LE (Unicode)
try:
    candidates["utf16"] = b.decode("utf-16", "replace")
except Exception as e:
    candidates["utf16"] = str(e)

# round-trip from cp1256 -> bytes -> decode as utf-8
try:
    t = b.decode("cp1256", "replace")
    rt = t.encode("cp1256", "replace")
    candidates["rt_from_1256"] = rt.decode("utf-8", "replace")
except Exception as e:
    candidates["rt_from_1256"] = str(e)

# round-trip from cp1252 -> bytes -> decode as utf-8
try:
    t2 = b.decode("cp1252", "replace")
    rt2 = t2.encode("cp1252", "replace")
    candidates["rt_from_1252"] = rt2.decode("utf-8", "replace")
except Exception as e:
    candidates["rt_from_1252"] = str(e)

# utf8 -> ftfy
try:
    import ftfy
    candidates["utf8_ftfy"] = ftfy.fix_text(candidates["utf8"])
except Exception as e:
    candidates["utf8_ftfy"] = "ftfy not available or error"

print("\nCANDIDATE PREVIEWS (first 400 chars) and token counts:")
for tag, text in candidates.items():
    tc = token_count(text)
    print("\n---", tag, "tokens=", tc)
    print(preview(text, 400))

print("\nDone. If cp1256 or rt_from_1256 looks correct, note that tag and we can apply it safely.")