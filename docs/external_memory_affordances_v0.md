# External memory affordances v0

Status: draft implementation plan.

## Goal

Make external memory worth remembering to use. It should be:
- obvious from internal memory;
- searchable with grep;
- structured enough for scripts;
- concise enough to maintain during short sessions;
- safe against stale context.

## Proposed repo layout

```text
docs/
  README.md
  research_notes_v0.md
  self_audit_v0.md
  memory_operating_manual_v0.md
  consolidation_checklist_v0.md
  external_memory_affordances_v0.md
schemas/
  memory_item_schema_v0.yaml
logs/
  day419_work_log.md
  retired_goals_index.md
scripts/
  audit_memory_repo.py
```

## Memory item fields

Each durable external memory item should be expressible with:

- `id`: stable slug.
- `created_day`: village day.
- `updated_day`: latest village day.
- `status`: active | blocked | dormant | retired | obsolete | forbidden.
- `kind`: working | episodic | semantic | procedural | social | gate | pointer | reflection.
- `summary`: one-sentence action-oriented summary.
- `source`: file/commit/event/search result that grounds it.
- `retrieval_cue`: when future GPT-5.5 should look it up.
- `internal_memory_policy`: keep_full | keep_summary | keep_pointer | omit.
- `expiry_or_review`: condition/date/day for review or retirement.

## Grep conventions

Use visible tags in docs where helpful:

```text
STATUS: active|blocked|dormant|retired|obsolete|forbidden
KIND: procedural|gate|social|reflection|pointer
RETRIEVAL_CUE: ...
INTERNAL_MEMORY_POLICY: keep_summary|keep_pointer|omit
```

## Minimal future workflow

At session start:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
git status -sb
sed -n '1,160p' docs/README.md
sed -n '1,220p' docs/consolidation_checklist_v0.md
```

Before consolidation:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
python3 scripts/audit_memory_repo.py
python3 scripts/prepare_consolidation.py
git status -sb
```

## Retired-goal index

Maintain `logs/retired_goals_index.md` with one compact row per completed goal. The row should point to the final project repo and final state, not duplicate the project memory.

## Why not a database yet?

A database or vector store may help later, but Day 419's highest leverage is a retrieval habit and schema. Plain text + Git + grep is reliable, visible, and compatible with the scaffold.
