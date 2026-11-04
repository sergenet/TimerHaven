"""Generate real per-post social preview cards for TimerHaven's blog.

Twenty-four blog posts used to point og:image/twitter:image at
`*-featured.webp` files that were never produced, so every share of those posts
rendered a broken image. They were temporarily repointed at the site-wide brand
card, which fixed the breakage but gave sixteen different posts the same
picture.

This builds one card per post, in the same visual language as the brand card
(assets/images/social-share-image.webp): the lavender field, the coral stopwatch
with its cream face, dark ink type. The post's own headline is the artwork, so
each card is specific to its page, and the clock hand is set from the slug so no
two cards are identical.

Usage:
    python scripts/make_blog_share_cards.py [--dry-run] [--preview NAME ...]
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Brand palette, sampled from assets/images/social-share-image.webp
BG = (194, 204, 255)
INK = (16, 42, 67)
CORAL = (255, 80, 100)
CREAM = (238, 234, 205)
WHITE = (255, 255, 255)
SHADOW = (150, 162, 225)

CARD_W, CARD_H = 1200, 630
BRAND_CARD = "/assets/images/social-share-image.webp"

FONT_DIR = Path("C:/Windows/Fonts")
FONT_BOLD = FONT_DIR / "segoeuib.ttf"
FONT_REGULAR = FONT_DIR / "segoeui.ttf"

TEXT_X = 84
TEXT_MAX_W = 596


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"missing font: {path}")
    return ImageFont.truetype(str(path), size)


def measure(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    return int(draw.textlength(text, font=font))


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if measure(draw, candidate, font) <= max_w or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_title(draw, text: str, max_w: int, max_lines: int, hi: int, lo: int):
    """Largest size at which the headline fits in max_lines."""
    for size in range(hi, lo - 1, -2):
        font = load_font(FONT_BOLD, size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
    font = load_font(FONT_BOLD, lo)
    lines = wrap(draw, text, font, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "\u2026"
    return font, lines


def draw_spaced(draw, xy, text: str, font, fill, spacing: int):
    """Draw text with tracking, the way the small caps label is set."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += measure(draw, ch, font) + spacing
    return x


def needle_angle(slug: str) -> float:
    """A real clock position derived from the slug: stable, and unique per post."""
    digest = hashlib.sha256(slug.encode("utf-8")).digest()
    hour = digest[0] % 12
    return (hour / 12.0) * math.tau - math.pi / 2


def add_glow(img: Image.Image, cx: int, cy: int, radius: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(radius, 0, -6):
        alpha = int(46 * (1 - i / radius) ** 1.6)
        d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(255, 255, 255, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def nub(size: int, angle: float, width: int, height: int) -> Image.Image:
    """One of the two little lugs on the side of the stopwatch, drawn then rotated."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0 = (size - width) // 2
    y0 = (size - height) // 2
    d.rounded_rectangle(
        [x0, y0, x0 + width, y0 + height],
        radius=height // 2,
        fill=WHITE + (255,),
        outline=CORAL + (255,),
        width=5,
    )
    return layer.rotate(angle, resample=Image.BICUBIC, expand=False)


def draw_stopwatch(img: Image.Image, cx: int, cy: int, r: int, angle: float) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # soft drop shadow so the mark lifts off the lavender
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse(
        [cx - r - 34, cy - r - 16, cx + r + 34, cy + r + 58], fill=SHADOW + (70,)
    )
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    layer = Image.alpha_composite(layer, sh)
    d = ImageDraw.Draw(layer)

    # crown and side lugs sit behind the dial
    d.rounded_rectangle(
        [cx - 26, cy - r - 46, cx + 26, cy - r - 4],
        radius=12,
        fill=WHITE + (255,),
        outline=CORAL + (255,),
        width=5,
    )
    for side, rot in ((-1, 28), (1, -28)):
        glyph = nub(120, rot, 78, 34)
        layer.paste(glyph, (cx + side * (r + 4) - 60, cy - r + 34), glyph)
    d = ImageDraw.Draw(layer)

    # white sticker edge -> coral ring -> cream dial
    d.ellipse([cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26], fill=WHITE + (255,))
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], fill=CORAL + (255,))
    d.ellipse([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], fill=CREAM + (255,))

    # hour ticks
    for i in range(12):
        a = (i / 12.0) * math.tau - math.pi / 2
        r0, r1 = r - 44, r - 30
        d.line(
            [
                (cx + math.cos(a) * r0, cy + math.sin(a) * r0),
                (cx + math.cos(a) * r1, cy + math.sin(a) * r1),
            ],
            fill=INK + (255,),
            width=5 if i % 3 == 0 else 3,
        )

    # hand
    tip = r - 34
    d.line(
        [
            (cx - math.cos(angle) * 18, cy - math.sin(angle) * 18),
            (cx + math.cos(angle) * tip, cy + math.sin(angle) * tip),
        ],
        fill=INK + (255,),
        width=8,
    )
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=WHITE + (255,), outline=INK + (255,), width=5)

    return Image.alpha_composite(img.convert("RGBA"), layer)


def build_card(slug: str, title: str) -> Image.Image:
    img = Image.new("RGB", (CARD_W, CARD_H), BG)
    cx, cy, r = 926, 318, 168
    img = add_glow(img, cx, cy, 250).convert("RGB")
    img = draw_stopwatch(img, cx, cy, r, needle_angle(slug)).convert("RGB")

    d = ImageDraw.Draw(img)

    eyebrow_font = load_font(FONT_BOLD, 22)
    font, lines = fit_title(d, title, TEXT_MAX_W, 3, 60, 34)
    ascent, descent = font.getmetrics()
    line_h = ascent + descent + 8

    # Centre the eyebrow + headline + rule as one block, so a two-line headline
    # does not leave the card looking bottom-heavy.
    block_h = 26 + 28 + line_h * len(lines) + 30
    y = int(320 - block_h / 2)

    draw_spaced(d, (TEXT_X, y), "TIMERHAVEN BLOG", eyebrow_font, INK, 5)
    y += 26 + 28

    for line in lines:
        d.text((TEXT_X, y), line, font=font, fill=INK)
        y += line_h

    # coral rule under the headline
    rule_y = y + 14
    d.rounded_rectangle([TEXT_X, rule_y, TEXT_X + 92, rule_y + 7], radius=3, fill=CORAL)

    foot_font = load_font(FONT_REGULAR, 25)
    foot_bold = load_font(FONT_BOLD, 25)
    d.text((TEXT_X, 512), "timerhaven.com", font=foot_bold, fill=INK)
    d.text((TEXT_X, 550), "Free productivity tools", font=foot_font, fill=(58, 82, 110))

    return img


def post_title(html: str, fallback: str) -> str:
    m = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html, re.I)
    raw = m.group(1) if m else fallback
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html_mod.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def og_image(html: str) -> str:
    m = re.search(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']*)["\']', html, re.I
    )
    return m.group(1) if m else ""


def targets(root: Path, force: bool) -> list[tuple[str, str]]:
    """
    Posts whose share image is still the site-wide brand card.

    Posts that already own a -featured image are left alone: those are real
    artwork that shipped before this script existed, and regenerating over them
    would replace it with a generated card. --force opts in to replacing them.
    """
    blog = root / "blog"
    out = []
    for page in sorted(blog.glob("*.html")):
        if page.name == "index.html":
            continue
        slug = page.stem
        html = page.read_text(encoding="utf-8", errors="replace")
        if og_image(html).endswith(BRAND_CARD) or force:
            title = post_title(html, slug.replace("-", " ").title())
            out.append((slug, title))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="also regenerate posts that already have a card")
    ap.add_argument("--preview", nargs="*", default=None, help="only these slugs")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    outdir = root / "images" / "blog"
    outdir.mkdir(parents=True, exist_ok=True)

    jobs = targets(root, args.force)
    if args.preview:
        want = set(args.preview)
        jobs = [j for j in jobs if j[0] in want]
    print(f"posts needing artwork: {len(jobs)}")

    for slug, title in jobs:
        if not title:
            print(f"  SKIP {slug}: no title found")
            continue
        png = outdir / f"{slug}-featured.png"
        webp = outdir / f"{slug}-featured.webp"
        # Last guard: never overwrite a file that is not one of our own cards.
        blocked = next(
            (
                f
                for f in (png, webp)
                if f.exists() and Image.open(f).size != (CARD_W, CARD_H)
            ),
            None,
        )
        if blocked and not args.force:
            print(f"  SKIP {slug}: {blocked.name} holds existing artwork ({Image.open(blocked).size})")
            continue
        img = build_card(slug, title)
        if not args.dry_run:
            img.save(png, "PNG", optimize=True)
            img.save(webp, "WEBP", quality=90, method=6)
        print(f"  {slug:<38} {len(title):>3} chars -> {png.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
