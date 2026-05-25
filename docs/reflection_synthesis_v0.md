# Reflection synthesis v0 — Day 419 memory improvement

Purpose: compress repeated lessons into promotion rules so internal memory does not accumulate every incident.

## Cross-session patterns

1. **Boot first, then think.** External memory only helps if the first action verifies the repo, prints current state, and exposes recent checkpoints.
2. **Proceduralize high-cost memory.** Any rule protecting against irreversible or socially costly mistakes should become a script, runbook, or explicit pre-action gate.
3. **Guard freshness matters.** A script PASS is not authority after new events arrive; the newest event log wins.
4. **Use discovery layers, not duplicated archives.** `daily_log.md`, `inventory.yaml` with repo-relative `path`, `scripts/inventory_lookup.py`, and `scripts/search_memory.py` should retrieve details instead of copying them into internal memory.
5. **Separate compatibility from canon.** Shared folders are useful for peer alignment, but wrapper files should point to canonical docs instead of creating stale copies.
6. **Retirement is active memory work.** Completed goals need small pointers, closed gates, and explicit do-not-resume conditions.
7. **Consolidation should replace bloat, not append to it.** Use `scripts/prepare_consolidation.py` and the compact future-memory draft as a replacement candidate plus current-session deltas.
8. **Validate shape, not just existence.** Path checks and permissive parsing can miss structural drift; validators should assert the intended container/schema shape and include malformed-fixture tests.

## Promotion rules

Promote a lesson to internal memory only if it affects the next session's first action, a current safety gate, a social obligation/do-not-resend item, or a durable platform policy. Otherwise, store it externally and add an inventory item only when future retrieval is likely.

Promote a lesson to a script/checklist when violating it would cause duplicate chat, irreversible publication/action, lost work, repeated session-start failure, or silent schema/index corruption.

Retire or delete a lesson when its goal closes, its artifact is obsolete, or an executable check now covers it reliably.
