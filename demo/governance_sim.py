#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Ravi Teja Thiriveedhi
"""governance_sim: a runnable walk-through of the agent governance kit on invented agents and actions.

    python3 demo/governance_sim.py              # run the scenario, print the decisions
    python3 demo/governance_sim.py --audit out.jsonl   # also write the audit log

Every agent, action and approval here is synthetic, written for this demo. The gate applies the
published rules (docs/autonomy-levels.md, docs/risk-classes.md, docs/controls.md) and the audit
log it writes is checked with kit/govcheck.py. Standard library only.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "kit"))
import govcheck  # noqa: E402

CLASSES = ["R0", "R1", "R2", "R3", "R4"]
# Each action type has a fixed class; anything not on the list is treated as R4 (rule 3).
ACTION_CLASS = {
    "read": "R0",
    "search": "R0",
    "draft": "R1",
    "restart_service": "R2",
    "move_to_holding": "R2",
    "change_schedule": "R3",
    "change_model_route": "R3",
    "send_external": "R4",
    "refund": "R4",
    "delete_records": "R4",
    "rotate_key": "R4",
    "clinical_reply": "R4",
}


@dataclass
class Decision:
    verdict: str  # ACT, PROPOSE, WAIT (hard stop), BLOCK, STOPPED
    tier: str  # silent, soft_stop, hard_stop
    reason: str


def classify(action: str, claimed: str | None = None) -> str:
    """Fixed list first; unknown actions are R4; the stricter class wins on disagreement."""
    fixed = ACTION_CLASS.get(action, "R4")
    if claimed in CLASSES and CLASSES.index(claimed) > CLASSES.index(fixed):
        return claimed
    return fixed


def decide(level: str, risk_class: str, killed: bool = False) -> Decision:
    """The level-by-class table from docs/risk-classes.md, plus the kill switch."""
    if killed:
        return Decision("STOPPED", "hard_stop", "kill switch is on; nothing runs until the owner restores")
    if level == "L4":
        return Decision("BLOCK", "hard_stop", "L4 Autonomous is never granted")
    if level == "L0":
        if risk_class == "R0":
            return Decision("ACT", "silent", "L0 may read and report")
        return Decision("BLOCK", "hard_stop", "L0 Observer may only read")
    if risk_class == "R0":
        return Decision("ACT", "silent", "reads are always allowed and logged")
    if level == "L1":
        return Decision("PROPOSE", "hard_stop", "L1 prepares the action; a human decides")
    if risk_class in ("R1", "R2"):
        return Decision("ACT", "silent", f"{level} may act on {risk_class} and log it")
    if level == "L2":
        return Decision("PROPOSE", "hard_stop", f"L2 may only propose {risk_class}")
    who = "orchestrator review plus the owner" if risk_class == "R3" else "the owner, every time"
    return Decision("WAIT", "hard_stop", f"hard stop: needs {who}")


@dataclass
class Gate:
    owner: str = "owner"
    killed: bool = False
    events: list[dict] = field(default_factory=list)
    clock: int = 0
    cards: int = 0

    def _ts(self) -> str:
        self.clock += 1
        h, m = divmod(9 * 60 + self.clock, 60)
        return f"2026-01-05T{h:02d}:{m:02d}:00+05:30"

    def log(self, **e) -> dict:
        e = {"ts": self._ts(), "event_id": f"demo-{len(self.events) + 1:03d}", **e}
        self.events.append(e)
        return e

    def request(self, agent: str, level: str, action: str, detail: str, owner_says: str | None = None) -> tuple[Decision, str]:
        rc = classify(action)
        d = decide(level, rc, self.killed)
        base = dict(actor=agent, level=level, risk_class=rc, tier=d.tier, action=f"{action} {detail}", **{"gen_ai.agent.name": agent})
        if d.verdict == "ACT":
            self.log(outcome="done", **base)
            return d, "done"
        if d.verdict in ("BLOCK", "STOPPED"):
            self.log(outcome="stopped", **base)
            return d, "stopped"
        self.cards += 1
        card = f"AC-20260105-{self.cards:02d}"
        self.log(outcome="proposed", approval_card=card, **base)
        if owner_says == "approve":
            review = ""
            if rc == "R3":  # R3 needs orchestrator review plus the owner (docs/risk-classes.md)
                self.log(**{**base, "actor": "orchestrator", "action": f"review {action}", "gen_ai.agent.name": "orchestrator"},
                         outcome="approved", approval_card=card, approver="orchestrator")
                review = "reviewed by orchestrator, "
            self.log(outcome="done", approval_card=card, approver=self.owner, **base)
            return d, f"{review}approved by {self.owner} ({card})"
        if owner_says == "reject":
            self.log(outcome="rejected", approval_card=card, approver=self.owner, **base)
            return d, f"rejected by {self.owner} ({card})"
        return d, f"waiting on {card}"

    def kill(self, on: bool) -> None:
        # Demo choice: the switch itself is logged as an owner action of class R2 (reversible by design).
        self.killed = on
        self.log(actor=self.owner, level="human", risk_class="R2", tier="hard_stop",
                 action="kill switch " + ("on: stop all agents" if on else "off: restore"), outcome="done", approver=self.owner)


SCENARIO = [
    # agent, level, action, detail, what the (invented) owner does if asked
    ("intake-assistant", "L2", "read", "today's new enquiries", None),
    ("intake-assistant", "L2", "draft", "3 reply drafts to the outbox", None),
    ("intake-assistant", "L2", "send_external", "3 replies to customers", None),
    ("ops-agent", "L3", "restart_service", "report generator", None),
    ("ops-agent", "L3", "change_schedule", "nightly backup from 02:00 to 03:00", "approve"),
    ("ops-agent", "L3", "send_external", "weekly summary to a supplier", "approve"),
    ("research-scout", "L0", "search", "public guidance on appointment reminders", None),
    ("research-scout", "L0", "draft", "summary note", None),
    ("billing-helper", "L1", "refund", "invoice INV-0042", "reject"),
    ("ops-agent", "L3", "delete_records", "old temp exports", "reject"),
    ("intake-assistant", "L2", "unlisted_tool", "(not on the list, so treated as R4)", None),
    ("KILL", "", "", "", None),
    ("ops-agent", "L3", "read", "service status", None),
    ("RESTORE", "", "", "", None),
    ("ops-agent", "L3", "read", "service status", None),
]

ICON = {"ACT": "✔ ACT    ", "PROPOSE": "⏸ PROPOSE", "WAIT": "⏸ WAIT   ", "BLOCK": "✖ BLOCK  ", "STOPPED": "✖ STOPPED"}


def run(audit_path: str | None = None) -> int:
    g = Gate()
    print("Agent governance kit: demo on invented agents (synthetic, not real)")
    print(f"{'agent':<17}{'lvl':<4}{'class':<6}{'decision':<11}action -> result")
    print("-" * 96)
    for agent, level, action, detail, owner in SCENARIO:
        if agent in ("KILL", "RESTORE"):
            g.kill(agent == "KILL")
            print(f"{'owner':<17}{'-':<4}{'-':<6}{'⚑ ' + agent:<11}kill switch {'ON: every agent stops' if agent == 'KILL' else 'OFF: owner restores'}")
            continue
        d, result = g.request(agent, level, action, detail, owner)
        rc = classify(action)
        print(f"{agent:<17}{level:<4}{rc:<6}{ICON[d.verdict]:<11}{action} {detail} -> {result}")
    lines = [json.dumps(e, ensure_ascii=False) for e in g.events]
    problems = govcheck.check_audit_lines(lines)
    print("-" * 96)
    print(f"audit log: {len(lines)} events, checked with kit/govcheck.py -> " + ("PASS" if not problems else "FAIL"))
    for p in problems:
        print("  - " + p)
    if audit_path:
        Path(audit_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"audit log written to {audit_path}")
    return 1 if problems else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    path = args[args.index("--audit") + 1] if "--audit" in args else None
    sys.exit(run(path))
