# Detailed Design Quality Gate

Use this as the final review. Mark an item `N/A` only when it genuinely does not apply.

## Scope and traceability

- [ ] Scope is explicit.
- [ ] Non-goals prevent accidental expansion.
- [ ] Important assumptions are labeled.
- [ ] Existing constraints and systems are preserved.
- [ ] Open issues are distinguishable from committed decisions.

## Architecture

- [ ] System context is understandable without internal implementation detail.
- [ ] Service/container boundaries have clear responsibility.
- [ ] Data ownership is explicit.
- [ ] Dependency direction is intentional.
- [ ] No accidental circular synchronous dependency exists.
- [ ] External systems are clearly separated from owned systems.
- [ ] Architecture views use consistent naming.

## Runtime behavior

- [ ] Critical success paths are documented.
- [ ] Material failure paths are documented.
- [ ] Sync vs async interactions are clear.
- [ ] Timeout behavior is defined where remote calls matter.
- [ ] Retry behavior is defined where retry is safe/useful.
- [ ] Idempotency is defined for duplicate-prone writes/events.
- [ ] Concurrency control is defined for conflicting updates.
- [ ] Long-running tasks have durable state or an explicit reason not to.

## Transactions and consistency

- [ ] Transaction boundaries are explicit for multi-write operations.
- [ ] External calls are not accidentally assumed atomic with DB commits.
- [ ] Event publication consistency is addressed where state + event must agree.
- [ ] Eventual consistency windows are acknowledged where applicable.
- [ ] Compensation/reconciliation exists for important partial failures.

## Data

- [ ] System of record is clear for important entities.
- [ ] Key identifiers and uniqueness constraints are clear.
- [ ] State/enum values match the behavioral design.
- [ ] Retention/deletion requirements are addressed where relevant.
- [ ] Sensitive data is identified and protected appropriately.
- [ ] Schema evolution/migration is addressed for existing systems.

## API and events

- [ ] API ownership and versioning are clear.
- [ ] Authentication and authorization boundaries are clear.
- [ ] Validation and error semantics are documented.
- [ ] Events identify producer, consumer, trigger, and delivery assumptions.
- [ ] Event schema compatibility is considered.

## Security

- [ ] Trust boundaries are visible.
- [ ] Secrets are not embedded in documents/examples.
- [ ] Least-privilege access is described where material.
- [ ] Tenant isolation is explicit for multi-tenant systems.
- [ ] Audit requirements are covered where material.

## Observability and operations

- [ ] Critical operations have logs/metrics/traces or explicit monitoring signals.
- [ ] Correlation/trace identifiers cross service boundaries where useful.
- [ ] Failure alerts map to actionable conditions.
- [ ] Deployment topology is understandable.
- [ ] Configuration and secrets are externalized appropriately.
- [ ] Rollback/recovery is addressed for risky changes.
- [ ] Health checks distinguish liveness/readiness when necessary.

## Performance and scale

- [ ] Performance targets are stated when they drive design.
- [ ] Expensive paths and bottlenecks are identified.
- [ ] Stateful components and scaling limits are known.
- [ ] Caches include ownership/TTL/invalidation rationale when used.
- [ ] Queues have backpressure/capacity considerations when relevant.

## Diagram quality

- [ ] Every diagram answers one primary question.
- [ ] Diagrams stay within a reasonable node/participant budget.
- [ ] Edge crossings are limited.
- [ ] Colors/styles have stable semantics.
- [ ] Important diagrams have a reading guide.
- [ ] Diagrams and prose agree.
- [ ] The same abstraction level is not mixed excessively in one view.

## Human readability

- [ ] The document does not read like an agent work log.
- [ ] Filler and generic AI phrasing have been removed.
- [ ] Important decisions are written directly.
- [ ] Rationale explains constraints/tradeoffs rather than using adjectives.
- [ ] Bullet walls are replaced with prose/tables where appropriate.
- [ ] Headings support navigation.
- [ ] A reviewer can quickly find ownership, failure, transaction, and state behavior.
