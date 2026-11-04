"""Generate the featured image for the breaks article.

640x640, dark navy with a cyan glow, matching the abstract style used by the
other blog featured images (deep-work, flow-state). Outputs both PNG and WebP
into images/blog/.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

W = H = 640
NAVY = (7, 16, 33)
CYAN = (34, 211, 238)
SOFT = (56, 189, 248)

random.seed(7)


def radial_background():
    """Vertical/radial gradient from near-black corners to a lit centre."""
    img = Image.new("RGB", (W, H), NAVY)
    px = img.load()
    cx, cy = W * 0.5, H * 0.52
    maxd = math.hypot(cx, cy)
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy) / maxd
            glow = max(0.0, 1.0 - d) ** 2.1
            # a second, tighter core so the middle reads as a light source
            core = max(0.0, 1.0 - d * 2.4) ** 2.4
            r = NAVY[0] + 26 * glow + 40 * core
            g = NAVY[1] + 74 * glow + 120 * core
            b = NAVY[2] + 96 * glow + 140 * core
            px[x, y] = (min(255, int(r)), min(255, int(g)), min(255, int(b)))
    return img


def add_rings(img):
    """Concentric thin rings, the motif shared with the deep-work artwork."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = W // 2, int(H * 0.52)
    for i, radius in enumerate(range(58, 300, 34)):
        alpha = 150 - i * 12
        d.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=(*SOFT, max(28, alpha)),
            width=1,
        )
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return img


def add_pause_glow(img):
    """A soft pair of rounded bars, the universal 'take a break' mark."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.52)
    bar_w, bar_h, gap = 26, 104, 32
    for offset in (-1, 1):
        x0 = cx + offset * (gap // 2 + bar_w // 2) - bar_w // 2
        d.rounded_rectangle(
            [x0, cy - bar_h // 2, x0 + bar_w, cy + bar_h // 2],
            radius=13,
            fill=(*CYAN, 235),
        )
    blurred = glow.filter(ImageFilter.GaussianBlur(18))
    out = Image.alpha_composite(img, blurred)
    out = Image.alpha_composite(out, glow.filter(ImageFilter.GaussianBlur(1)))
    return out


def add_particles(img):
    """Small bokeh dots scattered through the frame."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(30):
        angle = random.uniform(0, math.tau)
        dist = random.uniform(90, 280)
        x = W / 2 + math.cos(angle) * dist * random.uniform(0.6, 1.0)
        y = H * 0.52 + math.sin(angle) * dist * random.uniform(0.6, 1.0)
        r = random.uniform(1.2, 4.0)
        a = random.randint(40, 150)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*CYAN, a))
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    return Image.alpha_composite(img, layer)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outdir = os.path.join(root, "images", "blog")
    os.makedirs(outdir, exist_ok=True)

    img = radial_background()
    img = add_rings(img)
    img = add_pause_glow(img)
    img = add_particles(img)
    img = img.convert("RGB")

    png = os.path.join(outdir, "break-length-featured.png")
    webp = os.path.join(outdir, "break-length-featured.webp")
    img.save(png, "PNG", optimize=True)
    img.save(webp, "WEBP", quality=90, method=6)
    print("wrote", png, os.path.getsize(png), "bytes")
    print("wrote", webp, os.path.getsize(webp), "bytes")


if __name__ == "__main__":
    main()
