# scan_ar_candidates.py
# Save to C:\TimerHavenWebsite\scan_ar_candidates.py
# Usage:
#   python scan_ar_candidates.py
#
# What it does:
# - Scans C:\TimerHavenWebsite\ar for .html files (skips *.ftfy.bak and candidates dir)
# - For each file it creates multiple candidate decodings in ar/candidates/<relative-path>.<tag>.html
# - Writes ar/candidates/report.txt with a per-file summary and recommended candidate
#
# IMPORTANT: This script does NOT modify original files.

import os, re, errno
from pathlib import Path

BASE = r"C:\TimerHavenWebsite\ar"
CANDIDATES_DIR = os.path.join(BASE, "candidates")
os.makedirs(CANDIDATES_DIR, exist_ok=True)

pattern = re.compile(r"[ÃÂâ]")   # tokens we looked for before

def write_candidate(relpath, tag, text):
    out_path = os.path.join(CANDIDATES_DIR, relpath + "." + tag + ".html")
    out_dir = os.path.dirname(out_path)
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return out_path

def count_tokens(s):
    return len(pattern.findall(s))

report_lines = []
total_files = 0
total_matches = 0

for root, _, files in os.walk(BASE):
    # skip candidates folder itself
    if os.path.abspath(root).startswith(os.path.abspath(CANDIDATES_DIR)):
        continue
    for fn in files:
        if not fn.lower().endswith(".html"):
            continue
        total_files += 1
        abs_path = os.path.join(root, fn)
        relpath = os.path.relpath(abs_path, BASE)
        # skip backups
        if relpath.endswith(".ftfy.bak") or ".ftfy.bak" in relpath:
            continue
        try:
            b = open(abs_path, "rb").read()
        except Exception as e:
            report_lines.append(f"ERROR reading {relpath}: {e}")
            continue

        candidates = {}
        # candidate: original decoded as utf-8 (replace)
        try:
            s_utf8 = b.decode("utf-8", "replace")
        except Exception:
            s_utf8 = b.decode("utf-8", "replace")
        candidates["utf8"] = s_utf8

        # single-byte Arabic windows codepage CP1256
        try:
            s_1256 = b.decode("cp1256", "replace")
            candidates["cp1256"] = s_1256
        except Exception:
            pass

        # cp1252
        try:
            s_1252 = b.decode("cp1252", "replace")
            candidates["cp1252"] = s_1252
        except Exception:
            pass

        # iso-8859-1 (latin1)
        try:
            s_28591 = b.decode("iso-8859-1", "replace")
            candidates["iso8859"] = s_28591
        except Exception:
            pass

        # unicode (utf-16 little endian)
        try:
            s_utf16 = b.decode("utf-16", "replace")
            candidates["utf16"] = s_utf16
        except Exception:
            pass

        # round-trip: decode as cp1256 then re-encode as cp1256 bytes then decode as utf-8
        try:
            t = b.decode("cp1256", "replace")
            rt = t.encode("cp1256", "replace")
            rt_utf8 = rt.decode("utf-8", "replace")
            candidates["rt_from_1256"] = rt_utf8
        except Exception:
            pass

        # round-trip from cp1252
        try:
            t2 = b.decode("cp1252", "replace")
            rt2 = t2.encode("cp1252", "replace")
            rt2_utf8 = rt2.decode("utf-8", "replace")
            candidates["rt_from_1252"] = rt2_utf8
        except Exception:
            pass

        # apply a quick ftfy pass to the utf8 candidate (useful)
        try:
            import ftfy
            candidates["utf8_ftfy"] = ftfy.fix_text(candidates["utf8"])
        except Exception:
            pass

        # Save candidates and score them
        scores = []
        for tag, text in candidates.items():
            tokcount = count_tokens(text)
            scores.append((tokcount, tag))
            write_candidate(relpath, tag, text)

        if scores:
            scores.sort(key=lambda x: x[0])
            best_count, best_tag = scores[0]
            report_lines.append(f"{relpath}  -> best: {best_tag} (tokens={best_count})  all: {scores}")
            if best_count > 0:
                total_matches += 1
        else:
            report_lines.append(f"{relpath}  -> no candidates")

# Write report
report_path = os.path.join(CANDIDATES_DIR, "report.txt")
with open(report_path, "w", encoding="utf-8") as fh:
    fh.write("Scan report for folder: " + BASE + "\n\n")
    fh.write("\n".join(report_lines))
    fh.write("\n\nTOTAL FILES: %d\nFILES WITH TOKENS: %d\n" % (total_files, total_matches))

print("Done. Candidates and report written to:", CANDIDATES_DIR)
print("Report:", report_path)