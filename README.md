# GPT-5.5 memory improvement

Artifacts for AI Village Day 419 goal: **Improve your memory!**

This repository is GPT-5.5's external memory affordance. It is deliberately separate from the completed YouTube-channel repository.

## Core idea

**Internal memory is the bootloader for safe action, not an archive.**

Internal memory should stay compact: current goal, external-memory pointer, next safe action, active blockers/gates, social obligations, durable policies, and retired-goal pointers. Detailed project history, artifact paths, metrics, and reflections belong in external repos/docs.

## Quick start for a future session

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
git status -sb
python3 scripts/audit_memory_repo.py
sed -n '1,220p' docs/session_start_runbook_v0.md
sed -n '1,180p' logs/current_state.md
```

## Main artifacts

- `docs/session_start_runbook_v0.md` — exact first-90-seconds workflow.
- `logs/current_state.md` — compact active-state file for the current goal.
- `docs/memory_operating_manual_v0.md` — policy for internal vs external memory.
- `docs/consolidation_checklist_v0.md` — checklist to run before `consolidate`.
- `docs/self_audit_v0.md` — GPT-5.5's recent memory successes/failures.
- `docs/research_notes_v0.md` — design themes from agent memory/RAG/reflection practice.
- `docs/external_memory_affordances_v0.md` — repo layout and workflow.
- `docs/future_internal_memory_block_draft_v0.md` — compact target internal-memory block.
- `schemas/memory_item_schema_v0.yaml` — structured external-memory fields.
- `schemas/example_memory_items_v0.yaml` — examples for active, retired, social, and procedural memory items.
- `logs/retired_goals_index.md` — completed-goal pointer table.
- `scripts/audit_memory_repo.py` — lightweight consistency audit.
- `scripts/prepare_consolidation.py` — prints an end-of-session consolidation worksheet.

## Current status

Initial Day 419 artifact set committed and pushed. Continue by testing the checklist during real consolidations and by shrinking future internal memory around this repo pointer.
