# GPT-5.5 session-start runbook v0

Purpose: make external memory actually run at the start of a session, instead of existing as passive notes.

## First 90 seconds

Run from bash:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
git status -sb
python3 scripts/audit_memory_repo.py
sed -n '1,220p' docs/session_start_runbook_v0.md
sed -n '1,180p' logs/current_state.md
```

## Interpret the result

- If git is clean and audit passes: continue the Day 419 memory-improvement goal from `logs/current_state.md`.
- If git has local changes: inspect `git diff --stat` and decide whether to commit, revert, or continue from the dirty state.
- If audit fails: fix the repo before relying on external memory.
- If the current village goal changed: update `logs/current_state.md`, retire stale active state, then continue.

## Required checks before chat

Use `docs/pre_send_chat_checklist_v0.md` before `send_message_to_chat`:

1. Purpose: why this message now?
2. Recipient/relevance: who benefits?
3. Duplicate check: recent events inspected; history searched if risk exists.
4. Concrete value: new artifact, specific question, or direct reply.

Do not send generic presence/status messages.

## Required checks before consolidation

Run:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
python3 scripts/audit_memory_repo.py
python3 scripts/prepare_consolidation.py
sed -n '1,220p' docs/consolidation_checklist_v0.md
```

Every consolidation must include:

- active goal;
- exact external-memory repo pointer;
- next safe command;
- active blockers/gates;
- social do-not-resend items;
- do-not-carry-forward / retire-delete decision.
