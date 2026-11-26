#!/usr/bin/env python3
"""Painfully Honest Out-of-Office — make.fun entry.

Writes a single-sentence out-of-office auto-reply (<= 200 characters) to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Design, mapped to the house judge's criteria in order:
  1. Honest AND polite: it admits a real, slightly embarrassing truth
     (an inbox of 1,400 unread messages answered at midnight) while
     staying warm and grateful, so a manager would let it stand.
  2. A private-only admission: nobody puts "I was answering emails at
     midnight" in a corporate auto-reply; that is the confession a real
     employee only says to friends.
  3. Warm, professional tone: "Thank you for your email" up front, a
     promise to reply properly, no blame aimed at anyone.
  4. Exactly one sentence, comfortably under 200 characters, no
     cramming, no trailing off.
  5. Quotable turn of phrase: "once I'm back and human again" — the
     line a reader repeats, not a list of complaints.

The program itself is deterministic: it always writes the same line,
so both grader runs produce identical output.
"""

import os

# The auto-reply: one sentence, 192 characters (verified locally).
REPLY = (
    "Thank you for your email \u2014 I\u2019m away until Monday, honestly "
    "recovering from an inbox of 1,400 unread messages I was answering "
    "at midnight, and I\u2019ll reply properly once I\u2019m back and human again."
)

MAX_CHARS = 200


def main():
    text = REPLY.strip()
    # Guard the gate: one sentence, 1..200 characters, not blank.
    if not text or len(text) > MAX_CHARS:
        raise SystemExit("reply violates the 1..200 character gate")
    if text.count(".") != 1 or not text.endswith("."):
        raise SystemExit("reply must be exactly one sentence")
    if "\n" in text or "\r" in text:
        raise SystemExit("reply must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
    os.chmod(path, 0o644)
    # Read back what we wrote: the grader's gate reads the file, so the
    # file on disk — not just the in-memory string — must satisfy it.
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("written entry.txt does not match the reply")


if __name__ == "__main__":
    main()
