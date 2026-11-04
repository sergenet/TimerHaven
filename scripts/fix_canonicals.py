#!/usr/bin/env python3
"""Fix TimerHaven canonical tags the 2026-11-01 audit proved wrong.

Three defects, each justified by measurement in site-audits/00-MASTER.md:

 1. 21 locale guide stubs under <locale>/<feature>/<feature>-index.html declare a
    canonical pointing at a 404 (/en/pomodoro-index.html, /fr/focus-music/...)
    or at an unrelated page (/en/task-timer/ -> /timer-en.html, a different
    page). Visible-text similarity to every candidate page is <= 0.18, so they
    are distinct content, not duplicates: their canonical must be themselves.

 2. contact/privacy/terms declare https://timerhaven.com//<page>.html. The
    doubled slash is a different URL, so the tag is discarded.

 3. meeting-how-to.html is byte-identical French content (similarity 1.00,
    179 words) to meeting-how-to-fr.html, sitting at the English URL. Its
    canonical points at the French original.

Every edit is head-only and verified: exactly one canonical tag before and
after, and the surrounding bytes are asserted unchanged.

Run:  python scripts/fix_canonicals.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\TimerHavenWebsite")
BASE = "https://timerhaven.com"
LOCALES = ["en", "ar", "de", "el", "es", "fr", "ru"]
FEATURES = {"pomodoro-timer": "pomodoro", "focus-music": "focus-music", "task-timer": "task-timer"}
DOUBLE_SLASH = ["contact.html", "privacy.html", "terms.html"]
DUP_TO_FR = ["meeting-how-to.html"]

CANON = re.compile(r"""(?is)<link\b[^>]*\brel\s*=\s*["']?canonical["']?[^>]*>""")
HREF = re.compile(r"""(?is)(\bhref\s*=\s*)(?:"([^"]*)"|'([^']*)'|([^\s>]+))""")


def read(path: Path) -> str:
    # newline='' keeps CRLF exactly as stored; encoding='utf-8' keeps any BOM.
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def set_canonical(path: Path, want: str, dry: bool) -> tuple[bool, str]:
    """Point the single canonical tag at `want`. Returns (changed, detail)."""
    text = read(path)
    tags = list(CANON.finditer(text))
    if not tags:
        return insert_canonical(path, text, want, dry)
    if len(tags) != 1:
        return False, f"REFUSED ({len(tags)} canonical tags, expected 1)"
    tag = tags[0]
    m = HREF.search(tag.group(0))
    if not m:
        return False, "REFUSED (canonical tag has no href)"
    old = next(g for g in m.groups()[1:] if g is not None)
    if old == want:
        return False, "already correct"
    new_tag = tag.group(0)[: m.start()] + m.group(1) + f'"{want}"' + tag.group(0)[m.end():]
    new_text = text[: tag.start()] + new_tag + text[tag.end():]
    # Verify the only change is the canonical tag.
    if len(CANON.findall(new_text)) != 1:
        return False, "REFUSED (would change the tag count)"
    if new_text.replace(new_tag, "", 1) != text.replace(tag.group(0), "", 1):
        return False, "REFUSED (edit escaped the canonical tag)"
    if not dry:
        write(path, new_text)
    return True, f"{old}  ->  {want}"


def insert_canonical(path: Path, text: str, want: str, dry: bool) -> tuple[bool, str]:
    """Add a canonical tag immediately before </head> on a page that has none."""
    m = re.search(r"(?is)</head>", text)
    if not m:
        return False, "REFUSED (no </head>)"
    # Match the indentation of the preceding line so the diff stays minimal.
    prefix = "  "
    line_start = text.rfind("\n", 0, m.start())
    if line_start != -1:
        lead = text[line_start + 1: m.start()]
        if lead.strip() == "":
            prefix = lead
    tag = f'{prefix}<link rel="canonical" href="{want}" />\n'
    new_text = text[: line_start + 1] + tag + text[line_start + 1:]
    if len(CANON.findall(new_text)) != 1:
        return False, "REFUSED (insert produced the wrong tag count)"
    if new_text.replace(tag, "", 1) != text:
        return False, "REFUSED (insert escaped </head>)"
    if not dry:
        write(path, new_text)
    return True, f"(none)  ->  {want}"


def main():
    dry = "--dry-run" in sys.argv
    jobs: list[tuple[Path, str, str]] = []

    for loc in LOCALES:
        for folder, stem in FEATURES.items():
            for name in (f"{stem}-index.html", f"{folder}-index.html"):
                p = ROOT / loc / folder / name
                if p.exists():
                    rel = p.relative_to(ROOT).as_posix()
                    jobs.append((p, f"{BASE}/{rel}", f"{loc}/{folder}"))
                    break

    for rel in DOUBLE_SLASH:
        p = ROOT / rel
        if p.exists():
            jobs.append((p, f"{BASE}/{rel}", "double-slash"))

    for rel in DUP_TO_FR:
        p = ROOT / rel
        if p.exists():
            jobs.append((p, f"{BASE}/meeting-how-to-fr.html", "duplicate->fr"))

    print(f"{len(jobs)} files to check{' (dry-run)' if dry else ''}\n")
    changed = failed = 0
    for path, want, why in jobs:
        ok, detail = set_canonical(path, want, dry)
        rel = path.relative_to(ROOT).as_posix()
        status = "CHANGED" if ok else ("skip   " if "already" in detail else "FAILED ")
        if ok:
            changed += 1
        elif "REFUSED" in detail:
            failed += 1
        print(f"  [{status}] {rel:<48} {why:<16} {detail}")

    print(f"\n{changed} changed, {failed} refused")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
