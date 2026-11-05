"""One-shot repair pass for timerhaven.com.

Applies the remaining audit findings in a single deterministic sweep. Every step
prints what it changed so a dry run can be reviewed before any file is touched.

Steps
  1. homepage canonical: index.html told Google its canonical was the 77-word
     index-en.html stub, so the real 119 KB homepage was never the indexed page
  2. index-en.html becomes an alias of / (same canonical), which also lets the
     sitemap generator drop it in favour of /
  3. the in-article AdSense unit is added to the 7 blog hubs, which only carried
     the footer unit
  4. Home / Back / floating Up controls at the bottom of every page
  5. titles over 60 characters lose the redundant brand suffix
  6. the one double-encoded Greek title is repaired

Usage: python scripts/fix_remaining.py [--dry]
"""
import os
import re
import sys

DRY = "--dry" in sys.argv

SKIP_DIRS = {
    "_attic", "_site", "Backup_20260222", "Backup_20260222_Refined",
    "node_modules", ".git", "pre-multilang-backup", "assets", "_includes",
    "youtube", "_SYNCAPP", "android", "chrome_extension",
    "timerhaven-extension", "timerhaven-extension-v2", "components", "scripts",
}

LABELS = {
    "en": ("Home", "Back", "Back to top"),
    "de": ("Startseite", "Zur\u00fcck", "Nach oben"),
    "es": ("Inicio", "Atr\u00e1s", "Volver arriba"),
    "fr": ("Accueil", "Retour", "Haut de page"),
    "ru": ("\u0413\u043b\u0430\u0432\u043d\u0430\u044f", "\u041d\u0430\u0437\u0430\u0434", "\u041d\u0430\u0432\u0435\u0440\u0445"),
    "el": ("\u0391\u03c1\u03c7\u03b9\u03ba\u03ae", "\u03a0\u03af\u03c3\u03c9", "\u0395\u03c0\u03ac\u03bd\u03c9"),
    "ar": ("\u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629", "\u0631\u062c\u0648\u0639", "\u0625\u0644\u0649 \u0627\u0644\u0623\u0639\u0644\u0649"),
}

IN_ARTICLE = (
    '<div class="th-ad-slot" data-ad-placement="in-article" '
    'style="margin:24px auto;max-width:728px;min-height:90px;text-align:center;overflow:hidden">\n'
    '<span class="th-ad-label" style="display:block;font-size:10px;letter-spacing:.1em;'
    'text-transform:uppercase;opacity:.55;margin-bottom:4px">Advertisement</span>\n'
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-0467059729557007" '
    'data-ad-slot="2835722251" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '</div>\n'
)

NAV_MARK = "th-page-nav"


def nav_block(lang):
    home, back, up = LABELS.get(lang, LABELS["en"])
    return f"""
<nav class="{NAV_MARK}" aria-label="{home} / {back}" style="max-width:1100px;margin:0 auto 8px;padding:8px 16px 0;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
  <a href="/" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:999px;border:1px solid currentColor;text-decoration:none;font-size:14px;opacity:.85">&#8962; {home}</a>
  <button type="button" data-th-back style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer;font:inherit;font-size:14px;opacity:.85">&#8592; {back}</button>
</nav>
<button type="button" data-th-top aria-label="{up}" title="{up}" style="position:fixed;right:18px;bottom:18px;z-index:2147483000;width:44px;height:44px;border-radius:50%;border:1px solid rgba(0,0,0,.15);background:rgba(255,255,255,.92);color:#222;font-size:20px;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.18);display:none">&#8593;</button>
<script>
(function () {{
  var back = document.querySelector('[data-th-back]');
  if (back) back.addEventListener('click', function () {{
    if (window.history.length > 1) {{ window.history.back(); }} else {{ window.location.href = '/'; }}
  }});
  var top = document.querySelector('[data-th-top]');
  if (top) {{
    var toggle = function () {{ top.style.display = window.scrollY > 300 ? 'block' : 'none'; }};
    window.addEventListener('scroll', toggle, {{ passive: true }});
    toggle();
    top.addEventListener('click', function () {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});
  }}
}})();
</script>
"""


def pages():
    out = []
    for root, dirs, fs in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fs:
            if f.endswith(".html"):
                out.append(os.path.join(root, f).replace(os.sep, "/"))
    return sorted(out)


def lang_of(rel, html):
    first = rel.lstrip("./").split("/")[0]
    if first in ("ar", "de", "el", "es", "fr", "ru"):
        return first
    m = re.search(r"<html[^>]*\blang=[\"']([A-Za-z-]+)", html)
    if m:
        code = m.group(1)[:2].lower()
        if code in LABELS:
            return code
    return "en"


def is_stub(html):
    return 'http-equiv="refresh"' in html and "Redirecting to" in html


def strip_brand(title):
    for suf, side in ((" | TimerHaven", "end"), (" - TimerHaven", "end"), (" — TimerHaven", "end"),
                      ("TimerHaven | ", "start"), ("TimerHaven - ", "start")):
        if side == "end" and title.endswith(suf):
            return title[: -len(suf)].rstrip()
        if side == "start" and title.startswith(suf):
            return title[len(suf):].lstrip()
    return title


def repair_mojibake(text):
    # Double-encoded UTF-8 shows as runs of these lead bytes. Counting them is
    # more reliable than matching a pair, because the byte that follows is not
    # always in the Latin-1 range.
    if sum(text.count(c) for c in "ÃÂÎÏ") < 3:
        return text, False
    for enc in ("cp1252", "latin-1"):
        try:
            fixed = text.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if fixed != text:
            return fixed, True
    return text, False


def main():
    changes = {"canonical": [], "ads": [], "nav": [], "titles": [], "mojibake": [], "desc": []}
    all_pages = pages()
    print(f"pages: {len(all_pages)}")

    for rel in all_pages:
        path = rel.lstrip("./")
        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            html = fh.read()
        original = html

        # 1/2 — canonical consolidation on the homepage pair
        if path in ("index.html", "index-en.html"):
            new = re.sub(
                r'(<link\s+rel=["\']canonical["\'][^>]*href=["\'])[^"\']*(["\'])',
                r"\1https://timerhaven.com/\2",
                html,
                count=1,
            )
            if new != html:
                html = new
                changes["canonical"].append(path)
            if path == "index.html" and html.startswith("\ufeff"):
                html = html.lstrip("\ufeff")
                changes["canonical"].append(path + " (BOM)")
            # The old snippet promised no ads and no trackers. GA4 and AdSense
            # both run here now, so that claim is no longer true.
            if path == "index.html":
                new = html.replace(
                    "Master your focus with no trackers or ads.",
                    "No sign-up and no account needed \u2014 open a tool and focus.",
                )
                if new != html:
                    html = new
                    changes["desc"].append(path)

        # 3 — in-article unit for the blog hubs, which only carry the footer
        # unit. Deliberately not applied to the other 170 footer-only pages: 166
        # of them are under 200 words, and a second unit on a thin page is the
        # wrong direction for a site rejected for low-value content.
        if (
            path.endswith("blog/index.html")
            and 'data-ad-placement="footer"' in html
            and 'data-ad-placement="in-article"' not in html
        ):
            idx = html.find('<div class="th-ad-slot" data-ad-placement="footer"')
            if idx != -1:
                html = html[:idx] + IN_ARTICLE + html[idx:]
                changes["ads"].append(path)

        # 4 — bottom-of-page navigation
        if NAV_MARK not in html and "</body>" in html and not is_stub(html):
            idx = html.rfind("</body>")
            html = html[:idx] + nav_block(lang_of(path, html)) + html[idx:]
            changes["nav"].append(path)

        # 5/6 — titles
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S)
        if m:
            raw = m.group(1).strip()
            repaired, was_bad = repair_mojibake(raw)
            if was_bad:
                changes["mojibake"].append(path)
            final = repaired
            if len(final) > 60:
                trimmed = strip_brand(final)
                if trimmed and trimmed != final:
                    final = trimmed
            if final != raw:
                html = html[: m.start(1)] + final + html[m.end(1):]
                changes["titles"].append((path, len(raw), len(final)))

        if html != original:
            if not DRY:
                with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as fh:
                    fh.write(html)

    for key in ("canonical", "desc", "mojibake"):
        print(f"{key}: {len(changes[key])} {changes[key][:6]}")
    print(f"in-article ad added: {len(changes['ads'])}")
    for p in changes["ads"][:10]:
        print("   ", p)
    print(f"nav added: {len(changes['nav'])}")
    print(f"titles rewritten: {len(changes['titles'])}")
    for p, a, b in changes["titles"][:6]:
        print(f"    {a:3d}->{b:3d} {p}")
    if DRY:
        print("\nDRY RUN — nothing written")


if __name__ == "__main__":
    main()
