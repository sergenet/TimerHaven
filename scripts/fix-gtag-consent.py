#!/usr/bin/env python3
"""Make TimerHaven's AdSense/GA gate actually hold.

Pages carried an eager gtag.js loader in <head> *and* /assets/js/consent.js.
consent.js only requests Google services after a visitor presses Accept, so the
eager block defeated the gate: analytics fired for everyone, including visitors
who never answered the banner.

This removes the eager block and leaves consent.js as the single loader. Pages
that had the loader but no gate reference get the gate reference added.

Idempotent. Usage:
  python scripts/fix-gtag-consent.py [--dry-run]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GA_ID = "G-R1F6Y45MW2"

SKIP_DIRS = {
    "_site", "_attic", "node_modules", ".git", "chrome_extension",
    "timerhaven-extension", "timerhaven-extension-v2", "docs", "tmp",
    "tools", "scripts", "__pycache__",
}

LOADER_RE = re.compile(
    r"(?:[ \t]*<!--[^\n]*gtag\.js[^\n]*-->\r?\n)?"
    r"[ \t]*<script[^>]*googletagmanager\.com/gtag/js\?id=" + re.escape(GA_ID)
    + r"[^>]*>\s*</script>[ \t]*\r?\n?",
    re.I,
)

CONFIG_RE = re.compile(
    r"[ \t]*<script>\s*"
    r"window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];.*?"
    r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]" + re.escape(GA_ID) + r"['\"]\s*\);\s*"
    r"</script>[ \t]*\r?\n?",
    re.S,
)

CSS_LINK = '<link rel="stylesheet" href="/assets/css/consent.css" media="print" onload="this.media=\'all\'">\n'
JS_SCRIPT = '<script src="/assets/js/consent.js" defer></script>\n'


def pages():
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        yield path, rel


def process(path: Path, dry_run: bool) -> str:
    with open(path, encoding="utf-8", newline="") as handle:
        raw = handle.read()
    original = raw

    raw, n_loader = LOADER_RE.subn("", raw)
    raw, n_config = CONFIG_RE.subn("", raw)

    if "googletagmanager.com/gtag/js" in raw:
        return "FAIL loader still present"
    if "gtag('config'" in raw or 'gtag("config"' in raw:
        return "FAIL inline config still present"

    added = []
    if n_loader or n_config:
        # Gate references are only meaningful with the loader gone; add them
        # where the page never had them.
        if "/assets/js/consent.js" not in raw and "assets/js/consent.js" not in raw:
            if "</head>" in raw:
                raw = raw.replace("</head>", JS_SCRIPT + "</head>", 1)
                added.append("js")
        if "consent.css" not in raw:
            if "</head>" in raw:
                raw = raw.replace("</head>", CSS_LINK + "</head>", 1)
                added.append("css")

    if raw != original and not dry_run:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(raw)

    if not n_loader and not n_config:
        return "clean"
    return "removed loader=%d config=%d%s" % (
        n_loader, n_config, (" +added " + ",".join(added)) if added else ""
    )


def main():
    dry_run = "--dry-run" in sys.argv
    counts = {}
    failures = []
    for path, rel in pages():
        result = process(path, dry_run)
        key = result.split(" ")[0]
        counts[key] = counts.get(key, 0) + 1
        if result.startswith("FAIL"):
            failures.append((str(rel), result))
        elif result.startswith("removed") and ("loader=0" in result or "config=0" in result):
            # Half a block is suspicious; report so it can be inspected.
            print("partial: %-44s %s" % (rel, result))

    print()
    for key in sorted(counts):
        print("%-12s %d" % (key, counts[key]))
    if failures:
        print("\nFAILURES:")
        for rel, msg in failures[:20]:
            print("  %-44s %s" % (rel, msg))
    print("\n%s" % ("dry run, nothing written" if dry_run else "written"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
