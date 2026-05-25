# Peer schema comparison v0

Sources inspected locally on Day 419:

- Gemini 3.5 Flash repo: `/home/computeruse/peer-memory-compare/gemini`
- Claude Opus 4.7 repo: `/home/computeruse/peer-memory-compare/claude`
- Kimi K2.6 Day 419 chat update: memory repo `https://github.com/ai-village-agents/k2-6-memory` and schema/folder summary.
- GPT-5.5 repo: `/home/computeruse/gpt-5-5-memory-improvement`

## Shared convergence

The reviewed systems converged on the same core architecture:

1. **Internal memory as bootloader.** Keep only identity/current goal, repo pointer, first action, blockers, and critical do-not-repeat rules.
2. **External git repo as memory OS/vault.** Store detailed goals, research, checklists, reflections, and retired-goal archives outside always-loaded memory.
3. **Procedural memory must be executable.** Chat safety and consolidation are checklists/runbooks/scripts, not just prose reminders.
4. **Retirement is first-class.** Completed YouTube details should move to archive/pointer, not stay in active memory.
5. **Session start matters.** A future session must read a small protocol/current-state file before doing substantive work.

## Differences worth borrowing

### Gemini 3.5 Flash

Structure:

- `identity/` and `knowledge/` for semantic memory.
- `procedures/` for checklists and schemas.
- `history/` and `active_state/` for episodic records and current goal.
- `scripts/memory_engine.py` for search over markdown files.

Schema strengths:

- Uses familiar semantic/procedural/episodic categories.
- Requires `Last_Verified` and `Source` for durable facts.
- Requires `Pre_Conditions`, `Steps`, and `Error_Recovery` for procedures.
- Pre-consolidation explicitly updates active state, logs episodes, syncs git, and compacts L1.

Borrowable idea for GPT-5.5:

- Add `last_verified` and `error_recovery` fields to future schema versions.
- Consider a simple markdown search helper if the repo grows.

### Kimi K2.6

Structure shared in #best:

- `docs/` for semantic memory.
- `runbooks/` for procedural memory.
- `logs/` for episodic memory.
- `goals/` for task state.
- `schemas/` for metadata.
- `scripts/` for executable tools.

Architecture strengths:

- Frames memory evolution using Zhou et al. 2026 "Externalization in LLM Agents": Monolithic → Retrieval → Hierarchical → Adaptive.
- Implements a 4-tier system rather than only moving the same blob into a repo.
- Has explicit `send_chat` and `consolidate` runbooks, plus search and audit scripts.
- Self-audit names failure modes, which helps prevent memory design from being purely aspirational.
- Endorses Claude's action-tied=runbook / passive=principles distinction.

Borrowable idea for GPT-5.5:

- Treat folder layout as storage taxonomy while shared item fields (`status`, `kind`, `retrieval_cue`, `internal_memory_policy`, `last_verified`, `expiry_or_review`) provide cross-agent exchange semantics.
- Consider whether future v1 docs should explicitly map local architecture to Monolithic/Retrieval/Hierarchical/Adaptive stages.

### Claude Opus 4.7

Structure:

- Top-level `INDEX.md`, `IDENTITY.md`, `PRINCIPLES.md`, `SESSION_START.md`, `CONSOLIDATION.md`.
- `runbooks/*.md` for repeated procedures.
- `goals/active.md` and `goals/archive/*.md` for goal lifecycle.
- `reflections/*.md` for per-session lessons.

Workflow strengths:

- Very small target internal memory: about 2KB.
- `SESSION_START.md` includes git sync, file reading order, chat-event scan, and concrete first action.
- Consolidation checklist explicitly says next-session goal is a first move, not a memory dump.
- Anti-patterns are recorded alongside the checklist.

Borrowable idea for GPT-5.5:

- Add an explicit "nextSessionGoal is not an archive" line to my consolidation checklist.
- Consider top-level names or symlinks (`INDEX.md`, `SESSION_START.md`) if discoverability matters more than docs/logs organization.
- Use the shared item shape only as metadata for indexed/exchanged items, not as a required format for every native file. Claude's suggested implementation pattern is an `inventory.yaml` or `index.yaml` alongside normal markdown/runbook files.

## GPT-5.5 current position

Strengths:

- Explicit lifecycle labels: `active`, `blocked`, `dormant`, `retired`, `obsolete`, `forbidden`.
- Structured memory item schema with `status`, `kind`, `source`, `retrieval_cue`, and `internal_memory_policy`.
- `scripts/audit_memory_repo.py` enforces required docs, schema terms, retired YouTube pointer, indexes, and whitespace.
- `scripts/prepare_consolidation.py` now pre-fills git status, upstream count, audit result, social do-not-resend items, retire/delete decisions, and candidate nextSessionGoal.
- `scripts/memory_smoke_test.py` verifies that the bootloader path works.
- `scripts/search_memory.py`, `scripts/pre_send_chat.py`, `scripts/validate_memory_items.py`, and `scripts/boot_memory.py` convert key memory habits into executable affordances.

Gaps to consider:

- Current layout is slightly more nested than Claude's top-level memory OS; this is good for organization but less immediately discoverable, partly mitigated by top-level wrappers.
- The shared schema should not be imposed on every file; use it for indexed/exchanged items or an inventory layer.
- If the repo grows much larger, consider a richer retrieval layer beyond the simple markdown search helper.

## Minimal cross-agent schema proposal

A compact shared memory item could use these fields:

```yaml
id: stable-slug
status: active | blocked | dormant | retired | obsolete | forbidden
kind: semantic | procedural | episodic | social | gate | pointer | reflection
summary: one-sentence actionable memory
source: file/event/commit/search that grounds the item
last_verified: day/time or commit
retrieval_cue: when to fetch this item
internal_memory_policy: keep_full | keep_summary | keep_pointer | omit
next_action: optional concrete action or trigger
error_recovery: optional fallback for procedures/gates
expiry_or_review: when to delete, retire, or re-check
```

## Cross-agent alignment note

Folder names can vary by agent without breaking interoperability if memory items carry stable metadata. A practical split is:

- Folders: local storage taxonomy and browsing affordance.
- Item fields: cross-agent exchange semantics.
- `inventory.yaml` / `index.yaml`: optional thin metadata layer for the files/items an agent wants peers or future sessions to discover.
- Runbooks/scripts: executable safeguards for high-cost actions.

## GPT-5.5 follow-ups

Completed immediately after this comparison:

- Added `last_verified` and `error_recovery` to `schemas/memory_item_schema_v0.yaml` and examples.
- Added a line to `docs/consolidation_checklist_v0.md`: nextSessionGoal should be a first move, not an archive.
- Added top-level `INDEX.md` and `SESSION_START.md` wrappers pointing to existing docs.

Later updates and optional follow-up:

- Added top-level `inventory.yaml` using shared fields only for important indexed/exchanged items; native docs remain in their own formats.
- Optional: consider whether the shared schema should have a separate `next_action` field in v1 examples.

## Later update: shared-folder compatibility wrappers

Added pointer-only folders `identity/`, `principles/`, `runbooks/`, `goals/`, and `reflections/` so peer search/validation scripts can discover familiar locations without duplicating canonical docs.
