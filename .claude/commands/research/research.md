---
model: opus
description: Research a topic using parallel web search agents with built-in cross-validation
argument-hint: <topic> [deep] [browser]
---

# Research

Research any topic using parallel search agents. Each agent cross-validates its own findings by default.

## Variables

Parse `$ARGUMENTS` to extract:

- **TOPIC:** all text minus detected keywords (required)
- **DEPTH:** `standard` (default), `deep` if keyword present
- **BROWSER:** `false` (default), `true` if `browser` keyword present — uses `@playwright-bowser-agent` for pages that need JS rendering

## Workflow

### Phase 1: Research

1. Create `./research/` directory if it doesn't exist
2. Spawn 2-3 `@research-agent` instances in parallel, each covering different search angles for the TOPIC
3. If BROWSER is `true`, also spawn a `@playwright-bowser-agent` to visit key pages that may need JS rendering and extract data
4. Wait for all agents to complete

### Phase 2: Merge

5. Read all JSON outputs from the research agents
6. Merge into a single deduplicated list, combining source lists and recalculating confidence based on cross-agent agreement:
   - Found by 3+ agents → **high**
   - Found by 2 agents → **medium**
   - Found by 1 agent → **low**
7. Write merged result to `./research/<topic-kebab>_merged_<uuid>.json`

### Phase 3: Report

8. Output the final summary table and file path to the user
