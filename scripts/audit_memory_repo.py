#!/usr/bin/env python3
"""Lightweight audit for GPT-5.5 memory-improvement repo."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "INDEX.md",
    "SESSION_START.md",
    "inventory.yaml",
    "daily_log.md",
    "docs/README.md",
    "docs/research_notes_v0.md",
    "docs/self_audit_v0.md",
    "docs/memory_operating_manual_v0.md",
    "docs/consolidation_checklist_v0.md",
    "docs/session_start_runbook_v0.md",
    "docs/external_memory_affordances_v0.md",
    "docs/future_internal_memory_block_draft_v0.md",
    "schemas/memory_item_schema_v0.yaml",
    "schemas/example_memory_items_v0.yaml",
    "logs/day419_work_log.md",
    "logs/current_state.md",
    "logs/retired_goals_index.md",
    "scripts/search_memory.py",
    "scripts/boot_memory.py",
    "scripts/inventory_lookup.py",
    "scripts/validate_memory_items.py",
    "scripts/check_compact_memory_draft.py",
    "scripts/memory_metrics.py",
    "scripts/retrieval_self_test.py",
    "scripts/prepare_goal_transition.py",
]
README_DOCS = [
    "research_notes_v0.md",
    "self_audit_v0.md",
    "memory_operating_manual_v0.md",
    "consolidation_checklist_v0.md",
    "session_start_runbook_v0.md",
    "external_memory_affordances_v0.md",
]
FORBIDDEN_PHRASES = [
    "YouTube goal is current",
    "upload-ready",
]

SHARED_WRAPPERS = [
    "identity/README.md",
    "principles/README.md",
    "runbooks/README.md",
    "goals/active.md",
    "goals/archive/README.md",
    "reflections/README.md",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    missing += [p for p in SHARED_WRAPPERS if not (ROOT / p).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    docs_readme = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    for name in README_DOCS:
        if name not in docs_readme:
            fail(f"docs/README.md does not mention {name}")
    for script_name in [
        "scripts/boot_memory.py",
        "scripts/memory_metrics.py",
        "scripts/retrieval_self_test.py",
        "scripts/prepare_goal_transition.py",
    ]:
        if script_name not in docs_readme:
            fail(f"docs/README.md does not mention {script_name}")
    for doc in sorted((ROOT / "docs").glob("*.md")):
        if doc.name == "README.md":
            continue
        if doc.name not in docs_readme:
            fail(f"docs/README.md does not index {doc.name}")


    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required_phrase in ["INDEX.md", "SESSION_START.md", "docs/session_start_runbook_v0.md", "logs/current_state.md", "scripts/search_memory.py", "scripts/boot_memory.py", "scripts/memory_metrics.py", "scripts/retrieval_self_test.py", "scripts/prepare_goal_transition.py", "Internal memory is the bootloader"]:
        if required_phrase not in root_readme:
            fail(f"README.md missing bootstrap phrase {required_phrase!r}")

    runbook = (ROOT / "docs/session_start_runbook_v0.md").read_text(encoding="utf-8")
    for required_phrase in ["First 90 seconds", "pre_send_chat_checklist_v0.md", "prepare_consolidation.py", "do-not-carry-forward"]:
        if required_phrase not in runbook:
            fail(f"session start runbook missing {required_phrase!r}")

    current_state = (ROOT / "logs/current_state.md").read_text(encoding="utf-8")
    for required_phrase in ["Improve GPT-5.5's memory", "gpt-5-5-memory-improvement", "Run your own Youtube channel!", "825035a"]:
        if required_phrase not in current_state:
            fail(f"current_state.md missing {required_phrase!r}")

    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    session_start = (ROOT / "SESSION_START.md").read_text(encoding="utf-8")
    for required_phrase in ["external memory OS", "logs/current_state.md", "schemas/memory_item_schema_v0.yaml", "Shared compatibility folders"]:
        if required_phrase not in index:
            fail(f"INDEX.md missing {required_phrase!r}")
    for required_phrase in ["boot_memory.py", "memory_smoke_test.py", "logs/current_state.md"]:
        if required_phrase not in session_start:
            fail(f"SESSION_START.md missing {required_phrase!r}")

    for rel in SHARED_WRAPPERS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Pointer-only" not in text and "Pointer-only".lower() not in text.lower():
            fail(f"shared wrapper {rel} should be pointer-only")

    schema = (ROOT / "schemas/memory_item_schema_v0.yaml").read_text(encoding="utf-8")
    for required_phrase in ["path", "last_verified", "error_recovery"]:
        if required_phrase not in schema:
            fail(f"schema missing field {required_phrase}")
    for term in ["active", "blocked", "dormant", "retired", "obsolete", "forbidden"]:
        if term not in schema:
            fail(f"schema missing status term {term}")


    examples = (ROOT / "schemas/example_memory_items_v0.yaml").read_text(encoding="utf-8")
    required_example_terms = [
        "id:",
        "created_day:",
        "updated_day:",
        "status:",
        "kind:",
        "summary:",
        "source:",
        "retrieval_cue:",
        "internal_memory_policy:",
        "expiry_or_review:",
    ]
    item_count = examples.count("\n  - id:")
    if item_count < 3:
        fail("example memory items file has too few items")
    for term in required_example_terms:
        if examples.count(term) < item_count:
            fail(f"example memory items missing repeated field {term}")
    allowed_statuses = {"active", "blocked", "dormant", "retired", "obsolete", "forbidden"}
    for line in examples.splitlines():
        stripped = line.strip()
        if stripped.startswith("status:"):
            value = stripped.split(":", 1)[1].strip()
            if value not in allowed_statuses:
                fail(f"example memory item has invalid status {value}")


    for item_file in ["schemas/example_memory_items_v0.yaml", "inventory.yaml"]:
        validator = subprocess.run(["python3", "scripts/validate_memory_items.py", item_file], cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)
        if validator.returncode != 0:
            fail(f"validate_memory_items.py failed for {item_file}:\n" + validator.stdout + validator.stderr)

    compact_check = subprocess.run(["python3", "scripts/check_compact_memory_draft.py"], cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)
    if compact_check.returncode != 0:
        fail("check_compact_memory_draft.py failed:\n" + compact_check.stdout + compact_check.stderr)

    inventory = (ROOT / "inventory.yaml").read_text(encoding="utf-8")
    for required_phrase in ["boot-memory-procedure", "pre-send-chat-guard", "inventory-lookup-procedure", "compact-internal-memory-draft", "retired-youtube-goal-pointer", "memory-metrics-procedure", "retrieval-self-test-procedure", "goal-transition-procedure", "fa22204"]:
        if required_phrase not in inventory:
            fail(f"inventory.yaml missing {required_phrase!r}")
    inventory_item_count = inventory.count("\n  - id:")
    inventory_path_count = inventory.count("\n    path:")
    if inventory_path_count != inventory_item_count:
        fail(f"inventory.yaml should provide path for each indexed item: {inventory_path_count}/{inventory_item_count}")

    daily_log = (ROOT / "daily_log.md").read_text(encoding="utf-8")
    for required_phrase in ["D419", "stale pre-send PASS", "inventory lookup helper"]:
        if required_phrase not in daily_log:
            fail(f"daily_log.md missing {required_phrase!r}")

    retired = (ROOT / "logs/retired_goals_index.md").read_text(encoding="utf-8")
    if "Run your own Youtube channel!" not in retired or "825035a" not in retired:
        fail("retired goals index lacks completed YouTube goal pointer")


    future_block = (ROOT / "docs/future_internal_memory_block_draft_v0.md").read_text(encoding="utf-8")
    for required_phrase in [
        "gpt-5-5-memory-improvement",
        "consolidation_checklist_v0.md",
        "Run your own Youtube channel!",
        "825035a",
        "internal memory is the bootloader",
        "PASS is stale",
    ]:
        if required_phrase not in future_block:
            fail(f"future internal memory block missing {required_phrase!r}")
    code_lines = []
    in_block = False
    for line in future_block.splitlines():
        if line.strip() == "```text":
            in_block = True
            continue
        if line.strip() == "```" and in_block:
            in_block = False
            continue
        if in_block:
            code_lines.append(line)
    code_block = "\n".join(code_lines)
    if len(code_lines) > 40:
        fail(f"future internal memory block too long: {len(code_lines)} lines")
    if len(code_block) > 3000:
        fail(f"future internal memory block too large: {len(code_block)} characters")

    manual = (ROOT / "docs/memory_operating_manual_v0.md").read_text(encoding="utf-8")
    if "Internal memory is not an archive" not in manual:
        fail("operating manual missing core principle")

    checklist = (ROOT / "docs/consolidation_checklist_v0.md").read_text(encoding="utf-8")
    for section in ["Current goal", "Active blockers", "Social/chat", "Retire or delete"]:
        if section.lower() not in checklist.lower():
            fail(f"checklist missing section like {section}")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                fail(f"forbidden phrase {phrase!r} in {path.relative_to(ROOT)}")
        if re.search(r"[ \t]+$", text, flags=re.MULTILINE):
            fail(f"trailing whitespace in {path.relative_to(ROOT)}")

    print("Memory repo audit passed: required files, bootstrap runbook/current state, inventory, indexes, schema terms, memory-item validation, compact draft check and inventory pointer, memory metrics helper, retrieval self-test, retired-goal pointer, and whitespace are consistent.")


if __name__ == "__main__":
    main()
