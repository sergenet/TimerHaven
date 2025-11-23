#!/usr/bin/env python3
"""
update_tools.py

Usage:
  python3 update_tools.py /path/to/tools_dir

What it does:
- Walks the specified directory (non-recursive by default; set RECURSIVE=True below to walk subdirs)
- For each .html file found, creates a backup file filename.html.bak (if not already)
- Inserts the line <script src="/lang-fix.js"></script> immediately before the closing </body> tag
  (case-insensitive). If the script tag is already present, it does nothing for that file.

This is safe and reversible (backups kept).
"""
import sys
import os
import re
from pathlib import Path

# CONFIG
RECURSIVE = False   # set to True to process subdirectories
INCLUDE_LINE = '<script src="/lang-fix.js"></script>'
BACKUP_EXT = '.bak'

def process_file(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # try reading with latin-1 as fallback
        text = path.read_text(encoding='latin-1')

    if INCLUDE_LINE in text:
        print(f"SKIP (already has include): {path.name}")
        return

    # find last </body> (case-insensitive)
    m = re.search(r'</body\s*>', text, flags=re.IGNORECASE)
    if not m:
        print(f"WARNING: no </body> tag found, skipping: {path.name}")
        return

    # backup
    backup_path = path.with_suffix(path.suffix + BACKUP_EXT)
    if not backup_path.exists():
        try:
            backup_path.write_text(text, encoding='utf-8')
            print(f"Backup created: {backup_path.name}")
        except Exception:
            # fallback encoding
            backup_path.write_text(text, encoding='latin-1')
            print(f"Backup created (latin-1): {backup_path.name}")

    # insert include before closing body
    insert_at = m.start()
    new_text = text[:insert_at] + INCLUDE_LINE + '\n' + text[insert_at:]
    try:
        path.write_text(new_text, encoding='utf-8')
    except Exception:
        # fallback
        path.write_text(new_text, encoding='latin-1')
    print(f"UPDATED: {path.name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_tools.py /path/to/tools_dir")
        sys.exit(1)

    base = Path(sys.argv[1])
    if not base.exists() or not base.is_dir():
        print("Directory not found:", base)
        sys.exit(1)

    if RECURSIVE:
        files = list(base.rglob('*.html'))
    else:
        files = list(base.glob('*.html'))

    if not files:
        print("No .html files found in", base)
        sys.exit(0)

    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"ERROR processing {f.name}: {e}")

if __name__ == '__main__':
    main()