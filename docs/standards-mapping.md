# Standards mapping

Pointers from each control in this kit to the standards it helps meet. A mapping is a starting point for an assessment, not a certification.

## OWASP Top 10 for Agentic Applications 2026

| ID | Risk | Controls in this kit |
|---|---|---|
| ASI01 | Agent Goal Hijack | Prompt-injection defence; agent output treated as data; hard stop on R4 |
| ASI02 | Tool Misuse and Exploitation | Deny-by-default tools per agent; exec gate; risk classes |
| ASI03 | Identity and Privilege Abuse | Role-based access; autonomy ceilings; approvals only from registered devices |
| ASI04 | Agentic Supply Chain Vulnerabilities | Changesets with review; dependency preflight; pinned Python dependencies and SBOMs in releases |
| ASI05 | Unexpected Code Execution | Exec gate; pre-approved command list; approval card for destructive commands |
| ASI06 | Memory and Context Poisoning | Agent output as data; quarantine; eval suite with injection tests |
| ASI07 | Insecure Inter-Agent Communication | Outputs from other agents pass the same gate as outside input |
| ASI08 | Cascading Failures | Kill switch for all agents; budgets; automatic rollback |
| ASI09 | Human-Agent Trust Exploitation | Approval cards show the exact action and its class, not the agent's summary |
| ASI10 | Rogue Agents | Kill switches; automatic demotion; append-only audit |

## OWASP Top 10 for LLM Applications 2025

| ID | Risk | Controls |
|---|---|---|
| LLM01 | Prompt Injection | Canary patterns; output-as-data; injection eval set |
| LLM02 | Sensitive Information Disclosure | Deny-by-default data access; R4 for secrets; healthcare overlay |
| LLM03 | Supply Chain | Changesets; reviewed dependencies |
| LLM04 | Data and Model Poisoning | Quarantine; reviewed knowledge updates |
| LLM05 | Improper Output Handling | Exec gate; output never executed directly |
| LLM06 | Excessive Agency | Autonomy levels; risk classes; L4 unused |
| LLM07 | System Prompt Leakage | Secrets never placed in prompts |
| LLM08 | Vector and Embedding Weaknesses | Role-based access to knowledge stores |
| LLM09 | Misinformation | Human approval for clinical and external content |
| LLM10 | Unbounded Consumption | Per-agent token and run budgets |

## NIST AI Risk Management Framework (AI RMF 1.0)

| Function | Where this kit helps |
|---|---|
| Govern | Autonomy levels, named owner decisions, promotion gate |
| Map | Risk classes per action; healthcare overlay |
| Measure | Eval suite; audit log; incident counts in promotion reviews |
| Manage | HITL tiers; kill switches; demotion; incident RCAs |

## ISO/IEC 42001:2023 (AI management system)

| Clause | Pointer |
|---|---|
| 5 Leadership | The owner signs promotions and R4 actions |
| 6 Planning | Risk classes and the healthcare overlay as the risk treatment |
| 8 Operation | Changesets, exec gate, HITL tiers |
| 9 Performance evaluation | Audit log, eval suite, promotion reviews |
| 10 Improvement | Incident RCAs with a guard added after each one |

## Model Context Protocol (MCP)

The MCP specification asks hosts to obtain explicit user consent before invoking tools and before sharing user data with servers. In this kit, every MCP tool gets a risk class like any other tool, and R3/R4 tools pass the approval card.

## India: DPDP Act 2023 and DPDP Rules 2025

| Requirement (summary) | Control |
|---|---|
| Notice and consent before processing personal data | Healthcare overlay: consent-first messaging |
| Reasonable security safeguards, including logs kept for a year | Audit spine kept ≥ 1 year, encrypted off-site |
| Breach notice to affected people and to the Data Protection Board (detailed report within 72 hours) | Incident RCA template includes a notification step |
| Data minimisation and erasure on request | Deny-by-default access; quarantine instead of silent deletion, then owner-approved erasure |

The Rules were notified in November 2025 and most obligations phase in over 18 months.
