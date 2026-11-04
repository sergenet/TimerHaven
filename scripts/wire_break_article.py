"""Wire the new breaks article into the site.

Does four things, idempotently, by byte-level editing so nothing else in the
existing files is disturbed (their line endings differ between files):

  1. inserts the article card at the top of blog/index.html
  2. appends the URL to sitemap.xml
  3. adds an inbound "Further Reading" link from three related posts
  4. leaves every other file untouched

Run: python scripts/wire_break_article.py
"""
import os
import sys

SLUG = "how-long-should-a-break-be"
URL = f"https://timerhaven.com/blog/{SLUG}.html"
TITLE = "How Long Should a Break Be? The Science of Resting Well"
EXCERPT = (
    "Ten minutes after fifty is the pattern most people should start with. The research on "
    "break length, why phone breaks do not restore you, and how to time breaks you will "
    "actually take."
)

CARD = f"""            <article class="article-card">
                <img src="../images/blog/break-length-featured.webp" class="article-image"
                    alt="A glowing pause symbol surrounded by concentric rings" loading="lazy" width="640" height="640">
                <div class="article-content">
                    <div class="article-meta">
                        <span class="category-badge">Rest &amp; Recovery</span>
                        October 28, 2026 &middot; 8 min read
                    </div>
                    <a href="../blog/{SLUG}.html" class="article-title">{TITLE}</a>
                    <p class="article-excerpt">
                        {EXCERPT}
                    </p>
                    <a href="../blog/{SLUG}.html" class="read-more">
                        Read More <i class="fa fa-arrow-right"></i>
                    </a>
                </div>
            </article>

"""

SITEMAP_ENTRY = f"""  <url>
    <loc>{URL}</loc>
    <html:link rel="alternate" hreflang="en" href="{URL}"/>
    <html:link rel="alternate" hreflang="x-default" href="{URL}"/>
    <priority>0.8</priority>
    <changefreq>weekly</changefreq>
  </url>
"""

LINK_POSTS = [
    "afternoon-slump.html",
    "time-blocking-vs-pomodoro.html",
    "burnout-prevention-guide.html",
]


def read(path):
    with open(path, "rb") as f:
        return f.read()


def write(path, data):
    with open(path, "wb") as f:
        f.write(data)


def insert_card(blog):
    path = os.path.join(blog, "index.html")
    data = read(path)
    if SLUG.encode() in data:
        print("index.html: card already present")
        return
    marker = b'<div class="article-grid">'
    idx = data.find(marker)
    if idx < 0:
        sys.exit("index.html: article-grid marker not found")
    at = idx + len(marker)
    nl = b"\r\n" if data[:400].find(b"\r\n") >= 0 else b"\n"
    # keep the newline that followed the marker, then add the card after it
    payload = nl + CARD.replace("\n", nl.decode()).encode()
    write(path, data[:at] + payload + data[at:])
    print("index.html: card inserted at top of grid")


def insert_sitemap(root):
    path = os.path.join(root, "sitemap.xml")
    data = read(path)
    if SLUG.encode() in data:
        print("sitemap.xml: entry already present")
        return
    close = data.rfind(b"</urlset>")
    if close < 0:
        sys.exit("sitemap.xml: </urlset> not found")
    nl = b"\r\n" if b"\r\n" in data else b"\n"
    payload = SITEMAP_ENTRY.replace("\n", nl.decode()).encode()
    write(path, data[:close] + payload + data[close:])
    print("sitemap.xml: entry appended")


def add_related(blog):
    anchor = (
        f'<li><a href="../blog/{SLUG}.html">{TITLE}</a></li>'
    )
    for name in LINK_POSTS:
        path = os.path.join(blog, name)
        if not os.path.exists(path):
            print(f"{name}: missing, skipped")
            continue
        data = read(path)
        if SLUG.encode() in data:
            print(f"{name}: link already present")
            continue
        start = data.find(b"Further Reading")
        if start < 0:
            print(f"{name}: no Further Reading block, skipped")
            continue
        end = data.find(b"</ul>", start)
        if end < 0:
            print(f"{name}: no closing list, skipped")
            continue
        nl = b"\r\n" if b"\r\n" in data[start:end] else b"\n"
        # reuse the indentation of the last sibling list item
        last_li = data.rfind(b"<li>", start, end)
        if last_li < 0:
            print(f"{name}: empty list, skipped")
            continue
        line_start = data.rfind(b"\n", start, last_li) + 1
        line = data[line_start:data.find(b"\n", last_li)]
        indent = line[:len(line) - len(line.lstrip())]
        # step back over the whitespace in front of </ul> so the new item lands
        # on its own line at the same depth as its siblings
        cut = end
        while cut > 0 and data[cut - 1:cut] in (b" ", b"\t"):
            cut -= 1
        payload = indent + anchor.encode() + nl
        write(path, data[:cut] + payload + data[cut:])
        print(f"{name}: inbound link added")


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    blog = os.path.join(root, "blog")
    article = os.path.join(blog, SLUG + ".html")
    if not os.path.exists(article):
        sys.exit(f"missing article: {article} (run build_break_article.py first)")

    insert_card(blog)
    insert_sitemap(root)
    add_related(blog)


if __name__ == "__main__":
    main()
