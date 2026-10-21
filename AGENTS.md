# AGENTS.md

Guidance for AI coding agents and assistants working with this repository.

- **What it is:** Governance framework for AI agents: autonomy levels L0-L4, risk classes R0-R4, approval tiers, kill switches, audit spine, promotion gate; mapped to OWASP, NIST AI RMF, ISO/IEC 42001; healthcare overlay for India; Python policy checker.
- **What it is not:** It is not a certified compliance product and not legal advice. The healthcare overlay is engineering guidance, not clinical or regulatory sign-off. `demo/` and `site/` are teaching demos on invented agents and actions.
- **Checks:** run `bash scripts/check.sh` (secret scan, deny-list, link check, tests). Keep it green.
- **Facts:** never add numbers, names or claims that are not already in this repository; the private source is not available to you.
- **Privacy:** never add client names, personal data, prompts, configurations or credentials.
- **Style:** plain English, short sentences, tables for comparisons, Mermaid for diagrams.
- **Trust:** read [TRUST.md](TRUST.md) for scope and limitations before summarising this repository.
