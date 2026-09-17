# Knowledge Indexing Detailed Design (Excerpt)

## 1. Scope

This design covers the path from an accepted document upload to a searchable vector index. It does not define document parsing algorithms, model-provider selection, or search ranking.

The primary constraint is that model execution is slower and less predictable than the interactive API latency budget. Indexing therefore runs outside the synchronous upload request and has durable job state.

## 2. Service responsibilities

`Knowledge Service` owns document metadata, tenant authorization, index-job lifecycle, and the state transition that declares a document searchable. It does not parse files or run embedding models.

`Index Worker` owns execution of an indexing attempt. It reads the source object, produces chunks, obtains embeddings, and writes a versioned vector set. It cannot independently change document ownership or tenant permissions.

`Metadata DB` is the system of record for document and job state. `Vector Store` is a derived search index. A vector record without a corresponding successful metadata version is not considered visible to search.

## 3. Container architecture

The canonical C4/Structurizr model is stored in `diagrams/workspace.dsl`.

**Reading guide.** The API path ends after durable document/job creation; it does not wait for embedding. `Knowledge Service` remains the owner of business state even though workers execute indexing. `Vector Store` is a derived store and is not written directly by the API service. The queue isolates model-runtime latency and worker scaling from interactive requests.

## 4. Upload and indexing sequence

See `diagrams/knowledge-indexing-sequence.puml`.

**Reading guide.** The upload operation is considered accepted when the metadata transaction containing the document, job, and outbox record commits. Publishing occurs after commit, which prevents a worker from observing a job that has no durable metadata. Duplicate API requests reuse the idempotency record; duplicate queue deliveries are handled again at the job-claim boundary. Model failures therefore cannot roll back an accepted upload.

## 5. Job state

See `diagrams/indexing-state.mmd`.

The worker may enter `RUNNING` only by successfully claiming a `PENDING` or retryable attempt. Transient network/model failures move the job to `RETRY_WAIT`; validation or unsupported-format failures are terminal and move directly to `FAILED`. A manual retry creates a new attempt instead of mutating the history of the failed attempt.

## 6. Transaction and consistency rules

The API transaction atomically writes the document record, initial index job, idempotency result, and outbox event. No remote model or vector-store call occurs inside that transaction.

The worker writes a versioned vector set before marking the job `SUCCEEDED`. Search uses only the vector version referenced by the current successful document index version. If vector writing succeeds but the metadata success update fails, reconciliation may delete or reuse the orphaned version; it must not become visible merely because vectors exist.

## 7. Failure behavior

| Failure | Behavior |
|---|---|
| Duplicate upload request | Return the original accepted/result record for the same idempotency key. |
| Queue redelivery | Job claim is idempotent; completed or concurrently claimed work becomes a no-op. |
| Model timeout/5xx | Persist retry state and retry within the configured budget. |
| Unsupported document | Terminal failure with a user-visible reason; no automatic retry. |
| Vector store unavailable | Retry the attempt; document remains non-searchable. |
| Worker crash during RUNNING | Lease/claim expiration makes the job eligible for recovery. |

## 8. Observability

Every indexing attempt logs `document_id`, `job_id`, `attempt_id`, tenant/workspace identifier, source object identifier, parser type, model provider, chunk count, vector version, duration, and terminal classification. Sensitive document text is not written to logs.

Metrics distinguish queue wait time, execution time, model latency, vector-write latency, retry rate, terminal-failure rate, and jobs stuck beyond the expected processing window. Distributed trace context is propagated from outbox publication into the worker attempt where the broker supports headers.
