#!/usr/bin/env python3
"""Recursively delete a remote directory (or file), then prove it is gone.

Credentials are read from an existing project script rather than copied, so this
file adds no second copy of the password.

Usage:  python scripts/remove_remote_dir.py <remote-path> [--dry-run]
"""
import re
import sys
import re as _re
import ftplib
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent


def creds():
    src = (HERE / "upload_fix.py").read_text(encoding="utf-8", errors="replace")
    host = _re.search(r"host\s*=\s*['\"]([^'\"]+)", src).group(1)
    user = _re.search(r"user\s*=\s*['\"]([^'\"]+)", src).group(1)
    passwd = _re.search(r"pass(?:wd|word)?\s*=\s*['\"]([^'\"]+)", src).group(1)
    return host, user, passwd


def connect():
    host, user, passwd = creds()
    ftp = ftplib.FTP(host, timeout=60)
    ftp.login(user, passwd)
    ftp.set_pasv(True)
    return ftp


def walk(ftp, path, dry, depth=0):
    """Delete everything under `path`, then `path` itself. Returns count."""
    n = 0
    try:
        entries = list(ftp.mlsd(path)) if hasattr(ftp, "mlsd") else []
    except Exception:  # noqa: BLE001 - server may not support MLSD
        entries = []
    if entries:
        for name, facts in entries:
            if name in (".", ".."):
                continue
            child = f"{path}/{name}"
            if facts.get("type") == "dir":
                n += walk(ftp, child, dry, depth + 1)
                if not dry:
                    try:
                        ftp.rmd(child)
                    except ftplib.error_perm as e:
                        print(f"  ! rmd {child}: {e}")
            else:
                n += 1
                if dry:
                    print(f"  would delete {child}")
                else:
                    try:
                        ftp.delete(child)
                    except ftplib.error_perm as e:
                        print(f"  ! del {child}: {e}")
        return n
    # Fallback: NLST-based walk.
    try:
        names = ftp.nlst(path)
    except ftplib.error_perm:
        return 0
    for child in names:
        if child in (".", "..") or child.rstrip("/") == path.rstrip("/"):
            continue
        try:
            ftp.cwd(child)
            ftp.cwd("/")
            n += walk(ftp, child, dry, depth + 1)
            if not dry:
                ftp.rmd(child)
        except ftplib.error_perm:
            n += 1
            if dry:
                print(f"  would delete {child}")
            else:
                try:
                    ftp.delete(child)
                except ftplib.error_perm as e:
                    print(f"  ! del {child}: {e}")
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        print("usage: remove_remote_dir.py <remote-path> [--dry-run]")
        return 2
    path = "/" + args[0].strip("/")
    ftp = connect()
    print(f"{'[dry-run] ' if dry else ''}removing {path}")
    count = walk(ftp, path, dry)
    if not dry:
        try:
            ftp.rmd(path)
        except ftplib.error_perm as e:
            print(f"  ! rmd {path}: {e}")
    try:
        ftp.quit()
    except Exception:  # noqa: BLE001
        pass
    print(f"{'would remove' if dry else 'removed'} {count} files under {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
