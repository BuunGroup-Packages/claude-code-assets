---
description: Generate clean, modular SDKs from API documentation
argument-hint: "<command> [args]"
---

# SDK Generator

Parse the command from `$ARGUMENTS` and execute using the `sdk-generator` skill.

## Command Routing

| Pattern | Description |
|---------|-------------|
| `build <source> <name> [--lang ts\|py]` | Full SDK generation |
| `analyze <source>` | Analyze API docs, produce report |
| `init <name> [--lang ts\|py]` | Scaffold empty SDK project |
| `add-resource <name>` | Add resource to existing SDK |
| `core` | Generate/regenerate core modules |
| `tests` | Generate test scaffolding |

## Execution

1. Parse `$ARGUMENTS` to extract the command and its arguments
2. Invoke the `sdk-generator` skill with the extracted arguments
3. The skill reads `references/*.md` for generation patterns
4. If no command matches, show the help table

## Default Behavior

If only a source path and name are provided (no command keyword), treat as `build`:
```
/sdk-generator ./api-docs my-sdk          -> build ./api-docs my-sdk
/sdk-generator build ./api-docs my-sdk    -> build ./api-docs my-sdk
/sdk-generator analyze ./openapi.yaml     -> analyze ./openapi.yaml
```
