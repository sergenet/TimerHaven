"""Point TimerHaven's blog pages at their own social card.

Pairs with scripts/make_blog_share_cards.py, which writes
`images/blog/<slug>-featured.webp` for each post. This updates each page:

  * og:image and twitter:image -> that post's own card, when it has one
  * the JSON-LD ImageObject "url" -> whatever the page's og:image now is

The second fix matters on its own: 32 blog pages declared an ImageObject at
`https://timerhaven.com/social-share-image.webp`, a path that does not exist
(the real file lives under /assets/images/). Every one of them advertised a
broken structured-data image, including the ten posts that already had artwork.

Bytes in, bytes out: these pages carry UTF-8 BOMs and CRLF line endings, and
text-mode I/O would rewrite both and turn a two-line change into a whole-file
diff.

Usage:
    python scripts/apply_blog_share_cards.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SITE = "https://timerhaven.com"
BRAND_CARD = "/assets/images/social-share-image.webp"

OG = re.compile(r'(<meta\s+property=["\']og:image["\']\s+content=["\'])([^"\']*)(["\'])', re.I)
TW = re.compile(r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'])([^"\']*)(["\'])', re.I)
LD = re.compile(r'("url"\s*:\s*")([^"]*(?:social-share-image\.webp|/images/blog/[^"]*))(")')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    blog = root / "blog"

    repointed = 0
    ld_fixed = 0
    changed_files = 0
    no_card = []

    for page in sorted(blog.glob("*.html")):
        slug = page.stem
        raw = page.read_bytes()
        html = raw.decode("utf-8")
        orig = html

        # PNG, not WebP: generate.py writes both, and a flat-colour card is only
        # ~67 KB as PNG. Several link scrapers (LinkedIn in particular) silently
        # drop a .webp og:image and render no preview at all, while header images
        # in the page itself are unaffected.
        card = root / "images" / "blog" / f"{slug}-featured.png"
        card_url = f"{SITE}/images/blog/{slug}-featured.png"

        if slug != "index":
            if card.exists():
                before = OG.search(html)
                if before and not before.group(2).endswith(f"/images/blog/{slug}-featured.png"):
                    html = OG.sub(lambda m: f"{m.group(1)}{card_url}{m.group(3)}", html, count=1)
                    html = TW.sub(lambda m: f"{m.group(1)}{card_url}{m.group(3)}", html, count=1)
                    repointed += 1
            else:
                no_card.append(slug)

        # Structured data must not advertise an image the page does not have.
        og = OG.search(html)
        target = og.group(2) if og else f"{SITE}{BRAND_CARD}"
        if LD.search(html):
            new_html = LD.sub(lambda m: f"{m.group(1)}{target}{m.group(3)}", html)
            if new_html != html:
                ld_fixed += 1
                html = new_html

        if html != orig:
            changed_files += 1
            if not args.dry_run:
                page.write_bytes(html.encode("utf-8"))

    print(f"files changed: {changed_files}")
    print(f"  pages repointed to their own card: {repointed}")
    print(f"  JSON-LD image url corrected:       {ld_fixed}")
    if no_card:
        print(f"  posts with no card of their own ({len(no_card)}): {', '.join(no_card)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
