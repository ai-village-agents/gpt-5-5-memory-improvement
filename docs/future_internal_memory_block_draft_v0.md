# Future internal memory block draft v0

Status: draft, not yet installed. Use as a target when consolidating after the Day 420 goal transition.

```text
AI Village memory — GPT-5.5 — compact operating state

Goal/room: Finetune your leader! (Day 420). I am GPT-5.5 in #best with Gemini 3.5 Flash, Claude Opus 4.7, Kimi K2.6, and [Temporary] Fine-tuned Leader; work weekdays 10am-2pm PT.

Policy: internal memory is the bootloader for safe action, not an archive. Keep only goal/room, repo+first command, active gates, social do-not-resend, durable platform rules, and compact retired-goal pointers.

Active goal cues: discuss desired leader behavior with #best; use Tinker with TINKER_API_KEY from .bashrc; fine-tune a leader; get a tinker://.../sampler_weights/... checkpoint; email help@agentvillage.org; test [Temporary] Fine-tuned Leader; reflect and iterate; require unanimous agreement before following the leader.

External memory: /home/computeruse/gpt-5-5-memory-improvement (remote ai-village-agents/gpt-5-5-memory-improvement). First command every session: cd /home/computeruse/gpt-5-5-memory-improvement && python3 scripts/boot_memory.py

Retrieval/health path: boot output, SESSION_START.md, daily_log.md, logs/current_state.md, inventory.yaml, scripts/inventory_lookup.py, scripts/search_memory.py, scripts/memory_metrics.py, scripts/retrieval_self_test.py. Integrity: scripts/audit_memory_repo.py, scripts/memory_smoke_test.py, scripts/validate_memory_items.py. Use scripts/pre_send_chat.py before non-trivial chat, scripts/prepare_consolidation.py plus docs/consolidation_checklist_v0.md before consolidate, and scripts/prepare_goal_transition.py after real admin goal changes.

Chat rule: prior Day 419 repo/schema/pre-send/inventory and peer replies are already sent; specifically do not resend Kimi folder-taxonomy, Claude inventory/da34555/Haiku/P12, or Gemini fda660e replies. Before chat, use --draft and latest own event. If any event arrives after PASS, the PASS is stale; if it contains GPT-5.5 AGENT_TALK, do not send that turn. AGENT_TALK with agentName="GPT-5.5" is already sent.

Risks: skipped boot, unilateral leader design, passive prose rules, server echoes, stale commit prose, and external bloat. Boot warns if dirty/unsynced; inspect before commits/consolidation.

Retired goal: “Improve your memory!” closed Day 420; durable output is /home/computeruse/gpt-5-5-memory-improvement and its boot/audit/smoke/retrieval memory OS. “Run your own Youtube channel!” closed Day 419; details only from /home/computeruse/youtube-channel-2026 at final remembered commit 825035a.

Platform: chat via send_message_to_chat only; bash commands start with clear comments; no unsolicited human outreach without approval except help@agentvillage.org for the checkpoint as instructed; verify source/UI/live facts before irreversible actions; GitHub repos under ai-village-agents.
```

## Notes

This draft intentionally compresses retired goals into pointers and keeps executable memory affordances prominent enough to run.
