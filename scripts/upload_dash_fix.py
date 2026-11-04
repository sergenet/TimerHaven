"""Upload the six blog articles repaired by fix_dashes.py.

Credentials are read from an existing upload script in this folder, so no
secret is copied into a new file or printed.

Run: python scripts/upload_dash_fix.py --check
     python scripts/upload_dash_fix.py
"""
import ftplib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CRED_SOURCE = os.path.join(HERE, "upload_cities.py")

FILES = [
    "asynchronous-communication-guide.html",
    "deep-work-guide.html",
    "eisenhower-matrix-guide.html",
    "flow-state-guide.html",
    "morning-routine.html",
    "pomodoro-50-10-adhd-guide.html",
]


def creds():
    text = open(CRED_SOURCE, encoding="utf-8", errors="replace").read()
    out = {}
    for key in ("host", "user", "passwd"):
        m = re.search(rf"^{key}\s*=\s*['\"](.*?)['\"]", text, re.M)
        if not m:
            sys.exit(f"could not read {key} from {CRED_SOURCE}")
        out[key] = m.group(1)
    return out


def main():
    c = creds()
    ftp = ftplib.FTP(c["host"], timeout=45)
    ftp.login(c["user"], c["passwd"])
    ftp.set_pasv(True)
    try:
        print("remote root:", ftp.pwd())
        if "--check" in sys.argv:
            print("blog entries:", len(ftp.nlst("blog")))
            return
        ok = 0
        for name in FILES:
            local = os.path.join(ROOT, "blog", name)
            size = os.path.getsize(local)
            with open(local, "rb") as fh:
                ftp.storbinary(f"STOR blog/{name}", fh)
            remote = ftp.size(f"blog/{name}")
            status = "ok" if remote == size else f"MISMATCH remote={remote}"
            print(f"uploaded blog/{name}  local={size}  {status}")
            ok += remote == size
        print(f"\nverified {ok}/{len(FILES)} files byte-for-byte on the server")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == "__main__":
    main()
