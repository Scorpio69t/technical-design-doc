# Architecture Writing Rules

## Start from boundaries

Architecture prose should make boundaries visible. A useful boundary has at least one of these properties:

- independent responsibility;
- independent data ownership;
- independent lifecycle/deployment;
- different scaling characteristics;
- different trust/security boundary;
- different failure domain;
- clear domain ownership.

Do not split a system merely because two classes or packages can be named separately.

## Canonical vocabulary

Maintain a small canonical inventory during drafting.

| Type | Example fields |
|---|---|
| System | canonical name, purpose, owner |
| Service/container | name, responsibility, deployment unit, owned data |
| Module/component | name, responsibility, parent service |
| Store | name, owner, data type |
| Event/queue | name, producer, consumer, delivery semantics |
| External system | name, protocol, dependency criticality |

Do not use `User Service`, `Account Service`, and `Identity Service` interchangeably unless they are genuinely different things.

## Responsibility statement

For every important service or module, document:

- **Owns:** business state/capability it controls.
- **Does not own:** adjacent concerns that might otherwise be ambiguous.
- **Calls:** dependencies and why.
- **Called by:** upstream callers.
- **Persists:** stores/tables/entities it owns.
- **Publishes/subscribes:** asynchronous contracts.
- **Failure behavior:** what happens when dependencies are unavailable.

## Dependency direction

Prefer dependencies that follow ownership rather than convenience.

A module should not read another service's database because a join is convenient. If cross-domain data is required, use an API, event-derived local projection, shared platform capability, or an explicitly governed shared store.

Flag circular service dependencies. If A synchronously requires B and B synchronously requires A for the same request path, redesign or document a compelling reason.

## Runtime path writing

For each critical runtime path, include:

1. trigger;
2. authentication/authorization point;
3. validation;
4. durable state change;
5. synchronous dependencies;
6. asynchronous handoff;
7. success response semantics;
8. timeout/failure behavior;
9. retry/idempotency behavior;
10. observability signals.

## State and transactions

Whenever a design changes durable state, explain the transaction boundary.

Questions to answer:
- which writes are atomic;
- what is committed before external calls;
- whether events are transactional with state changes;
- how partial failure is reconciled;
- whether compensation exists;
- what concurrency control is used;
- what invariant prevents duplicate or conflicting state.

## Asynchronous work

For queues/events/jobs, document at least:

- producer and consumer;
- message/event name;
- when it is emitted;
- delivery assumption (`at-most-once`, `at-least-once`, or effectively-once behavior built above the broker);
- idempotency key;
- ordering assumptions;
- retry policy;
- poison/dead-letter handling;
- schema/version compatibility;
- correlation/trace context.

Do not claim “exactly once” unless the system actually provides end-to-end exactly-once semantics.

## Data ownership

For each persistent dataset, make one component the owner unless the architecture explicitly uses a shared-database model.

Document:
- system of record;
- read/write owner;
- replication/projections;
- retention;
- encryption or sensitivity constraints;
- deletion lifecycle;
- migration ownership.

## Failure domains

Design documents become useful when they explain degradation.

For every remote dependency, consider:
- timeout;
- retry;
- circuit breaking or admission control;
- fallback;
- queueing/buffering;
- partial response;
- stale-cache behavior;
- operational alerting.

Do not blindly prescribe every resilience pattern. State only mechanisms justified by the path and failure cost.

## Architecture rationale

Record rationale when a future maintainer might reasonably ask “why not the simpler alternative?”

Good rationale connects choice to a constraint:

> Indexing is asynchronous because model execution can exceed the API latency budget and consumes independently scalable GPU/CPU resources.

Weak rationale repeats preference:

> Asynchronous processing is more flexible and scalable.

## Level of detail

Use the lowest level that changes an engineering decision.

Do not document every utility class. Do document components that own state, define contracts, change failure boundaries, contain important algorithms, or are assigned to different teams/deployment units.
