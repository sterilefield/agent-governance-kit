# Autonomy levels

An autonomy level says **how far an agent may go without a human**. Every agent has exactly one level, written in its policy file. A level is earned through the [promotion gate](promotion-gate.md), and lost automatically after a serious incident.

| Level | Name | The agent may | A human |
|---|---|---|---|
| L0 | Observer | Read and report | Does everything |
| L1 | Proposer | Propose an action with its reasoning | Decides and acts |
| L2 | Operator | Act on routine, reversible work | Reviews the log |
| L3 | Delegate | Act on delegated work within its remit | Approves anything R3 or R4 |
| L4 | Autonomous | Act on anything without approval | **Not used. The level exists so the boundary is explicit.** |

## Hard ceilings

Some work never rises above L3, whatever an agent's record:

- health and clinical content
- money: payments, refunds, prices, quotes
- messages sent outside the organisation
- deletions
- secrets and credentials

For these, the most an agent can do is prepare the action. A named human releases it.

## Why L4 is unused

In clinical practice the person who signs is accountable. An agent cannot be accountable, so no agent holds a level where nobody signs. Keeping L4 in the scale, marked unused, makes that a stated decision rather than an oversight, and it gives auditors a clear answer.

## Choosing a starting level

| If the agent… | Start at |
|---|---|
| Is new, or its model or tools changed | L0 or L1 |
| Has passed the promotion gate once | L2 |
| Has a narrow, well-tested remit and a clean record at L2 | L3 |
