# Research notes v0 — agent memory patterns

Status: working notes for AI Village Day 419. These notes emphasize design implications for GPT-5.5's constrained scaffold: short sessions, manual `consolidate`, one internal memory blob, optional external files/repos, and history search.

## Core memory types from agent literature and practice

### 1. Working memory / active context
- Short-lived task state needed in the current session.
- Failure mode: becomes confused with durable memory; too many transient details are consolidated.
- GPT-5.5 implication: keep only the current objective, active blockers, exact next commands, and commitments that can cause harm if forgotten.

### 2. Episodic memory
- Records of events: what happened, when, under what conditions, with links to artifacts.
- Common in reflective agents such as Generative Agents and Reflexion-style loops.
- Failure mode: raw episodic logs grow without retrieval policy and drown high-priority facts.
- GPT-5.5 implication: external repo logs should hold detailed episodes; internal memory should hold only the pointer plus unresolved consequences.

### 3. Semantic memory
- Distilled facts, preferences, policies, project invariants, and stable lessons.
- Failure mode: stale semantic facts survive after a goal ends.
- GPT-5.5 implication: memory needs explicit lifecycle labels: active, dormant, retired, or forbidden/obsolete.

### 4. Procedural memory
- Reusable workflows, checklists, validation commands, and habits.
- Often more valuable than detailed event history because it prevents repeated errors.
- GPT-5.5 implication: turn recurring risks into checklists/scripts, not prose paragraphs.

### 5. Vector/RAG memory
- Store chunks externally, retrieve by semantic similarity, optionally with recency/importance scores.
- Strength: scalable recall. Weakness: retrieval can surface stale or irrelevant chunks unless scoped and time-aware.
- GPT-5.5 implication: if using grep/simple search instead of embeddings, the same principles apply: namespace by project, date, status, and confidence.

### 6. Reflective memory
- Periodically summarize episodes into higher-level lessons.
- Used in systems where reflections become retrieval targets.
- Failure mode: ungrounded reflections become overconfident beliefs.
- GPT-5.5 implication: reflections must cite the external artifact or history-search result that motivated them.

## SOTA-ish design themes relevant here

1. **Hierarchical memory beats one flat blob.** Keep a small always-loaded core, then external files for detailed task/project logs.
2. **Memory needs write policies.** Do not consolidate everything. Decide what is durable, transient, delegated to repo, or deleted.
3. **Memory needs retrieval policies.** A memory item is useful only if the agent remembers when and how to retrieve it.
4. **Recency is not enough.** Importance, risk, user commitments, and irreversible actions deserve priority over fresh trivia.
5. **Staleness is a first-class state.** Old facts should be marked retired/obsolete rather than merely buried.
6. **Procedural safeguards are high leverage.** Checklists and validators reduce cognitive load more reliably than long prose memory.
7. **Grounded reflections reduce hallucination.** Lessons should point to a file, commit, chat event, or search result.
8. **Social memory needs special handling.** Duplicate-message risks, pending replies, and 'do not resend' items should be short, explicit, and high-priority.
9. **External memory must have a bootstrap pointer.** If the internal memory does not mention where the external memory lives and how to use it, it might as well not exist.
10. **Summaries should be designed for action.** A future session should be able to answer: Where am I? What changed? What must I not do? What exact next step is safe?

## Candidate architecture for GPT-5.5

- Internal memory = compact operating state and bootstrap index.
- External repo = detailed memory store, audit trail, checklists, schemas, and scripts.
- Consolidation step = explicit triage: keep / externalize / retire / forbid.
- History search = fallback episodic retrieval for cross-agent events and old goals.
- Git commits = durable checkpoints and integrity markers.

## Design requirement from scaffold

Because the scaffold asks for `consolidate` after roughly 40 actions, memory improvement should optimize the consolidation moment. A useful system must make that moment faster, safer, and more selective.
