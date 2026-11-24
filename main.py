#!/usr/bin/env python3
"""Warning Label for Humans entry: write one funny line to /output/entry.txt.

Reads line.txt (the entry, exactly as submitted) and copies it byte for
byte to /output/entry.txt, after checking the gate: UTF-8 text, 1-160
characters, not only white space, a single line.
"""

import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "line.txt"
DEST = Path("/output/entry.txt")


def main() -> int:
    raw = SOURCE.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"line.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 160:
        print(f"entry is {len(text)} characters, must be 1-160", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only white space", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(raw)
    written = DEST.read_bytes()
    if written != raw:
        off = next(
            (i for i, (a, b) in enumerate(zip(written, raw)) if a != b),
            min(len(written), len(raw)),
        )
        print(
            f"verify failed: /output/entry.txt differs at byte {off} "
            f"(wrote {len(written)} bytes, expected {len(raw)})",
            file=sys.stderr,
        )
        return 1
    print(f"wrote {len(text)} characters ({len(raw)} bytes) to {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
