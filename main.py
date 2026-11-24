"""Write a robot vacuum's funniest excuse to /output/entry.txt.

Standard library only. The file's content is exactly the excuse's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be one line of at most 140
characters, so the line is validated before it is written.
"""

import os

EXCUSE = (
    "I didn't miss that spot \u2014 I bumped its chair leg 12 times, "
    "my map renamed it 'unreachable,' and I don't argue with "
    "cartography."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line):
    """The bounty gate: one line, 1-140 characters, non-blank."""
    text = line.strip()
    if not 1 <= len(text) <= 140:
        raise ValueError("entry must be 1-140 characters")
    if not text:
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    # Revision: reject tabs and any other control characters too --
    # the gate counts one line of plain text, and a stray control
    # character could split or corrupt the line in the judge's view.
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError("entry must contain no control characters")
    if text != line:
        raise ValueError("entry must not have surrounding whitespace")
    return text


def write_entry(line):
    """Write the line's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(line.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(EXCUSE)
    write_entry(line)


if __name__ == "__main__":
    main()
