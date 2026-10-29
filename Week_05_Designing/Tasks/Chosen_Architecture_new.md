# ADR-001: Choose a modular monolith for Teamify

- **Status:** Accepted
- **Date:** 2026-10-29
- **Decision owners:** Teamify project team

## Context

Teamify is an online application for personal task management and group
collaboration. Its requirements cover account creation, authentication, profile
management, password reset and account deletion; personal tasks and agendas; teams,
membership and administrator roles; shared events and event responses; group chat;
polls and voting; and in-app and real-time notifications.

The architecture decision concerns the initial deployable architecture and data
consistency model. It does not select a programming language, cloud provider, or
detailed database schema.

The most important workflows share authorization and consistency boundaries:

- Users must access and modify their own account and personal tasks.
- Team membership and administrator roles control access to team data and actions.
- Team events, invitations, responses, and completion state must remain coherent.
- Poll voting must prevent invalid or duplicate votes.
- Chat and notifications need near-real-time delivery.
- Account deletion must remove personal data where possible while handling shared
  history deliberately.

The requirements do not provide numeric throughput, latency, availability, or growth
targets. The decision therefore uses the following working assumptions:

- The initial system is small to medium scale.
- It is an online web application; offline operation is not required.
- Relational consistency is more important initially than independent scaling.
- No separate team ownership or deployment independence requirement is established.
- Chat and notifications need near-real-time behavior but can initially share the
  application runtime.

## Decision drivers and assumptions

| Driver | Why it matters | Weight (1-5) | Evidence or assumption |
|---|---|---:|---|
| Delivery and operational simplicity | The requirements describe a broad product but no distributed-operations capability or need | 5 | Assumption based on the stated scope |
| Transactional consistency and data integrity | Membership, roles, event responses, and votes affect shared user-visible state | 5 | User stories 15-31 |
| Workload isolation and independent scaling | Chat and notifications may grow differently from ordinary application requests | 4 | Real-time chat and notifications are explicit goals |
| Authorization and privacy boundaries | Personal data and team-admin actions require resource-level access control and deletion handling | 4 | User stories 1-8 and 15-31 |
| Development, testing, and debugging | The architecture must be practical to build and validate for the initial release | 4 | Assumption; no distributed testing requirement is stated |
| Availability and failure isolation | A shared runtime can affect all features when unavailable | 3 | No availability target is specified |
| Portability and cost predictability | Provider-neutral operation reduces lock-in while requirements are still evolving | 3 | No hosting provider is specified |

## Decision

Teamify will initially be implemented as a **modular monolith with a relational
database**. One deployable application will expose HTTP APIs for ordinary commands
and queries and a WebSocket or equivalent real-time channel for chat and
notifications. Internal modules will communicate through application services and
well-defined domain events rather than freely changing another module's data.

The database will enforce foreign keys, unique membership and vote constraints, and
transactions for operations that must remain consistent. Resource-level
authorization will be applied in application services: authentication alone will
not grant access to personal or team resources.

### Selected architecture

The initial modules are:

- **Identity and account:** registration, login, logout, profile, password reset,
  sessions, and account deletion.
- **Teams and membership:** teams, joining and invitations, membership state, and
  administrator roles.
- **Personal work:** personal tasks and personal agenda queries.
- **Shared work:** team events, event invitations, responses, completion, and shared
  agenda queries.
- **Collaboration:** group chat, polls, votes, and collaboration rules.
- **Notifications:** in-app notifications, notification preferences, and real-time
  delivery.

The relational database is the source of truth for transactional business data.
Creating a shared event and its invitations, changing membership roles, and
recording a vote should be completed in appropriate transactions. Shared-event
updates use optimistic locking: an update includes the version observed by the
editor, and a stale update is rejected rather than silently overwriting another
administrator's change.

The initial notification implementation may deliver directly from the application
request flow. This is not atomic with the database transaction and can delay a
request or lose delivery if a provider fails after the business operation commits.
A transactional outbox and background worker are the planned evolution path if
notification loss, latency, or provider failures become observable.

Account deletion deletes credentials, private profile data, and private tasks where
possible. Shared chat history, event responses, or poll participation may instead
be anonymized when deletion is needed to preserve team history and referential
integrity. Exact entity-level retention rules belong in the implementation design.

## Decision matrix

Scores use `1` for poor fit, `3` for acceptable or conditional fit, and `5` for
strong fit. Weighted totals are the sum of `weight x score`.

| Criterion | Weight | Modular monolith | Microservices | Serverless/event-driven |
|---|---:|---:|---:|---:|
| Delivery and operational simplicity | 5 | 5 | 2 | 3 |
| Transactional consistency and data integrity | 5 | 5 | 2 | 3 |
| Workload isolation and independent scaling | 4 | 3 | 5 | 5 |
| Authorization and privacy boundaries | 4 | 4 | 4 | 4 |
| Development, testing, and debugging | 4 | 5 | 2 | 2 |
| Availability and failure isolation | 3 | 3 | 5 | 4 |
| Portability and cost predictability | 3 | 5 | 2 | 2 |
| **Weighted total** |  | **122** | **85** | **92** |

The modular monolith leads because the highest-weight drivers favor local
transactions and lower operational complexity. Its weaker workload isolation is an
accepted risk, not evidence that chat or notifications cannot scale. The matrix is
dependent on the assumptions that the system is initially small to medium scale and
does not require independently owned deployments. If either assumption changes,
microservices or a serverless/event-driven design may rank higher.

## Requirement coverage

| Requirement group | Responsible boundary | Key invariant or behavior |
|---|---|---|
| Registration, login, logout, profile, password reset, and account deletion | Identity and account | Credentials and personal data are protected; deletion revokes access |
| Personal tasks and personal agenda | Personal work | Resource ownership is checked for every operation |
| Teams, joining, invitations, leaving, and administrator roles | Teams and membership | Membership and role transitions are transactionally valid |
| Shared events, invitations, responses, completion, editing, and deletion | Shared work | Team membership and administrator authorization are checked; stale edits are rejected |
| Group chat and real-time messages | Collaboration | Only authorized team members or conversation participants can send or receive |
| Poll creation, voting, and result viewing | Collaboration | Administrator creation and one-vote constraints are enforced |
| In-app and real-time notifications | Notifications | Notifications remain available in-app even if real-time delivery fails |
| Cross-cutting authorization and privacy | Application services plus database constraints | Authentication is separate from resource-level authorization |

## Component and data-flow view

```text
                  +----------------------+
                  |      Web client      |
                  +----------+-----------+
                             |
                    HTTP API + WebSocket
                             |
                  +----------v-----------+
                  |   Teamify monolith   |
                  |----------------------|
                  | Identity & account   |
                  | Teams & membership   |
                  | Personal work        |
                  | Shared work          |
                  | Collaboration        |
                  | Notifications        |
                  +----+------------+----+
                       |            |
                 SQL transactions  | delivery attempt
                       |            v
               +-------v------+  +----------------------+
               | Relational   |  | WebSocket, email,    |
               | database     |  | or push targets      |
               +--------------+  +----------------------+
```

For example, creating a team event first verifies the administrator's membership
and role, then persists the event and invitations in a database transaction. After
the transaction succeeds, the application creates notifications and attempts
real-time delivery. A delivery failure must not undo the committed event; the
notification remains available in the in-app notification section and can later
move to an outbox-based retry flow.

## Alternatives considered

### Microservices

**Benefits:** Identity, teams, shared work, chat, polls, and notifications could be
independently deployed and scaled. Service-owned data would enforce ownership
boundaries, and separate teams could release capabilities independently.

**Why not selected now:** The current requirements do not establish independent
team ownership, sustained monolith bottlenecks, or a high-availability requirement
that outweighs distributed-systems complexity. Teamify's consistency-sensitive
workflows are better served initially by local relational transactions.

**Costs and risks:** A complete agenda would require API composition or a replicated
read model. Account deletion would become a retryable saga. Events would need
idempotency, ordering, schema versioning, retries, tracing, and contract testing.
Membership and authorization state could be temporarily stale between services.
Operating several deployments, databases, a broker, and distributed observability
would increase development and operational burden.

**Reconsider when:** Separate teams need independent ownership or deployment,
chat or another workload causes sustained monolith bottlenecks, or fault isolation
and availability requirements become explicit.

### Serverless/event-driven architecture

**Benefits:** Managed functions and services can provide elastic scaling, scheduled
processing, notification fan-out, and real-time delivery with less server
management. It can be particularly useful for reminders and background work.

**Why not selected now:** Applying short-lived distributed handlers to every core
operation would make membership, event responses, voting, and account deletion
depend on durable workflows rather than straightforward relational transactions.
The requirements do not currently justify the additional provider and workflow
complexity.

**Costs and risks:** Every handler must tolerate retries and duplicate delivery.
Ordering, authorization changes, and multi-step deletion require explicit state and
durable orchestration. Local debugging and testing become harder because queues,
triggers, permissions, and managed WebSocket behavior must be reproduced. Provider
specific databases, queues, identity, and WebSocket services can increase lock-in
and make costs less predictable.

**Reconsider when:** Background notifications, scheduled reminders, or chat fan-out
demonstrate a clear need for elastic independent processing, or managed operations
become more valuable than portability and straightforward local testing.

### A bounded hybrid from the start

This is not one of the three primary candidates, but it is a relevant extension
option. A central application could be combined immediately with independently
managed chat, notification, queue, or data services.

**Benefits:** It could isolate a known high-load real-time workload while retaining
centralized transactional workflows.

**Why not selected now:** No current requirement identifies a workload that needs
separate deployment or scaling. Starting with the hybrid would introduce network
boundaries, service credentials, replication, and operational tooling before the
need is demonstrated.

**Costs and risks:** It combines much of the complexity of distributed alternatives
with less clear benefit, especially around authorization propagation and consistency
between the monolith and external services.

**Reconsider when:** Chat or notifications have measured workload or reliability
requirements that justify separate scaling while the remaining capabilities still
benefit from the monolith's transactions.

## Consequences

### Benefits

- One deployable system is proportionate to the stated initial scope.
- Relational transactions simplify membership, role, event, response, and voting
  rules.
- Combined personal and team agenda queries are straightforward.
- Local development, debugging, testing, and deployment are simpler than with
  distributed alternatives.
- Explicit module boundaries preserve a path to extract a high-load capability.

### Costs and risks

- A deployment or database failure can affect all features.
- Chat and ordinary requests share the application unless the runtime is scaled
  deliberately.
- Direct notification delivery can slow requests or lose delivery after a
  successful database operation.
- Module boundaries are initially enforced by code review and tests rather than
  separate deployments.
- Shared-data deletion and anonymization need explicit entity-level policy.

### Mitigations and evolution path

- Apply resource-level authorization and automated tests for personal and team
  access.
- Use optimistic locking for shared-event edits.
- Keep notification records independent of real-time delivery and introduce a
  transactional outbox and worker when delivery reliability requires it.
- Keep module interfaces and data ownership explicit so Chat or Notifications can
  later be extracted behind stable contracts.
- Define backup, restore, monitoring, retention, and exact deletion behavior in
  implementation and operations documentation.

## Validation and review triggers

Before implementation, validate:

- Authorization for every personal, team, administrator, and WebSocket operation.
- Concurrent shared-event edits and stale-version rejection.
- Account deletion, private-data removal, and shared-history anonymization rules.
- Notification behavior when the delivery provider is slow or unavailable.
- Database constraints for memberships, event responses, and votes.

Review this decision if:

- Chat or WebSocket load affects ordinary account, team, or task operations.
- Notification failures or latency become user-visible.
- Separate teams need independent ownership or deployment.
- Agenda queries or database contention prevent required behavior.
- Availability, compliance, data-isolation, or scale requirements exceed the
  modular monolith's capabilities.

## Open implementation questions

- Which relational database and application framework will be used?
- What exact entity-level retention or anonymization rules apply after account
  deletion?
- What notification provider and retry policy will be used?
- What operational monitoring, backup, and restore procedures are required?
- Which WebSocket protocol and client reconnection behavior will be implemented?