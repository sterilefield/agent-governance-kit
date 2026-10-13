import copy
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kit"))
import govcheck  # noqa: E402

POLICY = yaml.safe_load((ROOT / "templates" / "agent-policy.yaml").read_text())


def test_template_policy_passes():
    assert govcheck.check_policy(POLICY) == []


def test_l4_is_refused():
    p = copy.deepcopy(POLICY); p["level"] = "L4"
    assert any("L4" in e for e in govcheck.check_policy(p))


def test_l2_cannot_act_on_r4():
    p = copy.deepcopy(POLICY); p["risk"]["act"].append("R4")
    assert any("may not act on R4" in e for e in govcheck.check_policy(p))


def test_ceilings_are_mandatory():
    p = copy.deepcopy(POLICY); p["ceilings"].remove("clinical")
    assert any("clinical" in e for e in govcheck.check_policy(p))


def test_wildcard_tools_rejected():
    p = copy.deepcopy(POLICY); p["tools"] = ["*"]
    assert any("deny by default" in e for e in govcheck.check_policy(p))


def test_short_retention_and_window_rejected():
    p = copy.deepcopy(POLICY); p["audit"]["retention_days"] = 90; p["hitl"]["soft_stop_window_seconds"] = 60
    errs = govcheck.check_policy(p)
    assert any("one year" in e for e in errs) and any("3 minutes" in e for e in errs)


def test_sample_audit_passes():
    lines = (ROOT / "examples" / "audit-sample.jsonl").read_text().splitlines()
    assert govcheck.check_audit_lines(lines) == []


def test_r4_silent_is_flagged():
    e = {"ts": "t", "event_id": "x", "actor": "a", "level": "L3", "risk_class": "R4",
         "tier": "silent", "action": "send", "outcome": "done"}
    errs = govcheck.check_event(e)
    assert any("needs 'hard_stop'" in m for m in errs) and any("approver" in m for m in errs)


def test_duplicate_ids_and_bad_json():
    good = json.dumps({"ts": "t", "event_id": "d", "actor": "a", "level": "L1", "risk_class": "R0",
                       "tier": "silent", "action": "read", "outcome": "done"})
    errs = govcheck.check_audit_lines([good, good, "{not json"])
    assert any("duplicate" in m for m in errs) and any("not JSON" in m for m in errs)


def test_unknown_level_in_audit_flagged():
    e = {"ts": "t", "event_id": "u", "actor": "a", "level": "L9", "risk_class": "R0",
         "tier": "silent", "action": "read", "outcome": "done"}
    assert any("unknown level" in m for m in govcheck.check_event(e))
