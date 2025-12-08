#!/usr/bin/env python3
"""
Diagnostic: check FAQ presence/content, title/cta location, file length, and specific strings.

Usage:
  python check_faq_and_strings.py --folder "C:\TimerHavenWebsite\tools-other-langs" --files "countdown-ar.html,countdown-de.html"
  (files is optional; if omitted script checks all .html files in folder)
"""
import argparse, os, sys
from bs4 import BeautifulSoup

def analyze(path):
    name = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        return name, f"ERROR reading: {e}"

    soup = BeautifulSoup(src, 'lxml')
    length = len(src)
    # FAQ detection: common patterns
    faq_section = soup.select_one('.faq-section')
    details = soup.find_all('details')
    faq_content_len = 0
    if faq_section:
        faq_content_len = len(faq_section.get_text(strip=True))
    else:
        # fallback: check details and any element with "faq" in class or id
        for d in details:
            faq_content_len += len(d.get_text(strip=True))
        if faq_content_len == 0:
            # find elements matching faq token
            for el in soup.find_all(True):
                cls = " ".join(el.get('class') or [])
                if 'faq' in cls or 'question' in cls or 'foire' in cls.lower():
                    faq_content_len += len(el.get_text(strip=True))

    # Is CTA/title inside a tool-card?
    title = soup.find(['h1','h2','h3'])
    cta = soup.select_one('a.read-guide, a.cta, a[href*="index"]')
    def inside_tool(el):
        if not el: return False
        for p in el.parents:
            cls = " ".join(p.get('class') or [])
            if 'tool-card' in cls or 'article-card' in cls:
                return True
        return False

    title_in = inside_tool(title)
    cta_in = inside_tool(cta)

    # specific checks
    has_sekunden = 'sekunden' in src.lower()
    has_sekunde = 'sekunde' in src.lower()
    truncated = length < 2000  # heuristic small file may be truncated; adjust as needed

    return name, {
        'length': length,
        'faq_section_found': bool(faq_section),
        'faq_details_count': len(details),
        'faq_content_length': faq_content_len,
        'title_found': bool(title),
        'title_in_tool_card': title_in,
        'cta_found': bool(cta),
        'cta_in_tool_card': cta_in,
        'has_sekunden': has_sekunden,
        'has_sekunde': has_sekunde,
        'truncated_heuristic': truncated
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--folder','-f', required=True)
    p.add_argument('--files', help='Comma-separated filenames relative to folder (optional)')
    args = p.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print("ERROR: folder not found", folder); sys.exit(1)

    if args.files:
        files = [os.path.join(folder, fn.strip()) for fn in args.files.split(',')]
    else:
        files = sorted([os.path.join(folder, fn) for fn in os.listdir(folder) if fn.lower().endswith('.html')])

    for path in files:
        name, res = analyze(path)
        if isinstance(res, str):
            print(f"{name}: {res}")
        else:
            print(f"{name}: len={res['length']} faq_found={res['faq_section_found']} details={res['faq_details_count']} faq_text_len={res['faq_content_length']} title_in_card={res['title_in_tool_card']} cta_in_card={res['cta_in_tool_card']} sekunden={res['has_sekunden']} sekunde={res['has_sekunde']} trunc?={res['truncated_heuristic']}")

if __name__ == '__main__':
    main()