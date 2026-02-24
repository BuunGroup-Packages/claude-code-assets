---
description: Build Vite 6 + React + Cloudflare Workers apps with Hono
argument-hint: "<command> [args]"
---

# Vite + React + Cloudflare + Hono

Parse the command from `$ARGUMENTS` and execute using the `vite-cloudflare` skill.

## Command Routing

| Pattern | Description |
|---------|-------------|
| `build-app <name>` | Full app scaffold (parallel agents) |
| `add-feature <name>` | Complete feature (parallel agents) |
| `init <name>` | Project scaffold |
| `api <resource>` | Delegates to `api-generator` |
| `component <name> [path]` | React component |
| `page <name> [--with-components]` | React Router page |
| `binding <type> <name>` | D1/R2/KV binding |

## Execution

1. Parse `$ARGUMENTS` to extract the command and its arguments
2. Invoke the `vite-cloudflare` skill with the extracted arguments
3. The skill reads `references/*.md` for generation patterns
4. If no command matches, show the help table

## Default Behavior

If only a name is provided (no command keyword), treat as `build-app`:
```
/vite-cloudflare my-app              -> build-app my-app
/vite-cloudflare build-app my-app    -> build-app my-app
/vite-cloudflare api users           -> api users
```
