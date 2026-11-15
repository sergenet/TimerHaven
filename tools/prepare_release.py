#!/usr/bin/env python3
"""Prepare an iOS release: bump the version, regenerate the listing copy, verify.

It does the mechanical part of RELEASE.md so the order cannot drift:

  1. bump `expo.version` in app.json and `version` in package.json
  2. regenerate store.config.json from tools/write_store_listings.py
  3. compare all seven storefronts with what the App Store serves right now
  4. with --publish, push the regenerated copy to App Store Connect and re-verify

The build number is deliberately not touched: eas.json sets
`appVersionSource: remote` and `autoIncrement: true`, so EAS assigns the build
number it will accept. Writing one here would only disagree with the store.

    python tools/prepare_release.py --dry-run --version-name 1.1.4
    python tools/prepare_release.py --version-name 1.1.4
    python tools/prepare_release.py --publish            # asks before pushing
    python tools/prepare_release.py --publish --yes      # unattended

Exit status is 0 when the tree is ready to build, 1 when the version could not
be bumped or the live listing has drifted from the copy (publish it first, then
build), and 2 when the generator rejected the copy.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JSON = os.path.join(ROOT, "app.json")
PACKAGE_JSON = os.path.join(ROOT, "package.json")
EAS_JSON = os.path.join(ROOT, "eas.json")
WRITE = os.path.join(ROOT, "tools", "write_store_listings.py")
CHECK = os.path.join(ROOT, "tools", "check_store_listings.py")

VERSION_RE = re.compile(r'"version"\s*:\s*"([^"]*)"')
SEMVER_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")


def read(path):
    with io.open(path, encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def version_of(path):
    """Return the one "version" value in a JSON file, or die saying why not."""
    text = read(path)
    found = VERSION_RE.findall(text)
    if len(found) != 1:
        raise SystemExit(
            "cannot bump %s: expected exactly one \"version\" key, found %d"
            % (os.path.relpath(path, ROOT), len(found))
        )
    return found[0]


def set_version(path, new):
    """Rewrite the version in place so the rest of the file stays byte-identical."""
    text = read(path)
    replaced, count = VERSION_RE.subn(lambda m: '"version": "%s"' % new, text, count=1)
    if count != 1:
        raise SystemExit("cannot write %s: the version key moved" % os.path.relpath(path, ROOT))
    write(path, replaced)
    data = json.loads(read(path))
    actual = data["version"] if path == PACKAGE_JSON else (data.get("expo") or {}).get("version")
    if actual != new:
        raise SystemExit("wrote %s but the new version did not survive a re-read"
                         % os.path.relpath(path, ROOT))


def version_tuple(text):
    return tuple(int(part) for part in text.split("."))


def is_greater(new, old):
    """Compare versions of different lengths: 1.2 is not an increase on 1.1.0."""
    width = max(len(new), len(old))
    padded = lambda parts: parts + (0,) * (width - len(parts))
    return padded(new) > padded(old)


def run(command, label):
    """Run one step, echo its output and return the exit status."""
    print("\n$ " + " ".join(os.path.basename(part) if index == 0 else part
                            for index, part in enumerate(command)), flush=True)
    try:
        process = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8")
    except FileNotFoundError:
        # A traceback here would say nothing useful about the release.
        print("%s: %s is not installed or not on PATH" % (label, command[0]))
        return 1
    if process.returncode != 0:
        print("%s: exit %d" % (label, process.returncode))
    return process.returncode


def confirm(question, assume_yes):
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        print("not publishing: no terminal to confirm in; re-run with --yes")
        return False
    try:
        answer = input(question + " [y/N] ")
    except EOFError:
        # A redirected stdin can still look like a terminal on Windows.
        print("not publishing: no terminal to confirm in; re-run with --yes")
        return False
    return answer.strip().lower() in ("y", "yes")


def find_npx():
    """Windows ships npx as npx.cmd, which subprocess cannot find by bare name."""
    for name in ("npx", "npx.cmd"):
        found = shutil.which(name)
        if found:
            return found
    return None


def build_owner():
    """Say who owns the build number, from eas.json rather than from memory."""
    try:
        eas = json.loads(read(EAS_JSON))
    except (OSError, ValueError):
        return "unknown (eas.json unreadable)"
    source = (eas.get("cli") or {}).get("appVersionSource", "local")
    auto = ((eas.get("build") or {}).get("production") or {}).get("autoIncrement")
    if source == "remote" and auto:
        return "EAS (appVersionSource: remote, autoIncrement: true)"
    return "this repo (appVersionSource: %s, autoIncrement: %s)" % (source, bool(auto))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Bump the iOS version, regenerate the App Store listings and verify them."
    )
    parser.add_argument("--version-name", help="the App Store version to release, e.g. 1.1.4")
    parser.add_argument("--dry-run", action="store_true", help="show the bump, write nothing")
    parser.add_argument("--publish", action="store_true",
                        help="push the regenerated listing copy to App Store Connect")
    parser.add_argument("--yes", action="store_true", help="skip the publish confirmation")
    args = parser.parse_args(argv)

    app_version = version_of(APP_JSON)
    package_version = version_of(PACKAGE_JSON)
    print("app.json version:     %s" % app_version)
    print("package.json version: %s" % package_version)
    print("build number:         assigned by %s" % build_owner())

    new_version = args.version_name or app_version
    if args.version_name:
        if not SEMVER_RE.match(new_version):
            raise SystemExit("version = %r is not a version like 1.1.4" % new_version)
        if not is_greater(version_tuple(new_version), version_tuple(app_version)):
            raise SystemExit("version must increase: current %s, requested %s"
                             % (app_version, new_version))

    if args.dry_run:
        print("\nwould set app.json and package.json to %s; nothing written" % new_version)
        return 0

    if args.version_name:
        set_version(APP_JSON, new_version)
        set_version(PACKAGE_JSON, new_version)
        print("\nversion bump: app.json %s -> %s, package.json %s -> %s"
              % (app_version, new_version, package_version, new_version))
    else:
        print("\nno version given: regenerating and verifying the listing copy only")

    if run([sys.executable, WRITE], "generator failed") != 0:
        return 2

    status = run([sys.executable, CHECK], "drift check failed")
    if status == 2:
        print("\ndrift check skipped: it could not reach the App Store, so the live copy is "
              "unverified. Publish and confirm before uploading a build.")
    elif status == 1:
        print("\ndrift detected, publish the copy before building for upload:")
        if args.publish:
            if not confirm("Publish all seven listings to App Store Connect?", args.yes):
                return 1
            npx = find_npx()
            if not npx:
                print("publishing failed: npx is not installed or not on PATH")
                return 1
            if run([npx, "--no-install", "eas-cli", "metadata:push", "--non-interactive"],
                   "publishing failed") != 0:
                return 1
            # Only a clean comparison after the push counts as published.
            if run([sys.executable, CHECK], "post-publish check failed") != 0:
                print("\npublished, but the live listing still does not match: "
                      "App Store Connect may need a few minutes to serve the new copy")
                return 1
            print("\npublished and verified: the App Store now serves the regenerated listings")
        else:
            return 1

    print("""
still to do by hand:
  1. eas build -p ios --profile production    (EAS assigns the build number)
  2. eas submit -p ios --profile production   (or upload the .ipa from the build page)
  3. App Store Connect: release notes, then submit for review
  4. after review, re-run tools/check_store_listings.py and confirm the new version
     is what customers get — the daily workflow says so too""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
