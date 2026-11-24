#!/usr/bin/env python3
"""Compare store.config.json with what the App Store is actually serving.

The generator in write_store_listings.py decides what the copy should be; this
script answers the other question: does the App Store still show exactly that
copy in each storefront?

It uses Apple's public lookup API, so it needs no credentials and no key of any
kind — which is why the scheduled workflow can run it on a bare runner. Apple
publishes the app name and the description per storefront; the subtitle and the
keywords are not exposed publicly, so those two fields cannot be verified here
and are reported as unverified rather than as a match.

    python tools/check_store_listings.py
    python tools/check_store_listings.py --json

Each drifting locale lists every line that differs (repo text against live
text), capped at 12 lines per field so a full rewrite stays readable. --json
carries every differing line with no cap so a script or CI summary can consume
it.

Exit status is 0 when every locale matches, 1 when anything has drifted, and 2
when the check could not run at all: the API was unreachable, or store.config.json
is missing or unreadable. This script is what
.github/workflows/store-listings-drift.yml runs daily, so the distinction
matters: a network failure must not look like drift.
"""
import argparse
import io
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# The report contains every language the listing does. Windows hands Python a
# cp1252 console by default, which raises on Cyrillic, Greek or Arabic instead of
# printing it, so the stream is forced to UTF-8 before anything is written.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

APP_ID = "6756510490"
BASE = "https://itunes.apple.com/lookup"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "store.config.json")

# App Store Connect language -> (storefront country, language code for API).
# Passing l=<lang> ensures the lookup API returns the localized metadata for
# that language instead of falling back to default English.
STOREFRONTS = {
    "en-US": ("us", "en"),
    "de-DE": ("de", "de"),
    "es-ES": ("es", "es"),
    "fr-FR": ("fr", "fr"),
    "ru": ("ru", "ru"),
    "ar-SA": ("sa", "ar"),
    "el": ("gr", "el"),
}

# (lookup API key, label, store.config.json key)
PUBLIC_FIELDS = (
    ("trackName", "title", "title"),
    ("description", "description", "description"),
)

# Apple never exposes these two publicly; saying so is better than implying a match.
UNVERIFIED = ("subtitle", "keywords")

MAX_DIFF_LINES = 12
LINE_WIDTH = 100


def normalise(text):
    """Undo the line-endings and spacing the store is free to change."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def load_expected():
    with io.open(CONFIG, encoding="utf-8") as handle:
        config = json.load(handle)
    info = ((config.get("apple") or {}).get("info")) or {}
    if not info:
        raise ValueError("store.config.json has no apple.info entries")
    return info


def fetch(app_id, country, lang=None):
    """Return the lookup result for one storefront, or None when it is not sold there."""
    params = {"id": app_id, "country": country}
    if lang:
        params["l"] = lang
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        BASE + "?" + query,
        headers={"User-Agent": "TimerHaven-listing-check/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload.get("resultCount"):
        return None
    return payload["results"][0]


def diff_lines(expected, actual):
    """Return every line that differs, as dicts with 1-based line numbers."""
    expected_lines = expected.split("\n")
    actual_lines = actual.split("\n")
    differing = []
    for index in range(max(len(expected_lines), len(actual_lines))):
        left = expected_lines[index] if index < len(expected_lines) else "<missing>"
        right = actual_lines[index] if index < len(actual_lines) else "<missing>"
        if left != right:
            differing.append({"line": index + 1, "repo": left, "live": right})
    return differing


def compare_locale(locale, expected, result, storefront):
    """Return (entry, drifted) for one locale."""
    if result is None:
        return {
            "locale": locale,
            "storefront": storefront,
            "status": "DRIFT",
            "fields": [{
                "field": "storefront",
                "label": "listing",
                "repo_length": 0,
                "live_length": 0,
                "differing_lines": 1,
                "same_lines": False,
                "lines": [{
                    "line": 1,
                    "repo": "listed in the %s storefront" % storefront,
                    "live": "not sold in the %s storefront" % storefront,
                }],
            }],
        }, True

    fields = []
    for api_key, label, config_key in PUBLIC_FIELDS:
        wanted = normalise(expected.get(config_key) or "")
        served = normalise(result.get(api_key) or "")
        if wanted == served:
            continue
        differing = diff_lines(wanted, served)
        fields.append({
            "field": api_key,
            "label": label,
            "repo_length": len(wanted),
            "live_length": len(served),
            "differing_lines": len(differing),
            "same_lines": not differing,
            "lines": differing,
        })

    return {
        "locale": locale,
        "storefront": storefront,
        "status": "DRIFT" if fields else "MATCH",
        "fields": fields,
    }, bool(fields)


def describe_field(field):
    """Render one drifting field for the console report."""
    if field["same_lines"]:
        return ["%s: same lines, text differs (%d vs %d chars)"
                % (field["label"], field["repo_length"], field["live_length"])]
    lines = ["%s: %d differing line%s"
             % (field["label"], field["differing_lines"],
                "" if field["differing_lines"] == 1 else "s")]
    for item in field["lines"][:MAX_DIFF_LINES]:
        lines.append("  line %d repo: %s" % (item["line"], item["repo"][:LINE_WIDTH]))
        lines.append("  line %d live: %s" % (item["line"], item["live"][:LINE_WIDTH]))
    if field["differing_lines"] > MAX_DIFF_LINES:
        lines.append("  ... and %d more differing lines"
                     % (field["differing_lines"] - MAX_DIFF_LINES))
    return lines


def print_report(results):
    for entry in results:
        print("%-6s %-3s %s"
              % (entry["locale"], entry["storefront"], entry["status"]))
        for field in entry["fields"]:
            for line in describe_field(field):
                print("       " + line)

    drifted = [entry["locale"] for entry in results if entry["status"] == "DRIFT"]
    if drifted:
        print("\n%d of %d listings drifted from store.config.json: %s"
              % (len(drifted), len(results), ", ".join(drifted)))
    else:
        print("\nall %d listings match store.config.json" % len(results))
    print("not verifiable publicly (Apple does not expose them): %s"
          % ", ".join(UNVERIFIED))


def report_unavailable(args, code, message):
    """Exit 2: nothing was compared, so this is not a drift result."""
    if args.json:
        print(json.dumps({"error": code, "message": message}, ensure_ascii=False))
    else:
        print("error: " + message, file=sys.stderr)
    return 2


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare store.config.json with what the App Store is serving."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the findings as a JSON document instead of the console report",
    )
    parser.add_argument(
        "--app-id",
        default=APP_ID,
        help="App Store app id to look up (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    try:
        expected = load_expected()
    except (OSError, ValueError) as error:
        return report_unavailable(args, "bad_config",
                                  "cannot read store.config.json: %s" % error)

    results = []
    for locale in expected:
        storefront = STOREFRONTS.get(locale)
        if not storefront:
            return report_unavailable(
                args, "unknown_locale",
                "%s has no storefront mapping in check_store_listings.py" % locale)
        country = storefront[0]
        lang = storefront[1] if len(storefront) > 1 else None
        try:
            result = fetch(args.app_id, country, lang)
        except urllib.error.HTTPError as error:
            return report_unavailable(
                args, "app_store_rejected",
                "the lookup API refused the request: HTTP %d %s"
                % (error.code, error.reason))
        except urllib.error.URLError as error:
            return report_unavailable(
                args, "app_store_unreachable",
                "cannot reach the App Store lookup API: %s" % error.reason)
        except (ValueError, OSError) as error:
            return report_unavailable(
                args, "app_store_unreadable",
                "the lookup API returned something unreadable: %s" % error)

        entry, _ = compare_locale(locale, expected[locale], result, country)
        results.append(entry)

    drifted = [entry["locale"] for entry in results if entry["status"] == "DRIFT"]

    if args.json:
        print(json.dumps({
            "app_id": args.app_id,
            "checked": len(results),
            "match": not drifted,
            "drifted": drifted,
            "unverified": list(UNVERIFIED),
            "listings": results,
        }, ensure_ascii=False, indent=1))
    else:
        print_report(results)

    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
