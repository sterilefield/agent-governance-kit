# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Ravi Teja Thiriveedhi
"""Tests for demo/governance_sim.py: the gate follows the published level-by-class table."""
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "demo"))
import governance_sim as sim  # noqa: E402

TABLE = {  # docs/risk-classes.md, "Mapping levels to classes"
    "L0": ["ACT", "BLOCK", "BLOCK", "BLOCK", "BLOCK"],
    "L1": ["ACT", "PROPOSE", "PROPOSE", "PROPOSE", "PROPOSE"],
    "L2": ["ACT", "ACT", "ACT", "PROPOSE", "PROPOSE"],
    "L3": ["ACT", "ACT", "ACT", "WAIT", "WAIT"],
}


class GateTable(unittest.TestCase):
    def test_matches_published_table(self):
        for level, row in TABLE.items():
            for rc, want in zip(sim.CLASSES, row):
                self.assertEqual(sim.decide(level, rc).verdict, want, f"{level} {rc}")

    def test_l4_never_granted(self):
        for rc in sim.CLASSES:
            self.assertEqual(sim.decide("L4", rc).verdict, "BLOCK")

    def test_kill_switch_stops_everything(self):
        for level in TABLE:
            self.assertEqual(sim.decide(level, "R0", killed=True).verdict, "STOPPED")

    def test_unknown_action_is_r4_and_stricter_class_wins(self):
        self.assertEqual(sim.classify("something_new"), "R4")
        self.assertEqual(sim.classify("read", claimed="R2"), "R2")
        self.assertEqual(sim.classify("send_external", claimed="R0"), "R4")

    def test_hard_stops_for_r3_r4(self):
        for rc in ("R3", "R4"):
            self.assertEqual(sim.decide("L3", rc).tier, "hard_stop")


class Scenario(unittest.TestCase):
    def test_scenario_audit_log_passes_govcheck(self):
        with redirect_stdout(io.StringIO()) as out:
            code = sim.run()
        self.assertEqual(code, 0)
        self.assertIn("-> PASS", out.getvalue())

    def test_r3_r4_done_always_has_approver(self):
        g = sim.Gate()
        with redirect_stdout(io.StringIO()):
            for agent, level, action, detail, owner in sim.SCENARIO:
                if agent in ("KILL", "RESTORE"):
                    g.kill(agent == "KILL")
                else:
                    g.request(agent, level, action, detail, owner)
        for e in g.events:
            if e["risk_class"] in ("R3", "R4") and e["outcome"] == "done":
                self.assertTrue(e.get("approver"), json.dumps(e))


if __name__ == "__main__":
    unittest.main()
