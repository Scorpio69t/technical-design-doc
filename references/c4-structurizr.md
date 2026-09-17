# C4 and Structurizr Guide

Use Structurizr DSL when a design needs several architecture views that must remain consistent over time.

## Why model first

A C4/Structurizr model separates architecture facts from individual diagrams. The same model can support system-context, container, component, dynamic, and deployment views. This reduces name drift and “diagram A says one thing, diagram B says another” failures.

## Recommended levels

### System Context

Answer:
- who uses the system;
- what external systems it depends on;
- what responsibility the whole system has.

Do not include databases, queues, internal services, or implementation modules here.

### Container

Answer:
- what deployable/runnable units make up the system;
- what major data stores exist;
- how containers communicate;
- which technology choices matter at this level.

A container is not necessarily a Docker container. Treat it as an independently runnable/deployable application or data store in the C4 sense.

### Component

Use only for services where internal structure materially helps implementation or review.

Do not make a component view for every service. A component should represent a significant responsibility or boundary, not every class/package.

### Dynamic

Use for architecture-level collaboration when a sequence is useful but a detailed UML sequence diagram would be excessive.

Use PlantUML when interaction logic needs richer alternatives, loops, notes, or implementation-level messages.

### Deployment

Answer:
- where containers run;
- important runtime nodes/zones;
- ingress/load balancing;
- replicated instances;
- managed infrastructure dependencies;
- environment-specific topology where relevant.

Keep deployment topology separate from logical component structure.

## Structurizr DSL conventions

Use stable explicit identifiers and view keys where practical. Keep names canonical and concise.

Example skeleton:

```text
workspace "Product" "Architecture model" {
    model {
        user = person "User"

        product = softwareSystem "Product" {
            web = container "Web Console" "Browser UI" "Vue/React"
            api = container "API Service" "Owns product application logic" "Go/Java"
            db = container "Metadata DB" "Stores product state" "PostgreSQL" {
                tags "Database"
            }
        }

        user -> web "Uses"
        web -> api "Calls" "HTTPS/JSON"
        api -> db "Reads/writes" "SQL"
    }

    views {
        systemContext product "Product-SystemContext" {
            include *
            autoLayout lr
        }

        container product "Product-Containers" {
            include *
            autoLayout lr
        }

        styles {
            element "Software System" {
                background #176B87
                color #FFFFFF
                shape RoundedBox
            }
            element "Container" {
                background #2A7F9E
                color #FFFFFF
                shape RoundedBox
            }
            element "Database" {
                background #6B7280
                color #FFFFFF
                shape Cylinder
            }
            element "Person" {
                background #334155
                color #FFFFFF
                shape Person
            }
        }
    }
}
```

The examples in `examples/diagrams/workspace.dsl` show a fuller model.

## Relationship wording

Relationships should be verbs from source to destination:

Good:
- `Uploads documents`
- `Calls for document metadata`
- `Publishes indexing jobs`
- `Stores job state`
- `Queries vectors`

Weak:
- `Uses`
- `Connects to`
- `Depends on`

Generic verbs are acceptable at very high-level views when detail would create clutter, but become specific at lower levels.

## Technology labels

Use technology labels only when they explain a relevant implementation decision. Avoid turning every box into an inventory of frameworks and library versions.

Good container technology labels:
- `Go / HTTP API`
- `PostgreSQL 16`
- `RabbitMQ`
- `Vue 3 SPA`

Avoid:
- every minor package;
- IDE/editor;
- build-time dependencies that do not affect architecture.

## Styles and themes

Keep visual semantics stable through tags and styles. Themes can be layered with local styles. Do not assume all Structurizr rendering features survive export to Mermaid or PlantUML; exported formats may support a subset.

Prefer shapes and colors that communicate category rather than vendor-logo overload.

## Model hygiene

Before finalizing:
- every container has a responsibility description;
- relationships have meaningful direction;
- no unexplained cross-domain database access;
- external systems are visually outside the owned system;
- stores are near and clearly owned by their owning container/domain;
- view keys are stable if layout preservation matters;
- a view contains only the abstraction level it claims to show.
