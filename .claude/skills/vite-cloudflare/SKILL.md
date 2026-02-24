---
name: vite-cloudflare
description: Build Vite 6 + React 19 + Cloudflare Workers apps with Hono API. TypeScript-first, co-located components, CSS animations.
argument-hint: "<command> [args]"
user-invokable: true
---

# Vite 6 + React + Cloudflare Workers + Hono

Build full-stack apps with Vite 6, React 19, Cloudflare Workers, and Hono API.

## Pre-Flight

Read design system docs before creating components:
- `.claude/skills/vite-cloudflare/docs/DESIGN.md`
- `.claude/skills/vite-cloudflare/docs/COLORS.md`
- `.claude/skills/vite-cloudflare/docs/COMPONENTS.md`

## Commands

| Command | Reference | Model | Description |
|---------|-----------|-------|-------------|
| `build-app <name>` | `references/build-app.md` | sonnet | Full app scaffold (parallel) |
| `add-feature <name>` | `references/add-feature.md` | sonnet | Complete feature (parallel) |
| `init <name>` | `references/init.md` | haiku | Project scaffold |
| `api <resource>` | **delegates to `api-generator`** | sonnet | Hono API route |
| `component <name> [path]` | `references/component.md` | haiku | React component |
| `page <name> [--with-components]` | `references/page.md` | haiku | React Router page |
| `binding <type> <name>` | `references/binding.md` | haiku | D1/R2/KV binding |

## API Delegation

All API generation is delegated to the `api-generator` skill, which follows production best practices from `.claude/assets/best-practices/hono-cf-workers/`. This ensures proper service layers, Drizzle ORM, middleware, structured errors, and testing.

- `api <resource>` -> `api-generator add-route <resource>`
- `build-app` API step -> `api-generator init <name>` + `api-generator add-route health`
- `add-feature` API step -> `api-generator add-route <feature>` + `api-generator add-schema <feature>` + `api-generator add-service <feature>`

## Build Workflow (build-app)

1. **PARALLEL** -- init + binding + page (vite-cloudflare) + api-generator init (api-generator)
2. **FINALIZE** -- Verify wiring, summarize output

## Add Feature Workflow (add-feature)

1. **PARALLEL** -- page + component (vite-cloudflare) + add-route + add-schema + add-service (api-generator)
2. **FINALIZE** -- List integration steps

## Sub-Agent Instructions

When spawning Task agents, read the corresponding `references/*.md` file and pass its patterns to the agent. Use the model specified in the commands table.

For API work, invoke the `api-generator` skill instead of generating API code directly. The api-generator reads `.claude/assets/best-practices/hono-cf-workers/` and its own `references/*.md`.

For compound commands (`build-app`, `add-feature`), spawn ALL agents in a SINGLE message for parallel execution.

## Stack

| Layer | Technology |
|-------|------------|
| Build | Vite 6 + @cloudflare/vite-plugin |
| UI | React 19 (SPA) |
| Routing | React Router 7 |
| API | Hono (Cloudflare Workers) |
| Database | Cloudflare D1 |
| Storage | Cloudflare R2 |
| Cache | Cloudflare KV |
| Styling | CSS (no Framer Motion) |

## Architecture

- **Co-located pages** -- `_components/`, `_hooks/`, `_types/`, `_utils/` per page
- **Shared components** -- `src/client/components/` with barrel exports
- **BEM CSS** -- Design tokens via CSS custom properties
- **Hono API** -- `/api/*` routes with Zod validation
- **CSS animations** -- `fade-in`, `slide-in`, `scale-in` with reduced-motion support

## Execution

1. Parse `$ARGUMENTS` to determine command and args
2. Read the matching `references/*.md` for generation patterns
3. For compound commands, orchestrate parallel sub-agents
4. Default: if no command keyword, show help table
5. Always read design system docs before creating components

## Output

```
## Vite + Cloudflare

**Command**: [command]
**Sub-Agents**: [agents spawned]

### Files Created
- [list]

### Next Steps
- [actions]
```
