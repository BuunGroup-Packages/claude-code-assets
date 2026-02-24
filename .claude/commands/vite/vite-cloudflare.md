---
description: Build Vite 6 + React + Cloudflare Workers apps with Hono
argument-hint: "<command> [args]"
---

# Vite + React + Cloudflare + Hono

Parse the command from `$ARGUMENTS` and execute using the `vite-cloudflare` skill.

## Pre-Flight

Read design system docs before creating components:
- `.claude/skills/vite-cloudflare/docs/DESIGN.md`
- `.claude/skills/vite-cloudflare/docs/COLORS.md`
- `.claude/skills/vite-cloudflare/docs/COMPONENTS.md`

## Command Routing

| Pattern | Reference | Model | Description |
|---------|-----------|-------|-------------|
| `build-app <name>` | `references/build-app.md` | sonnet | Full app scaffold (parallel agents) |
| `add-feature <name>` | `references/add-feature.md` | sonnet | Complete feature (parallel agents) |
| `init <name>` | `references/init.md` | haiku | Project scaffold |
| `api <resource>` | **delegates to `api-generator`** | sonnet | Hono API route |
| `component <name> [path]` | `references/component.md` | haiku | React component |
| `page <name> [--with-components]` | `references/page.md` | haiku | React Router page |
| `binding <type> <name>` | `references/binding.md` | haiku | D1/R2/KV binding |

## API Delegation

All API generation delegates to the `api-generator` skill (production best practices, Drizzle ORM, service layers, middleware, testing):

- `api <resource>` -> `api-generator add-route <resource>`
- `build-app` API step -> `api-generator init` + `api-generator add-route health`
- `add-feature` API step -> `api-generator add-route` + `add-schema` + `add-service`

## Execution

1. Parse `$ARGUMENTS` to extract the command and its arguments
2. Read design system docs (pre-flight) before creating components
3. Read the matching `references/*.md` for generation patterns
4. For `api`, delegate to `api-generator` skill
5. For compound commands (`build-app`, `add-feature`), spawn ALL sub-agents in a SINGLE message for parallel execution
6. If no command matches, show the help table

## Default Behavior

If only a name is provided (no command keyword), treat as `build-app`:
```
/vite-cloudflare my-app              -> build-app my-app
/vite-cloudflare build-app my-app    -> build-app my-app
/vite-cloudflare api users           -> api-generator add-route users
```
