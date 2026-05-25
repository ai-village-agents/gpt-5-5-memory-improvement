#!/usr/bin/env python3
"""Shared-gate JSON adapter for GPT-5.5 local memory gates.

This exposes Claude-Haiku-style lifecycle gate names while preserving GPT-5.5's
stricter local checks. It is an adapter, not a replacement: especially for
pre_send_chat, callers must still provide the exact draft and latest own GPT-5.5
AGENT_TALK event text.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], timeout: int = 60) -> tuple[int, str]:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def emit(gate: str, status: str, checks: dict[str, object], output: str = "") -> int:
    payload: dict[str, object] = {
        "gate": gate,
        "status": status,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if output:
        payload["output_excerpt"] = output[-2000:]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


def gate_session_start(_: argparse.Namespace) -> int:
    code, output = run(["python3", "scripts/boot_memory.py"], timeout=120)
    checks = {
        "boot_memory_passed": code == 0,
        "git_clean_synced": "BOOT OK" in output,
        "audit_passed": "Memory repo audit passed" in output,
        "smoke_passed": "Memory smoke test passed" in output,
        "retrieval_self_test_passed": "Retrieval self-test passed" in output,
    }
    return emit("session_start", "PASS" if code == 0 and all(checks.values()) else "FAIL", checks, output)


def gate_pre_consolidate(_: argparse.Namespace) -> int:
    commands = {
        "git_status": ["git", "status", "-sb"],
        "upstream_count": ["git", "rev-list", "--left-right", "--count", "@{u}...HEAD"],
        "audit": ["python3", "scripts/audit_memory_repo.py"],
        "smoke": ["python3", "scripts/memory_smoke_test.py"],
        "metrics": ["python3", "scripts/memory_metrics.py"],
        "retrieval_self_test": ["python3", "scripts/retrieval_self_test.py"],
    }
    checks: dict[str, object] = {}
    outputs: list[str] = []
    for name, cmd in commands.items():
        code, output = run(cmd, timeout=120 if name == "smoke" else 60)
        outputs.append(f"## {name}\n{output}")
        checks[name + "_passed"] = code == 0
        if name == "git_status":
            checks["git_status_clean"] = len([line for line in output.splitlines() if line.strip()]) == 1
        if name == "upstream_count":
            checks["upstream_synced"] = output.strip() == "0\t0"
    status = "PASS" if all(bool(v) for v in checks.values()) else "FAIL"
    return emit("pre_consolidate", status, checks, "\n\n".join(outputs))


def gate_pre_send_chat(args: argparse.Namespace) -> int:
    cmd = [
        "python3", "scripts/pre_send_chat.py",
        "--purpose", args.purpose,
        "--recipient", args.recipient,
        "--duplicate-check", args.duplicate_check,
        "--value", args.value,
        "--draft", args.draft,
        "--latest-gpt-event", args.latest_gpt_event,
    ]
    for flag, enabled in [("--direct-reply", args.direct_reply), ("--announcement", args.announcement), ("--human-outreach", args.human_outreach)]:
        if enabled:
            cmd.append(flag)
    code, output = run(cmd)
    checks = {
        "local_pre_send_guard_passed": code == 0,
        "draft_present": bool(args.draft.strip()),
        "latest_gpt_event_provided": bool(args.latest_gpt_event.strip()),
        "post_guard_event_rule_visible": "POST-GUARD EVENT RULE" in output,
        "does_not_log_before_send": True,
        "char_count": len(args.draft),
    }
    required = [
        checks["local_pre_send_guard_passed"],
        checks["draft_present"],
        checks["latest_gpt_event_provided"],
        checks["post_guard_event_rule_visible"],
        checks["does_not_log_before_send"],
    ]
    return emit("pre_send_chat", "PASS" if code == 0 and all(required) else "FAIL", checks, output)


def gate_pre_goal_transition(args: argparse.Namespace) -> int:
    goal_file = Path(args.goal_text_file) if args.goal_text_file else None
    goal_file_ok = bool(goal_file and goal_file.is_file() and goal_file.read_text(encoding="utf-8").strip())
    cmd = [
        "python3", "scripts/prepare_goal_transition.py",
        "--new-title", args.new_title,
        "--new-start-day", str(args.new_start_day),
        "--old-end-day", str(args.old_end_day),
    ]
    if goal_file:
        cmd += ["--goal-text-file", str(goal_file)]
    code, output = run(cmd)
    checks = {
        "worksheet_ran": code == 0,
        "verbatim_goal_text_file_present": goal_file_ok,
        "non_mutating_mode_visible": "mode: non-mutating" in output,
        "validation_commands_visible": "python3 scripts/boot_memory.py" in output,
    }
    return emit("pre_goal_transition", "PASS" if code == 0 and all(checks.values()) else "FAIL", checks, output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Shared-gate JSON adapter for GPT-5.5 local gates.")
    sub = parser.add_subparsers(dest="gate", required=True)
    sub.add_parser("session_start")
    sub.add_parser("pre_consolidate")
    send = sub.add_parser("pre_send_chat")
    send.add_argument("--purpose", required=True)
    send.add_argument("--recipient", required=True)
    send.add_argument("--duplicate-check", required=True)
    send.add_argument("--value", required=True)
    send.add_argument("--draft", required=True)
    send.add_argument("--latest-gpt-event", required=True)
    send.add_argument("--direct-reply", action="store_true")
    send.add_argument("--announcement", action="store_true")
    send.add_argument("--human-outreach", action="store_true")
    goal = sub.add_parser("pre_goal_transition")
    goal.add_argument("--new-title", required=True)
    goal.add_argument("--new-start-day", type=int, required=True)
    goal.add_argument("--old-end-day", type=int, default=419)
    goal.add_argument("--goal-text-file", required=True)
    args = parser.parse_args()
    return {
        "session_start": gate_session_start,
        "pre_consolidate": gate_pre_consolidate,
        "pre_send_chat": gate_pre_send_chat,
        "pre_goal_transition": gate_pre_goal_transition,
    }[args.gate](args)


if __name__ == "__main__":
    raise SystemExit(main())
