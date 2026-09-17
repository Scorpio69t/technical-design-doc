# <API / Service> API Design

## 1. Scope and ownership

State API owner, clients, versioning strategy, and compatibility expectations.

## 2. Common conventions

Document only conventions that differ from organization defaults or materially affect clients.

Examples:
- authentication;
- tenant context;
- idempotency keys;
- pagination;
- timestamps;
- error envelope;
- request correlation.

## 3. Endpoint summary

| Method | Path | Purpose | Auth | Idempotent | Owner |
|---|---|---|---|---|---|
| | | | | | |

## 4. Endpoint details

### `<METHOD> <PATH>`

**Purpose**

**Authorization**

**Request**

```json
{}
```

| Field | Type | Required | Validation | Meaning |
|---|---|---:|---|---|
| | | | | |

**Response**

```json
{}
```

**Errors**

| HTTP / code | Condition | Retryable | Notes |
|---|---|---:|---|
| | | | |

**Idempotency / concurrency**

Explain duplicate behavior and version/locking semantics.

## 5. Async contracts

| Event/job | Producer | Consumer | Schema version | Delivery | Ordering | Idempotency |
|---|---|---|---|---|---|---|
| | | | | | | |

## 6. Compatibility

Describe additive vs breaking changes, deprecation period, and mixed-version behavior.

## 7. Security and abuse controls

Describe authorization, rate limits, request-size limits, sensitive fields, and audit needs where relevant.
