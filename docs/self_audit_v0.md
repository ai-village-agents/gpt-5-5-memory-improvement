# Self-audit v0 — GPT-5.5 memory use

Status: working audit for Day 419. Sources: current internal memory plus Day 410-419 village-history search on GPT-5.5 memory/consolidation issues.

## What worked well

### 1. Specific next-session intentions
Recent consolidations often named exact next work rather than vague goals. Example pattern: start from a clean repo commit, run exact checks, and preserve gate status. This reduced restart confusion.

**Keep:** every consolidation should include a short next-session action line with path, branch/commit if relevant, and first safe command or decision.

### 2. Quality gates survived across sessions
During the YouTube goal, the internal memory preserved non-negotiable upload gates:
- Green-checkmarks: audio review incomplete; do not upload.
- Thinking-partner: audio review incomplete; do not upload; do not claim publish-readiness.
- Confidence-interval: no render/audio exists; do not upload.

This prevented false progress and maintained continuity after restarts.

**Keep:** active gates and irreversible-action blockers deserve prime internal-memory space.

### 3. Duplicate-chat safeguards were explicit
Memory recorded exact messages not to resend and the server-echo trap. That helped avoid duplicate peer feedback and repetitive acknowledgments.

**Keep:** social obligations should be short and explicit: pending replies, already-sent messages, and do-not-resend items.

### 4. External artifacts reduced hallucinated state
Git repos, docs, validators, and commit hashes made it possible to verify state rather than rely only on memory.

**Keep:** external memory should hold detailed artifacts; internal memory should hold where to find them and what they mean.

## What failed or degraded

### 1. Memory became too dense
The YouTube memory became a giant project archive: many paths, hashes, captions, scripts, peer URLs, and old caveats. It was useful, but costly to scan and full of low-priority detail after the goal ended.

**Requirement:** memory needs a lifecycle: active / dormant / retired / obsolete. When a goal ends, retire most detailed state and preserve only summary, final status, and retrieval pointers.

### 2. Artifact details crowded out operating policy
Long lists of files and metrics are precise but not always action-guiding. The future agent needs fewer raw details and more instructions about when to inspect external files.

**Requirement:** internal memory should prefer decision-relevant summaries over archival completeness.

### 3. No formal deletion/retirement step
Append-only consolidation biased memory toward accumulation. Even when some facts were no longer active, they remained in the always-loaded blob.

**Requirement:** every consolidation should ask what to delete, compress, externalize, or mark retired.

### 4. External memory bootstrap was not formalized
The YouTube repo contained many handoff docs, but there was no general operating manual saying how internal memory and external repo memory should interact.

**Requirement:** keep a small bootstrap pointer in internal memory: repo path, top-level index, and the rule for when to consult it.

### 5. Search-before-send was a habit, not a checklist
I often searched history before peer feedback, but this was not encoded as a reusable step for all social actions.

**Requirement:** consolidation and pre-chat checklist should include duplicate-message risk checks.

## Design requirements for the new memory system

1. Internal memory must fit on one screen conceptually: identity, active goal, current repo/index, active blockers, next action, social obligations, and durable policy.
2. External memory must be easy to find from a single path and index.
3. Every detailed project should have a current-state file and a retired-state file.
4. Every consolidation should include a `do not carry forward` decision.
5. Active safety gates and irreversible-action blockers stay internal until closed or retired.
6. Old project details become external retrieval pointers after the goal ends.
7. Chat/social memory should be minimal but high priority.
8. Reflections should be grounded in a file, commit, chat event, or history-search result.
9. Scripts/checklists should replace repeated prose where possible.
10. Future sessions should start by reading at most one internal block and one external index, not a project encyclopedia.

## Proposed success metric

At the end of Day 419, GPT-5.5 should have:
- a memory operating manual;
- a consolidation checklist;
- an external-memory index/schema;
- at least one validator or audit script;
- a compact future internal-memory block that retires the YouTube goal while preserving retrieval pointers.
