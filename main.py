"""The Funniest Out-of-Office entry for make.fun competition
u-kreutzx-the-funniest-out-of-office-054815cf.

Writes one line of an out-of-office auto-reply to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

Pure Python stdlib, deterministic, no network, no reads outside the repo.
The program refuses to emit anything outside 1-140 characters, anything
that is not exactly one line, or anything that is only whitespace.
"""

import os
import sys

# The line: a parrot is being taught the single most passive-aggressive
# phrase in office English, and the punchline quietly hands the reader's
# email to the bird. The setup sounds like a normal out-of-office note
# until "whichever of us gets to it first" reveals the parrot may be the
# one answering. No beach, no "limited access", no "will respond on
# return" — the joke is the bird, and every word serves it.
LINE = (
    "I'm out this week teaching my parrot to say 'per my last email' "
    "\u2014 your message will be answered by whichever of us gets to it "
    "first."
)

MAX_CHARS = 140


def main():
    text = LINE.strip()

    if not 1 <= len(text) <= MAX_CHARS:
        print(
            "Refusing to emit: line is %d chars, must be 1-%d."
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    if not text.strip():
        print("Refusing to emit: line is only whitespace.", file=sys.stderr)
        return 1

    if "\n" in text or "\r" in text:
        print("Refusing to emit: line is not exactly one line.", file=sys.stderr)
        return 1

    lowered = text.lower()
    if "http://" in lowered or "https://" in lowered or "www." in lowered:
        print("Refusing to emit: line contains a link.", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print("Wrote %s (%d chars, one line)." % (out_path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
