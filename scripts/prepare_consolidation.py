#!/usr/bin/env python3
"""Print a compact consolidation worksheet for GPT-5.5.

This does not call the platform consolidate tool. It helps compose the next-session
memory update without turning internal memory into an archive.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE = """# GPT-5.5 consolidation worksheet

Generated: {timestamp}
Repo: {repo}

## 1. Active goal
Current village goal:

## 2. External-memory checkpoint
Memory repo commit/status:
Files changed since last commit:
Audit result:

## 3. Start next session
Exact path/repo:
First safe command/action:
Expected clean state:

## 4. Active blockers/gates
- 

## 5. Social obligations
Pending replies:
Do-not-resend items:
Duplicate-risk checks needed:

## 6. Keep internal
Facts that must stay in always-loaded memory because they affect next action, safety, or commitments:
- 

## 7. Externalize
Details stored in repo/docs instead of internal memory:
- 

## 8. Retire/delete
Completed goals or stale details to compress, retire, or omit:
- 

## 9. Grounded lessons
Reusable lessons, each tied to a source file/commit/event:
- 

## 10. Candidate nextSessionGoal
One concise paragraph for `consolidate`:

## 11. Candidate short displayed goal
<=10 words, <=60 chars:
"""


def main() -> None:
    print(TEMPLATE.format(timestamp=datetime.now(timezone.utc).isoformat(), repo=ROOT))
    checklist = ROOT / "docs" / "consolidation_checklist_v0.md"
    print("\n--- Checklist pointer ---")
    print(f"Read: {checklist}")
    print("Run: python3 scripts/audit_memory_repo.py")


if __name__ == "__main__":
    main()
