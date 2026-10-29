# Teamify architecture discussion

## Requirements understood

Teamify is a collaborative task and team-management application. Its core capabilities are:

- Account creation, login/logout, profile editing, password reset, and account deletion.
- Personal tasks and a personal agenda.
- Teams, invitations or joining, membership management, administrator promotion/demotion, and leaving a team.
- Team agendas with shared events that can be created, edited, completed, deleted, and accepted or refused by invited users.
- Team chat with real-time message delivery.
- Notifications, including real-time delivery.
- Administrator-created polls, member voting, and result viewing.

The design must enforce authorization boundaries: users may manage their own data, while team administrators may manage only the teams and shared content for which they have authority. Chat, notifications, polls, and event responses introduce concurrent updates and real-time delivery requirements.

## Candidate architecture 1: Modular monolith

A single deployable backend would contain clear modules such as Identity, Users, Teams, Tasks/Events, Chat, Polls, and Notifications. The modules would share one relational database but communicate through explicit application interfaces and internal domain events. A web or mobile client would call a REST or GraphQL API; WebSockets or Server-Sent Events would provide chat and notification updates.

**Advantages**

- Lowest operational and development complexity for an initial version.
- Transactions are straightforward for operations such as creating an event and its invitations, changing team roles, or recording a vote.
- A relational database can enforce foreign keys, unique membership constraints, and vote rules.
- Modules can still be tested and extracted later if boundaries remain explicit.

**Costs and difficult implementation points**

- The deployment is a shared failure and scaling unit; chat traffic can affect ordinary task operations.
- The codebase needs discipline to prevent modules from directly reaching into each other's data.
- Real-time connections and background notification delivery must be managed inside or alongside the monolith.
- Account deletion and privacy rules require careful cleanup or anonymization across all modules.

## Candidate architecture 2: Microservices

Separate services would own Identity, Team/Membership, Tasks/Events, Chat, Polls, and Notifications. Each service would own its data. An API gateway would expose a unified client API, while a message broker would distribute domain events such as `UserDeleted`, `TeamMemberAdded`, `EventCreated`, and `PollClosed`.

**Advantages**

- Chat and notification workloads can scale independently from task and account operations.
- Data ownership and service boundaries can be enforced technically.
- Individual services can be deployed or changed independently.

**Costs and difficult implementation points**

- A single user action may span multiple services, so distributed transactions and eventual consistency become unavoidable.
- Creating an event, inviting members, and notifying them needs retries, idempotency, and an outbox or equivalent reliable event-publishing mechanism.
- Reads such as “show my complete agenda with team events” require API composition or read models.
- Authentication, authorization propagation, observability, deployment, service discovery, and contract versioning add significant complexity.
- Account deletion becomes a distributed workflow and cannot be treated as one simple database transaction.

## Candidate architecture 3: Serverless/event-driven architecture

The API would be implemented with managed functions or containerized functions, while managed services would provide a relational or document database, a pub/sub broker, WebSockets, scheduled jobs, and notification delivery. Commands such as creating a task or voting would invoke functions; events would trigger notifications, projections, and other asynchronous work.

**Advantages**

- Automatic scaling and low infrastructure management overhead.
- Event-driven notifications and background processing fit naturally.
- Infrequent operations such as password reset, invitations, and poll closing can be cost-efficient.
- Real-time and scheduled capabilities can use managed platform services.

**Costs and difficult implementation points**

- Cold starts, execution limits, retries, duplicate delivery, and ordering must be handled explicitly.
- Debugging a workflow distributed across functions and managed services is harder.
- Queries that combine personal and team agendas need carefully designed projections or multiple data reads.
- Strong consistency for membership changes, authorization, event responses, and votes still requires transactional storage or conditional writes.
- The design becomes coupled to cloud-provider services and may be harder to run locally or migrate.

## Initial comparison

For a first release with 31 user stories, the modular monolith is the most proportionate choice: it supports relational consistency and keeps authentication, authorization, and data lifecycle manageable. Microservices become more attractive if independent scaling, organizational team ownership, or very high chat volume is already a known requirement. Serverless is attractive when managed cloud operations and elastic, event-driven workloads are more important than portability and straightforward local debugging.

The next discussion should test these assumptions, especially expected scale, offline behavior, privacy/account deletion semantics, consistency requirements for chat and votes, and the team's ability to operate distributed infrastructure.

## Discussion assumptions

The purpose of this exercise is to discuss all three proposals and expose their trade-offs; it is not necessary to choose a final architecture before the comparison is understood. Teamify is expected to be a small-to-medium-scale project and an online web application. The exact real-time consistency policy is intentionally left open for later discussion. Account deletion will probably need mixed rules: some personal data may be deleted while historical team content may need anonymization or retention.

## Deep dive 1: modular monolith

### A possible internal structure

The backend can be one deployable application with separate modules:

- Identity and Account: registration, sessions/tokens, password reset, profile data, and account deletion.
- Team and Membership: teams, invitations, membership state, administrator roles, and authorization checks.
- Personal Work: personal tasks and the personal agenda.
- Shared Work: team events, event responses, completion state, and shared agenda queries.
- Collaboration: chat messages, polls, votes, and notification preferences.
- Notification Delivery: an internal event handler plus a worker for email, in-app notifications, and WebSocket delivery.

The modules should expose application services rather than directly modifying another module's tables. A relational database would store users, teams, memberships, tasks, events, event responses, messages, polls, votes, and notifications. Foreign keys and unique constraints could prevent invalid memberships, duplicate votes, and duplicate event responses.

### Example request flow

When an administrator creates a team event, the Shared Work module would check the caller's membership and administrator role, create the event and invitation records in one transaction, and publish an internal `EventCreated` event after the transaction succeeds. Notification Delivery would consume that event and create in-app notification records, then attempt real-time delivery. If real-time delivery fails, the notification remains available in the notification section and can be retried.

### Painful implementation details

- Authorization must be checked at the resource level, not only at the route level. A user must not modify an event merely because they are authenticated.
- WebSocket connections are stateful while the rest of the application may be stateless. Multiple application instances need a shared pub/sub mechanism so a notification created on one instance reaches a client connected to another.
- Notification work should not run inside the request transaction. An outbox table or durable job queue is needed so a database commit cannot succeed while the notification event is silently lost.
- Agenda queries must combine personal tasks with team events while applying membership and event-response rules efficiently. Indexes and pagination become important even at moderate scale.
- Concurrent updates need explicit rules. Two administrators editing an event need optimistic version checks or a documented last-write-wins policy; two votes from the same user must be prevented by a database constraint.
- Account deletion is not one uniform `DELETE`: credentials and private profile data may be removed, while messages or votes may be anonymized to preserve team history and referential integrity.

### Main trade-off

The modular monolith keeps transactions, debugging, and local development understandable, but it relies on code-level module boundaries and shares its runtime and database. It is simpler than the other proposals only if the team takes the internal boundaries and asynchronous notification path seriously.

### Questions for discussion

1. Would you prefer an outbox table plus a background worker for notifications, or direct notification delivery in the request? The direct approach is simpler but can lose notifications or slow down user actions.
2. For simultaneous edits to the same event, should the system reject the second stale update, or silently use last-write-wins?
3. Should deleted users' chat messages and poll votes be anonymized so team history remains understandable, while credentials and private profile data are permanently deleted?

### Discussion response

The discussion emphasized that a monolith is one complete system: adding a feature can be easier because the related code is in one place, but the same shared location can make the system harder to change and can concentrate failures. Direct notification delivery was selected as the simplest option to discuss first. Its drawback is important: if delivery happens inside the request, a slow or unavailable notification provider can delay the user action, and a failure after the business operation can lose the notification. A production design would likely need retries or an outbox even if the first version starts with direct delivery.

For concurrent event edits, the comparison should present multiple policies rather than assume one:

- **Optimistic locking:** store a version or update timestamp and reject a stale edit. This protects data but requires the client to reload and resolve the conflict.
- **Last-write-wins:** accept the latest update. This is easy to implement but can silently overwrite another administrator's change.
- **Manual conflict resolution:** show both versions and require a user to merge them. This preserves intent but adds substantial UI and domain complexity.

For account deletion, the preferred initial direction is to delete personal data wherever possible. This must still define exceptions for shared records: deleting a chat message or vote may be required for privacy, but doing so can leave a confusing team history or alter poll results. The policy therefore needs to be specified per entity instead of using one global delete rule.

## Deep dive 2: microservices

### A possible service structure

Identity, Teams, Work, Chat, Polls, and Notifications would be independently deployable services. Each service would own its database and expose APIs or events rather than allowing another service to query its tables. An API gateway would authenticate requests and route client calls. A broker would carry events such as `MemberJoined`, `EventCreated`, `EventResponseChanged`, `MessageSent`, `VoteRecorded`, and `UserDeletionRequested`.

### Example cross-service flow

When a team administrator creates an event, the Work service first validates the membership information it knows locally and commits the event. It then publishes `EventCreated`. The Notifications service consumes the event and creates notifications. The Chat or presence layer may separately notify connected clients. If Team membership changes at the same time, each service may temporarily have a different view of authorization unless events are ordered and consumed promptly.

### Painful implementation details

- A request such as deleting a user crosses Identity, Teams, Work, Chat, Polls, and Notifications. There is no single transaction, so the system needs a saga, retryable commands, idempotency keys, and a way to report partial completion.
- The complete agenda is not stored in one database. The API gateway must compose results from several services, or a read-model service must subscribe to changes and accept eventual consistency.
- Events can be duplicated, delayed, or delivered out of order. Consumers must be idempotent and often store processed-event identifiers.
- Service-to-service authorization is separate from end-user authentication. A valid service call must still be constrained so one service cannot perform arbitrary operations on behalf of a user.
- Network failures become normal application cases. Timeouts, retries, circuit breakers, tracing, schema versioning, and contract tests are required.
- A chat service can scale independently, but operating a broker, several databases, deployment pipelines, logs, metrics, and distributed tracing is a large burden for a small-to-medium project.

### Main trade-off

Microservices offer independent scaling and stronger technical ownership boundaries, but they replace local consistency with distributed coordination. The architecture is justified when independent team ownership, very different scaling needs, or high availability requirements outweigh the operational and implementation cost.

### Discussion response

The strongest possible justification identified was independent ownership by separate teams, rather than Teamify's current scale alone. Chat is a good candidate for event-driven processing, but synchronization between services is difficult because events can be delayed, duplicated, or observed in a different order.

For combined agenda reads, a shared reporting/read database was considered. This can simplify queries across service-owned data, but it weakens strict ownership boundaries and introduces a data replication pipeline that must handle stale or missing records. An eventually consistent read model would preserve stronger ownership, while gateway composition would avoid replication at the cost of slower and more failure-prone reads.

For account deletion, blocking until every service confirms cleanup appears safer from a rights perspective, but access revocation and data cleanup should be separated:

1. Identity should immediately disable the account, revoke sessions/tokens, and prevent new access.
2. Team membership and authorization projections should immediately mark the user inactive.
3. A tracked saga can then delete or anonymize data in each service, retry failures, and expose completion status.

This prevents a deleted or malicious account from retaining access while avoiding an unavailable system when one cleanup service is temporarily down. If legal or product requirements demand all data be removed before reporting completion, the saga can keep the deletion request pending without restoring access.

## Deep dive 3: serverless/event-driven

### A possible structure

HTTP functions would implement account, task, team, event, poll, and query commands. Managed storage would hold transactional data, a pub/sub or queue service would carry domain events, and managed WebSocket or push-notification infrastructure would deliver updates. Scheduled functions could close polls, send reminders, expire invitations, and retry failed notification work.

The architecture can be combined with a relational database for membership and voting constraints and a document or key-value store for high-volume chat messages. The important distinction is that compute is short-lived and event handlers are independently triggered rather than running as one continuously deployed application.

### Example event-driven flow

`CreateEvent` invokes a function that validates the administrator and commits the event. It publishes `EventCreated` to a broker. Separate handlers create invitations, project agenda data, and enqueue notifications. A WebSocket delivery handler sends updates to currently connected clients. If any handler fails, the broker retries it or moves it to a dead-letter queue for inspection.

### Painful implementation details

- Every handler must tolerate retries. Without idempotency keys and conditional writes, one event can create duplicate invitations, notifications, or poll results.
- Event ordering is not automatically guaranteed across partitions or independent functions. A membership-removal event may arrive after an event notification and must still be interpreted safely.
- Short function lifetimes make transactions across multiple steps difficult. Long workflows need durable orchestration or explicit state machines.
- Cold starts and provider limits can affect login, chat, or agenda latency. Real-time connections may require a separate managed gateway rather than ordinary functions.
- Local development and debugging are harder because queues, triggers, permissions, and managed services must be reproduced or mocked.
- Provider-specific queues, WebSocket services, databases, and identity features can make portability and future migration expensive.
- Costs are usage-dependent and less predictable when chat produces many events, retries, or connected-client updates.

### Main trade-off

Serverless/event-driven architecture reduces server and scaling operations and fits notifications, reminders, and chat fan-out well. It does not remove consistency problems: it moves them into idempotent handlers, durable workflows, conditional storage operations, and event-replay tooling.

### Discussion response

The serverless proposal is considered a partial fit: it is especially suitable for notifications, chat fan-out, reminders, password-reset messages, and other background work, while core account, membership, task, event, and poll operations may be easier to keep in transactional services.

Event safety remains an implementation choice to compare:

- **Idempotent handlers and conditional writes:** handlers record event IDs and use unique constraints or conditional updates. This is broadly applicable but requires every consumer to be designed carefully.
- **Ordered streams per team or aggregate:** events for one team are processed in order. This helps membership and event workflows but does not automatically order unrelated aggregates and can reduce throughput.
- **Durable workflow orchestration:** a workflow engine tracks retries, timeouts, compensations, and human-visible progress. This is expressive for account deletion and invitations but adds a platform dependency and operational cost.

## Requirement satisfaction comparison

All three architectures can implement the 31 Teamify user stories. The differences are in how much infrastructure and consistency machinery is needed to implement them safely.

| Requirement area | Modular monolith | Microservices | Serverless/event-driven |
|---|---|---|---|
| Registration, login, logout, profile, password reset | Straightforward in one Identity module and relational database | Supported, but identity tokens and authorization must propagate across services | Supported through managed identity or functions; provider integration and cold starts add complexity |
| Account deletion | One coordinated transaction is possible, with explicit anonymization rules | Requires a saga across services; access must be revoked immediately while cleanup continues | Requires durable orchestration, retries, and status tracking across functions and stores |
| Personal tasks and agenda | Strong transactional consistency and simple joins | Work service supports them, but cross-service agenda reads need composition or a read model | Functions and storage support commands; combined agenda needs projections or multiple reads |
| Teams, invitations, membership, administrator roles | Natural fit for relational constraints and transactions | Supported, but authorization caches and replicated membership state can become stale | Supported with conditional writes and carefully ordered membership events |
| Shared events and event responses | Easy to enforce administrator permissions and event-response uniqueness | Supported, but event creation and invitations are an asynchronous workflow | Supported, but retries and duplicate event handling are mandatory |
| Chat | WebSockets plus shared pub/sub; requires scaling the connection layer | Strong fit for an independently scalable Chat service | Strong fit for managed WebSockets and event fan-out, with provider coupling |
| Polls and votes | Database constraints make one-vote and result consistency straightforward | Supported, but votes and results may use separate services/read models | Supported with conditional writes; duplicate delivery and result projection need care |
| In-app and real-time notifications | Internal events, worker/outbox, and WebSockets; direct delivery is simpler but less reliable | Natural event consumer, but broker operations and retries are required | Natural fit, although duplicate events, dead letters, and delivery status must be managed |
| Authorization and data privacy | Centralized policy enforcement is easiest to reason about | Strong boundaries are possible, but service-to-service authorization is complex | Must be repeated in functions and enforced by storage conditions and token claims |
| Operations and debugging | Lowest operational burden and easiest local testing | Highest burden: deployments, broker, databases, tracing, and contracts | Less server management, but harder local reproduction and provider-specific debugging |

## Final comparison

The requirements do not force one architecture. A modular monolith satisfies every Teamify story with the least distributed-systems complexity, making it the most proportionate baseline for a small-to-medium online project. Its painful parts are internal modularity, WebSocket scaling, reliable notification delivery, and concurrent updates.

Microservices also satisfy every story and are strongest when separate teams need independent ownership or when chat and notifications have very different scaling and availability needs. Their painful parts are distributed authorization, eventual consistency, cross-service account deletion, event contracts, retries, and operational observability. They should not be chosen merely because the application has multiple feature areas.

Serverless/event-driven also satisfies every story and is particularly effective for notification fan-out, reminders, password reset, and chat delivery. Its painful parts are idempotency, ordering, durable workflows, conditional writes, local debugging, and provider lock-in. A partial serverless design, with transactional core operations and event-driven background capabilities, may capture its benefits without forcing every requirement into short-lived functions.

The central architectural decision is therefore not whether a proposal can implement Teamify; all three can. It is whether the project wants to pay complexity in one shared codebase, across distributed services, or in cloud-managed event workflows. The decision should follow expected scale, team ownership, availability goals, and operational capability rather than architectural fashion.