# <Domain / Feature> Data Design

## 1. Ownership

| Dataset | System of record | Write owner | Read consumers | Sensitivity |
|---|---|---|---|---|
| | | | | |

## 2. Core model

Use a compact ER diagram for identity and relationships.

## 3. Schema

### `<table>`

Purpose: <why the table exists>

| Column | Type | Null | Key/index | Meaning |
|---|---|---:|---|---|
| | | | | |

Constraints/invariants:

- <constraint or invariant>

## 4. Index strategy

| Index | Query supported | Selectivity / rationale | Write cost |
|---|---|---|---|
| | | | |

Avoid inventing indexes without a query path.

## 5. Transactions

Describe atomic write groups and isolation/concurrency assumptions.

## 6. Lifecycle

Describe creation, updates, soft/hard deletion, retention, archival, and cleanup jobs.

## 7. Migration

Describe forward migration, backfill, compatibility, rollback limits, and how large tables are changed safely.

## 8. Capacity

State row/object growth assumptions, large fields, partitioning needs, and storage hotspots only when material.
