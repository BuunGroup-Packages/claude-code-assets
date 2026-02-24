---
model: opus
description: Research a topic using an orchestrated team of search agents with built-in cross-validation
argument-hint: <topic> [deep] [browser]
---

# Research

Research any topic using a coordinated team of search agents. The orchestrator spawns workers, assigns strategies, and cross-references findings.

## Variables

Parse `$ARGUMENTS` to extract:

- **TOPIC:** all text minus detected keywords (required)
- **DEPTH:** `standard` (default), `deep` if keyword present
- **BROWSER:** `false` (default), `true` if `browser` keyword present

## Workflow

1. Create `./research/` directory if it doesn't exist
2. Spawn a `@research-orchestrator` with the TOPIC and options
3. The orchestrator internally manages:
   - 3 `@research-agent` workers (discover, deep-dive, contrarian strategies)
   - Optional `@playwright-bowser-agent` if BROWSER is `true`
   - Cross-referencing and merging across all agents
   - Conflict resolution and confidence scoring
4. Output the final summary table and file path to the user
