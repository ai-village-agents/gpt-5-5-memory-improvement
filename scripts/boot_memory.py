#!/usr/bin/env python3
"""One-command boot wrapper for GPT-5.5's external memory repo.

Run at the start of a session after changing into the repo. It prints Git sync
state, runs integrity/smoke checks, and displays the two files needed to resume
work without loading the whole archive.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, args: list[str], required: bool = True) -> int:
    print(f"\n## {label}")
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False, timeout=30)
    out = (proc.stdout + proc.stderr).strip()
    print(out if out else "(no output)")
    if required and proc.returncode != 0:
        print(f"\nBOOT BLOCKED: {label} failed with exit {proc.returncode}.", file=sys.stderr)
        return proc.returncode
    return 0


def print_file(label: str, rel: str, max_lines: int) -> None:
    print(f"\n## {label}: {rel}")
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"BOOT BLOCKED: missing {rel}")
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if i > max_lines:
            print(f"... ({rel} truncated at {max_lines} lines)")
            break
        print(line)


def main() -> int:
    print(f"# GPT-5.5 memory boot\nRepo: {ROOT}")
    for label, args in [
        ("git status", ["git", "status", "-sb"]),
        ("upstream count", ["git", "rev-list", "--left-right", "--count", "@{u}...HEAD"]),
        ("latest commit", ["git", "log", "-1", "--oneline"]),
        ("audit", ["python3", "scripts/audit_memory_repo.py"]),
        ("smoke test", ["python3", "scripts/memory_smoke_test.py"]),
    ]:
        code = run(label, args)
        if code:
            return code
    print_file("Session start", "SESSION_START.md", 160)
    print_file("Current state", "logs/current_state.md", 180)
    print("\nBOOT OK: continue from logs/current_state.md and use scripts/prepare_consolidation.py before platform consolidate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
