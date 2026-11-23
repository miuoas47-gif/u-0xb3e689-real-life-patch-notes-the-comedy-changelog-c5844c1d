#!/usr/bin/env python3
"""Write the Real-Life Patch Notes entry to entry.txt.

Stdlib only, no network, no arguments. The output directory comes from
$MAKEFUN_OUTPUT_DIR and falls back to /output.
"""

import os
import sys

ENTRY = (
    "v5.3.1: fixed a bug where walking through a doorway "
    "cleared the user's short-term memory buffer."
)


def main() -> int:
    # The gate requires a single line of 1-160 characters, not only
    # whitespace, so validate the line before writing it.
    if not ENTRY or ENTRY != ENTRY.strip():
        print("error: entry is empty or has surrounding whitespace", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(ENTRY) > 160:
        print("error: entry exceeds 160 characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Read it back and verify the written bytes decode to the same line.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("error: read-back mismatch in entry.txt", file=sys.stderr)
        return 1
    if written.decode("utf-8") != ENTRY:
        print("error: entry.txt is not the entry as UTF-8 text", file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(ENTRY)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
