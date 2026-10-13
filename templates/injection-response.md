# Suspected prompt injection: starting runbook

Adapt this to your system. Keep your canary patterns private.

1. **Stop.** The canary or a human trips the kill switch for the affected agent.
2. **Quarantine.** Move the triggering input (message, document, page or agent output) aside. Do not delete it.
3. **Scope.** Search the audit log for every action the agent took since it first saw that input.
4. **Contain.** Roll back any changes, revoke any tokens the agent could reach, and check outbound messages.
5. **Record.** Write the incident up with [incident-rca.md](incident-rca.md); the agent is demoted if an R3/R4 action was involved.
6. **Guard.** Add the case to the injection eval set and, if useful, a new canary pattern before restoring the agent.
