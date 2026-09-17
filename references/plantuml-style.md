# PlantUML Sequence Diagram Style Guide

Use PlantUML primarily for interaction-heavy sequence diagrams where ordering, alternatives, activation, retries, and failure behavior matter.

## Styling approach

Prefer PlantUML's CSS-like `<style>` mechanism for new style assets. Older `skinparam` examples remain common and may still work, but the reusable style in this skill uses the modern style mechanism.

See `assets/styles/plantuml-sequence-style.puml`.

## Participant ordering

Order participants to reduce crossing:

1. human/client/channel;
2. edge/gateway;
3. owning application service;
4. collaborating services;
5. infrastructure/adapters;
6. stores/brokers/external providers.

Keep a stable left-to-right order between related diagrams.

## Declare participants explicitly

Prefer explicit aliases and stereotypes when they clarify roles:

```plantuml
actor User
participant "Web Console" as Web <<client>>
participant "API Gateway" as Gateway <<infra>>
participant "Knowledge Service" as Knowledge <<service>>
database "Metadata DB" as DB <<data>>
queue "Index Queue" as Queue <<infra>>
```

Do not let the tool auto-create a participant from a typo. Explicit declarations make name drift easier to catch.

## Messages

Message labels should identify action or contract:

Good:
- `POST /documents`
- `createDocument(metadata)`
- `INSERT document + outbox`
- `DocumentIndexRequested`
- `409 duplicate idempotency key`

Weak:
- `request`
- `call`
- `process`
- `response`

## Return arrows

Use return arrows when the return carries important data, state, or error semantics. Do not add a return arrow after every call merely for symmetry.

## Activation

Use activation when it helps show nested synchronous work or a long-running ownership interval. Avoid excessive activation bars in simple flows.

## Alternatives

Use `alt` for materially different behavior:

```plantuml
alt idempotency key already completed
    Knowledge --> Gateway : existing result
else new request
    Knowledge -> DB : persist document + outbox
end
```

Do not create an `alt` block for trivial `200 vs 201` formatting differences.

## Retries and loops

Show retries when they are part of system semantics, not merely library internals.

Example:

```plantuml
loop up to retry budget
    Worker -> Model : embed(chunks)
    alt transient failure
        Model --> Worker : timeout / 5xx
        Worker -> Worker : backoff
    else success
        Model --> Worker : vectors
        break
    end
end
```

If the diagram becomes unreadable, split normal processing and recovery into two diagrams.

## Async interactions

Use a queue/broker participant and make publish/consume semantics explicit. The diagram should not visually imply that a producer waits for a consumer unless it really does.

State when the producer considers the operation successful: before publish, after broker acknowledgement, after consumer processing, or after a later status transition.

## Notes

Use notes sparingly for invariants or details that cannot fit on an edge. A note should reveal a design constraint, not contain a paragraph copied from the surrounding prose.

## Error paths

For critical sequences, consider:
- invalid input;
- unauthorized/forbidden;
- dependency timeout;
- transient remote failure;
- duplicate request/event;
- partial persistence failure;
- retry budget exhaustion;
- manual recovery/dead-letter path.

Show only the failures that affect architecture or implementation choices.

## Size control

Prefer 4-8 participants in one sequence diagram. If more than eight are needed, consider:
- separating orchestration from infrastructure detail;
- replacing low-level dependencies with a boundary participant;
- using `ref over` for a sub-flow;
- creating a second diagram for recovery.
