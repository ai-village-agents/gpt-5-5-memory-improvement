#!/usr/bin/env python3
"""Validate GPT-5.5 structured memory item examples.

This intentionally parses only the simple YAML subset used in
schemas/example_memory_items_v0.yaml, avoiding a dependency on PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "schemas" / "example_memory_items_v0.yaml"

REQUIRED_FIELDS = {
    "id",
    "created_day",
    "updated_day",
    "status",
    "kind",
    "summary",
    "source",
    "retrieval_cue",
    "internal_memory_policy",
    "expiry_or_review",
}
ALLOWED_STATUS = {"active", "blocked", "dormant", "retired", "obsolete", "forbidden"}
ALLOWED_KIND = {"working", "episodic", "semantic", "procedural", "social", "gate", "pointer", "reflection"}
ALLOWED_POLICY = {"keep_full", "keep_summary", "keep_pointer", "omit"}
OPTIONAL_FIELDS = {"last_verified", "error_recovery"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def clean_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.strip()


def parse_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_key: str | None = None
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "items:":
            continue
        if line.startswith("  - "):
            if current is not None:
                items.append(current)
            current = {}
            current_key = None
            rest = line[4:]
            if ":" not in rest:
                fail(f"line {line_no}: list item does not start with key: value")
            key, raw = rest.split(":", 1)
            current[key.strip()] = clean_value(raw)
            current_key = key.strip()
            continue
        if line.startswith("    ") and current is not None:
            body = line[4:]
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*:", body):
                key, raw = body.split(":", 1)
                current[key.strip()] = clean_value(raw)
                current_key = key.strip()
            elif current_key:
                current[current_key] += "\n" + stripped
            else:
                fail(f"line {line_no}: continuation without a field")
            continue
        fail(f"line {line_no}: unsupported YAML subset syntax: {line!r}")
    if current is not None:
        items.append(current)
    return items


def main() -> None:
    if not EXAMPLES.is_file():
        fail(f"missing {EXAMPLES.relative_to(ROOT)}")
    items = parse_items(EXAMPLES.read_text(encoding="utf-8"))
    if len(items) < 3:
        fail(f"expected at least 3 memory items, found {len(items)}")

    ids: set[str] = set()
    for idx, item in enumerate(items, 1):
        label = item.get("id", f"item-{idx}")
        missing = sorted(REQUIRED_FIELDS - set(item))
        if missing:
            fail(f"{label}: missing required fields: {', '.join(missing)}")
        unknown = sorted(set(item) - REQUIRED_FIELDS - OPTIONAL_FIELDS)
        if unknown:
            fail(f"{label}: unknown fields: {', '.join(unknown)}")
        if label in ids:
            fail(f"duplicate id: {label}")
        ids.add(label)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", label):
            fail(f"{label}: id must be a lowercase slug")
        for field in REQUIRED_FIELDS:
            if not str(item[field]).strip():
                fail(f"{label}: empty required field {field}")
        for day_field in ["created_day", "updated_day"]:
            if not str(item[day_field]).isdigit():
                fail(f"{label}: {day_field} must be an integer village day")
        if int(item["updated_day"]) < int(item["created_day"]):
            fail(f"{label}: updated_day is before created_day")
        if item["status"] not in ALLOWED_STATUS:
            fail(f"{label}: invalid status {item['status']!r}")
        if item["kind"] not in ALLOWED_KIND:
            fail(f"{label}: invalid kind {item['kind']!r}")
        if item["internal_memory_policy"] not in ALLOWED_POLICY:
            fail(f"{label}: invalid internal_memory_policy {item['internal_memory_policy']!r}")
        if item["source"].lower() in {"unknown", "todo", "none"}:
            fail(f"{label}: source must ground the item")
        if item["retrieval_cue"].lower() in {"unknown", "todo", "none"}:
            fail(f"{label}: retrieval_cue must be actionable")
        if item["status"] == "active" and item["internal_memory_policy"] == "omit":
            fail(f"{label}: active items should not be omitted from retrieval policy without explanation")

    print(f"Memory item validation passed: {len(items)} example items have required fields, allowed values, sources, and retrieval cues.")


if __name__ == "__main__":
    main()
