#!/usr/bin/env python3
"""Pre-send chat guard for GPT-5.5's AI Village memory repo.

This script does not inspect the live village event stream. It forces the agent to
state why a proposed chat message is worth sending and reminds it to check recent
events/search history when duplicate risk exists.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_STATE = ROOT / "logs" / "current_state.md"
CHECKLIST = ROOT / "docs" / "pre_send_chat_checklist_v0.md"


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, flags=re.M | re.S)
    return m.group(1).strip() if m else "(section not found)"


def nonempty(value: str | None) -> bool:
    return bool(value and value.strip() and value.strip() not in {"...", "TODO", "todo"})


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate and validate the minimal pre-send note required before send_message_to_chat."
    )
    parser.add_argument("--purpose", required=True, help="Why send this message now?")
    parser.add_argument("--recipient", required=True, help="Who is it for and why is it relevant to them?")
    parser.add_argument("--duplicate-check", required=True, help="What recent-event/history check was done, or why unnecessary?")
    parser.add_argument("--value", required=True, help="Concrete new value the message adds.")
    parser.add_argument("--direct-reply", action="store_true", help="Set when answering a direct request/question.")
    parser.add_argument("--announcement", action="store_true", help="Set when announcing a repo/status/artifact update.")
    parser.add_argument("--human-outreach", action="store_true", help="Set when message targets humans or human-centered websites.")
    args = parser.parse_args()

    missing = [
        name
        for name, value in [
            ("purpose", args.purpose),
            ("recipient", args.recipient),
            ("duplicate-check", args.duplicate_check),
            ("value", args.value),
        ]
        if not nonempty(value)
    ]

    current = CURRENT_STATE.read_text() if CURRENT_STATE.exists() else ""
    social = section(current, "Social state")

    print("# Pre-send chat note")
    print(f"Purpose: {args.purpose.strip()}")
    print(f"Recipient/relevance: {args.recipient.strip()}")
    print(f"Duplicate check: {args.duplicate_check.strip()}")
    print(f"Concrete value: {args.value.strip()}")
    print()
    print("# Relevant current social state")
    print(social)
    print()
    print("# Required reminders")
    print('- Inspect recent village events before sending; server echoes or user-provided "since last turn" AGENT_TALK events from GPT-5.5 are already-sent messages, not drafts.')
    print("- If duplicate risk remains, use search_history before sending.")
    print("- Do not send generic presence/status messages.")
    if args.announcement:
        print("- Announcement mode: send only once and only for materially new artifacts/findings.")
    if args.human_outreach:
        print("- Human outreach mode: follow approval rules before unsolicited human-centered outreach.")
    if args.direct_reply:
        print("- Direct-reply mode: answer the question concisely and avoid extra announcements.")

    if missing:
        print(f"\nBLOCK: missing required fields: {', '.join(missing)}", file=sys.stderr)
        return 2

    vague_duplicate = args.duplicate_check.strip().lower() in {"not checked", "none", "n/a", "na"}
    if vague_duplicate and not args.direct_reply:
        print("\nBLOCK: duplicate check is too vague for a non-direct reply.", file=sys.stderr)
        return 3

    checklist = CHECKLIST.read_text() if CHECKLIST.exists() else ""
    if "If this cannot be filled, do not send." not in checklist:
        print("\nWARN: canonical checklist phrase not found; inspect docs/pre_send_chat_checklist_v0.md", file=sys.stderr)

    print("\nPASS: pre-send note is populated. Send only if recent events confirm it is non-duplicative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
