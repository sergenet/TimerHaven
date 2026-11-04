"""
Bring TimerHaven's social-preview tags up to a consistent, correct standard.

Findings this repairs (from a 436-URL audit of the live sitemap):

  * 22 blog posts pointed og:image/twitter:image at `*-featured.webp` files that
    were never produced - every share of those posts showed a broken image.
  * 650 pages used a 640x640 `social-banner.webp` on a `summary_large_image`
    card, which crops badly; the site already ships a 1200x630
    `assets/images/social-share-image.webp`.
  * 149 pages lacked og:site_name, twitter:title and twitter:description.
  * 15 pages had no social tags whatsoever.
  * 23 pages advertised an og:url that disagreed with their own canonical.

Only files that appear in the live sitemap are touched, so stale local copies
that are not deployed cannot be pushed by accident.

Usage:
    python scripts/fix-social-tags.py --root . [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://timerhaven.com"
SITE_NAME = "TimerHaven"
SHARE_IMAGE = "/assets/images/social-share-image.webp"
SQUARE_BANNER = "/images/social-banner.webp"

OG_IMAGE = re.compile(r'(<meta\s+property=["\']og:image["\']\s+content=["\'])([^"\']*)(["\'])', re.I)
TW_IMAGE = re.compile(r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'])([^"\']*)(["\'])', re.I)


def sitemap_urls() -> list[str]:
    req = urllib.request.Request(
        f"{SITE}/sitemap.xml", headers={"User-Agent": "Mozilla/5.0 (compatible; social-tags)"}
    )
    xml = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    return [m.strip() for m in re.findall(r"<loc>([^<]+)</loc>", xml)]


def url_to_path(url: str) -> str:
    p = re.sub(r"^https?://[^/]+", "", url)
    if p in ("", "/"):
        return "index.html"
    return p.lstrip("/")


def has_og(html: str) -> bool:
    return bool(re.search(r'property=["\']og:title["\']', html, re.I))


def attr(html: str, name: str, prop: bool = True) -> str | None:
    key = "property" if prop else "name"
    m = re.search(
        rf'<meta\s+{key}=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']', html, re.I
    )
    return m.group(1) if m else None


def insert_before_head_close(html: str, block: str, nl: str = "\n") -> str:
    """Insert markup at the end of <head>, closing it first if it never closes.

    134 of TimerHaven's blog pages open <head> and go straight to <body> with
    no </head> at all. Browsers auto-correct that, but the markup is invalid and
    any tag added without closing it would land in the wrong place, so the
    missing close tag is written as part of the insertion.
    """
    low = html.lower()
    i = low.rfind("</head>")
    if i != -1:
        return html[:i] + block + html[i:]
    b = low.find("<body")
    if b != -1:
        return html[:b] + block + f"{nl}  </head>{nl}  " + html[b:]
    return html


def ensure_meta(
    html: str, prop: str, name: str, value: str, is_property: bool, nl: str = "\n"
) -> tuple[str, bool]:
    """Add a meta tag if absent. Returns (html, changed)."""
    key = "property" if is_property else "name"
    if re.search(rf'<meta\s+{key}=["\']{re.escape(name)}["\']', html, re.I):
        return html, False
    tag = f'{nl}    <meta {key}="{name}" content="{value}">'
    return insert_before_head_close(html, tag, nl), True


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    )


def fix_file(path: Path, root: Path, page_url: str, dry: bool) -> dict:
    # Bytes in, bytes out. 316 of these pages carry a UTF-8 BOM and 428 use CRLF
    # line endings; text-mode I/O would silently strip the BOM and rewrite every
    # line ending, turning a tag fix into a whole-file diff.
    raw = path.read_bytes()
    html = raw.decode("utf-8")
    orig = html
    nl = "\r\n" if b"\r\n" in raw else "\n"
    actions: list[str] = []

    # Which referenced blog images actually exist on disk?
    def resolve(u: str) -> str | None:
        rel = re.sub(r"^https?://[^/]+", "", u).lstrip("/")
        return rel or None

    def repoint(match: re.Match, label: str) -> str:
        rel = resolve(match.group(2))
        if not rel:
            return match.group(0)
        new = None
        if rel.startswith("images/blog/") and not (root / rel).exists():
            new = SHARE_IMAGE
            actions.append(f"{label}: missing file -> share image")
        elif rel == SQUARE_BANNER.lstrip("/") and (root / "assets/images/social-share-image.webp").exists():
            new = SHARE_IMAGE
            actions.append(f"{label}: 640x640 -> 1200x630")
        if not new:
            return match.group(0)
        return f"{match.group(1)}{SITE}{new}{match.group(3)}"

    html = OG_IMAGE.sub(lambda m: repoint(m, "og:image"), html)
    html = TW_IMAGE.sub(lambda m: repoint(m, "twitter:image"), html)

    title = None
    mt = re.search(r"<title[^>]*>([\s\S]*?)</title>", html, re.I)
    if mt:
        title = re.sub(r"\s+", " ", mt.group(1)).strip()
    desc = attr(html, "description", prop=False)
    canonical = None
    mc = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html, re.I)
    if mc:
        canonical = mc.group(1)
    page_abs = canonical or page_url

    og_title = attr(html, "og:title")
    og_desc = attr(html, "og:description")
    og_image = attr(html, "og:image")

    if not has_og(html):
        # Build the whole block from the page's own title/description/canonical.
        if title:
            block = [f"{nl}    <!-- Social preview (added: page previously had none) -->"]
            block.append(f'<meta property="og:title" content="{esc(title)}">')
            if desc:
                block.append(f'<meta property="og:description" content="{esc(desc)}">')
            block.append(f'<meta property="og:url" content="{esc(page_abs)}">')
            block.append('<meta property="og:type" content="website">')
            block.append(f'<meta property="og:site_name" content="{SITE_NAME}">')
            block.append(f'<meta property="og:image" content="{SITE}{SHARE_IMAGE}">')
            block.append('<meta name="twitter:card" content="summary_large_image">')
            block.append(f'<meta name="twitter:title" content="{esc(title)}">')
            if desc:
                block.append(f'<meta name="twitter:description" content="{esc(desc)}">')
            block.append(f'<meta name="twitter:image" content="{SITE}{SHARE_IMAGE}">')
            html = insert_before_head_close(html, f"{nl}    " + f"{nl}    ".join(block), nl)
            actions.append("added full social block")
    else:
        # og:url must agree with the page's own canonical.
        m = re.search(
            r'(<meta\s+property=["\']og:url["\']\s+content=["\'])([^"\']*)(["\'])', html, re.I
        )
        if m and canonical and m.group(2).rstrip("/") != canonical.rstrip("/"):
            html = html[: m.start()] + f"{m.group(1)}{esc(canonical)}{m.group(3)}" + html[m.end():]
            actions.append("og:url -> canonical")

        html, c1 = ensure_meta(html, "og:site_name", "og:site_name", SITE_NAME, True, nl)
        if c1:
            actions.append("+og:site_name")
        html, c2 = ensure_meta(
            html, "twitter:card", "twitter:card", "summary_large_image", False, nl
        )
        if c2:
            actions.append("+twitter:card")
        if og_title:
            html, c3 = ensure_meta(html, "twitter:title", "twitter:title", esc(og_title), False, nl)
            if c3:
                actions.append("+twitter:title")
        if og_desc:
            html, c4 = ensure_meta(
                html, "twitter:description", "twitter:description", esc(og_desc), False, nl
            )
            if c4:
                actions.append("+twitter:description")
        if og_image:
            html, c5 = ensure_meta(
                html, "twitter:image", "twitter:image", esc(og_image), False, nl
            )
            if c5:
                actions.append("+twitter:image")

    changed = html != orig
    if changed and not dry:
        path.write_bytes(html.encode("utf-8"))
    return {"changed": changed, "actions": actions}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    urls = sitemap_urls()
    print(f"sitemap: {len(urls)} URLs")

    stats: dict[str, int] = {}
    closed_head = 0
    changed_files = 0
    missing: list[str] = []

    for u in urls:
        rel = url_to_path(u)
        p = root / rel
        if not p.exists():
            missing.append(rel)
            continue
        had_head_close = "</head>" in p.read_bytes().decode("utf-8", "replace").lower()
        res = fix_file(p, root, u, args.dry_run)
        if res["changed"]:
            changed_files += 1
            if not had_head_close:
                closed_head += 1
            for a in res["actions"]:
                stats[a] = stats.get(a, 0) + 1

    print(f"files changed: {changed_files}")
    print(f"  of which had a missing </head> that is now closed: {closed_head}")
    for a, n in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {n:5d}  {a}")
    if missing:
        print(f"\nnot found locally ({len(missing)}):")
        for m in missing[:15]:
            print("   ", m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
