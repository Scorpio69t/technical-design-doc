# <Module> Design

## 1. Purpose and boundary

Explain what this module owns, why it exists, and what adjacent responsibility is explicitly outside its boundary.

## 2. Inputs and outputs

| Direction | Interface / event | Caller / consumer | Semantics |
|---|---|---|---|
| In | | | |
| Out | | | |

## 3. Internal components

Include a small component diagram only if it reveals useful structure.

| Component | Responsibility | State | Dependencies |
|---|---|---|---|
| | | | |

## 4. Runtime flow

Use a sequence or flow diagram for the critical behavior.

**Reading guide:** explain ownership, transaction point, failure boundary, and any async handoff.

## 5. State and persistence

Describe durable/transient state, schema ownership, lifecycle, and transaction boundaries.

## 6. Concurrency and idempotency

State duplicate handling, locking/versioning, race conditions, and retry safety.

## 7. Error behavior

| Condition | Classification | Behavior | Retry | Caller-visible result |
|---|---|---|---|---|
| | | | | |

## 8. Observability

List the logs, metrics, traces, and audit events that allow operators to distinguish normal, degraded, and failed behavior.

## 9. Design rationale

Explain choices that are not obvious from the code structure.

## 10. Open issues

Keep unresolved items explicit and separate from committed design.
