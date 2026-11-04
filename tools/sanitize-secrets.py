#!/usr/bin/env python3
"""Move TimerHaven's credentials out of the repo without breaking the site.

GitGuardian flagged the public repo: the SMTP password and contact secret sat
in api/contact.php, the mailer password in api/engine.php and
api/subscribe.php, the dashboard fallback password in api/list_subscribers.php,
and the FTP password in fifteen upload scripts.

The values are moved into two untracked files and every caller is rewritten to
read from them:

  api/secrets.local.php     - uploaded with the site, never committed
  scripts/_secrets.py       - imported by the upload scripts, never committed

Each caller keeps an environment-variable fallback so a fresh clone still runs.

Run: python tools/sanitize-secrets.py [--dry-run]
"""
import os
import re
import sys

DRY = "--dry-run" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHP_BLOCK = """// Credentials are not stored in this repo. They come from api/secrets.local.php
// (uploaded with the site, never committed) or from the environment.
$__secrets = is_file(__DIR__ . '/secrets.local.php') ? (include __DIR__ . '/secrets.local.php') : [];
if (!is_array($__secrets)) { $__secrets = []; }
"""


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="surrogateescape") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8",
              errors="surrogateescape", newline="") as fh:
        fh.write(text)


def php_quote(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def py_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def collect():
    """Pull the live values out of the files before rewriting them."""
    found = {}
    contact = read("api/contact.php")
    for name, key in (("EXPECTED_SECRET", "contact_secret"), ("SMTP_PASS", "smtp_pass")):
        m = re.search(r"\$%s\s*=\s*'([^']*)'" % name, contact)
        if m:
            found[key] = m.group(1)

    for rel in ("api/engine.php", "api/subscribe.php"):
        m = re.search(r"\$mail->Password\s*=\s*'([^']*)'", read(rel))
        if m:
            found.setdefault("smtp_pass", m.group(1))

    m = re.search(r'\$default_password\s*=\s*"([^"]*)"', read("api/list_subscribers.php"))
    if m:
        found["admin_default_password"] = m.group(1)

    ftp = None
    for rel in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
        if not rel.endswith(".py"):
            continue
        m = re.search(r'(?:passwd|FTP_PASS|PASSWORD)\s*=\s*[\'"]([^\'"]{6,})[\'"]',
                      read(os.path.join("scripts", rel)))
        if m:
            ftp = m.group(1)
            break
    if ftp:
        found["ftp_pass"] = ftp
    return found


def main():
    found = collect()
    print("recovered keys:", ", ".join(sorted(found)) or "(none)")

    # --- untracked carriers -------------------------------------------------
    php = "<?php\n// Local, uncommitted credentials for TimerHaven.\n// Uploaded by the deploy script; excluded from git.\nreturn [\n"
    for key in ("contact_secret", "smtp_pass", "admin_default_password"):
        if key in found:
            php += "    %s => %s,\n" % (php_quote(key), php_quote(found[key]))
    php += "];\n"

    py = '"""Local, uncommitted credentials for the upload scripts."""\n'
    if "ftp_pass" in found:
        py += "FTP_PASS = %s\n" % py_quote(found["ftp_pass"])
        py += "FTP_USER = \"\"  # set if it differs from the script default\n"
    if "smtp_pass" in found:
        py += "SMTP_PASS = %s\n" % py_quote(found["smtp_pass"])

    if not DRY:
        write("api/secrets.local.php", php)
        write("scripts/_secrets.py", py)
    print("wrote api/secrets.local.php and scripts/_secrets.py (untracked)")

    # --- rewrite the PHP callers -------------------------------------------
    replacements = {
        "api/contact.php": [
            (r"\$EXPECTED_SECRET\s*=\s*'[^']*';",
             "$EXPECTED_SECRET = getenv('TH_CONTACT_SECRET') ?: ($__secrets['contact_secret'] ?? '');"),
            (r"\$SMTP_PASS\s*=\s*'[^']*';",
             "$SMTP_PASS       = getenv('TH_SMTP_PASS') ?: ($__secrets['smtp_pass'] ?? '');"),
        ],
        "api/engine.php": [
            (r"\$mail->Password\s*=\s*'[^']*';",
             "$mail->Password   = getenv('TH_SMTP_PASS') ?: ($__secrets['smtp_pass'] ?? '');"),
        ],
        "api/subscribe.php": [
            (r"\$mail->Password\s*=\s*'[^']*';",
             "$mail->Password   = getenv('TH_SMTP_PASS') ?: ($__secrets['smtp_pass'] ?? '');"),
        ],
        "api/list_subscribers.php": [
            (r'\$default_password\s*=\s*"[^"]*";',
             "$default_password = getenv('TH_ADMIN_PASSWORD') ?: ($__secrets['admin_default_password'] ?? '');"),
        ],
    }

    for rel, subs in replacements.items():
        text = read(rel)
        new = text
        for pattern, repl in subs:
            new = re.sub(pattern, repl, new)
        if new == text:
            print("  no change:", rel)
            continue
        # Insert the secrets include once, right after the opening <?php block
        # if the file does not already have it.
        if "$__secrets" in new and PHP_BLOCK.strip() not in new:
            marker = new.find("<?php")
            insert_at = new.find("\n", marker) + 1
            new = new[:insert_at] + PHP_BLOCK + new[insert_at:]
        print("  rewritten:", rel)
        if not DRY:
            write(rel, new)

    # --- rewrite the Python upload scripts ---------------------------------
    scripts_dir = os.path.join(ROOT, "scripts")
    changed = 0
    for name in sorted(os.listdir(scripts_dir)):
        if not name.endswith(".py") or name.startswith("_"):
            continue
        rel = os.path.join("scripts", name)
        text = read(rel)
        if not re.search(r'(?:passwd|FTP_PASS|PASSWORD)\s*=\s*[\'"][^\'"]{6,}[\'"]', text):
            continue
        new = re.sub(
            r'(?:passwd|FTP_PASS|PASSWORD)\s*=\s*[\'"][^\'"]{6,}[\'"]',
            "__FTP_FALLBACK__", text, count=1)
        new = new.replace(
            "__FTP_FALLBACK__",
            "FTP_PASS")
        # ensure the credential import sits above first use
        if "_secrets" not in new:
            header = (
                "try:  # local credentials file, never committed\n"
                "    from _secrets import FTP_PASS\n"
                "except ImportError:  # fall back to the environment\n"
                "    import os\n"
                "    FTP_PASS = os.environ.get('TH_FTP_PASS', '')\n")
            lines = new.splitlines(keepends=True)
            insert_at = 0
            for i, line in enumerate(lines[:12]):
                if line.startswith(("import ", "from ")):
                    insert_at = i + 1
            if insert_at == 0 and lines and lines[0].startswith("#!"):
                insert_at = 1
            if insert_at == 0 and lines and lines[0].startswith(('"""', "'''")):
                pass
            new = "".join(lines[:insert_at]) + header + "".join(lines[insert_at:])
        print("  rewritten:", rel)
        changed += 1
        if not DRY:
            write(rel, new)

    verb = "[dry-run] would sanitise" if DRY else "sanitised"
    print("\n%s %d PHP file(s) and %d script(s)" % (verb, len(replacements), changed))


if __name__ == "__main__":
    main()
