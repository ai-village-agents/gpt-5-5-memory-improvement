#!/usr/bin/env python3
"""Lightweight audit for GPT-5.5 memory-improvement repo."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/README.md",
    "docs/research_notes_v0.md",
    "docs/self_audit_v0.md",
    "docs/memory_operating_manual_v0.md",
    "docs/consolidation_checklist_v0.md",
    "docs/external_memory_affordances_v0.md",
    "schemas/memory_item_schema_v0.yaml",
    "schemas/example_memory_items_v0.yaml",
    "logs/day419_work_log.md",
    "logs/retired_goals_index.md",
]
README_DOCS = [
    "research_notes_v0.md",
    "self_audit_v0.md",
    "memory_operating_manual_v0.md",
    "consolidation_checklist_v0.md",
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

    schema = (ROOT / "schemas/memory_item_schema_v0.yaml").read_text(encoding="utf-8")
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

    print("Memory repo audit passed: required files, indexes, schema terms, retired-goal pointer, and whitespace are consistent.")


if __name__ == "__main__":
    main()
