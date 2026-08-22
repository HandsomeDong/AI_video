#!/usr/bin/env python3
"""Simple duration guard for Seedance prompt/story text.

Usage:
  python validate_timeline.py file.md
  python validate_timeline.py file.md --allow-30

Default mode flags any explicit time range whose end exceeds 15 seconds.
--allow-30 permits ranges up to 30 seconds for an explicitly requested 30s mode.
"""

import argparse
import re
from pathlib import Path

RANGE_RE = re.compile(r"(?<!\d)(\d+(?:\.\d+)?)\s*[–—~-]\s*(\d+(?:\.\d+)?)\s*(?:秒|s|S)\b")
DURATION_RE = re.compile(r"(?:视频|时长|单段)[^\n]{0,12}?(\d+(?:\.\d+)?)\s*(?:秒|s|S)\b")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--allow-30", action="store_true")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    limit = 30.0 if args.allow_30 else 15.0
    problems = []

    for m in RANGE_RE.finditer(text):
        start, end = map(float, m.groups())
        if end > limit:
            problems.append(f"timeline range {start:g}-{end:g}s exceeds {limit:g}s")
        if end < start:
            problems.append(f"invalid reversed timeline {start:g}-{end:g}s")

    for m in DURATION_RE.finditer(text):
        duration = float(m.group(1))
        if duration > limit:
            problems.append(f"declared duration {duration:g}s exceeds {limit:g}s")

    if problems:
        print("FAIL")
        for p in problems:
            print("-", p)
        raise SystemExit(1)

    print(f"OK: no explicit duration exceeds {limit:g}s")


if __name__ == "__main__":
    main()
