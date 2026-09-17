# Usage Recipes

These are invocation patterns, not text that must appear in the generated document.

## Generate from PRD + repository

```text
Use technical-design-doc to produce an implementation-level detailed design from the PRD and current repository. Existing code and API names are source of truth. First establish canonical system/service/module names, then produce only the diagrams needed for review and implementation. Include failure paths, state/transaction/idempotency rules, observability, deployment impact, and a final quality-gate review. Do not invent infrastructure that the repository does not use.
```

## Rewrite an AI-generated design

```text
Use technical-design-doc to rewrite this document for human engineers. Preserve verified technical facts. Remove agent-facing language, generic filler, repeated conclusions, and speculative recommendations. Split overloaded diagrams, make naming consistent, and add short reading guides that explain architecture consequences rather than repeating arrows.
```

## Diagram-only refactor

```text
Use the diagram policy from technical-design-doc. Inventory the questions the current diagrams are trying to answer, then redesign the diagram set. Prefer C4/Structurizr for architecture, PlantUML for complex sequences, Mermaid for flows/states/ER. Keep each diagram focused and preserve all factual relationships.
```

## Architecture review only

```text
Review this design with technical-design-doc without rewriting it. Return findings grouped by boundary/ownership, runtime failure handling, data/transaction consistency, security, observability/operations, diagram quality, and human readability. Cite the exact section or diagram name for each finding and distinguish blocker, important, and optional improvement.
```

## Existing system migration

```text
Use technical-design-doc for an existing-system change. Preserve current behavior unless the requirement explicitly changes it. Document current state, target state, compatibility constraints, migration stages, rollback, dual-read/dual-write behavior if any, data backfill, and how mixed old/new versions behave during deployment.
```

## Module-level design

```text
Use technical-design-doc at module scope. Do not generate a full system architecture chapter unless necessary for context. Focus on module responsibility, interfaces, internal components, data/state, algorithm or workflow, critical sequence, concurrency/idempotency, errors, observability, and testability.
```
