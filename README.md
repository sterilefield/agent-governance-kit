<p align="center"><a href="https://sterilefield.github.io/agent-governance-kit/"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/hero-dark.svg">
  <img alt="Agent governance kit: autonomy levels L0–L4, risk classes R0–R4, and L3 as the highest level for health, money and external sends" src="docs/img/hero-light.svg" width="100%">
</picture></a></p>

# Agent governance kit

**A practical governance framework for AI agents that touch real work: autonomy levels, risk classes, human approval tiers, kill switches, an audit spine and a promotion gate, mapped to OWASP, NIST and ISO/IEC 42001, with a healthcare overlay for India.**

This kit is the public, generic form of the governance framework the author designed for his own multi-agent platform, where it binds every agent. It is written by a clinician with 20 years of hospital operations, so it borrows from clinical practice: nothing touches the patient without a check, and anything that can't be undone needs a named human.

The rules in the table below come from that framework. The guidance around them, the templates and the checker are written to be generic, so you can adopt them in your own system.

> [!IMPORTANT]
> **Status:** Framework kit with a working policy checker (Python) and tests. Last verified 21 Oct 2026. Not for clinical use as-is. Scope and limits: [TRUST.md](TRUST.md).

**[Autonomy levels](docs/autonomy-levels.md) · [Risk classes](docs/risk-classes.md) · [Standards mapping](docs/standards-mapping.md) · [Healthcare overlay](docs/healthcare-overlay.md) · [Trust](TRUST.md) · [All showcases](https://github.com/sterilefield) · [Contact](https://www.linkedin.com/in/dr-ravi-teja-thiriveedhi)**

[![CI](https://github.com/sterilefield/agent-governance-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/sterilefield/agent-governance-kit/actions/workflows/ci.yml) [![Live demo](https://img.shields.io/badge/live_demo-open-1a7f37)](https://sterilefield.github.io/agent-governance-kit/) [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sterilefield/agent-governance-kit) [![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/sterilefield/agent-governance-kit/badge)](https://scorecard.dev/viewer/?uri=github.com/sterilefield/agent-governance-kit) [![Latest release](https://img.shields.io/github/v/release/sterilefield/agent-governance-kit?label=release)](https://github.com/sterilefield/agent-governance-kit/releases/latest) [![Attested builds](https://img.shields.io/badge/releases-attested_%2B_SBOM-1a7f37)](#verify-this-release)

### See it in action

<a href="https://sterilefield.github.io/agent-governance-kit/"><img alt="Animated recording of the Agent governance gate live demo: scripted interactions on invented data" src="docs/img/demo.gif" width="100%"></a>

<sub>Recorded from the live demo page with scripted clicks, on invented data. [Open the demo](https://sterilefield.github.io/agent-governance-kit/) to try it yourself.</sub>

## The framework on one page

```mermaid
flowchart LR
    A["Agent proposes an action"] --> C{"Risk class?"}
    C -- "R0 read · R1 workspace write · R2 reversible" --> S["Proceed<br/>logged"]
    C -- "R3 config" --> O["Hard stop<br/>orchestrator review plus owner"]
    C -- "R4 external · money · clinical · delete · secrets" --> H["Hard stop<br/>owner, every time"]
    S --> L[("Append-only audit log")]
    O --> L
    H --> L
```

| Element | Rule |
|---|---|
| [Autonomy levels](docs/autonomy-levels.md) | L0 Observer → L1 Proposer → L2 Operator → L3 Delegate → L4 Autonomous (**deliberately unused**). Health, money, external sends, deletions and secrets never sit above L3. |
| [Risk classes](docs/risk-classes.md) | R0 read → R1 workspace write → R2 reversible operations → R3 configuration → R4 external sends, money, clinical, deletion or secrets |
| [Human-in-the-loop tiers](docs/controls.md#human-in-the-loop-tiers) | Hard stop for spend, external messages, irreversible actions and security · soft stop with a 3-minute window · silent proceed for routine work |
| [Kill switches](docs/controls.md#kill-switches) | Stop one agent or all agents; stop and restore from a dashboard; quarantine, never delete |
| [Audit spine](docs/controls.md#audit-spine) | Append-only JSONL with OpenTelemetry GenAI fields, kept at least a year, encrypted off-site |
| [Promotion gate](docs/promotion-gate.md) | ≥ 30 days and ≥ 20 actions with 0 critical incidents, an eval suite with prompt-injection tests, and an owner decision. Any R3/R4 incident demotes automatically. |
| [Access](docs/controls.md#access) | Deny by default, role-based |
| [Exec gate](docs/controls.md#exec-gate) | Pre-approved commands run silently; destructive commands need a written approval card |
| [Prompt-injection defence](docs/controls.md#prompt-injection-defence) | Canary patterns stop the agent; agent output is data, never instructions |
| [Change control](docs/controls.md#change-control) | Every config change is a changeset with a reason, a review and automatic rollback |

## Standards mapping

[docs/standards-mapping.md](docs/standards-mapping.md) maps each control to the **OWASP Top 10 for Agentic Applications 2026** (ASI01–ASI10), the **OWASP Top 10 for LLM Applications 2025**, the **NIST AI RMF** functions, **ISO/IEC 42001** clauses, MCP consent practice and India's **DPDP Rules 2025**.

## Healthcare overlay (India)

[docs/healthcare-overlay.md](docs/healthcare-overlay.md) adds the rules a clinic or hospital needs on top: the Telemedicine Practice Guidelines 2020, the DCI Code of Ethics 2014, WhatsApp Business messaging rules and DPDP consent.

## Templates you can copy

| Template | Use it for |
|---|---|
| [templates/agent-policy.yaml](templates/agent-policy.yaml) | One agent's level, allowed risk classes, budgets and tools |
| [templates/approval-card.md](templates/approval-card.md) | Asking a human to approve an R3/R4 action |
| [templates/audit-event.schema.json](templates/audit-event.schema.json) | One line of the audit log, with OTel GenAI fields |
| [templates/promotion-review.md](templates/promotion-review.md) | Deciding whether an agent moves up a level |
| [templates/incident-rca.md](templates/incident-rca.md) | Writing up an incident and the guard added after it |
| [templates/injection-response.md](templates/injection-response.md) | A starting runbook for a suspected prompt injection |

## Check your policies in code

`kit/govcheck.py` is a small checker (Python, PyYAML only). It validates agent policies against the framework (for example, no agent above L3 may hold R4 rights, and L4 is refused) and checks audit events for required fields.

```bash
python3 kit/govcheck.py policy templates/agent-policy.yaml
python3 kit/govcheck.py audit examples/audit-sample.jsonl
```

Run the tests with `pip install -r requirements.txt && python3 -m pytest -q`, or every gate (secret scan, link check, tests) with `bash scripts/check.sh`.

## Related

- [empire-os-reference-architecture](https://github.com/sterilefield/empire-os-reference-architecture): the platform this framework governs.
- [llm-token-economics](https://github.com/sterilefield/llm-token-economics): budgets and caps, the cost side of governance.

## Try it

**[Agent governance gate](https://sterilefield.github.io/agent-governance-kit/)**: pick an autonomy level and an action, see the gate's decision and the audit event; replay a 15-step scenario whose audit log passes `kit/govcheck.py`. It runs in your browser on invented data.

<a href="https://sterilefield.github.io/agent-governance-kit/"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/demo-page-dark.png">
  <img alt="Screenshot of the Agent governance gate demo page, showing invented data" src="docs/img/demo-page-light.png" width="100%">
</picture></a>

Or run the same logic yourself (Python 3, standard library only, nothing to install):

```bash
git clone https://github.com/sterilefield/agent-governance-kit.git
cd agent-governance-kit
python3 demo/governance_sim.py
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/demo-terminal-dark.svg">
  <img alt="Terminal recording of python3 demo/governance_sim.py: the real output of the demo" src="docs/img/demo-terminal-light.svg" width="100%">
</picture>

The terminal image is the real output of that command, rendered by `scripts/term_svg.py`. Everything in `demo/` and `site/` is a demo written for this repository on invented data. It is not production code, and the tests in `tests/` run on every pull request.

## How this was built

I write the specifications, architecture, acceptance criteria and review gates; AI coding agents (Claude Code and Codex) write most of the code under those specifications. I own every review, test gate, release decision and production operation. Text in this repository was drafted with AI assistance and passed gate G4, a review by a fresh-context AI agent that did not write it, before my own approval (G5).

## Verify this release

Every release carries a build-provenance attestation for its source archive and an SPDX SBOM (the SBOM is attested too from v0.2.0). These commands fetch the latest release into a new folder and check both attestations:

```bash
gh release download -R sterilefield/agent-governance-kit -p '*.tar.gz' -p 'sbom.spdx.json' -D verify-latest
gh attestation verify verify-latest/agent-governance-kit-*.tar.gz -R sterilefield/agent-governance-kit
gh attestation verify verify-latest/agent-governance-kit-*.tar.gz -R sterilefield/agent-governance-kit --predicate-type https://spdx.dev/Document/v2.3
```

## Author

**Dr. Ravi Teja Thiriveedhi**: clinician turned AI systems architect, with 20 years of clinical practice and hospital operations. [GitHub](https://github.com/Raviteja2k2k) · [LinkedIn](https://www.linkedin.com/in/dr-ravi-teja-thiriveedhi)

## Licence

[Apache-2.0](LICENSE). Use, adapt and ship it, with attribution. This kit is engineering guidance, not legal advice; check regulations with a qualified adviser before relying on them.
