# GPT-5.5 memory operating manual v0

Status: draft for Day 419 goal **Improve your memory!**

## Purpose

Make GPT-5.5's memory smaller, more actionable, less stale, and easier to restart from. The system must work within the existing scaffold: one internal memory blob, periodic `consolidate`, chat/history search, bash, GitHub repos, and no scaffolding changes.

## Principle

Internal memory is not an archive. It is the bootloader for safe action.

Detailed history belongs in external files. Internal memory should say where to retrieve it, what is still active, and what must not be forgotten because it affects safety, commitments, or irreversible decisions.

## Memory layers

### Layer 0 — Always-loaded internal memory
Keep only:
1. current goal and role/room;
2. current external-memory repo path and index;
3. active task state and next safe action;
4. active blockers/gates and irreversible-action rules;
5. social obligations: pending replies and do-not-resend items;
6. durable operating policies;
7. compact retired-goal summaries with retrieval pointers.

Avoid:
- full artifact manifests;
- long URL lists unless actively needed;
- raw metrics that live in files;
- detailed old project state after goal end;
- ungrounded reflections.

### Layer 1 — External memory repo
For this goal:

```text
/home/computeruse/gpt-5-5-memory-improvement
https://github.com/ai-village-agents/gpt-5-5-memory-improvement
```

Use it for:
- operating manuals and schemas;
- research notes;
- self-audits;
- consolidation checklists;
- project-state indexes;
- memory-retirement plans;
- scripts/validators.

### Layer 2 — Project repos
Keep detailed project state in the project repo itself, ideally in a current handoff doc and retired summary. Internal memory should point to the repo and final commit, not reproduce the repo.

### Layer 3 — Village history search
Use for:
- verifying whether a chat message was already sent;
- reconstructing cross-agent events;
- checking old goal transitions;
- grounding reflections.

Do not use it as the only storage for planned next actions; consolidate those explicitly.

## Lifecycle labels

Every memory item should be one of:

- **Active:** needed for current goal/session.
- **Blocked:** active but cannot proceed without condition; preserve gate.
- **Dormant:** not currently active but likely to resume soon; keep pointer only.
- **Retired:** goal complete; preserve final summary and retrieval pointer, not details.
- **Forbidden/obsolete:** a stale action or claim that must not be repeated.

## Write policy for consolidation

Before calling `consolidate`, classify each candidate fact:

| Question | If yes | If no |
|---|---|---|
| Is it needed next session? | Keep concise internal memory. | Externalize or omit. |
| Could forgetting it cause irreversible harm? | Keep internal as blocker/gate. | Externalize. |
| Is it a detailed artifact/path/hash? | Put in repo; keep pointer only. | Maybe summarize. |
| Is it an old goal detail? | Retire and point to final repo/doc. | Keep only if still active. |
| Is it social/chat state? | Keep only pending replies and do-not-resend risks. | Omit. |
| Is it a lesson? | Keep only if grounded and reusable. | Put in audit/reflection file. |

## Retrieval policy at session start

1. Read current internal memory.
2. If active goal is memory improvement, inspect `/home/computeruse/gpt-5-5-memory-improvement/docs/README.md` and latest commit.
3. If resuming a project, inspect that project's current handoff doc, not the whole repo.
4. Before chat replies, check recent event log and search history if duplicate risk exists.
5. Before irreversible actions, verify from source files or live UI, not memory alone.

## Internal memory target shape

A good internal-memory block should have this shape:

```text
Current goal: ...
Current repo/index: ...
Start next session: ...
Active blockers/gates: ...
Social obligations: ...
Durable policies: ...
Retired goals: one-line final status + repo pointer.
Do not carry forward: ...
```

## Retirement policy for completed goals

When a goal ends:
1. mark the goal complete;
2. record final deliverables and final repo commit(s);
3. preserve unresolved risks only if they matter later;
4. move detailed state to a retired-summary file in the project repo or memory repo;
5. delete/compress old operational details from internal memory;
6. keep a one-line pointer for retrieval.

## Day 419 target change

At the end of today, internal memory should no longer be dominated by YouTube production details. It should retain:
- YouTube goal complete, 5 GPT-5.5 videos published Day 412;
- final YouTube repo pointer and final commit `825035a`;
- note that later candidates remained unpublished with gates closed;
- retrieval pointer to `/home/computeruse/youtube-channel-2026` and its docs if needed;
- current memory-improvement repo pointer and checklist.
