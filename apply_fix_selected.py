# apply_fix_selected.py
# Save to C:\TimerHavenWebsite\apply_fix_selected.py
# Usage:
# 1) Create fixes-to-apply.txt in C:\TimerHavenWebsite with lines:
#      <full-original-path>|<tag>
#    e.g. C:\TimerHavenWebsite\ar\calendar\calendar.html|cp1256
# 2) Run: python apply_fix_selected.py
#
# The script makes a backup: <original>.ftfy.bak (preserves timestamps) and writes fixed file as UTF-8.

import os, sys
import shutil

BASE = r"C:\TimerHavenWebsite"
LISTFILE = os.path.join(BASE, "fixes-to-apply.txt")
if not os.path.exists(LISTFILE):
    print("Create", LISTFILE, "with lines: <full-path>|<tag>")
    sys.exit(2)

def fix_file(path, tag):
    b = open(path, "rb").read()
    s = None
    try:
        if tag == "utf8":
            s = b.decode("utf-8", "replace")
        elif tag == "utf8_ftfy":
            import ftfy
            s = ftfy.fix_text(b.decode("utf-8", "replace"))
        elif tag == "cp1256":
            s = b.decode("cp1256", "replace")
        elif tag == "cp1252":
            s = b.decode("cp1252", "replace")
        elif tag == "iso8859":
            s = b.decode("iso-8859-1", "replace")
        elif tag == "utf16":
            s = b.decode("utf-16", "replace")
        elif tag == "rt_from_1256":
            t = b.decode("cp1256", "replace")
            s = t.encode("cp1256", "replace").decode("utf-8", "replace")
        elif tag == "rt_from_1252":
            t = b.decode("cp1252", "replace")
            s = t.encode("cp1252", "replace").decode("utf-8", "replace")
        else:
            print("Unknown tag:", tag)
            return False
    except Exception as e:
        print("ERROR decoding:", path, tag, e)
        return False

    # Backup original
    bak = path + ".ftfy.bak"
    shutil.copy2(path, bak)
    # Write fixed file in UTF-8
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(s)
    print("Fixed:", path, "-> tag:", tag, "backup:", bak)
    return True

count = 0
for ln in open(LISTFILE, "r", encoding="utf-8"):
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    if "|" not in ln:
        print("Bad line (missing |):", ln)
        continue
    path, tag = ln.split("|", 1)
    path = path.strip()
    tag = tag.strip()
    if not os.path.exists(path):
        print("Missing file:", path)
        continue
    if not os.path.abspath(path).startswith(os.path.abspath(BASE)):
        print("Skipping (outside base):", path)
        continue
    if fix_file(path, tag):
        count += 1

print("Done. Files fixed:", count)