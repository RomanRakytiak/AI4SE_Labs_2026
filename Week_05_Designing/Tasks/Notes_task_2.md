# Task 2 architecture decision discussion

## Starting point

Task 2 asks for an architecture decision record based on the three proposals discussed in Task 1. `Notes_1.md` is locked and remains unchanged. This file records the new discussion and review of the ADR.

The three candidates were:

1. Modular monolith.
2. Microservices.
3. Serverless/event-driven architecture.

## Decision discussion

The project is expected to remain small to medium scale and is an online web application. The selected architecture is a modular monolith with a relational database. It will contain explicit modules for identity, teams and membership, personal work, shared events, collaboration, and notifications.

The relational database is preferred because Teamify has several consistency-sensitive operations:

- Membership and administrator role changes.
- Event creation and invitation/response records.
- One vote per member and consistent poll results.
- Account deletion and privacy-related cleanup.

The initial notification decision is direct delivery from the application request flow. This is simpler and matches the current project scope, but it is a conscious risk: a notification provider failure can delay a request or cause a notification to be missed after the business transaction succeeds. The ADR therefore records a transactional outbox and background worker as a future evolution, not as the initial decision.

## ADR review criteria

The ADR should be informative enough for someone who did not participate in Task 1. It should include:

- Context and requirements.
- The chosen architecture and its internal modules.
- A simple component and data-flow diagram.
- Why each alternative was rejected.
- Benefits, costs, and operational risks.
- Conditions that would cause the decision to be reconsidered.
- A compact comparison table for quickly understanding the alternatives.

The ADR should not claim that direct notification delivery is reliable by itself, or that microservices and serverless cannot satisfy Teamify's requirements. All three can implement the requirements; the decision is based on proportional complexity and the current project assumptions.

## Initial ADR review

The first ADR version covered the decision, context, modules, relational constraints, API shape, diagram, alternatives, consequences, and review triggers. It also explicitly called out the direct-notification risk.

The first review found that the requested comparison table was missing. A diagram explains the selected architecture, but it does not quickly show why the alternatives were rejected. The ADR was therefore revised to add a decision matrix and to change the status from `Proposed` to `Accepted` after review.

One important detail to preserve is the distinction between:

- **Core consistency:** database transactions protect membership, roles, events, responses, and votes.
- **Delivery reliability:** direct notifications can fail independently of the database operation.

The ADR should also keep the rejection reasons specific. Microservices are rejected for the current scale and lack of an independent-ownership requirement, not because they are incapable of implementing Teamify. Serverless is rejected as the primary architecture because it adds distributed workflow and provider-specific complexity to core operations, while remaining a possible fit for selected background workloads.

## Final review outcome

The revised ADR is accepted as the current decision. It contains the standard context, decision, architecture view, alternatives, consequences, and validation-trigger sections, plus the requested comparison matrix. The decision can be reconsidered if scale, ownership, availability, notification reliability, or workload isolation requirements change.

## Follow-up review backlog

The ADR is sufficient for the Task 2 deliverable. It is informative, structured, and explains why the chosen modular monolith is preferable without claiming that the alternatives are incapable of implementing Teamify. The comparison matrix and component/data-flow diagram satisfy the request for an overview and visual representation.

The following are optional refinements rather than missing fundamentals:

1. **Clarify direct notification delivery.** The current decision is intentionally simple, but direct delivery after a database commit can lose notifications or make requests slow. The ADR could state an explicit acceptable-loss assumption and a measurable trigger for replacing direct delivery with an outbox and worker.
2. **Add security and authorization principles.** The ADR could state that authentication is separate from resource authorization, that every team operation checks membership and role, and that WebSocket subscriptions are authorized per team.
3. **Specify concurrency policy.** The ADR currently identifies simultaneous event edits as a pre-implementation question. It could record optimistic locking, last-write-wins, or manual conflict resolution as the selected policy.
4. **Specify account-deletion behavior.** The ADR could define which private records are deleted and whether shared chat messages or poll votes are deleted, anonymized, or retained for team history.
5. **Improve the real-time diagram.** The diagram could distinguish the HTTP request path, WebSocket connection path, and notification-provider path more clearly. The current diagram is adequate but intentionally high-level.
6. **Add operational quality attributes.** Expected availability, response-time targets, backup/restore expectations, and monitoring responsibilities could make the ADR more actionable, although exact values are not present in the requirements.

## Discussion questions for refinement

The next review should decide whether these optional details belong in the ADR or should remain implementation-level documentation:

- Should direct notification delivery remain the accepted initial choice, or should the ADR select a transactional outbox from the beginning?
- Which concurrency policy should apply to simultaneous edits of the same shared event?
- What exact deletion policy should apply to private data, chat messages, event responses, and poll votes?
- Should security and quality-attribute constraints be added now despite the requirements not giving numeric targets?
- Is the current high-level diagram sufficient, or should it be replaced with a more detailed request and real-time data-flow diagram?

## Refinement decisions

The review kept direct notification delivery for the initial scope. The ADR should preserve its warning that direct delivery is not atomic with the database transaction and should document the transactional-outbox migration path rather than silently presenting direct delivery as fully reliable.

The concurrency policy is refined to **optimistic locking**: an event update includes the version observed by the editor, and a stale update is rejected so one administrator cannot silently overwrite another administrator's change.

The account-deletion policy is refined to **delete private data and anonymize shared history**. Credentials, private profile data, and private tasks should be deleted where possible. Shared chat history, event responses, or poll participation may need anonymization to preserve team history and referential integrity; the exact entity-level rules still belong in the implementation design.

Security principles should be added to the ADR, especially resource-level authorization, team membership and administrator checks, and authorization of WebSocket subscriptions. Numeric quality targets should not be invented because the requirements do not provide them.

The current diagram is considered good enough. It is intentionally high-level and does not need another visual revision.

## ADR format assessment

The ADR already follows a valid and informative structure:

1. **Title and metadata:** identifies the decision, status, date, and owners.
2. **Context:** explains Teamify, scale assumptions, consistency needs, and considered alternatives.
3. **Decision:** states the modular-monolith and relational-database choice.
4. **Decision matrix:** provides a quick comparison.
5. **Requirement coverage:** connects Teamify capabilities to modules.
6. **Architecture view:** shows the main components and data flow.
7. **Alternatives considered:** explains why microservices, primary serverless, and a distributed hybrid were rejected.
8. **Consequences:** records benefits, costs, and risks.
9. **Validation and review triggers:** defines when the decision should be reconsidered.

Standard ADR formats do not require one universal set of headings. The current structure is therefore not missing a mandatory section. A useful optional refinement would be a short **Decision drivers and assumptions** section before the decision matrix. It would summarize the facts that make the decision appropriate: small-to-medium scale, online web use, relational consistency needs, no confirmed independent team ownership, and no numeric availability or throughput target.

The ADR should avoid adding speculative technologies, numeric service-level objectives, or detailed schema design. Those belong in implementation and operations documentation rather than in this architecture decision.

## Final refinement and outcome

The final refinement was approved and applied to the ADR:

- Added a concise decision-drivers and assumptions section.
- Added resource-level authorization and WebSocket subscription security principles.
- Selected optimistic locking for concurrent shared-event edits.
- Recorded deletion of private data with anonymization of shared history where necessary.
- Kept direct notification delivery for the initial scope while retaining the outbox migration path.
- Kept the existing high-level component/data-flow diagram because it is sufficient for an ADR.

After this refinement, the ADR is considered complete for Task 2. It is detailed enough to justify the decision and guide implementation, while leaving numeric performance targets, exact data-retention rules, and schema details to later design documents.

## Rejection review backlog

The rejection sections were reviewed separately. They were already sufficient for Task 2 because they named the alternatives, identified Teamify-specific drawbacks, explained why the drawbacks mattered under current assumptions, and included reconsideration triggers.

The review found that the sections could be made more consistent without changing the decision. Each alternative should state:

1. What benefits it would provide.
2. Why those benefits are not currently worth the added complexity.
3. Which concrete costs it introduces for Teamify.
4. When it should be reconsidered.

The ADR was refined accordingly:

- **Microservices** now explicitly acknowledges independent scaling, ownership, and fault isolation before explaining the costs of distributed transactions, stale authorization, agenda composition, account deletion, and operations.
- **Serverless/event-driven** now explicitly acknowledges elastic scaling and real-time fan-out before explaining the need for idempotency, ordering, durable orchestration, local testing, and provider-specific services.
- **Distributed hybrid** is labeled as an additional option beyond the three primary proposals and is explained as combining complexity without a demonstrated requirement. A specific reconsideration condition was added for workloads that later need separate scaling.

The chosen modular monolith was not changed. The refinement improves the fairness and traceability of the rejected alternatives rather than turning them into absolute architectural prohibitions.