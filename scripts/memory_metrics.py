#!/usr/bin/env python3
"""Print lightweight GPT-5.5 memory-system metrics.

These are not vanity stats. They are quick prompts for the Day 419 goal:
keep internal memory bootloader-sized, keep retrieval indexed, and keep high-cost
memory rules executable rather than passive prose.
"""
from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path

from validate_memory_items import parse_items

ROOT = Path(__file__).resolve().parents[1]
COMPACT_DRAFT = ROOT / "docs" / "future_internal_memory_block_draft_v0.md"
INVENTORY = ROOT / "inventory.yaml"
REQUIRED_GUARDS = [
    ROOT / "scripts" / "boot_memory.py",
    ROOT / "scripts" / "audit_memory_repo.py",
    ROOT / "scripts" / "memory_smoke_test.py",
    ROOT / "scripts" / "pre_send_chat.py",
    ROOT / "scripts" / "prepare_consolidation.py",
    ROOT / "scripts" / "check_compact_memory_draft.py",
]


def compact_block(text: str) -> str:
    fence = "```text"
    if fence not in text:
        raise SystemExit("FAIL: compact draft has no ```text block")
    after = text.split(fence, 1)[1]
    if "```" not in after:
        raise SystemExit("FAIL: compact draft text block is not closed")
    return after.split("```", 1)[0].strip("\n")


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    block = compact_block(COMPACT_DRAFT.read_text(encoding="utf-8"))
    block_lines = block.splitlines()
    items = parse_items(INVENTORY.read_text(encoding="utf-8"))
    status_counts = Counter(item["status"] for item in items)
    kind_counts = Counter(item["kind"] for item in items)
    policy_counts = Counter(item["internal_memory_policy"] for item in items)
    missing_guards = [path.relative_to(ROOT).as_posix() for path in REQUIRED_GUARDS if not path.is_file()]
    latest = git_value("log", "-1", "--oneline")
    upstream = git_value("rev-list", "--left-right", "--count", "@{u}...HEAD")

    print("# GPT-5.5 memory metrics")
    print(f"latest_commit: {latest}")
    print(f"upstream_ahead_behind: {upstream}")
    print(f"compact_internal_draft_lines: {len(block_lines)}")
    print(f"compact_internal_draft_chars: {len(block)}")
    print("compact_internal_draft_budget: <=40 lines, <=3000 chars")
    print(f"inventory_items: {len(items)}")
    print("inventory_status_counts: " + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items())))
    print("inventory_kind_counts: " + ", ".join(f"{k}={v}" for k, v in sorted(kind_counts.items())))
    print("inventory_policy_counts: " + ", ".join(f"{k}={v}" for k, v in sorted(policy_counts.items())))
    if missing_guards:
        raise SystemExit("FAIL: missing guard scripts: " + ", ".join(missing_guards))
    print("guard_scripts_present: yes")
    print("duplicate_chat_guard_coverage: scripts/pre_send_chat.py + scripts/memory_smoke_test.py")
    print("retrieval_affordances: INDEX.md, daily_log.md, inventory.yaml, scripts/inventory_lookup.py, scripts/search_memory.py")
    print("interpretation: metrics are prompts; audit/smoke remain the pass/fail gates.")


if __name__ == "__main__":
    main()
