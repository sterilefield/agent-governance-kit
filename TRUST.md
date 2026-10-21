# Trust, scope and limitations

> [!WARNING]
> Sanitised public showcase. Not for clinical use as-is, not legal or regulatory advice, and not a product. Last verified 21 Oct 2026.

## What this repository is
Framework documentation, templates and a small python checker. Teams that let AI agents touch real work and need autonomy levels, risk classes, approval tiers, kill switches and an audit spine they can adopt.

## Out of scope
It is not a certified compliance product and not legal advice. The healthcare overlay is engineering guidance, not clinical or regulatory sign-off.

## Limitations
- The standards mapping reflects the author's reading of OWASP, NIST AI RMF, ISO/IEC 42001 and India's DPDP Rules; verify with a qualified adviser.
- govcheck.py checks policy files and audit events for structure and the framework's rules; it does not inspect a running agent.
- Thresholds such as the promotion gate are the author's defaults, to be tuned per organisation.

## Data provenance
No client data, patient data, prompts or credentials. Example audit events are invented. Every release passes five gates before it is public: G1 allow-list of files, G2 secret and deny-list scan, G3 fresh history (no private commits travel), G4 fresh-context AI review (an agent that did not write the material), G5 owner approval (the human check) with a licence check. See the [publication policy](https://github.com/sterilefield/.github/blob/main/PUBLICATION_POLICY.md).

## Privacy and regulation
No personal data is processed by anything in this repository. Where the text discusses India's DPDP Act and Rules, systems are described as *designed toward* those requirements, never as certified or compliant.

## AI assistance
AI coding agents (Claude Code and Codex) drafted much of the material under the author's specifications; the author reviewed every change and owns every claim.

## Report a problem
Security issues: see [SECURITY.md](SECURITY.md). Factual errors or overclaims: open an issue; corrections are welcome.
