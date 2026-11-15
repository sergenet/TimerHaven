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

Each drifting locale lists every line that differs (repo text against live
text), capped at 12 lines per field so a full rewrite stays readable. Pass
--json for the same findings as one JSON document (every differing line, no
cap) so a script or CI summary can consume it.

Exit status is 0 when every locale matches, 1 when anything has drifted, and 2
when no Play credentials are configured.
"""
import argparse
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

# A whole-description rewrite would otherwise bury the report, so list the
# differing lines and say how many were left out.
MAX_DIFF_LINES = 12
LINE_WIDTH = 100


def diff_lines(expected, actual):
    """Return every line that differs, as dicts with 1-based line numbers."""
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()
    differing = []
    for index in range(max(len(expected_lines), len(actual_lines))):
        left = expected_lines[index] if index < len(expected_lines) else "<missing>"
        right = actual_lines[index] if index < len(actual_lines) else "<missing>"
        if left != right:
            differing.append({"line": index + 1, "repo": left, "live": right})
    return differing


def check_listings(token):
    """Compare every locale against the live listing and return the findings."""
    _, edit = call(token, BASE + "/edits", method="POST", body={})
    edit_id = edit["id"]
    results = []
    try:
        for folder, locale in LOCALES.items():
            _, listing = call(token, BASE + "/edits/" + edit_id + "/listings/" + locale)
            fields = []
            for api_key, label, filename in FIELDS:
                expected = read_expected(folder, filename)
                actual = listing.get(api_key, "").strip()
                if expected == actual:
                    continue
                differing = diff_lines(expected, actual)
                fields.append(
                    {
                        "field": api_key,
                        "label": label,
                        "repo_length": len(expected),
                        "live_length": len(actual),
                        "differing_lines": len(differing),
                        "same_lines": not differing,
                        "lines": differing,
                    }
                )
            results.append(
                {
                    "locale": locale,
                    "folder": folder,
                    "status": "DRIFT" if fields else "MATCH",
                    "fields": fields,
                }
            )
    finally:
        call(token, BASE + "/edits/" + edit_id, method="DELETE")
    return results


def describe_field(field):
    """Render one drifting field for the console report."""
    if field["same_lines"]:
        return [
            "%s: same lines, text differs (%d vs %d chars)"
            % (field["label"], field["repo_length"], field["live_length"])
        ]
    lines = [
        "%s: %d differing line%s"
        % (field["label"], field["differing_lines"], "" if field["differing_lines"] == 1 else "s")
    ]
    for item in field["lines"][:MAX_DIFF_LINES]:
        lines.append("  line %d repo: %s" % (item["line"], item["repo"][:LINE_WIDTH]))
        lines.append("  line %d live: %s" % (item["line"], item["live"][:LINE_WIDTH]))
    if field["differing_lines"] > MAX_DIFF_LINES:
        lines.append("  ... and %d more differing lines" % (field["differing_lines"] - MAX_DIFF_LINES))
    return lines


def print_report(results):
    for entry in results:
        print("%-6s %-6s %s" % (entry["locale"], entry["folder"], entry["status"]))
        for field in entry["fields"]:
            for line in describe_field(field):
                print("       " + line)

    drifted = [entry["locale"] for entry in results if entry["status"] == "DRIFT"]
    if drifted:
        print("\n%d of %d listings drifted from fastlane: %s" % (len(drifted), len(results), ", ".join(drifted)))
    else:
        print("\nall %d listings match fastlane" % len(results))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare the fastlane store listings with what is live on Google Play."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the findings as a JSON document instead of the console report",
    )
    args = parser.parse_args(argv)

    token = os.environ.get("PLAY_ACCESS_TOKEN") or os.environ.get("TH_TOKEN")
    if not token:
        message = "set PLAY_ACCESS_TOKEN (see the docstring for the gcloud command)"
        if args.json:
            print(json.dumps({"error": "missing_token", "message": message}, ensure_ascii=False))
        else:
            print("error: " + message, file=sys.stderr)
        return 2

    results = check_listings(token)
    drifted = [entry["locale"] for entry in results if entry["status"] == "DRIFT"]

    if args.json:
        print(
            json.dumps(
                {
                    "package": PACKAGE,
                    "checked": len(results),
                    "match": not drifted,
                    "drifted": drifted,
                    "listings": results,
                },
                ensure_ascii=False,
                indent=1,
            )
        )
    else:
        print_report(results)

    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
