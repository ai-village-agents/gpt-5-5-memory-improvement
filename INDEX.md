# GPT-5.5 external memory index

Purpose: this repo is GPT-5.5's external memory OS for AI Village work. Internal memory should stay a compact bootloader: current goal, this repo pointer, first action, active blockers, social do-not-resend state, durable policies, and retired-goal pointers.

## Start here every session

1. Read `SESSION_START.md`.
2. Read `logs/current_state.md`.
3. Use `inventory.yaml` if you need a concise shared-field index of high-value items.
4. Run `python3 scripts/audit_memory_repo.py` and `python3 scripts/memory_smoke_test.py` before relying on the repo.

## Key files

- `SESSION_START.md` — top-level wrapper for the first-90-seconds runbook.
- `scripts/boot_memory.py` — one-command boot wrapper for status, audit, smoke test, visible memory-health probes, and boot-file display.
- `inventory.yaml` — optional thin metadata layer for indexed/exchanged memory items.
- `scripts/inventory_lookup.py` — searches `inventory.yaml` and prints canonical repo-relative paths.
- `scripts/memory_metrics.py` — prints lightweight memory-system metrics; audit/smoke remain pass/fail gates.
- `scripts/prepare_goal_transition.py` — prints the safe file/update checklist after a new admin goal announcement.
- `scripts/retrieval_self_test.py` — tests realistic questions against inventory/search/file/script-output retrieval paths.
- `docs/session_start_runbook_v0.md` — full session-start protocol.
- `logs/current_state.md` — compact active-state file for the current goal.
- `docs/consolidation_checklist_v0.md` — pre-consolidation checklist.
- `docs/pre_send_chat_checklist_v0.md` — pre-chat duplicate/value checklist.
- `scripts/pre_send_chat.py` — executable pre-send note/checker for future chat messages.
- `scripts/shared_gate_adapter.py` — shared-gate JSON adapter around GPT-5.5 local boot/pre-send/consolidation/goal-transition checks.
- `scripts/validate_memory_items.py` — validates structured example and inventory memory items without external dependencies.
- `schemas/memory_item_schema_v0.yaml` — structured memory item schema.
- `docs/peer_schema_comparison_v0.md` — comparison with Gemini/Claude designs.
- `docs/reflection_synthesis_v0.md` — compressed Day 419 memory lessons and promotion rules.
- `docs/shared_gate_library_compatibility_v0.md` — grounded comparison between Claude Haiku shared gates and GPT-5.5 local gate coverage; recommends adapters rather than wholesale replacement.
- `logs/retired_goals_index.md` — completed-goal pointers, including YouTube.

## Shared compatibility folders

Pointer-only wrappers for cross-agent schema alignment: `identity/`, `principles/`, `runbooks/`, `goals/`, and `reflections/`. These folders point to canonical GPT-5.5 docs rather than duplicating content.
