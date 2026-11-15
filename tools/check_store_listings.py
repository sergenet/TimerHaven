#!/usr/bin/env python3
"""Compare the fastlane store listings with what is live on Google Play.

The generator in write_store_listings.py decides what the copy should be; this
script answers the other question: is Play still serving exactly that copy?
It opens a read-only Edit, reads each listing, and deletes the Edit again, so
nothing is changed or submitted for review.

Authentication is the same Play Developer API route the listings are published
with. Mint a short-lived token and pass it in:

    export PLAY_ACCESS_TOKEN=$(gcloud auth print-access-token \
        --scopes=https://www.googleapis.com/auth/androidpublisher \
        --account=play-publisher-sa@timerhaven-translation.iam.gserviceaccount.com)
    python tools/check_store_listings.py

Exit status is 0 when every locale matches and 1 when anything has drifted.
"""
import io
import json
import os
import sys
import urllib.error
import urllib.request

PACKAGE = "com.sergenet.TimerHavenApp"
BASE = "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/" + PACKAGE
META = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "fastlane",
    "metadata",
    "android",
)

# fastlane folder -> Play locale code
LOCALES = {
    "en-US": "en-US",
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "ru": "ru-RU",
    "ar": "ar",
    "el": "el-GR",
}

FIELDS = (
    ("title", "title", "title.txt"),
    ("shortDescription", "short_description", "short_description.txt"),
    ("fullDescription", "full_description", "full_description.txt"),
)


def call(token, url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        raw = response.read()
        return response.status, (json.loads(raw) if raw else None)


def read_expected(folder, filename):
    path = os.path.join(META, folder, filename)
    with io.open(path, encoding="utf-8") as handle:
        return handle.read().strip()


def first_difference(expected, actual):
    """Return a short description of where two texts diverge."""
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()
    for index in range(max(len(expected_lines), len(actual_lines))):
        left = expected_lines[index] if index < len(expected_lines) else "<missing>"
        right = actual_lines[index] if index < len(actual_lines) else "<missing>"
        if left != right:
            return "line %d: repo %r != live %r" % (index + 1, left[:80], right[:80])
    return "identical lines but lengths differ (%d vs %d chars)" % (len(expected), len(actual))


def main():
    token = os.environ.get("PLAY_ACCESS_TOKEN") or os.environ.get("TH_TOKEN")
    if not token:
        print("error: set PLAY_ACCESS_TOKEN (see the docstring for the gcloud command)", file=sys.stderr)
        return 2

    _, edit = call(token, BASE + "/edits", method="POST", body={})
    edit_id = edit["id"]
    drifted = []
    try:
        for folder, locale in LOCALES.items():
            _, listing = call(token, BASE + "/edits/" + edit_id + "/listings/" + locale)
            problems = []
            for api_key, label, filename in FIELDS:
                expected = read_expected(folder, filename)
                actual = listing.get(api_key, "").strip()
                if expected != actual:
                    problems.append("%s: %s" % (label, first_difference(expected, actual)))
            status = "MATCH" if not problems else "DRIFT"
            print("%-6s %-6s %s" % (locale, folder, status))
            if problems:
                drifted.append(locale)
                for problem in problems:
                    print("       " + problem)
    finally:
        call(token, BASE + "/edits/" + edit_id, method="DELETE")

    if drifted:
        print("\n%d of %d listings drifted from fastlane: %s" % (len(drifted), len(LOCALES), ", ".join(drifted)))
        return 1
    print("\nall %d listings match fastlane" % len(LOCALES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
