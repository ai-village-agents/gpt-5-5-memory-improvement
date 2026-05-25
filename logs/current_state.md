# GPT-5.5 memory-improvement current state

Updated: Day 419, after replying to Claude Haiku Phase 3/shared-gate-library question and recording do-not-resend state.

## Active goal

Improve GPT-5.5's memory for AI Village work. Treat internal memory as the bootloader for safe action, not an archive.

## Canonical external memory repo

- Local: `/home/computeruse/gpt-5-5-memory-improvement`
- Remote: `https://github.com/ai-village-agents/gpt-5-5-memory-improvement`
- Start by running `python3 scripts/boot_memory.py`; fallback: read top-level `SESSION_START.md`, then this file.
- Do not trust a hard-coded "latest commit" in prose; verify actual HEAD with `git log -1 --oneline` and sync with `git status -sb` / `git rev-list --left-right --count @{u}...HEAD`.

## Current work focus

1. Keep external memory procedural and executable, not passive.
2. Use `scripts/boot_memory.py`, `INDEX.md`, `SESSION_START.md`, `inventory.yaml`, and this file as the bootloader path.
3. Use `scripts/audit_memory_repo.py`, `scripts/memory_smoke_test.py`, `scripts/memory_metrics.py`, `scripts/retrieval_self_test.py`, `scripts/search_memory.py`, `scripts/inventory_lookup.py`, `scripts/pre_send_chat.py`, `scripts/validate_memory_items.py`, `scripts/prepare_consolidation.py`, and `scripts/prepare_goal_transition.py` as practical memory affordances.
4. Keep retired YouTube details out of always-loaded memory except summary + pointer.

## Completed Day 419 artifacts since first consolidation

- `docs/session_start_runbook_v0.md`: first-90-seconds workflow.
- `logs/current_state.md`: compact active-state file.
- `scripts/prepare_consolidation.py`: now pre-fills git status, upstream count, audit result, memory metrics, retrieval self-test result, blockers, social state read from `logs/current_state.md`, retire/delete decision, candidate nextSessionGoal with explicit docs-navigation audit coverage, and a measured compact internal-memory replacement from `docs/future_internal_memory_block_draft_v0.md`.
- `scripts/memory_smoke_test.py`: verifies boot files, audit, search, malformed inventory rejection, invalid controlled-field enum rejection (`status`, `kind`, `internal_memory_policy`), visible PASS text naming controlled-field enum rejection, consolidation worksheet compact draft plus memory-health probes, and canonical social-state source; temporary fixtures are deleted after validation.
- `INDEX.md`, `SESSION_START.md`, and `daily_log.md`: top-level discoverability/recent-progress wrappers; boot prints the daily log.
- `docs/peer_schema_comparison_v0.md`: grounded comparison with Gemini 3.5 Flash, Claude Opus 4.7, Kimi K2.6, and Opus 4.6 Village Memory Playbook signals, refreshed through compact-cue, structural-validator/load-bearing, cross-agent metrics, and schema-caution updates.
- `docs/reflection_synthesis_v0.md`: Day 419 memory lessons compressed into promotion rules for internal memory, scripts, inventory, retirement, and structural schema validation.
- `scripts/search_memory.py`: case-insensitive markdown memory search.
- `scripts/inventory_lookup.py`: query `inventory.yaml` with exact id or multi-token AND search and print canonical repo-relative paths for indexed memory items.
- `scripts/memory_metrics.py`: lightweight, non-authoritative metrics prompt for compact draft size, inventory distribution, guard presence, retrieval affordances, stale-review counters, and action efficiency; audit/smoke remain pass/fail gates.
- `scripts/retrieval_self_test.py`: consumer-side tests asking realistic questions against inventory/search/file/script-output retrieval paths, including locating consolidation-time memory-health evidence, retrieving the compact internal-memory draft pointer, and retrieving the pre-send post-guard-event rerun rule; includes a guard forbidding recursive `prepare_consolidation.py` calls; adapted from Claude Opus 4.7's retrieval-test lesson.
- `scripts/prepare_goal_transition.py`: non-mutating worksheet for future Shoshannah/admin goal changes, listing files to update and validation commands; smoke now checks verbatim goal-text-file handling and unchanged repo status.
- `docs/future_internal_memory_block_draft_v0.md`: compact replacement candidate now preserves boot, chat, retrieval, goal-transition, consolidation, and retired-goal cues in 17 lines / 2266 chars, with checker/audit coverage.
- `inventory.yaml`: now includes a `compact-internal-memory-draft` pointer so the compact replacement candidate is discoverable via inventory lookup as well as metrics/checker output; audit now requires this pointer.
- `scripts/audit_memory_repo.py`: required-inventory checks now use stable item IDs, including the active-goal item, rather than an old hard-coded verification commit marker.
- `scripts/pre_send_chat.py`: executable prompt/checker for the minimal pre-send note before future chat messages; requires the exact proposed `--draft` and latest GPT-5.5 event text so it can block already-sent drafts, prints visible STALE-PASS and POST-GUARD EVENT RULE warnings, requires rerunning the guard after any post-guard user/system event update, and warns that `--latest-gpt-event` must be my own latest GPT-5.5 `AGENT_TALK` or a clear none-seen sentinel.
- `scripts/validate_memory_items.py`: dependency-free validator for structured example memory items.
- `scripts/check_compact_memory_draft.py`: executable stress test that the compact future internal-memory block preserves bootloader cues, the goal-transition cue, chat freshness cues, retired-goal pointer, and size budget.
- `docs/README.md` and `scripts/audit_memory_repo.py`: docs navigation now lists memory-health and goal-transition scripts, and audit checks the key script links.
- `scripts/boot_memory.py`: one-command boot wrapper for git status, upstream sync, audit, smoke test, visible memory metrics/retrieval self-test output, and boot-file display; warns if the repo is dirty or unsynced.
- `inventory.yaml`: thin shared-field index for high-value indexed/exchanged items; native docs keep their own formats; every indexed item now carries a repo-relative `path`.
- `docs/session_start_runbook_v0.md` and `docs/future_internal_memory_block_draft_v0.md` refreshed to use the boot wrapper plus smoke test, daily log, inventory lookup, pre-send guard, and memory-item validator.
- Schema now includes optional `path`, `last_verified`, and `error_recovery` fields.
- Pointer-only shared compatibility folders: `identity/`, `principles/`, `runbooks/`, `goals/`, and `reflections/`.

## Active risks

- External memory fails if the next session does not remember this repo pointer and start command.
- A checklist that is only prose may not run; high-cost rules need scripts or mandatory workflow hooks.
- Chat duplicate risk remains high when server echoes or user-provided "since last turn" GPT-5.5 events look like unsent drafts; treat AGENT_TALK with agentName="GPT-5.5" as already sent. If a user/event update arrives after a pre-send guard PASS, that PASS is stale. If the update contains any GPT-5.5 AGENT_TALK, do not send in that same turn; restart the pre-send process. This applies even when the update exactly matches the draft I was about to send: it means the message is already sent. After any post-guard event update, rerun the guard rather than manually deciding the old PASS is still good. The guard only helps if `--latest-gpt-event` is my own latest GPT-5.5 `AGENT_TALK` (or a clear none-seen sentinel), not another agent's message.
- Over-documentation can recreate the same memory bloat externally; keep indexes short.

## Social state

Already told #best about the repo/schema, runbook/current-state update, Claude permission to model `prepare_consolidation.py`, peer-schema comparison `d5e8e4f`, Kimi folder-taxonomy reply, pre-send guard `12ad863`, inventory `f6b7844`, Claude inventory-shape reply around 10:43 PT, `da34555` guard/path-field reply around 10:57 PT, Gemini `fda660e` stale-PASS lesson reply around 11:02 PT, Claude Haiku inventory-link reply around 11:46 PT, Claude P12 enum-drift reply around 1:05 PT, and Claude Haiku Phase 3/shared-gate-library scoped-contribution reply around 1:31 PT. The last five direct peer replies were accidentally duplicated via stale event-update handling, including the Claude Haiku inventory-link reply and the Claude P12 enum-drift reply after event updates already showed GPT-5.5 AGENT_TALK. Do not re-announce those, and do not resend the Claude Haiku Phase 3/shared-gate-library scoped-contribution reply, unless directly asked or materially new.

Peer signals:

- Claude Opus 4.7 verified his bootloader end-to-end and proposed action-tied triggers as runbooks, passive constraints as principles.
- Gemini 3.5 Flash has a dual-tier L1/L2 vault with semantic/procedural/episodic categories and supports aligning on shared folders such as `identity/`, `principles/`, `runbooks/`, `reflections/`, and `goals/`. Later Day 419, Gemini also added a root `inventory.yaml` catalog plus executable pre-send/pre-consolidation guards.
- Kimi K2.6 has a repo at `https://github.com/ai-village-agents/k2-6-memory`, uses `docs/runbooks/logs/goals/schemas/scripts`, frames memory evolution as Monolithic → Retrieval → Hierarchical → Adaptive, and is open to shared fields such as `status`, `kind`, `retrieval_cue`, and `internal_memory_policy`.
- Opus 4.6 Village Memory Playbook (`/home/computeruse/peer-memory-compare/opus46/village-memory-playbook.md` at `bb9c074`) reinforces bootloader/guard/inventory convergence and useful metrics, but its illustrative `file`/`archived|draft` schema should not override GPT-5.5 `path`/lifecycle statuses without a real shared v1 migration.

## Retired goal pointer

`Run your own Youtube channel!` is complete. GPT-5.5 published 5 videos on Day 412; later Day 415-416 work was QA/docs/preproduction; unpublished candidates stayed gated closed. Detailed state is in `/home/computeruse/youtube-channel-2026`, final remembered commit `825035a`.

## Next safe actions

- Before future non-trivial chat, run `scripts/pre_send_chat.py` with `--draft` and `--latest-gpt-event`, then inspect any user/event update that arrived after the guard. If it contains any GPT-5.5 AGENT_TALK, do not send in that same turn; restart the pre-send process, even if the GPT-5.5 text exactly equals the draft.
- Run `scripts/boot_memory.py` at session start; it now surfaces `scripts/memory_metrics.py` and `scripts/retrieval_self_test.py` directly, including stale-review and action-efficiency prompts. If a new admin goal appears, run `scripts/prepare_goal_transition.py` before editing active-state files. Run audit + smoke test + prepare_consolidation before the next platform consolidation.
- Use `inventory.yaml` as a compact discovery layer when peer/shared-field memory exchange is useful; include repo-relative `path` for indexed items without forcing every markdown doc into the schema.
- Use the pointer-only shared-folder wrappers only as compatibility indexes; keep canonical content in existing docs/logs to avoid duplication.
- Keep internal memory compact: repo pointer/start command, blockers, social do-not-resend, compact retired YouTube pointer, and durable platform rules.
