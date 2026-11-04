"""Repair em dashes destroyed by an earlier encoding pass in six blog articles.

Two damage patterns were found:
  1. the em dash was replaced by '?'        -> "effort?it's"
  2. the em dash was dropped entirely       -> "cortexthe part"

Both repairs use the &#8212; entity, which is already used elsewhere on the
site and cannot be re-mangled by a later encoding pass.
"""
import io
import os
import re
import sys

BLOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")

FILES = [
    "asynchronous-communication-guide.html",
    "deep-work-guide.html",
    "eisenhower-matrix-guide.html",
    "flow-state-guide.html",
    "morning-routine.html",
    "pomodoro-50-10-adhd-guide.html",
]

DASH = "&#8212;"

# Fused words: the dash between them was dropped.
FUSED = {
    "boredin": "bored" + DASH + "in",
    "humanand": "human" + DASH + "and",
    "hereyou": "here" + DASH + "you",
    "honestis": "honest" + DASH + "is",
    "cortexthe": "cortex" + DASH + "the",
    "scienceone": "science" + DASH + "one",
    "dowhat": "do" + DASH + "what",
}


def fix_question_marks(text):
    """Replace '?' sitting between two letters, ignoring the gtag URL."""
    out = []
    count = 0
    i = 0
    while True:
        j = text.find("?", i)
        if j == -1:
            out.append(text[i:])
            break
        prev_ch = text[j - 1] if j else ""
        next_ch = text[j + 1] if j + 1 < len(text) else ""
        guarded = "gtag/js" in text[max(0, j - 12):j + 6]
        if prev_ch.isalpha() and next_ch.isalpha() and not guarded:
            out.append(text[i:j] + DASH)
            count += 1
        else:
            out.append(text[i:j + 1])
        i = j + 1
    return "".join(out), count


def main():
    total_q = total_f = 0
    for name in FILES:
        path = os.path.join(BLOG, name)
        # newline="" keeps the file's existing CRLF endings byte-for-byte.
        with io.open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()

        new, q = fix_question_marks(text)

        f = 0
        for bad, good in FUSED.items():
            hits = len(re.findall(r"\b" + bad + r"\b", new))
            if hits:
                new = re.sub(r"\b" + bad + r"\b", good, new)
                f += hits
                print("    fused: %-12s -> %-18s x%d" % (bad, good, hits))

        if new != text:
            with io.open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
        print("%-38s ? sites: %d   fused: %d" % (name, q, f))
        total_q += q
        total_f += f

    print("\nTOTAL: %d question-mark sites, %d fused words" % (total_q, total_f))
    return 0


if __name__ == "__main__":
    sys.exit(main())
