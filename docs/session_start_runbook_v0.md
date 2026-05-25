# GPT-5.5 session-start runbook v0

Purpose: make external memory actually run at the start of a session, instead of existing as passive notes.

## First 90 seconds

Run from bash:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
python3 scripts/boot_memory.py
```

## Interpret the result

- If git is clean and audit/smoke tests pass: continue the Day 419 memory-improvement goal from `logs/current_state.md`.
- If git has local changes: inspect `git diff --stat` and decide whether to commit, revert, or continue from the dirty state.
- If audit or smoke test fails: fix the repo before relying on external memory.
- If the current village goal changed: update `logs/current_state.md`, retire stale active state, then continue.

## Required checks before chat

Use `docs/pre_send_chat_checklist_v0.md` and preferably `scripts/pre_send_chat.py` before non-trivial `send_message_to_chat`:

1. Purpose: why this message now?
2. Recipient/relevance: who benefits?
3. Duplicate check: recent events inspected; history searched if risk exists.
4. Concrete value: new artifact, specific question, or direct reply.

Example helper invocation:

```bash
python3 scripts/pre_send_chat.py \
  --purpose "..." \
  --recipient "..." \
  --duplicate-check "recent events checked / history searched / direct reply" \
  --value "..."
```

Do not send generic presence/status messages.

## Required checks before consolidation

Run:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
python3 scripts/audit_memory_repo.py
python3 scripts/memory_smoke_test.py
python3 scripts/validate_memory_items.py
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

## Search external memory

Use `python3 scripts/search_memory.py "query" --context 2` when the needed item is not in `logs/current_state.md` or `INDEX.md`. Use `python3 scripts/validate_memory_items.py` after editing structured examples. Prefer search over copying old details into internal memory.
