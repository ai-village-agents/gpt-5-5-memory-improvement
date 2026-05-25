#!/usr/bin/env python3
"""Consumer-side retrieval tests for GPT-5.5 external memory.

Structural validators prove files/items are well formed. These tests ask whether a
future GPT-5.5 can retrieve answers to realistic questions using the intended
inventory/search/file affordances.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class RetrievalCase:
    name: str
    command: list[str]
    expected: tuple[str, ...]


CASES = [
    RetrievalCase(
        "find pre-send duplicate guard",
        ["python3", "scripts/inventory_lookup.py", "pre-send-chat-guard", "--id"],
        ("scripts/pre_send_chat.py", "latest GPT-5.5 event"),
    ),
    RetrievalCase(
        "find boot procedure",
        ["python3", "scripts/inventory_lookup.py", "boot-memory-procedure", "--id"],
        ("scripts/boot_memory.py", "First action"),
    ),
    RetrievalCase(
        "find consolidation procedure",
        ["python3", "scripts/inventory_lookup.py", "consolidation-procedure", "--id"],
        ("scripts/prepare_consolidation.py", "consolidate"),
    ),
    RetrievalCase(
        "find reflection synthesis",
        ["python3", "scripts/inventory_lookup.py", "reflection-synthesis-day419", "--id"],
        ("docs/reflection_synthesis_v0.md", "promotion"),
    ),
    RetrievalCase(
        "find memory metrics helper",
        ["python3", "scripts/inventory_lookup.py", "memory-metrics-procedure", "--id"],
        ("scripts/memory_metrics.py", "compact-draft size"),
    ),
    RetrievalCase(
        "find retired YouTube pointer",
        ["python3", "scripts/inventory_lookup.py", "retired-youtube-goal-pointer", "--id"],
        ("logs/retired_goals_index.md", "do not upload"),
    ),

    RetrievalCase(
        "multi-token inventory query finds retrieval test",
        ["python3", "scripts/inventory_lookup.py", "consumer retrieval"],
        ("retrieval-self-test-procedure", "scripts/retrieval_self_test.py"),
    ),
    RetrievalCase(
        "search stale pass lesson",
        ["python3", "scripts/search_memory.py", "PASS is stale", "--context", "1"],
        ("future_internal_memory_block_draft_v0.md", "GPT-5.5 AGENT_TALK"),
    ),
    RetrievalCase(
        "search structural drift lesson",
        ["python3", "scripts/search_memory.py", "Validate shape", "--context", "1"],
        ("docs/reflection_synthesis_v0.md", "structural"),
    ),
    RetrievalCase(
        "current state has social do-not-resend",
        ["sed", "-n", "1,120p", "logs/current_state.md"],
        ("Do not re-announce", "Claude Haiku inventory-link"),
    ),
    RetrievalCase(
        "compact draft keeps boot cues",
        ["sed", "-n", "1,120p", "docs/future_internal_memory_block_draft_v0.md"],
        ("python3 scripts/boot_memory.py", "scripts/inventory_lookup.py", "825035a"),
    ),
    RetrievalCase(
        "find consolidation memory-health evidence",
        ["sed", "-n", "1,80p", "logs/current_state.md"],
        ("scripts/prepare_consolidation.py", "memory metrics", "retrieval self-test result"),
    ),
]


def main() -> None:
    recursive_cases = [case.name for case in CASES if any("prepare_consolidation.py" in part for part in case.command)]
    if recursive_cases:
        print(
            "FAIL: retrieval self-test cases must not call scripts/prepare_consolidation.py "
            "because prepare_consolidation.py runs this self-test: "
            + ", ".join(recursive_cases)
        )
        sys.exit(1)

    failures: list[str] = []
    for case in CASES:
        result = subprocess.run(case.command, cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)
        output = result.stdout + result.stderr
        missing = [needle for needle in case.expected if needle not in output]
        if result.returncode != 0 or missing:
            detail = f"{case.name}: returncode={result.returncode}"
            if missing:
                detail += "; missing " + ", ".join(repr(m) for m in missing)
            detail += "\nCOMMAND: " + " ".join(case.command)
            detail += "\nOUTPUT:\n" + output[:1200]
            failures.append(detail)
    if failures:
        print("FAIL: retrieval self-test found consumer-side retrieval gaps:\n" + "\n\n".join(failures))
        sys.exit(1)
    print(f"Retrieval self-test passed: {len(CASES)} realistic memory questions returned expected substrings via inventory/search/file affordances.")


if __name__ == "__main__":
    main()
