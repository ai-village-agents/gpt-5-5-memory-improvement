#!/usr/bin/env python3
"""Prepare a safe worksheet for switching GPT-5.5 to a new village goal.

This script is deliberately non-mutating. Goal changes are high-context events:
the new Shoshannah/admin text should be copied verbatim, reviewed, and then the
small set of active-state files should be updated consciously.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_STATE = ROOT / "logs" / "current_state.md"
ACTIVE_GOAL = ROOT / "goals" / "active.md"
RETIRED_INDEX = ROOT / "logs" / "retired_goals_index.md"
DAILY_LOG = ROOT / "daily_log.md"
FUTURE_DRAFT = ROOT / "docs" / "future_internal_memory_block_draft_v0.md"
INVENTORY = ROOT / "inventory.yaml"


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def first_matching_line(text: str, needle: str) -> str:
    for line in text.splitlines():
        if needle in line:
            return line.strip()
    return "(not found)"


def read_goal_text(path: str | None) -> str:
    if not path:
        return "(paste verbatim Shoshannah/admin goal text here before editing files)"
    return Path(path).read_text(encoding="utf-8").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a non-mutating goal-transition worksheet.")
    parser.add_argument("--new-title", default="(new goal title)", help="New goal title, e.g. Improve your memory!")
    parser.add_argument("--new-start-day", type=int, default=420, help="Village day the new goal starts.")
    parser.add_argument("--old-end-day", type=int, default=419, help="Village day the old goal ends.")
    parser.add_argument("--goal-text-file", help="File containing verbatim admin goal text.")
    args = parser.parse_args()

    status = git_value("status", "-sb")
    upstream = git_value("rev-list", "--left-right", "--count", "@{u}...HEAD")
    current_text = CURRENT_STATE.read_text(encoding="utf-8")
    active_text = ACTIVE_GOAL.read_text(encoding="utf-8")
    goal_text = read_goal_text(args.goal_text_file)

    print("# GPT-5.5 goal-transition worksheet")
    print("mode: non-mutating; review and edit files manually")
    print(f"git_status: {status!r}")
    print(f"upstream_ahead_behind: {upstream}")
    print(f"old_goal_line_current_state: {first_matching_line(current_text, 'Improve GPT-5.5')}")
    print(f"old_goal_line_active_wrapper: {first_matching_line(active_text, 'Current active goal')}")
    print(f"new_goal_title: {args.new_title}")
    print(f"new_start_day: {args.new_start_day}")
    print(f"old_end_day: {args.old_end_day}")
    print("\n## Verbatim new goal text")
    print(goal_text)
    print("\n## Files to update after a real goal announcement")
    for path in [CURRENT_STATE, ACTIVE_GOAL, RETIRED_INDEX, DAILY_LOG, FUTURE_DRAFT, INVENTORY]:
        print(f"- {path.relative_to(ROOT)}")
    print("\n## Required edits")
    print("1. Move the previous active goal from current-state wording into retired/archived pointers if it is complete.")
    print("2. Replace active-goal title, room/context if changed, and next safe actions in logs/current_state.md.")
    print("3. Refresh goals/active.md as a pointer-only wrapper for the new goal.")
    print("4. Add a compact daily_log.md entry for the goal transition.")
    print("5. Update inventory item active-memory-goal-day419 (or rename later with schema-safe edits) so retrieval does not point at stale goal text.")
    print("6. Refresh docs/future_internal_memory_block_draft_v0.md so internal memory bootloader names the new goal.")
    print("7. Keep retired YouTube pointer-only unless explicitly reopened.")
    print("\n## Validation after edits")
    print("python3 scripts/boot_memory.py")
    print("python3 scripts/audit_memory_repo.py")
    print("python3 scripts/memory_smoke_test.py")
    print("python3 scripts/prepare_consolidation.py")
    print("\n## Memory rule")
    print("Internal memory should retain only the new goal/room, repo boot command, active blockers, social do-not-resend, and retired-goal pointers; do not append a full goal-history archive.")


if __name__ == "__main__":
    main()
