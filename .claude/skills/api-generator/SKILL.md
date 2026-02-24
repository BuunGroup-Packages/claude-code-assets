---
name: api-generator
description: Generate production-ready Hono + Cloudflare Workers APIs. Reads project context, requirements, or API documentation then plans and builds robust APIs with D1, Drizzle ORM, Zod validation, typed middleware, and full test coverage.
argument-hint: "<command> [args]"
user-invokable: true
---

# API Generator

Generate production-ready Hono + Cloudflare Workers APIs.

## Pre-Flight

Read before any generation:
- `.claude/assets/best-practices/hono-cf-workers/` (read relevant topic files)
- `.claude/skills/api-generator/docs/PATTERNS.md`

## Commands

| Command | Reference | Model | Description |
|---------|-----------|-------|-------------|
| `build <name> [context]` | `references/build.md` | opus | Full API generation |
| `plan <context>` | `references/plan.md` | opus | Architecture plan |
| `init <name>` | `references/init.md` | haiku | Scaffold project |
| `add-route <resource>` | `references/routes.md` | sonnet | Add route module |
| `add-service <resource>` | `references/services.md` | sonnet | Add service layer |
| `add-schema <resource>` | `references/schemas.md` | sonnet | Add Zod schemas |
| `add-middleware <type>` | `references/middleware.md` | sonnet | Add middleware |
| `add-db <resource>` | `references/db.md` | sonnet | Add Drizzle table |
| `tests` | `references/tests.md` | sonnet | Generate tests |

## Build Workflow

1. **PLAN** (sequential) — Analyze context, produce architecture plan, get approval
2. **SCAFFOLD** (sequential) — Initialize project structure
3. **FOUNDATION** (parallel) — Schemas + Middleware + Database
4. **LOGIC** (parallel) — Services + Routes
5. **TESTS** (sequential) — Route integration + service unit tests
6. **FINALIZE** (sequential) — Verify all files wired correctly

## Sub-Agent Instructions

When spawning Task agents for generation steps, read the corresponding `references/*.md` file and pass its patterns to the agent. Use the model specified in the commands table.

For `build`, follow `references/build.md` which orchestrates all phases with parallel execution where possible.

## Architecture Principles

- **Routes are thin** — validate input, call services, return responses
- **Services contain business logic** — framework-agnostic, testable without HTTP
- **Schemas are the single source of truth** — validation AND OpenAPI documentation
- **Types are centralized** — `types.ts` prevents circular imports
- **Middleware is layered** — request-id > logger > CORS > rate-limit > auth

## Execution

1. Parse `$ARGUMENTS` to determine command and args
2. Read the matching `references/*.md` for generation patterns
3. For `build`, orchestrate the full phased workflow
4. Default: if only a name is provided, treat as `build`
5. Always read best practices before generating

## Output

```
## API Generated

**Name**: {API_NAME}
**Stack**: Hono + Cloudflare Workers + D1 + Drizzle ORM
**Resources**: {count} | **Endpoints**: {count}

### Quick Start
cd {API_NAME} && npm install && npm run dev

### Test
npm test

### Deploy
npm run deploy
```
