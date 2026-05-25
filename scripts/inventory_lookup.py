#!/usr/bin/env python3
"""Look up indexed memory items from inventory.yaml.

This makes inventory.yaml actionable: search by id/summary/retrieval cue and print
repo-relative paths that a future session can open immediately. Multi-word queries match when every token appears somewhere in the indexed fields.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_memory_items import parse_items  # noqa: E402


def load_items() -> list[dict[str, str]]:
    return parse_items((ROOT / "inventory.yaml").read_text(encoding="utf-8"))


def matches(item: dict[str, str], query: str) -> bool:
    haystack = "\n".join(str(item.get(field, "")) for field in [
        "id",
        "status",
        "kind",
        "summary",
        "source",
        "path",
        "retrieval_cue",
        "internal_memory_policy",
        "error_recovery",
    ]).lower()
    tokens = [token for token in query.lower().split() if token]
    return bool(tokens) and all(token in haystack for token in tokens)


def print_item(item: dict[str, str], show_file: bool = False, max_lines: int = 40) -> None:
    print(f"id: {item.get('id')}")
    for field in ["status", "kind", "summary", "path", "source", "retrieval_cue", "internal_memory_policy", "expiry_or_review", "last_verified", "error_recovery"]:
        if field in item:
            print(f"{field}: {item[field]}")
    if show_file and item.get("path"):
        path = ROOT / item["path"]
        print(f"--- {item['path']} first {max_lines} lines ---")
        if path.is_file():
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for idx, line in enumerate(lines[:max_lines], 1):
                print(f"{idx:03d}: {line}")
        else:
            print("(path is not a file; validation should catch missing paths)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search GPT-5.5 memory inventory by query or exact id.")
    parser.add_argument("query", help="token query to search across inventory fields; all tokens must match unless --id is used")
    parser.add_argument("--id", action="store_true", help="require exact id match")
    parser.add_argument("--show-file", action="store_true", help="print the first lines of the item's path target")
    parser.add_argument("--max-lines", type=int, default=40, help="lines to show with --show-file")
    args = parser.parse_args()

    items = load_items()
    if args.id:
        hits = [item for item in items if item.get("id") == args.query]
    else:
        hits = [item for item in items if matches(item, args.query)]
    if not hits:
        print(f"No inventory hits for {args.query!r}")
        sys.exit(1)
    print(f"{len(hits)} inventory hit(s) for {args.query!r}")
    for idx, item in enumerate(hits, 1):
        if idx > 1:
            print()
        print_item(item, show_file=args.show_file, max_lines=args.max_lines)


if __name__ == "__main__":
    main()
