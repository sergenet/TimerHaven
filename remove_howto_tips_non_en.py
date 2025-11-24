#!/usr/bin/env python3
# remove_howto_tips_non_en.py
# Finds non-en tool pages, backs them up (.bak), removes "how-to" and "tips" card blocks,
# and inserts a single "Read full guide" CTA that targets /{lang}/{tool}/{tool}-index.html.
# Does NOT touch files under /en/.
# Run: python remove_howto_tips_non_en.py
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path.cwd()
NON_EN_LANGS = {'fr','es','de','ru','el','ar'}

def is_non_en_file(p: Path):
    # files in language folders: fr/... or filename like pomodoro-fr.html at repo root
    parts = p.parts
    if len(parts) >= 2 and parts[0] in NON_EN_LANGS:
        return True
    if re.search(r'-(?:' + '|'.join(NON_EN_LANGS) + r')\.html$', p.name):
        return True
    return False

def detect_lang_tool(p: Path):
    parts = p.parts
    if len(parts) >= 2 and parts[0] in NON_EN_LANGS:
        lang = parts[0]
        # if file is at lang root (fr/pomodoro.html) -> tool = stem without -fr suffix
        if len(parts) >= 3:
            tool = parts[1]
        else:
            tool = re.sub(r'-(?:' + '|'.join(NON_EN_LANGS) + r')$', '', p.stem)
        return lang, tool
    m = re.match(r'(?P<tool>.+?)-(?P<lang>' + '|'.join(NON_EN_LANGS) + r')$', p.stem)
    if m:
        return m.group('lang'), m.group('tool')
    return None, None

def backup_and_write(p: Path, content: str):
    bak = p.with_suffix(p.suffix + '.bak')
    if not bak.exists():
        bak.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
    p.write_text(content, encoding='utf-8')

def process_file(p: Path):
    if not is_non_en_file(p):
        return False
    lang, tool = detect_lang_tool(p)
    if not lang or not tool:
        return False

    raw = p.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    modified = False

    # Remove blocks that include links to -how-to or -tips
    anchors = soup.find_all('a', href=True)
    for a in anchors:
        href = a['href']
        if re.search(r'(-how-to|-tips)(?:\.html)?', href):
            # attempt to remove nearest reasonable ancestor block
            ancestor = a
            removed = False
            for _ in range(6):
                ancestor = ancestor.parent
                if ancestor is None:
                    break
                if ancestor.name in ('div','section','article'):
                    ancestor.decompose()
                    modified = True
                    removed = True
                    break
            if not removed:
                a.decompose()
                modified = True

    # ensure there's a centered-tool container and then add CTA
    container = soup.select_one('.centered-tool') or soup.select_one('.card') or soup.body
    if container:
        # remove any existing CTA duplicates
        for old in container.select('a.cta'):
            old.decompose()
        new_p = soup.new_tag('p')
        new_p['style'] = 'margin-top:1rem;'
        new_a = soup.new_tag('a', href=f'/{lang}/{tool}/{tool}-index.html')
        new_a['class'] = 'cta'
        new_a.string = 'Read full guide'
        new_p.append(new_a)
        container.append(new_p)
        modified = True

    if modified:
        backup_and_write(p, str(soup))
        print(f'Updated: {p} (backup: {p.name}.bak)')
        return True
    return False

def main():
    # candidate files: root *.html, lang/*.html, lang/*/*.html
    candidates = list(ROOT.glob('*.html'))
    for L in NON_EN_LANGS:
        candidates += list(ROOT.glob(f'{L}/*.html'))
        candidates += list(ROOT.glob(f'{L}/*/*.html'))
    candidates = sorted(set([p for p in candidates if p.is_file()]))

    touched = []
    for p in candidates:
        if process_file(p):
            touched.append(p)
    print(f'Done. Files modified: {len(touched)}')

if __name__ == '__main__':
    main()