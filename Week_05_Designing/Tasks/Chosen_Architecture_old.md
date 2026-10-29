# ADR-001: Choose a modular monolith for Teamify

- **Status:** Accepted
- **Date:** 2026-10-29
- **Decision owners:** Teamify project team

## Context

Teamify is an online web application for personal and team collaboration. It must support account management, personal tasks and agendas, teams and role management, shared events, event responses, group chat, polls, voting, and real-time notifications.

The project is expected to be small to medium scale. Its most important consistency boundaries are user access, team membership and administrator roles, shared events, event responses, and poll votes. Chat and notification delivery need near-real-time behavior, but the requirements do not currently establish a need for independent service scaling, offline operation, or very high availability.

Three architectures were considered:

1. A modular monolith.
2. Independently deployed microservices.
3. A serverless/event-driven system built primarily from managed functions and services.

## Decision

Teamify will be implemented as a **modular monolith** with a **relational database**.

The initial deployable application will contain explicit modules for:

- Identity and account management.
- Teams, memberships, invitations, and administrator roles.
- Personal tasks and agendas.
- Shared team events and event responses.
- Chat, polls, and votes.
- Notifications and notification preferences.

The modules will communicate through application services and well-defined internal domain events. They must not bypass module boundaries by freely changing another module's data. The relational database will enforce foreign keys, unique membership and vote constraints, and transactional updates for operations that must remain consistent.

The web client will use HTTP APIs for ordinary commands and queries. WebSockets may be used for chat and real-time notification delivery. The first implementation will deliver notifications directly from the application request flow because this is the selected simple approach for the current project. This choice must be revisited if delivery latency, provider failures, or lost notifications become observable; a transactional outbox and background worker is the planned evolution path.

Authorization is enforced at the resource level, not only at the route level. Team operations must verify membership and administrator roles, personal operations must verify resource ownership, and WebSocket subscriptions must verify access to the relevant team or conversation. The application will use optimistic locking for shared-event updates so a stale edit is rejected instead of silently overwriting another administrator's change.

Account deletion will delete credentials, private profile data, and private tasks where possible. Shared chat history, event responses, and poll participation may be anonymized rather than deleted when needed to preserve team history and referential integrity. The exact entity-level retention rules must be defined before implementation.

## Decision drivers and assumptions

This decision is based on the following assumptions:

- Teamify is a small-to-medium-scale online web application.
- Relational consistency is more important initially than independent scaling.
- No confirmed requirement currently calls for separate team ownership, offline operation, or very high availability.
- The project has no numeric throughput, latency, or availability targets yet.
- Chat and notifications need near-real-time behavior, but can initially share the monolith's runtime.

## Decision matrix

| Criterion | Modular monolith | Microservices | Serverless/event-driven |
|---|---|---|---|
| Fit for current Teamify scale | Strong; one deployable system is proportionate | Weak initially; operational cost is high without a scaling or ownership need | Partial; managed scaling helps, but core workflows become distributed |
| Membership, events, and voting consistency | Strong relational transactions | Requires cross-service coordination and eventual consistency | Requires conditional writes and durable workflows |
| Chat and notification scaling | Shared runtime; can be scaled deliberately | Strong independent scaling | Strong managed fan-out and elastic scaling |
| Agenda queries | Simple relational queries and joins | API composition or a replicated read model | Projections or multiple reads are needed |
| Account deletion | One application workflow can coordinate cleanup | Saga and retries across services | Durable orchestration and retries across functions |
| Development and operations | Lowest complexity | Highest complexity: services, broker, tracing, and contracts | Moderate infrastructure work but more provider coupling |
| Current decision | **Selected** | Rejected for now | Rejected as the primary architecture |

## Requirement coverage

| Teamify requirement group | Responsible module or boundary |
|---|---|
| Registration, login, logout, profile, password reset, and account deletion | Identity and account management |
| Personal tasks and personal agenda | Personal tasks and agendas |
| Teams, joining, invitations, leaving, and administrator roles | Teams and membership |
| Shared events, invitations, responses, completion, editing, and deletion | Shared team events and event responses |
| Group chat and real-time messages | Chat |
| Poll creation, voting, and result viewing | Polls and votes |
| In-app and real-time notifications | Notifications and notification preferences |
| Authorization across personal and team data | Application services plus relational membership constraints |

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
                  | Identity             |
                  | Teams & membership   |
                  | Tasks & agendas      |
                  | Events & responses   |
                  | Chat, polls & votes  |
                  | Notifications        |
                  +----+------------+----+
                       |            |
                 SQL transactions  | direct notification delivery
                       |            v
               +-------v------+  +----------------------+
               | Relational   |  | Email/push/WebSocket |
               | database     |  | notification targets |
               +--------------+  +----------------------+
```

For example, creating a team event is authorized by the Teams and Events modules, persisted with its invitations in a database transaction, and then used to trigger notification delivery. The event, invitations, and authorization state are consistent at commit time. Direct notification delivery is not guaranteed to be atomic with the database transaction.

## Alternatives considered and rejected

### Microservices

Microservices would separate Identity, Teams, Work, Chat, Polls, and Notifications, with service-owned databases and a message broker.

Microservices would provide genuine benefits: Chat and Notifications could scale independently, separate teams could own and deploy services, and failures could be isolated more precisely. They were rejected for the initial version because Teamify is small to medium scale and there is no confirmed need for those benefits to outweigh the distributed-systems cost.

The main costs for Teamify would be:

- A complete agenda would need API composition or a replicated read model.
- Account deletion would require a retryable cross-service workflow.
- Membership and authorization state could be temporarily stale in another service.
- Events would require idempotency, ordering rules, schema versioning, retries, tracing, and operational tooling.
- Relational transaction boundaries would be replaced by coordination across service databases.
- The team would need to operate a broker, multiple deployments, service contracts, distributed logs, metrics, and tracing.

Microservices should be reconsidered if the project gains independently owned teams, substantially different scaling needs, sustained monolith bottlenecks, or a strong fault-isolation requirement.

### Serverless/event-driven as the primary architecture

Serverless functions and managed queues/WebSockets would scale automatically and fit notifications, reminders, and chat fan-out.

Those are meaningful benefits for Teamify's background and real-time workloads. They were rejected as the primary architecture because applying short-lived, distributed handlers to every core operation would make membership changes, event responses, votes, and account deletion depend on durable workflows rather than straightforward relational transactions.

The main costs would be:

- Every handler would need idempotency and conditional writes to survive retries and duplicate delivery.
- Event ordering and authorization changes would need explicit handling.
- Multi-step account deletion and invitation flows would need durable orchestration and progress tracking.
- Local debugging and testing would require reproducing queues, triggers, permissions, and managed WebSocket behavior.
- Provider-specific queues, identity, databases, and WebSocket services would increase lock-in and complicate migration.

Serverless or event-driven components may be introduced later for background notifications, scheduled reminders, or chat delivery if those workloads justify their operational and provider costs.

### Distributed hybrid from the start

This extra option combines a monolith with independently managed real-time, queue, or data services from the beginning. It could provide specialized scaling while preserving a central core, but it would introduce network boundaries, service credentials, replication concerns, and operational tooling before Teamify has demonstrated a need for them. It is not selected because it combines much of the complexity of the rejected alternatives without a clear additional benefit at the current scale.

It should be reconsidered only if one workload, such as Chat or Notifications, demonstrates a clear need for separate scaling while the remaining capabilities still benefit from monolithic transactions.

## Consequences

### Benefits

- One deployable system is appropriate for the expected project scale.
- Relational transactions simplify membership, role, event, response, and voting rules.
- Cross-feature workflows and combined agenda queries are easier to implement and test.
- Local development, debugging, deployment, and monitoring are simpler than with distributed alternatives.
- Explicit module boundaries leave a path to extract a high-load capability later.

### Costs and risks

- A deployment or database failure can affect all features.
- Chat and ordinary requests share the application unless the runtime is scaled deliberately.
- Direct notification delivery can slow requests or lose delivery when a provider fails after the database operation succeeds.
- Module boundaries are conventions enforced by code review and tests rather than separate deployments.
- A later extraction of Chat or Notifications will require defining service contracts and dealing with data migration and eventual consistency.

## Validation and review triggers

The decision should be reviewed when any of these occur:

- Chat or WebSocket load affects task, account, or team operations.
- Notification failures or latency become user-visible.
- Separate teams need to deploy or own capabilities independently.
- Agenda queries or database contention prevent the required performance.
- Availability, compliance, or data-isolation requirements exceed the monolith's capabilities.

Before implementation, the team should define authorization tests, concurrency behavior for simultaneous event edits, the account-deletion policy for shared content, and monitoring for notification failures.