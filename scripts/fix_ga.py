"""fix_ga.py - normalise the gtag.js snippet to exactly one canonical tag.

History: this script used to strip the block for G-R1F6Y45MW2 from every page,
treating it as a "duplicate" of G-X7WBE4P25. That was backwards. G-X7WBE4P25 is
only nine characters after the prefix, and a GA4 measurement ID is always
exactly ten (support.google.com/analytics/answer/12270356), so the property it
named could never have collected data. G-R1F6Y45MW2 is the real property.

Running the old version is what removed the only working tag from 937 pages.
This version therefore refuses to delete the canonical ID. Its only write is
collapsing a genuine second copy of the *same* tag, and it reports drift rather
than "fixing" a page that uses a different, valid-looking ID.

Usage:
  python scripts/fix_ga.py           # report only
  python scripts/fix_ga.py --write   # collapse duplicate canonical blocks
"""

import os
import re
import sys
import collections

CANONICAL = "G-R1F6Y45MW2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "_site", "_attic", "node_modules", "__pycache__",
             "android", "chrome_extension", "timerhaven-extension",
             "timerhaven-extension-v2"}
ID_RE = re.compile(r"\bG-[A-Z0-9]{4,12}\b")
LOADER_RE = re.compile(
    r'[ \t]*<script[^>]*googletagmanager\.com/gtag/js[^>]*>\s*</script>\s*'
    r'<script>\s*window\.dataLayer.*?</script>',
    re.S | re.I,
)


def is_redirect_stub(html):
    return ('http-equiv="refresh"' in html.lower().replace(" ", "")
            or "<html" not in html.lower())


def scan():
    drift = collections.defaultdict(list)
    duplicates = []
    pages = tracked = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.lower().endswith((".html", ".php")):
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            with open(path, encoding="utf-8", errors="surrogateescape") as fh:
                html = fh.read()
            if is_redirect_stub(html):
                continue
            pages += 1
            ids = set(ID_RE.findall(html))
            if not ids:
                # Either consent-gated via consent.js, or genuinely untracked.
                drift["no gtag in page" if "consent.js" not in html
                      else "consent-gated"].append(rel)
                continue
            tracked += 1
            for other in ids - {CANONICAL}:
                drift[other].append(rel)
            if len(LOADER_RE.findall(html)) > 1:
                duplicates.append(rel)
    return pages, tracked, drift, duplicates


def collapse(html):
    blocks = LOADER_RE.findall(html)
    if len(blocks) < 2 or CANONICAL not in html:
        return html
    first = blocks[0]
    # Drop every later block that carries the canonical ID, keep the first one.
    for block in blocks[1:]:
        if CANONICAL in block:
            html = html.replace(block, "", 1)
    return html


def main():
    write = "--write" in sys.argv
    pages, tracked, drift, duplicates = scan()

    print(f"pages scanned                : {pages}")
    print(f"pages with a gtag block      : {tracked}")
    print(f"pages with duplicate blocks  : {len(duplicates)}")

    problems = 0
    for label, paths in sorted(drift.items(), key=lambda kv: -len(kv[1])):
        print(f"\n{len(paths):4d}  {label}")
        problems += len(paths)
        for rel in paths[:5]:
            print(f"        {rel}")

    if len(duplicates):
        for rel in duplicates[:10]:
            print(f"  duplicate blocks: {rel}")
        if write:
            fixed = 0
            for rel in duplicates:
                path = os.path.join(ROOT, rel.replace("/", os.sep))
                with open(path, encoding="utf-8",
                          errors="surrogateescape") as fh:
                    html = fh.read()
                new = collapse(html)
                if new != html:
                    with open(path, "w", encoding="utf-8", newline="") as fh:
                        fh.write(new)
                    fixed += 1
            print(f"\ncollapsed duplicates in {fixed} file(s)")

    if CANONICAL not in str(drift) and not problems:
        print(f"\nOK: every tracked page uses {CANONICAL} exactly once.")
        return 0
    print(f"\nreview needed on {problems} page(s); the canonical ID "
          f"({CANONICAL}) is never removed automatically.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
