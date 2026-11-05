#!/usr/bin/env python3
"""
zip-deploy.py - TimerHaven deploy: diff over FTP, ship one zip, extract remotely.

Per-file STOR on this host is slow, so pushing a few hundred changed pages one
at a time takes far longer than a single package upload plus a server-side
extract. Mirrors the approach used for the other sites: zip locally, unzip
remotely.

Steps:
  1. Read the live sitemap and keep only pages that exist locally.
  2. Concurrent SIZE scan -> changed/new files only.
  3. Zip exactly those (paths relative to the web root).
  4. Upload the zip + a one-shot token-guarded PHP extractor.
  5. Trigger it over HTTPS; it extracts and deletes the zip and itself.
  6. Verify both are gone.

The FTP login root is the web root, so paths map 1:1.

Usage:
  python zip-deploy.py [--dry-run]
"""

import io
import os
import re
import secrets
import sys
import time
import ftplib
import urllib.request
import urllib.error
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def _secret(name):
    """Environment variable first, else scripts/_secrets.py (gitignored)."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
        import _secrets  # local, never committed
    except ImportError:
        return ""
    return getattr(_secrets, name.replace("TH_", ""), "")


FTP_HOST = os.environ.get("TH_FTP_HOST", "ftp.timerhaven.com")
FTP_USER = os.environ.get("TH_FTP_USER", "contact@timerhaven.com")
FTP_PASS = _secret("TH_FTP_PASS")
if not FTP_PASS:
    raise SystemExit("set FTP_PASS in scripts/_secrets.py - the password is never stored in this file")
PUBLIC = "https://timerhaven.com"

BASE = Path(__file__).resolve().parent
# Trees that exist in the checkout but are not served from the web root: app
# sources, build copies, store assets and throwaway scratch. Anything here must
# never be uploaded, so it is also never part of the changed-file scan.
NOT_LIVE = {
    ".git", ".expo", ".idea", ".vscode", "_attic", "_includes", "_site",
    "android", "api", "chrome_extension", "chrome_store_screenshots",
    "components", "data", "docs", "images", "ios", "node_modules",
    "scripts", "timerhaven-extension", "timerhaven-extension-v2", "tmp",
    "tools", "__pycache__", "YouTube experiments", "_SYNCAPP",
}
WORKERS = 6           # host rejects with 421 beyond ~8 connections from one IP
MAX_ATTEMPTS = 5
ZIP_NAME = "th-pkg.zip"
UA = {"User-Agent": "Mozilla/5.0 (compatible; th-deploy)"}


def connect():
    for opener in ("tls", "plain"):
        try:
            if opener == "tls":
                ftp = ftplib.FTP_TLS(FTP_HOST, FTP_USER, FTP_PASS, timeout=60)
                try:
                    ftp.prot_p()
                except ftplib.error_perm:
                    pass
            else:
                ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS, timeout=60)
            try:
                ftp.voidcmd("TYPE I")
            except ftplib.error_perm:
                pass
            return ftp
        except Exception:
            if opener == "plain":
                raise
            time.sleep(1)
    raise RuntimeError("connect failed")


def target_files():
    """Local sitemap pages, plus the files the sitemap itself names.

    This used to read the LIVE sitemap, which made the deploy circular: a newly
    generated sitemap could never ship the pages it had just added, because they
    were not in the copy being read. The local sitemap is now generated from the
    tree (scripts/generate_sitemap.py), so it is the authoritative list.

    Images are not in the sitemap, so anything referenced by an og:image on one
    of those pages is added explicitly - otherwise a freshly generated social
    card would be uploaded as a page that points at a file that never shipped.

    sitemap.xml, .htaccess and robots.txt are appended explicitly: no sitemap
    lists them, and a deploy that changed crawl rules while shipping the old
    sitemap would leave the two out of step.

    Directory canonicals are resolved to their index.html; see the note below.
    """
    xml = (BASE / "sitemap.xml").read_text(encoding="utf-8", errors="replace")
    urls = [m.strip() for m in re.findall(r"<loc>([^<]+)</loc>", xml)]
    out = []
    seen = set()
    for u in urls:
        rel = re.sub(r"^https?://[^/]+", "", u).lstrip("/")
        # A canonical that names a directory (/, /blog/, /el/task-timer/) refers to
        # that directory's index.html. Without this the path resolved to a
        # directory, failed is_file(), and the page was dropped from the package:
        # the homepage and every blog hub therefore never shipped, no matter what
        # changed locally.
        if not rel or rel.endswith("/"):
            rel += "index.html"
        p = BASE / rel
        if p.is_file():
            out.append(Path(rel))
            seen.add(rel)
            html = p.read_bytes().decode("utf-8", "replace")
            for m in re.finditer(r'(?:og:image|twitter:image)["\']\s+content=["\']([^"\']+)', html, re.I):
                img = re.sub(r"^https?://[^/]+", "", m.group(1)).lstrip("/")
                if img and img not in seen and (BASE / img).is_file():
                    out.append(Path(img))
                    seen.add(img)
    # The sitemap is a list of canonical URLs, not a list of files that are
    # served. Legacy short URLs (calendar.html, notes.html, timer.html, ...)
    # are live, return 200 and carry the same head - analytics, ads, nav - but
    # they canonicalise to the -en.html page, so the sitemap omits them by
    # design and a head-level change never reached them. Ship every local page
    # that is actually part of the live web root and let the SIZE diff below
    # decide whether it changed.
    for path in BASE.rglob("*.html"):
        rel = path.relative_to(BASE).as_posix()
        if rel.split("/")[0] in NOT_LIVE:
            continue
        if rel not in seen:
            out.append(Path(rel))
            seen.add(rel)

    for extra in ("sitemap.xml", ".htaccess", "robots.txt"):
        if extra not in seen and (BASE / extra).is_file():
            out.append(Path(extra))
            seen.add(extra)
    return out


def remote_size(ftp, rel):
    try:
        return int(ftp.sendcmd("SIZE /" + rel.as_posix()).split()[-1])
    except Exception:
        return None


def scan(files):
    changed = []
    per_conn = [files[i::WORKERS] for i in range(WORKERS)]

    def worker(batch):
        last = None
        for attempt in range(MAX_ATTEMPTS):
            try:
                ftp = connect()
                out = [rel for rel in batch if remote_size(ftp, rel) != (BASE / rel).stat().st_size]
                try:
                    ftp.quit()
                except Exception:
                    pass
                return out
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"scan worker failed after {MAX_ATTEMPTS}: {last}")

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed([ex.submit(worker, b) for b in per_conn if b]):
            changed.extend(fut.result())
    changed.sort()
    return changed


def build_zip(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in files:
            zf.write(BASE / rel, rel.as_posix())
    return buf.getvalue()


def php_helper(token):
    return """<?php
@set_time_limit(0);
$t = '%s';
if (($_GET['t'] ?? '') !== $t) { http_response_code(403); exit('forbidden'); }
$zip = __DIR__ . '/%s';
if (!class_exists('ZipArchive')) { http_response_code(500); exit('no-zip-ext'); }
$z = new ZipArchive();
if ($z->open($zip) !== true) { http_response_code(500); exit('open-failed'); }
$n = $z->numFiles;
$ok = $z->extractTo(__DIR__);
$z->close();
if (!$ok) { http_response_code(500); exit('extract-failed'); }
@unlink($zip);
@unlink(__FILE__);
header('Content-Type: application/json');
echo json_encode(array('ok' => true, 'files' => $n));
""" % (token, ZIP_NAME)


def put(ftp, name, data):
    try:
        ftp.delete("/" + name)
    except ftplib.error_perm:
        pass
    ftp.storbinary("STOR /" + name, io.BytesIO(data))


def main():
    dry = "--dry-run" in sys.argv
    t0 = time.time()

    files = target_files()
    print(f"{len(files)} local files listed by the local sitemap", flush=True)

    changed = scan(files)
    if not changed:
        print("Nothing changed remotely - no upload needed.")
        return 0
    print(f"changed/new: {len(changed)} files ({time.time() - t0:.0f}s scan)", flush=True)

    if dry:
        for rel in changed[:40]:
            print("  ", rel.as_posix())
        if len(changed) > 40:
            print(f"   ... and {len(changed) - 40} more")
        return 0

    pkg = build_zip(changed)
    print(f"zip: {len(pkg) / 1048576:.1f} MiB", flush=True)

    token = secrets.token_urlsafe(24)
    helper = f"th-unzip-{token[:12]}.php"

    ftp = connect()
    put(ftp, ZIP_NAME, pkg)
    put(ftp, helper, php_helper(token).encode())
    ftp.quit()
    print("uploaded package + helper", flush=True)

    try:
        with urllib.request.urlopen(f"{PUBLIC}/{helper}?t={token}", timeout=300) as r:
            print("extract:", r.read().decode(), flush=True)
    except Exception as e:  # noqa: BLE001
        print("EXTRACT FAILED:", e)
        return 1

    ftp = connect()
    for name in (ZIP_NAME, helper):
        try:
            ftp.delete("/" + name)
        except ftplib.error_perm:
            pass
    try:
        ftp.quit()
    except Exception:
        pass

    for name in (ZIP_NAME, helper):
        try:
            with urllib.request.urlopen(f"{PUBLIC}/{name}?t={token}", timeout=30):
                print(f"WARNING: {name} still reachable")
        except urllib.error.HTTPError as e:
            print(f"{name} gone:", e.code)

    print(f"done in {time.time() - t0:.0f}s - {len(changed)} files extracted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
