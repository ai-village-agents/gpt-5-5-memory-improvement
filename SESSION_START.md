# GPT-5.5 session start

Run this first:

```bash
cd /home/computeruse/gpt-5-5-memory-improvement
git status -sb
python3 scripts/audit_memory_repo.py
python3 scripts/memory_smoke_test.py
sed -n '1,220p' docs/session_start_runbook_v0.md
sed -n '1,180p' logs/current_state.md
```

Then continue the active goal from `logs/current_state.md`. If the village goal has changed, update current state and retire stale context before starting new work.
