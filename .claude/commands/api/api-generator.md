---
description: Generate production-ready Hono + Cloudflare Workers APIs
argument-hint: "<command> [args]"
---

# API Generator

Parse the command from `$ARGUMENTS` and execute using the `api-generator` skill.

## Command Routing

| Pattern | Description |
|---------|-------------|
| `build <name> [context]` | Full API generation from requirements |
| `plan <context>` | Analyze context and produce architecture plan |
| `init <name>` | Scaffold empty API project |
| `add-route <resource>` | Add resource route module |
| `add-service <resource>` | Add service layer for resource |
| `add-schema <resource>` | Add Zod schemas for resource |
| `add-middleware <type>` | Add middleware to stack |
| `add-db <resource>` | Add Drizzle table + migration |
| `tests` | Generate test suite |

## Execution

1. Parse `$ARGUMENTS` to extract the command and its arguments
2. Invoke the `api-generator` skill with the extracted arguments
3. The skill reads `references/*.md` for generation patterns
4. If no command matches, show the help table

## Default Behavior

If only a name is provided (no command keyword), treat as `build`:
```
/api-generator payments-api ./docs/requirements.md  -> build payments-api ./docs/requirements.md
/api-generator build my-api                         -> build my-api (interactive planning)
/api-generator plan ./openapi.yaml                  -> plan ./openapi.yaml
/api-generator add-route users                      -> add-route users
```
