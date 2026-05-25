#!/usr/bin/env python3
"""Check that the compact internal-memory draft preserves load-bearing cues."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "docs/future_internal_memory_block_draft_v0.md"
REQUIRED_CUES = [
    "Improve your memory!",
    "#best",
    "gpt-5-5-memory-improvement",
    "python3 scripts/boot_memory.py",
    "daily_log.md",
    "logs/current_state.md",
    "inventory.yaml",
    "scripts/inventory_lookup.py",
    "scripts/pre_send_chat.py",
    "scripts/prepare_consolidation.py",
    "PASS is stale",
    "GPT-5.5 AGENT_TALK",
    "Gemini fda660e",
    "Run your own Youtube channel!",
    "/home/computeruse/youtube-channel-2026",
    "825035a",
]
FORBIDDEN_CUES = [
    "youtu.be/",
    "upload-ready",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def extract_text_blocks(text: str) -> list[str]:
    pattern = re.compile(r"```text\n(.*?)\n```", re.DOTALL)
    return pattern.findall(text)


def main() -> None:
    if not DRAFT.is_file():
        fail(f"missing draft file: {DRAFT.relative_to(ROOT)}")
    text = DRAFT.read_text(encoding="utf-8")
    blocks = extract_text_blocks(text)
    if len(blocks) != 1:
        fail(f"expected exactly one fenced text block, found {len(blocks)}")
    block = blocks[0]
    lines = block.splitlines()
    if len(lines) > 40:
        fail(f"compact memory draft too long: {len(lines)} lines")
    if len(block) > 3000:
        fail(f"compact memory draft too large: {len(block)} characters")
    for cue in REQUIRED_CUES:
        if cue not in block:
            fail(f"compact memory draft missing cue {cue!r}")
    for cue in FORBIDDEN_CUES:
        if cue in block:
            fail(f"compact memory draft contains forbidden cue {cue!r}")
    print("Compact memory draft check passed: bootloader cues, chat freshness cues, retired-goal pointer, and size budget are intact.")


if __name__ == "__main__":
    main()
