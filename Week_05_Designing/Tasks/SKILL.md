---
name: architecture-decision
description: "Make and document an evidence-based software architecture decision without an open-ended debate. Use when choosing an architecture, comparing a modular monolith, microservices, serverless, event-driven, or other alternatives, evaluating architecture proposals, creating an ADR, or deciding how a new or existing project should be structured."
argument-hint: "[project description, requirements, or paths to project documents]"
user-invocable: true
---

# Architecture Decision

## Purpose

Produce a defensible architecture decision for a project in one bounded workflow. The
result must explain not only what was selected, but why it fits the project's current
requirements better than credible alternatives and when the decision should be revisited.

This skill generalizes the following decision pattern:

1. Understand the project and its requirements.
2. Propose three materially different architecture candidates.
3. Examine the candidates against the same project-specific drivers.
4. Select and justify one candidate.
5. Record the decision, consequences, assumptions, and review triggers in an ADR.

Do not simulate a long multi-agent conversation. Perform the analysis directly, expose
uncertainty explicitly, and ask at most one focused clarification round when an
unresolved answer could change the decision.

## When to Use

- Selecting an architecture for a new project.
- Reconsidering the architecture of an existing project.
- Comparing a modular monolith, microservices, serverless, event-driven, hybrid, or
  other architectural styles.
- Turning an architecture discussion or proposal set into a decision record.
- Reviewing whether an existing ADR is sufficiently justified and actionable.

Do not use this skill for detailed component design, database schema design, technology
selection, deployment implementation, or performance testing. Those may be follow-up
work after the decision.

## Inputs

Accept any combination of:

- A project description, requirements, user stories, or existing documentation.
- A repository or source tree to inspect.
- Existing architecture proposals, ADRs, diagrams, or decision notes.
- Constraints such as team size, delivery date, budget, compliance, hosting, scale,
  availability, latency, data residency, or operational capability.
- A requested output location or ADR numbering convention.

If requirements are incomplete, infer only low-risk facts from the available evidence.
Mark assumptions and do not invent numeric quality targets. Ask one consolidated
clarification round only for missing facts that could change the ranking.

## Procedure

### 1. Establish the decision context

Inspect the supplied project documents and, when a repository is provided, inspect its
structure and relevant configuration. Summarize:

- Project purpose and primary user or system workflows.
- Major functional boundaries and integrations.
- Consistency, authorization, privacy, and data-lifecycle needs.
- Real-time, batch, offline, reporting, and failure-handling needs.
- Expected scale and growth, only where supported by evidence.
- Team, operations, delivery, hosting, and organizational constraints.
- Known risks, unknowns, and assumptions.

Separate facts from assumptions. Identify the decision scope, for example:
"initial deployment architecture for the web application", not "the entire future
technology stack."

### 2. Define decision drivers

Create 5-8 drivers that are specific to the project. Typical drivers include:

- Delivery and operational simplicity.
- Transactional consistency and data integrity.
- Independent scaling or workload isolation.
- Availability and fault isolation.
- Security and authorization boundaries.
- Development, testing, and debugging complexity.
- Team ownership and deployment independence.
- Portability and provider coupling.
- Cost predictability.

For each driver, state why it matters and assign a weight from 1 (minor) to 5
(critical). Do not use generic drivers without connecting them to observed project
requirements.

### 3. Generate three credible candidates

Produce exactly three primary candidates unless the user supplied a different required
set. They must be materially different, not three minor technology variations. Select
the candidates appropriate to the context; common candidates are:

- Modular monolith with a shared relational database.
- Independently deployed services with service-owned data.
- Serverless or event-driven architecture using managed services.
- A deliberately bounded hybrid when one workload has distinct requirements.

For each candidate, describe:

- Shape and ownership boundaries.
- Request, event, and data flows.
- How the most important workflows are implemented.
- Consistency, authorization, failure, and retry behavior.
- Operational and testing model.
- Benefits for this project.
- Project-specific costs and risks.
- Conditions under which it becomes a better choice.

Do not reject an alternative because it is incapable of implementing the requirements.
Reject it only when its benefits do not justify its costs under the current evidence.

### 4. Evaluate with a common matrix

Score every candidate against every driver using:

- `1` = poor fit
- `3` = acceptable or conditional fit
- `5` = strong fit

Calculate a weighted score (`weight × score`) and show the totals. Scores are
structured judgment, not false precision: add a short evidence-based rationale for
each important score and flag scores that depend on assumptions.

The matrix is a decision aid, not the sole decision rule. Explicitly discuss:

- Any high-weight driver where the leading candidate is weak.
- Risks that are not captured by the numeric score.
- Reversibility and the cost of changing direction later.
- Whether a simpler first step preserves an evolution path.

### 5. Resolve consequential uncertainty

If the leading candidate changes when one or more assumptions change, ask a single
consolidated clarification round containing only those questions. Prioritize:

- Expected scale or workload shape.
- Required consistency and availability.
- Independent team ownership.
- Offline or data-residency requirements.
- Compliance, privacy, or deletion obligations.
- Operational capability and hosting constraints.

If the user does not answer, proceed with clearly labeled assumptions and choose the
most proportionate option. Do not restart the analysis or conduct another debate.

### 6. Select and validate the decision

Choose the candidate with the best fit for the current scope, not the most powerful
or fashionable architecture. Validate that the selected architecture:

- Covers every major requirement group.
- Has explicit authorization and data ownership boundaries.
- Explains consistency and concurrency behavior for shared data.
- Explains delivery reliability separately from database consistency.
- Has a practical local development, testing, deployment, and monitoring story.
- Provides a credible evolution path where future scale or workload isolation is
  plausible.

If no candidate is acceptable, state the blocking constraint instead of forcing a
choice.

### 7. Write the ADR

Use [the ADR template](./assets/adr-template.md). The ADR must include:

1. Title and metadata (`Status`, date, decision owners).
2. Context and requirements.
3. Decision drivers and assumptions.
4. The selected architecture and its boundaries.
5. A compact weighted comparison matrix.
6. Requirement-to-boundary coverage.
7. A component and data-flow view, using a diagram when useful.
8. Alternatives considered, including benefits, rejection reasons, concrete costs,
   and reconsideration conditions.
9. Consequences: benefits, costs, risks, and operational implications.
10. Validation plan and explicit review triggers.

Use `Accepted` only when the decision is ready to guide implementation. Use `Proposed`
when the user has not approved it. Keep implementation details, numeric SLOs, and
entity-level retention rules out of the ADR unless the input explicitly establishes
them.

### 8. Report outputs

Return a concise decision summary containing:

- Selected architecture and one-sentence rationale.
- The three candidates and weighted ranking.
- Critical assumptions and unresolved risks.
- Files created or updated.
- The earliest review trigger.

The durable output should normally be one ADR. If the user asks for the intermediate
analysis, also save the proposal set and evaluation matrix; otherwise keep them as
sections or an appendix in the ADR rather than creating unnecessary files.

## Quality bar

- Be fair to rejected alternatives and acknowledge their genuine strengths.
- Tie every major claim to a requirement, constraint, or explicit assumption.
- Prefer a proportionate, reversible decision over speculative future-proofing.
- Never claim reliability, consistency, security, or scalability that the design does
  not provide.
- Record important risks with a mitigation or a concrete review trigger.
- Keep the ADR understandable to a reader who did not participate in the analysis.

