#!/usr/bin/env python3
"""Compare each TimerHaven stub page against the real feature pages.

Answers one question per stub: is it a duplicate of an existing page (so its
canonical should point there) or distinct content (so its canonical should be
itself)? Uses visible-text similarity, not byte identity, because the stubs
carry different templates.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\TimerHavenWebsite")
LOCALES = ["en", "ar", "de", "el", "es", "fr", "ru"]
FEATURES = ["pomodoro-timer", "focus-music", "task-timer"]
STEM = {"pomodoro-timer": "pomodoro", "focus-music": "focus-music", "task-timer": "timer"}
SUFFIX = {"pomodoro-timer": "pomodoro", "focus-music": "focus-music", "task-timer": "timer"}


def words(path: Path):
    try:
        html = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&[a-z]+;|&#\d+;", " ", text)
    return re.findall(r"[a-z0-9\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff\u0590-\u05ff\u0600-\u06ff]{3,}", text.lower())


def shingles(ws, n=4):
    return {tuple(ws[i:i + n]) for i in range(max(0, len(ws) - n + 1))}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    # Stub filenames are not uniformly `<feature>-index.html`: the pomodoro one
    # is `<stem>-index.html` (pomodoro-index.html), not pomodoro-timer-index.html.
    stubs = []
    for loc in LOCALES:
        for feat in FEATURES:
            for name in (f"{feat}-index.html", f"{STEM[feat]}-index.html"):
                p = ROOT / loc / feat / name
                if p.exists():
                    stubs.append((loc, feat, p))
                    break

    # Candidate "real" pages for a locale: the -locale variants plus the
    # untagged English originals.
    cands = {}
    for stem in ("pomodoro", "focus-music", "timer"):
        for loc in LOCALES:
            for name in (
                f"{stem}-{loc}.html",
                f"{stem}.html",
                f"{stem}-how-to-{loc}.html",
                f"{stem}-how-to.html",
                f"{stem}-how.html",
                f"{stem}-tips-{loc}.html",
                f"{stem}-tips.html",
            ):
                p = ROOT / name
                if p.exists() and (name not in cands):
                    cands[name] = p

    cand_shi = {name: shingles(words(p)) for name, p in cands.items()}

    print(f"{len(stubs)} stubs, {len(cands)} candidate pages\n")
    for loc, feat, path in stubs:
        ws = words(path)
        s = shingles(ws)
        scored = sorted(((jaccard(s, c), n) for n, c in cand_shi.items()), reverse=True)[:3]
        best = scored[0] if scored else (0, "-")
        verdict = "DUPLICATE" if best[0] >= 0.55 else ("PARTIAL" if best[0] >= 0.30 else "DISTINCT")
        print(f"{loc}/{feat}: {len(ws)} words -> {verdict}")
        for score, name in scored:
            print(f"    {score:5.2f}  {name}")
        print()


if __name__ == "__main__":
    main()
