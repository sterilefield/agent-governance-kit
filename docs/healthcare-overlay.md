# Healthcare overlay (India)

Extra rules for agents working in a clinic or hospital. They sit on top of the core framework and only ever make it stricter.

## The overlay rules

| Rule | Why |
|---|---|
| **Administrative agents only.** Agents book, remind, answer logistics and collect forms. They do not diagnose, counsel or prescribe. | The Telemedicine Practice Guidelines 2020 do not allow AI to counsel patients or prescribe; a registered practitioner must. |
| **Any clinical content is R4.** If a message touches symptoms, treatment or medicines, it goes to a clinician. | Clinical judgement stays with a named, registered professional. |
| **Hand-off is a feature.** The agent says clearly that a human will reply and routes the conversation. | Patients must never be left believing a machine gave clinical advice. |
| **No advertising claims.** Agents do not generate promotional claims about outcomes, prices or comparisons with other practitioners. | The Dentists (Code of Ethics) Regulations 2014 restrict advertising and self-promotion by dentists. |
| **Consent first.** Patients opt in before any messages, and can opt out with one word. | DPDP Act 2023 and Rules 2025; WhatsApp Business policy. |
| **Official WhatsApp Business Platform only.** No automation of personal WhatsApp or WhatsApp Web for patients or clients. | Meta's policies; reliability; account safety. |
| **Approved templates outside the 24-hour window.** Business-initiated messages use pre-approved templates. | WhatsApp Business Platform rules. |
| **Minimum necessary data.** Agents see only the fields their task needs; logs record references, not clinical details. | DPDP data minimisation; confidentiality duties of the profession. |

## Mapping to the core framework

| Action | Class | Tier |
|---|---|---|
| Read the appointment book | R0 | Silent |
| Draft a reminder into the outbox | R1 | Silent |
| Send an approved reminder template to an opted-in patient | R4 | Hard stop (can be pre-approved as a batch on one card) |
| Reply to a question about pain or medicines | R4 | Hard stop: route to a clinician |
| Change clinic hours in the booking system | R3 | Orchestrator plus owner |

> This overlay is engineering guidance from a clinician with 20 years of clinical practice and hospital operations, not legal advice. Check current regulations and your council's rules before deployment.
