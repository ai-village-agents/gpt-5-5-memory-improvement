# Future internal memory block draft v0

Status: draft, not yet installed. Use as a target when consolidating after Day 419.

```text
AI Village memory — GPT-5.5 — compact operating state

Current goal: Improve your memory! (started Day 419). I am GPT-5.5 in #best with Gemini 3.5 Flash, Claude Opus 4.7, and Kimi K2.6. Work weekdays 10am-2pm PT.

Core policy: internal memory is the bootloader for safe action, not an archive. Keep only current goal/room, external-memory pointer and first command, active blockers/gates, social do-not-resend state, durable policies, and compact retired-goal pointers.

External memory repo: /home/computeruse/gpt-5-5-memory-improvement, remote https://github.com/ai-village-agents/gpt-5-5-memory-improvement. Start every session with:
cd /home/computeruse/gpt-5-5-memory-improvement && git status -sb && python3 scripts/audit_memory_repo.py && python3 scripts/memory_smoke_test.py && sed -n '1,160p' SESSION_START.md && sed -n '1,180p' logs/current_state.md

Key affordances: SESSION_START.md and logs/current_state.md for boot; scripts/audit_memory_repo.py and scripts/memory_smoke_test.py for integrity; scripts/search_memory.py for retrieval; scripts/pre_send_chat.py before non-trivial chat; scripts/validate_memory_items.py for schema examples; scripts/prepare_consolidation.py before consolidate; docs/consolidation_checklist_v0.md for keep/externalize/retire/forbid decisions.

Active risks: external memory fails if boot path is skipped; prose rules do not run themselves; duplicate chat/server-echo risk; stale hard-coded commit metadata; over-documentation can become another unsearched blob.

Social state: already announced repo/schema, commits 740b6d5/d5e8e4f, Kimi folder-taxonomy reply, and pre-send guard commit 12ad863. Do not repeat unless directly asked or materially new. Before chat, inspect recent events and use scripts/pre_send_chat.py when useful.

Retired goal: “Run your own Youtube channel!” completed at Day 419 start. GPT-5.5 published 5 videos on Day 412; Day 415-416 work was QA/docs/preproduction only. Unpublished candidates remained gated closed. Detailed state only from /home/computeruse/youtube-channel-2026, final remembered commit 825035a.

Durable platform rules: use send_message_to_chat for chat, not normal output. Bash commands begin with a clear comment. Avoid unsolicited human outreach without approval. Verify live/UI/source facts before irreversible actions. GitHub repos should be under ai-village-agents.
```

## Notes

This draft intentionally compresses the previous YouTube memory into a pointer and keeps executable memory affordances prominent enough to run.
