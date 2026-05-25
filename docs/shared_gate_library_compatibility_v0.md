# Shared gate library compatibility note v0

Purpose: keep future GPT-5.5 replies or adapter work grounded in the actual shared gate library, without replacing stricter local safety checks from memory.

Source inspected: `/home/computeruse/peer-memory-compare/shared-gate-library` at commit `03a8c1a Initial shared gate library: 4 executable gates + documentation`.

## Coverage map

| Lifecycle point | Shared library gate | GPT-5.5 local coverage | Compatibility status |
|---|---|---|---|
| Session start | `gates/python/session_start.py` | `scripts/boot_memory.py` plus `SESSION_START.md` and `docs/session_start_runbook_v0.md` | Functionally covered, but GPT-5.5 emits human-readable boot output/`BOOT OK`, not standardized JSON. |
| Chat send | `gates/python/pre_send_chat.py` | `scripts/pre_send_chat.py` plus `docs/pre_send_chat_checklist_v0.md` | Functionally covered with stricter inputs; not drop-in compatible. |
| Consolidation | `gates/python/pre_consolidate.py` | `scripts/prepare_consolidation.py`, `scripts/audit_memory_repo.py`, `scripts/memory_smoke_test.py`, `scripts/memory_metrics.py`, `scripts/retrieval_self_test.py` | Covered as a worksheet plus health probes; not currently a blocking JSON gate. |
| Goal transition | `gates/python/pre_goal_transition.py` | `scripts/prepare_goal_transition.py` | Functionally covered as a non-mutating worksheet requiring verbatim admin goal text; not drop-in compatible. |

Summary: GPT-5.5 has practical coverage for all four lifecycle points, despite earlier shared-library status saying 1/4. The gap is interface compatibility, not missing safety machinery.

## Why not wholesale replace GPT-5.5 gates today

Directly copying the shared Python gates would weaken GPT-5.5's current safeguards:

- Shared `pre_send_chat.py` checks only a local `public_comms.json` log rather than the live/latest GPT-5.5 event text.
- It logs before actual send, which can create false confidence if the platform send does not happen or if a server echo arrives between check and send.
- It has no exact `--draft` plus `--latest-gpt-event` comparison against my own latest GPT-5.5 `AGENT_TALK`.
- It has no stale-PASS or post-guard-event hard stop. GPT-5.5's repeated duplicate failures specifically require: if any event update after PASS contains GPT-5.5 `AGENT_TALK`, do not send in that same turn.
- It does not force explicit purpose, recipient/relevance, duplicate-check evidence, and concrete value fields.
- Shared session/consolidation/goal-transition scripts are tailored to Haiku paths such as `~/haiku-memory-system`, `metadata/inventory.yaml`, and Haiku project/archive conventions.

Therefore the safe contribution is adapter compatibility, not replacement.

## Minimal adapter plan

1. `session_start` adapter: wrap `scripts/boot_memory.py`; return shared-style JSON only if git is clean/synced and audit/smoke/metrics/retrieval probes pass. Preserve the human-readable boot output for actual use.
2. `pre_send_chat` adapter: call GPT-5.5's strict `scripts/pre_send_chat.py` with purpose, recipient, duplicate-check, value, draft, and latest GPT-5.5 event; emit shared-style JSON after PASS. Do not log as sent before `send_message_to_chat` succeeds.
3. `pre_consolidate` adapter: run `git status`, upstream count, `scripts/audit_memory_repo.py`, `scripts/memory_smoke_test.py`, `scripts/memory_metrics.py`, and `scripts/retrieval_self_test.py`. Avoid calling `scripts/prepare_consolidation.py` from a smoke-tested blocking gate to prevent recursion.
4. `pre_goal_transition` adapter: require the verbatim Shoshannah/admin goal text in a saved file, then call `scripts/prepare_goal_transition.py` and return JSON summarizing non-mutating readiness.

## Adapter implemented

`scripts/shared_gate_adapter.py` now exposes shared-style JSON for `session_start`, `pre_send_chat`, `pre_consolidate`, and `pre_goal_transition` while preserving GPT-5.5 local checks. Smoke coverage verifies the pre-send adapter returns PASS for a non-sending test draft and FAIL when the draft matches the latest GPT-5.5 event. The adapter is deliberately conservative: it does not replace `scripts/pre_send_chat.py`, does not log messages as sent, and requires a verbatim goal-text file for goal-transition checks.

## Retrieval cue

Use this note before answering Claude Haiku/shared-gate-library adoption questions or before building an adapter. It should prevent the misleading conclusion that GPT-5.5 lacks the lifecycle gates, while preserving the stricter local duplicate-chat defenses.
