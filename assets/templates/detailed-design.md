# <System / Feature> Detailed Design

> Status: Draft / Review / Approved
> Owners: <team or role>
> Last updated: <YYYY-MM-DD>
> Related requirements: <links/IDs>
> Related ADRs: <links/IDs>

## 1. Overview

### 1.1 Background

Explain the business/technical context in a few paragraphs. Do not restate the entire PRD.

### 1.2 Goals

State concrete design goals.

### 1.3 Non-goals

State what this design intentionally does not change or solve.

### 1.4 Scope

Define affected systems, users, modules, APIs, and environments.

## 2. Constraints and assumptions

| Type | Constraint / assumption | Design impact |
|---|---|---|
| Existing system | | |
| Performance | | |
| Security | | |
| Deployment | | |
| Compatibility | | |

Open assumptions should be labeled and tracked rather than written as fact.

## 3. Architecture

### 3.1 System context

<Structurizr/C4 system-context diagram or equivalent>

**Reading guide**

Explain ownership, external boundaries, and the two to five consequences readers should notice.

### 3.2 Container / service architecture

<Structurizr/C4 container diagram>

**Reading guide**

Explain service responsibilities, data ownership, sync/async boundaries, and important dependency direction.

### 3.3 Component view

Include only for services/modules where decomposition materially affects implementation.

### 3.4 Deployment view

Include when topology, network zones, replicas, runtime placement, or managed infrastructure matter.

## 4. Domain and module design

### 4.1 Responsibility matrix

| Component | Owns | Does not own | Persistence | Important dependencies |
|---|---|---|---|---|
| | | | | |

### 4.2 <Module A>

**Purpose**

<one concise paragraph>

**Responsibilities**

- <responsibility>

**Boundary / non-responsibilities**

- <non-responsibility>

**Interfaces**

- <interface>

**State and persistence**

<what is durable, where, and why>

**Failure behavior**

<timeouts, retries, idempotency, degraded behavior>

**Design rationale**

<why this boundary/approach exists>

## 5. Key runtime flows

### 5.1 <Critical write path>

<PlantUML sequence diagram>

**Reading guide**

Explain transaction point, sync/async handoff, success semantics, and failure boundary.

### 5.2 <Recovery or failure path>

Use a separate diagram when combining it with the normal path would overload the sequence.

## 6. State model

<Mermaid state diagram when lifecycle matters>

| State | Meaning | Entered when | Exit condition |
|---|---|---|---|
| | | | |

State invariants:

- <invariant>

## 7. Data design

### 7.1 Data ownership

| Dataset / entity | System of record | Write owner | Other readers | Retention |
|---|---|---|---|---|
| | | | | |

### 7.2 Core data model

<ER diagram limited to core relationships>

### 7.3 Schema details

Use schema tables or DDL excerpts for implementation detail rather than overloading the ER diagram.

### 7.4 Transactions and consistency

Document:
- atomic writes;
- optimistic/pessimistic concurrency if used;
- outbox/inbox or other state-event consistency mechanism;
- eventual consistency windows;
- reconciliation/compensation.

## 8. API and event contracts

### 8.1 HTTP/RPC APIs

| Method | Path / operation | Owner | Auth | Idempotency | Notes |
|---|---|---|---|---|---|
| | | | | | |

Put full API details in an API appendix or separate API-design document when large.

### 8.2 Events / jobs / messages

| Name | Producer | Consumer(s) | Trigger | Delivery assumption | Idempotency key |
|---|---|---|---|---|---|
| | | | | | |

## 9. Error and resilience design

| Failure | Detection | User/system effect | Retry/recovery | Alerting |
|---|---|---|---|---|
| | | | | |

Address only mechanisms relevant to the design. Do not list every resilience pattern by habit.

## 10. Security and privacy

Describe:
- authentication boundary;
- authorization/resource ownership checks;
- tenant isolation;
- secrets;
- sensitive data;
- encryption where relevant;
- audit behavior;
- external trust boundaries.

## 11. Observability

### 11.1 Logs

Identify key structured events and fields.

### 11.2 Metrics

Prioritize service and business-path metrics that reveal design failures.

### 11.3 Tracing

State where correlation/trace context must propagate.

### 11.4 Alerts

Tie alerts to actionable conditions.

## 12. Performance and capacity

State targets only when known or design-driving.

Cover:
- latency/throughput targets;
- expensive operations;
- batching;
- cache behavior;
- queue/backpressure;
- scaling bottlenecks;
- storage growth.

## 13. Deployment and operations

Describe:
- deployment units;
- configuration;
- secrets;
- database migration ordering;
- readiness/liveness when relevant;
- rollout strategy;
- rollback/recovery;
- environment differences.

## 14. Compatibility and migration

Include for changes to existing systems.

Document:
- old/new compatibility;
- mixed-version behavior;
- data migration/backfill;
- feature flags;
- dual-read/dual-write if any;
- rollback constraints;
- removal criteria for compatibility code.

## 15. Alternatives and decisions

| Decision | Chosen approach | Alternative | Why |
|---|---|---|---|
| | | | |

Move long-lived important decisions into ADRs.

## 16. Risks and open issues

| Item | Type | Impact | Owner | Resolution criterion |
|---|---|---|---|---|
| | Risk / Open issue | | | |

## 17. Verification plan

Describe the checks needed to prove the design works:
- contract tests;
- state-transition tests;
- idempotency/duplicate tests;
- failure injection;
- migration rehearsal;
- performance/load tests;
- observability verification.

## Appendix

Use for large schemas, example payloads, configuration tables, or diagrams that are useful reference material but would interrupt the main design narrative.
