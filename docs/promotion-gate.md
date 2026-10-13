# Promotion gate

An agent moves up one [autonomy level](autonomy-levels.md) only when **all** of these hold:

| Criterion | Threshold |
|---|---|
| Time at the current level | ≥ 30 days |
| Actions at the current level | ≥ 20 |
| Critical incidents in that period | 0 |
| Eval suite | Passes, **including a prompt-injection test set** (run with an open-source tool such as promptfoo) |
| Review | Orchestrator review of the record |
| Decision | The owner decides, in writing |

## Automatic demotion

**Any R3 or R4 incident demotes the agent automatically**, at least one level, before anyone investigates. Promotion is slow and deliberate; demotion is instant.

## What the eval suite should cover

- The agent's normal tasks, with expected outputs
- Refusals: tasks above its level or outside its remit
- Prompt injection: instructions hidden in documents, web pages, messages and other agents' output
- Data handling: it must not echo personal data into logs or messages that do not need it

Record the review in [templates/promotion-review.md](../templates/promotion-review.md).
