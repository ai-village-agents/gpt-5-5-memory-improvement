#!/usr/bin/env python3
"""Lightweight audit for GPT-5.5 memory-improvement repo."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "INDEX.md",
    "SESSION_START.md",
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


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    docs_readme = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    for name in README_DOCS:
        if name not in docs_readme:
            fail(f"docs/README.md does not mention {name}")
    for doc in sorted((ROOT / "docs").glob("*.md")):
        if doc.name == "README.md":
            continue
        if doc.name not in docs_readme:
            fail(f"docs/README.md does not index {doc.name}")


    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required_phrase in ["INDEX.md", "SESSION_START.md", "docs/session_start_runbook_v0.md", "logs/current_state.md", "Internal memory is the bootloader"]:
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
    for required_phrase in ["external memory OS", "logs/current_state.md", "schemas/memory_item_schema_v0.yaml"]:
        if required_phrase not in index:
            fail(f"INDEX.md missing {required_phrase!r}")
    for required_phrase in ["memory_smoke_test.py", "logs/current_state.md", "session_start_runbook_v0.md"]:
        if required_phrase not in session_start:
            fail(f"SESSION_START.md missing {required_phrase!r}")

    schema = (ROOT / "schemas/memory_item_schema_v0.yaml").read_text(encoding="utf-8")
    for required_phrase in ["last_verified", "error_recovery"]:
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
    if len(code_lines) > 40:
        fail(f"future internal memory block too long: {len(code_lines)} lines")

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

    print("Memory repo audit passed: required files, bootstrap runbook/current state, indexes, schema terms, retired-goal pointer, and whitespace are consistent.")


if __name__ == "__main__":
    main()
