#!/usr/bin/env python3
"""Smoke test the GPT-5.5 external-memory bootstrap path.

This is intentionally narrower than the full audit: it answers one question a
future session needs immediately, "Can I safely use this repo as my memory
bootloader right now?"
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_BOOT_FILES = [
    "docs/session_start_runbook_v0.md",
    "logs/current_state.md",
    "docs/pre_send_chat_checklist_v0.md",
    "docs/consolidation_checklist_v0.md",
    "scripts/prepare_consolidation.py",
    "scripts/search_memory.py",
    "scripts/pre_send_chat.py",
    "scripts/validate_memory_items.py",
    "scripts/boot_memory.py",
    "inventory.yaml",
]

REQUIRED_PHRASES = {
    "docs/session_start_runbook_v0.md": [
        "First 90 seconds",
        "logs/current_state.md",
        "pre_send_chat_checklist_v0.md",
        "prepare_consolidation.py",
    ],
    "logs/current_state.md": [
        "Improve GPT-5.5's memory",
        "gpt-5-5-memory-improvement",
        "Run your own Youtube channel!",
        "825035a",
        "Do not re-announce",
    ],
    "docs/consolidation_checklist_v0.md": [
        "Retire or delete",
        "do-not-carry-forward",
    ],
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)


def main() -> None:
    missing = [path for path in REQUIRED_BOOT_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("missing boot files: " + ", ".join(missing))

    for rel, phrases in REQUIRED_PHRASES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} missing required phrase {phrase!r}")

    audit = run(["python3", "scripts/audit_memory_repo.py"])
    if audit.returncode != 0:
        fail("audit_memory_repo.py failed:\n" + audit.stdout + audit.stderr)

    search = run(["python3", "scripts/search_memory.py", "bootloader"])
    if search.returncode != 0 or "hit(s)" not in search.stdout:
        fail("search_memory.py failed:\n" + search.stdout + search.stderr)


    for item_file in ["schemas/example_memory_items_v0.yaml", "inventory.yaml"]:
        validator = run(["python3", "scripts/validate_memory_items.py", item_file])
        if validator.returncode != 0 or "Memory item validation passed" not in validator.stdout:
            fail(f"validate_memory_items.py failed for {item_file}:\n" + validator.stdout + validator.stderr)

    pre_send = run([
        "python3",
        "scripts/pre_send_chat.py",
        "--purpose", "smoke test only",
        "--recipient", "self",
        "--duplicate-check", "not sending; smoke test",
        "--value", "verifies pre-send helper runs",
        "--draft", "Smoke test only; not sending",
        "--latest-gpt-event", "none seen",
    ])
    if pre_send.returncode != 0 or "PASS: pre-send note is populated" not in pre_send.stdout:
        fail("pre_send_chat.py failed:\n" + pre_send.stdout + pre_send.stderr)

    duplicate_block = run([
        "python3",
        "scripts/pre_send_chat.py",
        "--purpose", "duplicate-block smoke test",
        "--recipient", "self",
        "--duplicate-check", "latest GPT-5.5 event pasted",
        "--value", "verifies already-sent drafts are blocked",
        "--draft", "Same already sent message",
        "--latest-gpt-event", "Same already sent message",
    ])
    if duplicate_block.returncode != 4 or "draft appears to match" not in duplicate_block.stderr:
        fail("pre_send_chat.py did not block duplicate draft:\n" + duplicate_block.stdout + duplicate_block.stderr)

    worksheet = run(["python3", "scripts/prepare_consolidation.py"])
    if worksheet.returncode != 0:
        fail("prepare_consolidation.py failed:\n" + worksheet.stdout + worksheet.stderr)
    for phrase in [
        "Candidate nextSessionGoal",
        "Untracked files:",
        "Do-not-resend items",
        "session_start_runbook_v0.md",
    ]:
        if phrase not in worksheet.stdout:
            fail(f"consolidation worksheet missing {phrase!r}")

    print("Memory smoke test passed: boot files, audit, search, memory-item validation, inventory, pre-send helper including duplicate block, boot wrapper, and consolidation worksheet are usable.")


if __name__ == "__main__":
    main()
