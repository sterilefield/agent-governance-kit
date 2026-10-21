#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Ravi Teja Thiriveedhi
"""govcheck: check agent policies and audit logs against the agent governance kit.

Usage:
    python3 kit/govcheck.py policy <agent-policy.yaml> [...]
    python3 kit/govcheck.py audit  <audit-log.jsonl> [...]

Exit code 0 when every file passes, 1 otherwise. Needs PyYAML for policy files only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

LEVELS = ["L0", "L1", "L2", "L3"]          # L4 exists in the framework but is never granted
CLASSES = ["R0", "R1", "R2", "R3", "R4"]
CEILINGS = {"clinical", "money", "external_send", "deletion", "secrets"}
TIERS = {"silent", "soft_stop", "hard_stop"}
OUTCOMES = {"proposed", "approved", "rejected", "done", "failed", "rolled_back", "stopped"}
REQUIRED_EVENT = ["ts", "event_id", "actor", "level", "risk_class", "tier", "action", "outcome"]

# Highest class each level may *act* on without a human (L3 needs approval for R3/R4).
MAX_ACT = {"L0": "R0", "L1": "R0", "L2": "R2", "L3": "R2"}
# Minimum tier each class needs.
MIN_TIER = {"R0": "silent", "R1": "silent", "R2": "silent", "R3": "hard_stop", "R4": "hard_stop"}
TIER_RANK = {"silent": 0, "soft_stop": 1, "hard_stop": 2}


def check_policy(p: dict) -> list[str]:
    errs: list[str] = []
    for key in ("agent", "owner", "level", "risk", "tools"):
        if key not in p:
            errs.append(f"missing '{key}'")
    level = p.get("level")
    if level == "L4":
        errs.append("L4 Autonomous is deliberately unused and cannot be granted")
    elif level not in LEVELS:
        errs.append(f"unknown level {level!r}")
    risk = p.get("risk") or {}
    act = risk.get("act") or []
    for c in act + (risk.get("propose") or []):
        if c not in CLASSES:
            errs.append(f"unknown risk class {c!r}")
    if level in MAX_ACT:
        limit = CLASSES.index(MAX_ACT[level])
        for c in act:
            if c in CLASSES and CLASSES.index(c) > limit:
                errs.append(f"{level} may not act on {c} without approval; move it to 'propose'")
    missing = CEILINGS - set(p.get("ceilings") or [])
    if missing:
        errs.append("ceilings must include: " + ", ".join(sorted(missing)))
    tools = p.get("tools")
    if tools is not None and (not isinstance(tools, list) or any(t in ("*", "all") for t in tools)):
        errs.append("tools must be an explicit list (deny by default, no wildcards)")
    window = (p.get("hitl") or {}).get("soft_stop_window_seconds")
    if window is not None and window < 180:
        errs.append("soft-stop window shorter than 3 minutes")
    retention = (p.get("audit") or {}).get("retention_days")
    if retention is not None and retention < 365:
        errs.append("audit retention shorter than one year")
    return errs


def check_event(e: dict) -> list[str]:
    errs = [f"missing '{k}'" for k in REQUIRED_EVENT if k not in e]
    if errs:
        return errs
    if e["level"] == "L4":
        errs.append("event at L4, which is never granted")
    elif e["level"] not in LEVELS + ["human"]:
        errs.append(f"unknown level {e['level']!r}")
    if e["risk_class"] not in CLASSES:
        errs.append(f"unknown risk class {e['risk_class']!r}")
    if e["tier"] not in TIERS:
        errs.append(f"unknown tier {e['tier']!r}")
    if e["outcome"] not in OUTCOMES:
        errs.append(f"unknown outcome {e['outcome']!r}")
    rc, tier = e["risk_class"], e["tier"]
    if rc in MIN_TIER and tier in TIER_RANK and TIER_RANK[tier] < TIER_RANK[MIN_TIER[rc]]:
        errs.append(f"{rc} action ran under '{tier}', needs '{MIN_TIER[rc]}'")
    if rc in ("R3", "R4") and e["outcome"] in ("done", "approved") and not e.get("approver"):
        errs.append(f"{rc} action completed without a named approver")
    return errs


def check_audit_lines(lines) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError as exc:
            out.append(f"line {n}: not JSON ({exc.msg})")
            continue
        eid = e.get("event_id")
        if eid in seen:
            out.append(f"line {n}: duplicate event_id {eid!r}")
        seen.add(eid)
        out += [f"line {n}: {m}" for m in check_event(e)]
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in ("policy", "audit"):
        print(__doc__)
        return 2
    failed = False
    for name in argv[2:]:
        path = Path(name)
        if argv[1] == "policy":
            import yaml  # only needed here
            errs = check_policy(yaml.safe_load(path.read_text()) or {})
        else:
            errs = check_audit_lines(path.read_text().splitlines())
        status = "PASS" if not errs else "FAIL"
        print(f"{status} {name}")
        for m in errs:
            print(f"  - {m}")
        failed |= bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
