# Human Technical Writing

Use this reference during the editing pass. Its job is to turn a technically correct draft into a document that humans can scan, reason about, review, and maintain.

## 1. Write to explain a design, not to narrate generation

A design document is a stable project artifact. It must not expose the drafting process unless that process is itself relevant.

Remove phrases such as:

- “next we need to...”
- “the agent should...”
- “you can ask...”
- “I will...”
- “we can continue to...”
- “based on the above, we can consider...”
- “the following will introduce...” when the heading already says what follows.
- “基于上述设计，下一步需要...”
- “智能体应该继续...”
- “可以考虑进一步优化...” when no owner, condition, or target follows.

Do not mention prompts, context windows, tools, tokens, chain-of-thought, generation steps, or other agent mechanics.

## 2. Prefer ownership statements

Weak:

> The system needs to support document indexing and provide an efficient vectorization capability.

Strong:

> `Knowledge Service` owns document lifecycle and index-job state. `Embedding Service` converts chunks into vectors; it does not change document state.

Ownership statements reduce ambiguity. Use verbs such as `owns`, `validates`, `persists`, `publishes`, `subscribes`, `authorizes`, `schedules`, `retries`, `rejects`, `caches`, and `routes`.

## 3. Prefer conditions and invariants over adjectives

Weak:

> The solution is highly available, efficient, flexible, and reliable.

Strong:

> API instances are stateless and may scale horizontally. Index jobs are persisted before dispatch, so a worker restart does not lose accepted work. Duplicate deliveries reuse the same idempotency key and do not create a second index version.

Do not claim high availability, security, scalability, performance, or reliability without describing the mechanism or target.

## 4. Separate decision from possibility

When the design is committed, write it as a decision:

> The service publishes `DocumentIndexRequested` after the transaction commits.

When the choice is open, label it:

> **Open issue:** whether the event broker is RabbitMQ or Kafka depends on the shared platform decision.

When an alternative was rejected, state the reason:

> **Alternative considered:** invoking the embedding model inside `Knowledge Service` would reduce one network hop, but couples business availability to model-runtime availability and complicates independent scaling.

Do not blur these states with “could”, “may consider”, and “recommended” everywhere.

## 5. Paragraph pattern for a module

For important modules, a useful paragraph order is:

1. identity and purpose;
2. owned responsibility;
3. explicit boundary/non-responsibility;
4. major collaboration;
5. rationale or operational consequence.

Example:

> `Index Orchestrator` coordinates indexing jobs. It owns job state, retry counters, and version transitions, but it does not parse files or compute embeddings. Workers claim persisted jobs and call the parser and embedding adapters. This boundary allows the expensive model runtime to scale independently and lets failed work resume without re-uploading the original document.

## 6. Use bullets for sets, not for prose camouflage

Bullets are appropriate for:
- constraints;
- API fields;
- invariants;
- responsibilities;
- error codes;
- explicit review findings.

Bullets are not a substitute for explaining architecture. If five consecutive bullets each contain several sentences, consider a table or prose subsection.

Avoid walls of more than seven bullets unless the reader is intentionally scanning a catalogue or checklist.

## 7. Use tables when readers compare dimensions

Good table uses:
- component responsibility matrix;
- API error mapping;
- state transition table;
- configuration matrix;
- alternative comparison;
- data retention rules;
- environment differences.

Avoid tables whose cells contain mini-essays. If the explanation is causal, use prose.

## 8. Remove filler transitions

Usually delete or rewrite:

- in order to achieve the above goal;
- based on the above design;
- it should be noted that;
- in the actual implementation process;
- according to the actual situation;
- in addition;
- at the same time;
- furthermore;
- provides strong support for;
- lays a solid foundation for;
- effectively improves;
- comprehensively empowers;
- unified, efficient, stable and reliable;
- can be flexibly expanded in the future.
- 基于以上设计；
- 需要注意的是；
- 在实际实施过程中；
- 根据实际情况；
- 为后续工作提供有力支撑；
- 为未来演进奠定坚实基础；
- 全面赋能；
- 后续可灵活扩展。

These phrases are not banned words. They are warnings that a sentence may not contain a design fact.

## 9. Be specific about time and causality

Instead of:

> The task is retried when an exception occurs.

Write:

> A worker retries transient model or network failures up to three times with exponential backoff. Validation failures are terminal and move the job directly to `FAILED`.

Instead of:

> Data is eventually synchronized.

Write:

> The outbox relay publishes committed events asynchronously. Consumers may observe the new document version after the write API returns, so read-after-write across services is not guaranteed.

## 10. Explain diagrams, do not transcribe them

Bad reading guide:

> The user calls the gateway, the gateway calls the knowledge service, and the knowledge service calls the database.

Good reading guide:

> Authentication terminates at the gateway, but resource authorization remains in `Knowledge Service` because it owns tenant/document permissions. The database is not shared with other services; integrations must use the service API or published events. This preserves ownership and keeps schema changes local to the domain.

## 11. Heading quality

Prefer headings that help navigation:

- `4.2 Index job state model`
- `5.1 Synchronous upload path`
- `5.2 Asynchronous indexing path`
- `7.3 Duplicate event handling`

Avoid vague headings:

- `Design details`
- `Other considerations`
- `Technical implementation`
- `Optimization`
- `设计细节`
- `技术实现`
- `其他考虑`
- `优化`

## 12. Reader tests

Before finalizing, test whether a reader can answer these questions quickly:

- What owns this data?
- What is synchronous?
- What is asynchronous?
- What can fail independently?
- What happens after a timeout?
- Can the operation be retried safely?
- What state is durable?
- What is the transaction boundary?
- Which calls cross a trust boundary?
- Where would I look when this fails in production?

If the document is long but these answers are difficult to find, rewrite for information architecture rather than adding more content.
