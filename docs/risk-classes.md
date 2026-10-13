# Risk classes

The risk class belongs to the **action**, not to the agent. The same agent can read a file (R0) and then ask to send an email (R4). The class decides which approval tier applies.

| Class | Covers | Approval | Example |
|---|---|---|---|
| R0 | Read | None needed | Read a log, search notes |
| R1 | Workspace write | None needed; logged | Write a draft into the agent's own folder |
| R2 | Reversible operations | Logged; reversible by design | Restart a service, move a file to a holding folder |
| R3 | Configuration changes | Orchestrator review plus the owner | Change a schedule, a model route or an agent's tools |
| R4 | External sends, money, clinical, deletion or secrets | The owner, every time | Message a patient or client, issue a refund, delete records, rotate a key |

## Rules that make the classes work

1. **Classify before acting.** The agent states the class in its proposal; the gate checks it against a fixed list, and the stricter class wins when they disagree.
2. **No class is downgraded by context.** "It is only a test message" is still R4.
3. **Unknown actions are R4** until someone classifies them.
4. **Batching does not lower the class.** Twenty R4 sends are twenty R4 approvals, or one approval card that lists all twenty.
5. **Every class is logged**, including R0, so a pattern of reads can be audited later.

## Mapping levels to classes

| Level | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| L0 Observer | ✔ | — | — | — | — |
| L1 Proposer | ✔ | propose | propose | propose | propose |
| L2 Operator | ✔ | ✔ | ✔ | propose | propose |
| L3 Delegate | ✔ | ✔ | ✔ | with approval | with owner approval |
| L4 Autonomous | not used | | | | |

✔ = may act and log. "Propose" = may prepare the action for a human.
