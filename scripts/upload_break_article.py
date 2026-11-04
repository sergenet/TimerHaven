"""Upload the new breaks article and the files it touches.

Credentials are read from an existing upload script in this folder so no secret
is copied into a new file or printed. Run with --check first to list what is on
the server without changing anything.

Run: python scripts/upload_break_article.py --check
     python scripts/upload_break_article.py
"""
import ftplib
import os
import re
import sys

CRED_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "upload_cities.py")

FILES = [
    ("blog", "how-long-should-a-break-be.html"),
    ("blog", "index.html"),
    ("blog", "afternoon-slump.html"),
    ("blog", "time-blocking-vs-pomodoro.html"),
    ("images/blog", "break-length-featured.webp"),
    ("images/blog", "break-length-featured.png"),
    ("", "sitemap.xml"),
]

ROOT = "C:\\TimerHavenWebsite"


def creds():
    text = open(CRED_SOURCE, encoding="utf-8", errors="replace").read()
    out = {}
    for key in ("host", "user", "passwd"):
        m = re.search(rf"^{key}\s*=\s*['\"](.*?)['\"]", text, re.M)
        if not m:
            sys.exit(f"could not read {key} from {CRED_SOURCE}")
        out[key] = m.group(1)
    return out


def connect(c):
    ftp = ftplib.FTP(c["host"], timeout=45)
    ftp.login(c["user"], c["passwd"])
    ftp.set_pasv(True)
    return ftp


def check(ftp):
    print("remote root:", ftp.pwd())
    for remote_dir in ("blog", "images/blog"):
        print(f"\n--- {remote_dir} (first 6 entries)")
        try:
            names = ftp.nlst(remote_dir)
        except ftplib.error_perm as exc:
            print("  cannot list:", exc)
            continue
        for n in sorted(names)[:6]:
            print("  ", n)
        print("   total entries:", len(names))


def upload(ftp, path, remote_dir):
    local = os.path.join(ROOT, path, remote_dir) if False else os.path.join(
        ROOT, path.replace("/", "\\"), remote_dir
    )
    if not os.path.exists(local):
        print(f"MISSING LOCAL: {local}")
        return False
    size = os.path.getsize(local)
    target = f"{path}/{remote_dir}" if path else remote_dir
    with open(local, "rb") as f:
        ftp.storbinary(f"STOR {path}/{remote_dir}" if path else f"STOR {remote_dir}", f)
    print(f"uploaded {target} ({size} bytes)")
    return True


def main():
    c = creds()
    ftp = connect(c)
    try:
        check(ftp)
        if "--check" in sys.argv:
            return
        print("\n--- uploading")
        ok = 0
        for path, name in FILES:
            if upload(ftp, path, name):
                ok += 1
        print(f"\nuploaded {ok}/{len(FILES)} files")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == "__main__":
    main()
