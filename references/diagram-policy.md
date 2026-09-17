# Diagram Policy

## One diagram, one primary question

Before drawing, state the question internally. If the answer contains two unrelated questions, split the diagram.

Examples:

- “Who interacts with the product?” -> System Context
- “What services run the product?” -> Container view
- “What happens when a document is indexed?” -> Sequence diagram
- “How can an indexing job transition?” -> State diagram
- “What data belongs to which entity?” -> ER diagram
- “Where do components run?” -> Deployment view

## Complexity budget

Default budgets:

| Diagram | Primary-node guideline |
|---|---:|
| System context | 5-10 |
| Container/service architecture | 6-12 |
| Component view | 6-12 |
| Deployment view | 6-14 |
| Flowchart | 6-14 |
| Sequence participants | 4-8 |
| State diagram | 4-10 states |
| ER diagram | 4-10 core entities |

These are readability triggers, not rigid syntax limits. If a diagram exceeds the budget, justify the density or split it.

## Split patterns

When a diagram becomes dense, split by:

- abstraction level;
- domain;
- runtime phase;
- happy path vs recovery path;
- control plane vs data plane;
- online vs offline processing;
- application vs infrastructure;
- write path vs read path.

## Stable semantics

Use consistent semantics across a document.

Suggested palette categories:

| Category | Meaning |
|---|---|
| Primary | application/service under design |
| External | third-party or outside-owned system |
| Data | database/object/vector/search storage |
| Infra | broker/cache/gateway/scheduler/runtime |
| Actor | human/client/channel |
| Risk | failure/manual intervention/exception path |

Exact colors may vary by renderer or company brand. Semantic roles must not.

## Edges

Every non-obvious edge should answer at least one of:

- what is sent;
- why the dependency exists;
- protocol/type;
- sync vs async;
- success vs failure path.

Avoid generic labels such as `call`, `data`, `request`, or `process` when a more precise verb exists.

## Layout

Prefer architecture layouts with clear layers or domains. Do not force a visually symmetric picture when it makes dependency direction less clear.

Rules of thumb:
- left-to-right for request/data pipelines;
- top-to-bottom for branching workflows;
- users/external callers at an outer edge;
- data stores near their owning services;
- external dependencies visually separated;
- asynchronous infrastructure placed so producers and consumers are easy to trace.

## Diagram reading guide

Add a short prose section after important diagrams. It should identify two to five consequences or constraints.

Good topics:
- ownership;
- trust boundary;
- sync/async split;
- data isolation;
- independent scaling;
- retry boundary;
- forbidden bypasses;
- why a dependency is one-way.

Do not repeat all nodes and arrows.

## When not to draw

Use a table instead of a diagram when the reader mainly compares fields, configuration, ownership, permissions, error codes, or environment values.

Use prose instead of a diagram when there are fewer than three meaningful relationships and the visual does not reveal structure.

Do not draw decorative diagrams that contain no additional information beyond the section title.
