#!/usr/bin/env python3
"""Audit every canonical tag in the TimerHaven tree.

Classes of defect, in order of severity:
  DOUBLE-SLASH  href has "//" after the host -> a different URL, tag discarded
  RELATIVE      href is not absolute
  MISSING       no canonical tag at all
  DUPLICATE     two tags on one page (first wins, silently)
  NOT-SELF      href names a different URL than the file's own path

NOT-SELF is reported only: whether a page should canonicalise elsewhere is a
content decision, not something to rewrite automatically.

Run:  python scripts/check_canonicals.py [--json out.json]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\TimerHavenWebsite")
BASE = "https://timerhaven.com"
SKIP_DIRS = {"node_modules", "_site", ".git", ".tmpcheck", "scripts", "assets"}
SKIP_FILES = {"404.html", "500.html"}

CANON = re.compile(r"""(?is)<link\b[^>]*\brel\s*=\s*["']?canonical["']?[^>]*>""")
HREF = re.compile(r"""(?is)\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""")


def url_for(rel_path: str) -> str:
    if rel_path in ("index.html", "/index.html"):
        return BASE + "/"
    return f"{BASE}/{rel_path}"


def main():
    rows = []
    files = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in rel.split("/")[:-1]):
            continue
        if rel in SKIP_FILES or rel.startswith("."):
            continue
        files.append((rel, p))

    for rel, path in sorted(files):
        try:
            html = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        tags = CANON.findall(html) or [" ".join(m) for m in CANON.findall(html)]
        tags = [m.group(0) for m in CANON.finditer(html)]
        want = url_for(rel)
        if not tags:
            rows.append({"file": rel, "class": "MISSING", "canonical": None, "want": want})
            continue
        if len(tags) > 1:
            rows.append({"file": rel, "class": "DUPLICATE", "canonical": len(tags), "want": want})
            continue
        m = HREF.search(tags[0])
        href = next((g for g in m.groups() if g is not None), "").strip() if m else ""
        if not href:
            rows.append({"file": rel, "class": "MISSING", "canonical": None, "want": want})
        elif "//" in href.split("://", 1)[-1]:
            rows.append({"file": rel, "class": "DOUBLE-SLASH", "canonical": href, "want": want})
        elif not href.startswith(("http://", "https://")):
            rows.append({"file": rel, "class": "RELATIVE", "canonical": href, "want": want})
        elif href != want:
            rows.append({"file": rel, "class": "NOT-SELF", "canonical": href, "want": want})

    by_class = {}
    for r in rows:
        by_class.setdefault(r["class"], []).append(r)

    print(f"{len(files)} HTML files scanned, {len(files) - len(rows)} with a correct self-canonical\n")
    for cls in ("DOUBLE-SLASH", "RELATIVE", "DUPLICATE", "MISSING", "NOT-SELF"):
        items = by_class.get(cls, [])
        if not items:
            continue
        print(f"=== {cls}: {len(items)} ===")
        for r in items:
            if cls == "NOT-SELF":
                print(f"  {r['file']:<52} -> {r['canonical']}")
            else:
                print(f"  {r['file']}")
        print()

    if "--json" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
        print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
