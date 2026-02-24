---
name: sdk-generator
description: Generate clean, modular SDKs from API documentation or source code. Reads OpenAPI specs, API routes, or documentation then scaffolds TypeScript or Python SDKs following Stripe/Anthropic-style best practices.
argument-hint: "<command> [args]"
user-invokable: true
---

# SDK Generator

Generate production-quality SDKs from API documentation, OpenAPI specs, or API source code.

## Pre-Flight

Read before any generation:
- `.claude/assets/best-practices/sdk/` (read relevant topic files)
- `.claude/skills/sdk-generator/docs/PATTERNS.md`

## Supported Input

| Source | Detection |
|--------|-----------|
| OpenAPI Spec | `.yaml`/`.json` with `openapi:` or `swagger:` |
| API Routes | Route handler files (Hono, Express, FastAPI) |
| Markdown Docs | `.md` files with endpoint descriptions |
| Live API | `http://` or `https://` URLs |

## Supported Output

| Language | HTTP Client | Validation | Package Manager |
|----------|-------------|------------|----------------|
| TypeScript (default) | `fetch` (native) | Zod | npm |
| Python (`--lang py`) | `httpx` | Pydantic v2 | uv / pip |

## Commands

| Command | Reference | Model | Description |
|---------|-----------|-------|-------------|
| `build <source> <name> [--lang]` | `references/build.md` | opus | Full SDK generation |
| `analyze <source>` | `references/analyze.md` | opus | API analysis report |
| `init <name> [--lang]` | `references/init.md` | haiku | Scaffold project |
| `add-resource <name>` | `references/resources.md` | sonnet | Add resource class |
| `core` | `references/core.md` | sonnet | Generate core modules |
| `tests` | `references/tests.md` | sonnet | Generate tests |

## Build Workflow

1. **ANALYZE** (sequential) -- Read API source, produce structured report
2. **GENERATE** (parallel) -- Init + Core + Resources
3. **TESTS** (sequential) -- Unit tests + integration scaffolding
4. **FINALIZE** (sequential) -- Verify exports, wiring, README

## Sub-Agent Instructions

When spawning Task agents, read the corresponding `references/*.md` file and pass its patterns to the agent. Use the model specified in the commands table.

For `build`, follow `references/build.md` which orchestrates all phases with parallel execution.

## Architecture (Stripe/Anthropic Style)

- **Resource-oriented client** -- `client.users.create()`, `client.orders.list()`
- **Auto-pagination** -- `for await (const item of client.items.listAutoPaging())`
- **Typed errors** -- `APIError > AuthenticationError | NotFoundError | RateLimitError`
- **Retry with backoff** -- Exponential + jitter, respects `Retry-After`
- **Env-based auth** -- Auto-reads API key from env, or pass explicitly

## Execution

1. Parse `$ARGUMENTS` to determine command and args
2. Read the matching `references/*.md` for generation patterns
3. For `build`, orchestrate the full phased workflow
4. Default: if source + name provided without command, treat as `build`
5. Always read best practices before generating

## Output

```
## SDK Generated

**Name**: {SDK_NAME}
**Language**: {LANG}
**Resources**: {count} | **Endpoints**: {count}

### Quick Start
cd {SDK_NAME} && npm install && npm run build

### Test
npm test
```
