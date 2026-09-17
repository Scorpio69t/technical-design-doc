---
name: technical-design-doc
description: Create, rewrite, or review implementation-level software design documents for human readers. Use for detailed designs, architecture documentation, C4 or Structurizr models, Mermaid or PlantUML diagrams, or to fix inconsistent diagrams and agent-like technical prose.
license: MIT
metadata:
  author: Scorpio69t
  version: "1.0.1"
  repository: "https://github.com/Scorpio69t/technical-design-doc"
---

# Technical Design Document

Produce engineering design documents that a human project team can read, review, implement, and maintain. Optimize for architectural clarity, traceability, diagram quality, and decision rationale rather than raw length.

## Operating principle

A detailed design document is not a requirements list, a prompt transcript, or an agent work plan. It must explain the system in the order a technical reader needs:

1. what is being designed;
2. what constraints shape the design;
3. where the design sits in the larger system;
4. how responsibilities are divided;
5. how important runtime paths behave;
6. how data and state are managed;
7. what happens on failure;
8. why important design choices were made;
9. how the design is deployed, observed, secured, and evolved.

Do not inflate the document to look comprehensive. Prefer a small number of high-information sections and diagrams.

## Required workflow

Perform the work in six passes. Do not collapse all passes into one free-form generation step.

### Pass 1: Design frame

Establish the design scope before drafting.

Capture:
- goals and non-goals;
- actors and external systems;
- functional scope;
- non-functional constraints;
- deployment/environment constraints;
- existing systems that cannot be redesigned;
- assumptions that materially affect architecture;
- unresolved questions.

When the source material is incomplete, make conservative assumptions and label them. Do not invent business rules, APIs, components, SLAs, infrastructure, or technologies merely to make the document look complete.

Read `references/architecture-writing.md` when defining boundaries and responsibilities.

### Pass 2: Architecture model

Build a stable vocabulary before drawing diagrams.

Create a canonical inventory of:
- system names;
- containers/services;
- modules/components;
- external dependencies;
- data stores;
- queues/topics;
- important domain entities.

Each concept gets one canonical name. Aliases may be introduced once, then use the canonical name consistently.

For non-trivial systems, model architecture hierarchically:
- L1: system context;
- L2: containers/services;
- L3: components/modules only where implementation detail is useful;
- deployment view when runtime topology matters;
- dynamic/sequence views for important interactions.

Prefer Structurizr DSL for C4-style architecture models because one model can produce multiple consistent views. Use Mermaid for compact Markdown-native diagrams and PlantUML for interaction-heavy sequence diagrams.

Read `references/c4-structurizr.md` and `references/diagram-policy.md` before creating a large architecture set.

### Pass 3: Detailed design

Write the design around responsibilities and runtime behavior, not around feature bullet lists.

For every important module or service, answer:
- what responsibility does it own;
- what does it explicitly not own;
- what input does it receive;
- what output or state transition does it produce;
- what dependencies may it call;
- what persistence does it own;
- what failure modes matter;
- what retries, timeouts, idempotency, concurrency, or transaction rules apply;
- what must be observable;
- why the boundary exists.

For critical paths, include the unhappy path. A sequence diagram that only shows success is incomplete when timeout, duplicate delivery, partial failure, retry, compensation, authorization failure, or eventual consistency is material.

### Pass 4: Diagram pass

Choose the diagram type from the question the reader is trying to answer. Do not select a diagram language first and force every problem into it.

Use:
- Structurizr/C4 for system context, container, component, deployment, and model-derived architecture views;
- Mermaid flowchart for business/data/control flows;
- Mermaid state diagram for lifecycle/state transitions;
- Mermaid ER diagram for conceptual/logical data relationships;
- PlantUML sequence diagram for interaction-heavy runtime behavior;
- a table instead of a diagram when the content is primarily attributes, mappings, ownership, or configuration.

Every non-trivial diagram must have a short reading guide immediately after it that explains the architectural meaning, not merely repeats node labels.

Load the matching reference before generating a diagram:
- `references/mermaid-style.md`
- `references/plantuml-style.md`
- `references/c4-structurizr.md`

### Pass 5: Human writing edit

Rewrite the draft for engineers, reviewers, product owners, SREs, and future maintainers.

Remove agent-facing language, work-plan language, filler, self-commentary, empty transitions, exaggerated adjectives, and generic recommendations.

Replace vague statements with ownership, conditions, invariants, or measurable behavior.

Read `references/human-writing.md` and apply it as an editing pass, not merely as a style suggestion.

### Pass 6: Quality gate

Run a consistency and review pass before delivery.

Check:
- naming consistency;
- diagram/text consistency;
- ownership and dependency direction;
- missing failure paths;
- transaction boundaries;
- idempotency;
- concurrency;
- timeout and retry behavior;
- state transitions;
- data ownership;
- authentication and authorization boundaries;
- secrets and sensitive data;
- logs, metrics, traces, and audit events;
- deployability and rollback;
- horizontal-scaling assumptions;
- migration/compatibility when changing an existing system;
- unresolved assumptions.

Use `references/quality-gate.md` and `references/consistency-rules.md`.

When files are available locally, optionally run:

```bash
python scripts/lint_design_doc.py path/to/design.md
```

Treat script output as review hints, not as a substitute for engineering judgment.

## Diagram quality rules

Apply these by default unless project constraints require otherwise.

### Complexity budget

A diagram should normally contain no more than 12 primary nodes. Up to 18 is acceptable when grouping is strong and the relationships remain readable. Beyond that, split the view.

Do not combine context, deployment, component internals, storage details, and runtime sequence into one diagram.

Minimize crossing edges. If crossings are common, first reorder or regroup the model; do not solve structural confusion with decorative styling.

### Visual semantics

Color communicates category or state, not decoration. Keep a small palette with stable semantics across the document.

Recommended semantic categories:
- primary application/service;
- external system;
- data store;
- messaging/infrastructure;
- user/client;
- warning/failure path.

Do not create a unique color for every service.

### Direction

Prefer left-to-right for architecture and request/data pipelines. Prefer top-to-bottom for workflows with branching, approval steps, or state transitions. Use the direction that reduces edge crossings.

### Diagram text

Node labels should name things. Edge labels should describe actions, data, protocols, or events. Avoid prose paragraphs inside nodes.

### Reading guide

After each important diagram, explain two to five design consequences, such as:
- why a boundary exists;
- which component owns state;
- which calls are synchronous versus asynchronous;
- where failures are isolated;
- where scaling occurs independently;
- what cannot bypass the shown boundary.

Do not write “the diagram above shows...” followed by a transcription of the diagram.

## Human-readable prose rules

Write in direct technical prose.

Prefer:

> `Knowledge Service` owns document lifecycle and index-job state. It does not run embedding models. Once parsing succeeds, it creates an indexing job and submits chunks to `Embedding Service`. This keeps business state independent of model runtime availability.

Avoid:

> In order to realize the above goals, the system needs to provide a unified knowledge capability, and the embedding capability can be considered for further decoupling in subsequent implementation.

Do not talk to an agent in the final artifact. Avoid sentences such as “the implementer should next...”, “the agent needs to...”, “you can consider...”, or “we should now...”, unless the document is explicitly an implementation playbook.

Do not use speculative language where a design decision is already being made. Use “the design uses” rather than “it is recommended to consider using”.

Keep recommendations separate from committed design. Use explicit labels such as `Decision`, `Alternative`, `Open issue`, or `Future work` when necessary.

## Document structure

Do not force every project into a giant fixed outline. Select only applicable sections from `assets/templates/detailed-design.md`.

A typical substantial document includes:
- overview and scope;
- constraints and assumptions;
- architecture views;
- domain/module design;
- key runtime flows;
- data and state design;
- API/event contracts;
- failure and resilience design;
- security;
- observability;
- deployment and operations;
- performance/capacity considerations;
- migration/compatibility if applicable;
- design decisions and alternatives;
- risks/open issues.

Do not create empty sections merely to satisfy a template.

## Choosing how much detail to include

Use three levels of detail.

**Review level:** enough to approve architecture boundaries, dependencies, data ownership, failure handling, and major tradeoffs.

**Implementation level:** add interfaces, schemas, state machines, sequences, idempotency/transaction rules, configuration, and operational behavior.

**Handoff level:** add rollout/migration details, acceptance checks, troubleshooting signals, backward compatibility, and explicit implementation constraints.

Default to implementation level for requests containing “详细设计”, “detailed design”, “implementation design”, or equivalent wording.

## Source of truth rules

When modifying an existing design, treat existing code, schemas, APIs, architecture definitions, and user-provided documents as stronger evidence than generic best practice.

Never silently rename existing production concepts for aesthetic consistency. If names are poor but established, preserve them and optionally recommend a migration separately.

When architecture diagrams and prose disagree, do not choose whichever is more convenient. Resolve the mismatch or flag it explicitly.

## Output contract

A finished design document should:
- be understandable without access to the original prompt transcript;
- use stable terminology;
- distinguish fact, decision, assumption, and future work;
- contain only diagrams that answer a useful question;
- explain critical design rationale in prose;
- include important failure paths;
- avoid AI/agent-oriented phrasing;
- avoid unsupported claims and invented requirements;
- be ready to place under version control.

For a full document, start from `assets/templates/detailed-design.md`.
For a focused module, use `assets/templates/module-design.md`.
For API design, use `assets/templates/api-design.md`.
For data design, use `assets/templates/database-design.md`.
For architecture decisions, use `assets/templates/adr.md`.
For a formal review, use `assets/templates/review-report.md`.
