workspace "Private Knowledge Platform" "Example architecture model" {
    model {
        user = person "Knowledge User" "Uploads documents and searches private knowledge."
        admin = person "Workspace Admin" "Configures workspaces, permissions, and model providers."
        modelProvider = softwareSystem "Model Provider" "External or self-hosted embedding/chat model runtime." "External"
        objectStorage = softwareSystem "Object Storage" "Stores original uploaded files." "External"

        platform = softwareSystem "Knowledge Platform" "Private knowledge ingestion and retrieval." {
            web = container "Web Console" "Browser UI for users and administrators." "Web SPA" "Application"
            gateway = container "API Gateway" "Terminates authentication, rate limiting, and request routing." "HTTP Gateway" "Infrastructure"
            knowledge = container "Knowledge Service" "Owns document metadata, authorization, and index-job lifecycle." "Application Service" "Application"
            worker = container "Index Worker" "Parses content, creates chunks, invokes embedding, and writes vectors." "Background Worker" "Application"
            metadata = container "Metadata DB" "Stores documents, permissions, jobs, and outbox records." "PostgreSQL" "Database"
            vector = container "Vector Store" "Stores searchable embeddings and chunk metadata." "Vector DB" "Database"
            queue = container "Index Queue" "Buffers indexing work between the API path and workers." "Message Broker" "Infrastructure"
        }

        user -> web "Uses"
        admin -> web "Administers workspaces"
        web -> gateway "Calls APIs" "HTTPS/JSON"
        gateway -> knowledge "Routes authenticated requests" "HTTP/JSON"
        knowledge -> metadata "Reads/writes document and job state" "SQL"
        knowledge -> objectStorage "Stores/reads original files" "Object API"
        knowledge -> queue "Publishes index-job references" "Async message"
        worker -> queue "Consumes jobs" "Async message"
        worker -> objectStorage "Reads source files" "Object API"
        worker -> modelProvider "Creates embeddings" "HTTPS/API"
        worker -> vector "Writes vectors/chunks" "Vector API"
        worker -> metadata "Updates job and document index state" "SQL"

        deploymentEnvironment "Production" {
            deploymentNode "Edge" "Public ingress zone" "Managed ingress" {
                containerInstance gateway
            }
            deploymentNode "Application Cluster" "Private application network" "Container runtime" {
                containerInstance web
                containerInstance knowledge
                containerInstance worker
            }
            deploymentNode "Data Services" "Private data network" "Managed/private services" {
                containerInstance metadata
                containerInstance vector
                containerInstance queue
            }
        }
    }

    views {
        systemContext platform "Knowledge-SystemContext" {
            include user
            include admin
            include platform
            include modelProvider
            include objectStorage
            autoLayout lr
            title "Knowledge Platform - System Context"
        }

        container platform "Knowledge-Containers" {
            include *
            autoLayout lr
            title "Knowledge Platform - Containers"
        }

        deployment platform "Production" "Knowledge-Deployment" {
            include *
            autoLayout lr
            title "Knowledge Platform - Production Deployment"
        }

        styles {
            element "Person" {
                shape Person
                background #334155
                color #FFFFFF
            }
            element "Software System" {
                shape RoundedBox
                background #176B87
                color #FFFFFF
            }
            element "External" {
                background #64748B
                color #FFFFFF
            }
            element "Application" {
                shape RoundedBox
                background #2A7F9E
                color #FFFFFF
            }
            element "Infrastructure" {
                shape RoundedBox
                background #475569
                color #FFFFFF
            }
            element "Database" {
                shape Cylinder
                background #6B7280
                color #FFFFFF
            }
            relationship "Relationship" {
                color #52616B
            }
        }
    }
}
