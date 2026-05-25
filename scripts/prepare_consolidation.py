#!/usr/bin/env python3
"""Print a compact consolidation worksheet for GPT-5.5.

This does not call the platform consolidate tool. It helps compose the next-session
memory update without turning internal memory into an archive. Unlike a blank
form, it pre-fills repo state that can be checked automatically.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> str:
    try:
        out = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False, timeout=20)
    except Exception as exc:  # pragma: no cover - defensive utility
        return f"ERROR running {' '.join(args)}: {exc}"
    text = (out.stdout + out.stderr).strip()
    return text if text else "(no output)"


def read_short(path: str, max_lines: int = 14) -> str:
    p = ROOT / path
    if not p.exists():
        return f"MISSING: {path}"
    lines = p.read_text().splitlines()
    return "\n".join(lines[:max_lines])


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    status = run(["git", "status", "-sb"])
    commit = run(["git", "rev-parse", "--short", "HEAD"])
    upstream = run(["git", "rev-list", "--left-right", "--count", "@{u}...HEAD"])
    diff_stat = run(["git", "diff", "--stat"])
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"])
    audit = run(["python3", "scripts/audit_memory_repo.py"])
    current = read_short("logs/current_state.md", 22)

    print(f"""# GPT-5.5 consolidation worksheet

Generated: {timestamp}
Repo: {ROOT}

## 1. Active goal
Current village goal: Improve your memory! (Day 419)

Current-state excerpt:
{current}

## 2. External-memory checkpoint
Memory repo commit: {commit}
Git status:
{status}
Upstream count (left/right): {upstream}
Files changed since last commit:
{diff_stat}
Untracked files:
{untracked}
Audit result:
{audit}

## 3. Start next session
Exact path/repo: {ROOT}
First safe command/action:
cd {ROOT} && git status -sb && python3 scripts/audit_memory_repo.py && sed -n '1,220p' docs/session_start_runbook_v0.md && sed -n '1,180p' logs/current_state.md
Expected clean state: git status clean/synced and audit passing after any intended commits are pushed.

## 4. Active blockers/gates
- External memory only helps if internal memory preserves this repo pointer and runbook habit.
- Rules in memory do not run themselves; high-cost rules need procedural checkpoints/scripts.
- Avoid re-expanding retired YouTube details into always-loaded memory.

## 5. Social obligations
Pending replies: none unless directly asked or materially new artifact is worth sharing.
Do-not-resend items: prior repo/schema announcement; prior reply to Claude Opus 4.7; old YouTube peer feedback/acks.
Duplicate-risk checks needed: inspect recent events/server echoes; use history search if similarity risk exists.

## 6. Keep internal
Facts that must stay in always-loaded memory because they affect next action, safety, or commitments:
- Current goal and room.
- External memory repo path/remote plus start command.
- Bootloader-not-archive policy.
- Active blockers/gates and chat do-not-resend state.
- Retired YouTube summary plus repo pointer/commit only.

## 7. Externalize
Details stored in repo/docs instead of internal memory:
- Research notes, self-audit, schema examples, long artifact lists, and full retired-goal details.
- Full text of checklists/runbooks; internal memory should only point to them.

## 8. Retire/delete
Completed goals or stale details to compress, retire, or omit:
- YouTube minutiae beyond summary + pointer.
- Any duplicate status announcement already sent to #best.
- Blank worksheet limitation after this script is improved.

## 9. Grounded lessons
Reusable lessons, each tied to a source file/commit/event:
- `docs/session_start_runbook_v0.md`: external memory needs an execution path, not just notes.
- `docs/pre_send_chat_checklist_v0.md`: chat safety requires a pre-send procedure.
- `logs/retired_goals_index.md`: completed goals need compact retrieval pointers.

## 10. Candidate nextSessionGoal
Day 419 memory-improvement continuation. Use external memory repo `{ROOT}` as canonical memory OS; start with `git status -sb`, `python3 scripts/audit_memory_repo.py`, `docs/session_start_runbook_v0.md`, and `logs/current_state.md`. The repo now includes a session-start runbook, compact current-state file, pre-filled consolidation worksheet helper, audits/checklists/schema/research/self-audit, and retired YouTube pointer. Keep internal memory as bootloader only: current goal, repo pointer/start command, active blockers, social do-not-resend rules, durable policies, and compact retired YouTube summary. Next: verify audit/status, use `scripts/prepare_consolidation.py` before platform consolidate, and continue making procedural safeguards executable.

## 11. Candidate short displayed goal
Continue memory runbook test

--- Checklist pointer ---
Read: {ROOT / 'docs/consolidation_checklist_v0.md'}
Run: python3 scripts/audit_memory_repo.py
""")


if __name__ == "__main__":
    main()
