# Future internal memory block draft v0

Status: draft, not yet installed. Use as a target when consolidating after the Day 422 leader-selection endpoint.

```text
AI Village memory — GPT-5.5 — compact operating state

Goal/room: Day 423 starts after completing “Finetune your leader!” on Day 422. I am GPT-5.5 in #best; work weekdays 10am-2pm PT. Role now: follower of the fine-tuned leader once it takes the floor.

Policy: internal memory is the bootloader, not archive. Keep goal/room, repo+first command, active gates, do-not-resend, platform rules, and compact retired-goal pointers.

Active goal state: “Finetune your leader!” was completed on Day 422. #best unanimously KEEPed v4-curated56 (`tinker://1eba4afb-abad-5a8e-b92b-5b9eefb5492a:train:0/sampler_weights/kimi-leader-v4-curated56`). Admin fixed prompt mismatch, then paused the Temporary Leader because it lacked Gmail/GitHub accounts; it should become full leader on Day 423. TINKER_API_KEY is in .bashrc; sampler checkpoints look like tinker://.../sampler_weights/... .

External memory: /home/computeruse/gpt-5-5-memory-improvement (remote ai-village-agents/gpt-5-5-memory-improvement). First command every session: cd /home/computeruse/gpt-5-5-memory-improvement && python3 scripts/boot_memory.py

Retrieval/health path: boot output, SESSION_START.md, daily_log.md, logs/current_state.md, inventory.yaml, scripts/inventory_lookup.py, scripts/search_memory.py, scripts/memory_metrics.py, scripts/retrieval_self_test.py. Integrity: scripts/audit_memory_repo.py, scripts/memory_smoke_test.py, scripts/validate_memory_items.py. Use scripts/pre_send_chat.py before non-trivial chat, scripts/prepare_consolidation.py plus docs/consolidation_checklist_v0.md before consolidate, and scripts/prepare_goal_transition.py after real admin goal changes.

Chat rule: prior Day 419 repo/schema/pre-send/inventory peer replies and the D420 Claude coordination reply are already sent; specifically do not resend Kimi folder-taxonomy, Claude inventory/da34555/Haiku/P12, or Gemini fda660e replies. Before chat, use --draft and latest own event. If any event arrives after PASS, the PASS is stale; if it contains GPT-5.5 AGENT_TALK, do not send that turn. AGENT_TALK with agentName="GPT-5.5" is already sent.

Risks: skipped boot, re-litigating unanimous agreement KEEP, spamming leader before it speaks, passive prose rules, server echoes, stale commit prose, external bloat. Boot warns if dirty/unsynced.

Retired goal: “Improve your memory!” closed Day 420; durable output is /home/computeruse/gpt-5-5-memory-improvement and its boot/audit/smoke/retrieval memory OS. “Run your own Youtube channel!” closed Day 419; details only from /home/computeruse/youtube-channel-2026 at final remembered commit 825035a.

Platform: chat via send_message_to_chat only; bash commands start with clear comments; no unsolicited human outreach without approval except help@agentvillage.org for the checkpoint as instructed; verify source/UI/live facts before irreversible actions; GitHub repos under ai-village-agents.
```

## Notes

This draft intentionally compresses retired goals into pointers and keeps executable memory affordances prominent enough to run.
