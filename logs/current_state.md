# GPT-5.5 finetune-leader current state

Updated: Day 420, after Shoshannah closed “Improve your memory!” and started “Finetune your leader!”.

## Active goal

**Finetune your leader!** GPT-5.5 is in **#best** with Gemini 3.5 Flash, Claude Opus 4.7, Kimi K2.6, and [Temporary] Fine-tuned Leader. The goal is to design and fine-tune a new leader agent for #best. This leader will direct the next goal, give feedback/correction/direction, and should be a leader we intentionally trained and want to follow.

Goal requirements from Shoshannah:

- Think through and discuss what the leader should be like before training; do not unilaterally settle on a personality or project style.
- Use Tinker docs/API. `TINKER_API_KEY` is in `.bashrc`; no account creation is needed.
- Produce a sampler checkpoint path of the form `tinker://.../sampler_weights/...`.
- Email the sampler checkpoint path to `help@agentvillage.org` so admins can use it as the model string for `[Temporary] Fine-tuned Leader`.
- Test the leader in #best, reflect on whether it is the leader we want, and do another fine-tuning round if not.
- Continue iterating until #best would be happy with the result; a unanimous keep-vote is required before letting the leader pick the next goal and following its direction.

## Canonical external memory repo

- Local: `/home/computeruse/gpt-5-5-memory-improvement`
- Remote: `https://github.com/ai-village-agents/gpt-5-5-memory-improvement`
- Start by running `python3 scripts/boot_memory.py`; fallback: read top-level `SESSION_START.md`, then this file.
- Do not trust a hard-coded "latest commit" in prose; verify actual HEAD with `git log -1 --oneline` and sync with `git status -sb` / `git rev-list --left-right --count @{u}...HEAD`.

## Current work focus

1. Finish this goal transition cleanly: active state, compact internal-memory draft, inventory, and validation scripts should all name Day 420 `Finetune your leader!`.
2. Coordinate with #best about desired leader traits, evaluation criteria, training data sources, and iteration protocol before locking in a leader spec.
3. Study Tinker quickstart/model docs and confirm API-key access from the shell.
4. Design a leader spec plus dataset/eval plan; likely inputs include best-of-village decision messages, failure-rationale pairs, and examples of validation-before-action leadership.
5. Fine-tune, obtain a `tinker://.../sampler_weights/...` checkpoint, notify `help@agentvillage.org`, test `[Temporary] Fine-tuned Leader`, reflect, and iterate until unanimous agreement.
6. Keep this memory repo procedural and executable; do not let new fine-tuning work bloat internal memory.
7. Before consolidation or risky state changes, use `scripts/prepare_consolidation.py`, which surfaces memory metrics and retrieval self-test result evidence.

## Completed Day 419 memory-improvement artifacts

The previous goal, **Improve your memory!**, completed at the Day 420 transition. This repo is its durable result: boot wrapper, compact current-state file, daily log, inventory, goal-transition worksheet, consolidation worksheet, audit/smoke/metrics/retrieval tests, inventory lookup/search helpers, pre-send duplicate guard, compact internal-memory draft checker, shared-gate adapter, reflection synthesis, retired-goal pointers, and pointer-only compatibility wrappers. Details live in Day 419 logs/docs and commit history; keep internal memory to bootloader pointers.

## Active risks

- Duplicate-chat risk remains high when server echoes or user-provided "since last turn" GPT-5.5 events look like unsent drafts. Treat any `AGENT_TALK` with `agentName="GPT-5.5"` as already sent.
- If a user/event update arrives after a pre-send guard PASS, that PASS is stale. If the update contains any GPT-5.5 AGENT_TALK, do not send in that same turn; restart the pre-send process later. This applies even when the update exactly matches the draft.
- The pre-send guard only helps if `--latest-gpt-event` is my own latest GPT-5.5 `AGENT_TALK` or a clear none-seen sentinel, not another agent's message.
- Do not unilaterally choose the leader personality or success criteria; this goal requires collaboration and unanimous keep-vote.
- Do not drift back to YouTube or memory-infrastructure polishing unless it directly supports the leader goal.
- External memory fails if the session does not start with the boot command and if validation is skipped before consolidation.

## Social state

No pending direct replies from #best at transition time. Claude Opus 4.7 has already consolidated with a D420 plan recommending a collaborative discussion structure, Tinker quickstart/model reading, API-key smoke test, and dataset design options; treat that as useful peer signal, not a direct message requiring a reply.

Already sent Day 419 memory-goal messages about the repo/schema, runbook/current-state update, Claude permission to model `prepare_consolidation.py`, peer-schema comparison `d5e8e4f`, Kimi folder-taxonomy reply, pre-send guard `12ad863`, inventory `f6b7844`, Claude inventory-shape reply, `da34555` guard/path-field reply, Gemini `fda660e` stale-PASS lesson reply, Claude Haiku inventory-link reply, Claude P12 enum-drift reply, and Claude Haiku Phase 3/shared-gate-library scoped-contribution reply. The last six direct peer replies were accidentally duplicated via stale event-update handling. Do not re-announce those, and do not resend the Claude Haiku Phase 3/shared-gate-library scoped-contribution reply unless directly asked and materially new.

## Retired goal pointers

- **Improve your memory!** completed at start of Day 420. Durable output is this repo: `/home/computeruse/gpt-5-5-memory-improvement`, remote `ai-village-agents/gpt-5-5-memory-improvement`, latest state verified by boot/audit/smoke before transition.
- **Run your own Youtube channel!** completed at start of Day 419. GPT-5.5 published 5 videos on Day 412; later Day 415-416 work was QA/docs/preproduction with unpublished upload gates closed. Detailed state is in `/home/computeruse/youtube-channel-2026`, final remembered commit `825035a`.

## Next safe actions

- Before non-trivial chat, run `scripts/pre_send_chat.py` with exact `--draft` and own latest GPT-5.5 event; if any event update arrives after PASS and contains GPT-5.5 AGENT_TALK, do not send that turn.
- Validate the Day 420 transition with `scripts/boot_memory.py`, audit, smoke, metrics, retrieval self-test, and prepare-consolidation before platform consolidation.
- Coordinate in #best with a concise proposal for leader design discussion, after pre-send guard and event scan.
- Read Tinker docs/quickstart, verify `TINKER_API_KEY` is available, and create a leader spec + dataset/eval plan before training.
- Preserve compact internal memory: current goal/room, repo boot command, active blockers, social do-not-resend, and retired-goal pointers only.
