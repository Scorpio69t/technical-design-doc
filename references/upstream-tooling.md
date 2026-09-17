# Upstream Tooling Notes

This skill is intentionally renderer-aware but not renderer-dependent. The project should pin tool versions in its own build environment when deterministic rendering matters.

## Agent Skills format

The package follows the common Agent Skills structure: a directory with a required `SKILL.md` containing YAML frontmatter (`name` and `description`) plus optional `scripts`, `references`, `assets`, and client metadata.

References:
- https://agentskills.io/
- https://github.com/agentskills/agentskills
- https://github.com/openai/skills

## Mermaid

The style guidance assumes modern Mermaid configuration with YAML frontmatter. Mermaid 12 uses ELK as the default layout for several diagram types, while `layout: elk` may still be stated explicitly when the design wants to make layout intent obvious.

Architecture diagrams are available in modern Mermaid releases, but this skill reserves Structurizr/C4 for architecture sets that need a single shared model across several views.

References:
- https://mermaid.js.org/config/layouts.html
- https://mermaid.js.org/config/configuration.html
- https://mermaid.js.org/config/theming.html
- https://mermaid.js.org/syntax/architecture.html
- https://mermaid.js.org/syntax/flowchart.html

## PlantUML

PlantUML supports CSS-like styling through `<style>`. New style assets in this skill use that mechanism as the primary approach. Legacy `skinparam` remains widespread in existing code and documentation but should not be the default for new shared style definitions.

References:
- https://plantuml.com/style
- https://plantuml.com/style-evolution
- https://plantuml.com/sequence-diagram

## Structurizr

Structurizr DSL is used for model-as-code C4 architecture. The DSL supports system landscape/context, container, component, dynamic, deployment, filtered, and other views. Structurizr can also export views to formats including PlantUML and Mermaid, although not every renderer-specific visual feature maps perfectly across export formats.

References:
- https://docs.structurizr.com/
- https://docs.structurizr.com/dsl
- https://docs.structurizr.com/dsl/language
- https://docs.structurizr.com/export

## Maintenance rule

When a project upgrades Mermaid, PlantUML, or Structurizr, check this file and the corresponding style reference before changing diagram syntax across existing documents. Keep architecture semantics stable even when rendering syntax evolves.
