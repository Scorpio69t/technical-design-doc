# Consistency Rules

Run these checks after the document and diagrams exist.

## Naming consistency

Build a set of canonical names and scan for near-duplicates.

Common failures:
- `AI Runtime` vs `Model Runtime` vs `LLM Runtime` for the same service;
- `Knowledge DB` vs `Metadata DB` for the same database;
- singular/plural event names used inconsistently;
- API path renamed in prose but not sequence diagrams.

If an alias is necessary, declare it once.

## Diagram/prose consistency

For each architecture element shown in a diagram, verify that the prose does not assign its responsibility elsewhere.

For each important dependency described in prose, decide whether it belongs in the relevant architecture view. Not every low-level dependency needs a diagram, but contradictions must be resolved.

For every participant in an implementation-level sequence diagram, verify that it exists in the architecture vocabulary or is clearly a local component inside an existing service.

## Data consistency

Check:
- same entity names across ER diagrams, schema tables, API examples, and state descriptions;
- ownership of each table/index/bucket;
- primary identifiers and idempotency identifiers are not conflated;
- enum/state names match state diagrams;
- deletion/retention statements do not conflict.

## Contract consistency

Check:
- HTTP method/path names;
- request/response field names;
- event names and versions;
- error codes;
- sync/async semantics;
- timeout claims;
- retry counts and backoff rules.

If numeric values are not yet decided, use a named configuration placeholder rather than inventing a precise number.

## State consistency

Every persistent state should have:
- an entry path;
- permitted transitions;
- terminal or recovery behavior;
- persistence owner.

Do not allow prose to mention transitions that the state diagram forbids, or vice versa.

## Security consistency

Authentication and authorization are different. Verify that the document does not say “the gateway handles security” while domain services still require resource-level permission checks.

Check where tenant/user identity is established and where it is trusted.

## Operational consistency

Metrics, logs, alerts, and traces should use the same operation/event names as the runtime design. Avoid observability sections full of generic “monitor CPU/memory” statements while omitting the actual business failure signals.
