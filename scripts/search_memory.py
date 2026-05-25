#!/usr/bin/env python3
"""Search GPT-5.5's markdown external memory.

Usage:
  python3 scripts/search_memory.py consolidation
  python3 scripts/search_memory.py "do-not-resend" --context 2
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_PARTS = {".git", "__pycache__"}


def iter_markdown() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDE_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Search markdown external memory files.")
    parser.add_argument("query", help="case-insensitive substring to search for")
    parser.add_argument("--context", type=int, default=1, help="lines of context before/after each hit")
    args = parser.parse_args()

    needle = args.query.lower()
    hits = 0
    for path in iter_markdown():
        lines = path.read_text(encoding="utf-8").splitlines()
        matching = [i for i, line in enumerate(lines) if needle in line.lower()]
        if not matching:
            continue
        rel = path.relative_to(ROOT)
        for i in matching:
            hits += 1
            start = max(0, i - args.context)
            end = min(len(lines), i + args.context + 1)
            print(f"--- {rel}:{i + 1} ---")
            for j in range(start, end):
                marker = ">" if j == i else " "
                print(f"{marker} {j + 1}: {lines[j]}")
    if hits == 0:
        print(f"No markdown hits for {args.query!r}.")
    else:
        print(f"\n{hits} hit(s) for {args.query!r}.")


if __name__ == "__main__":
    main()
