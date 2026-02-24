---
name: just
description: Use `just` to save and run project-specific commands. Use when the user mentions `justfile`, `recipe`, or needs a simple alternative to `make` for task automation.
---

# Just Command Runner

## Pre-Flight

Before running or creating recipes, **always read the project justfile first**:
- Read `.claude/justfile` to see available modules and cross-skill recipes
- Run `just --list` from `.claude/` to see all top-level recipes
- Run `just <module>` to list recipes within a module (e.g. `just research`)

## Project Justfile

The project justfile lives at `.claude/justfile`. It uses `mod` to import skill modules, each with their own `skill.just`. Run all recipes from the `.claude/` directory.

### Modules

| Module | Path | What it does |
|--------|------|-------------|
| `api` | `skills/api-generator/skill.just` | Hono + Cloudflare Workers API generation |
| `lighthouse` | `skills/lighthouse/skill.just` | Performance, a11y, SEO audits |
| `playwright` | `skills/playwright-bowser/skill.just` | Browser automation, QA, workflows |
| `research` | `skills/research/skill.just` | Web research with orchestrated agent teams |
| `sdk` | `skills/sdk-generator/skill.just` | TypeScript/Python SDK generation |
| `seo` | `skills/seo/skill.just` | Full SEO implementation |
| `vite` | `skills/vite-cloudflare/skill.just` | Vite + React + Cloudflare apps |

### Cross-Skill Recipes (mprocs)

| Recipe | What it does |
|--------|-------------|
| `research-and-audit <url> <topic>` | Research + Lighthouse in parallel |
| `project-setup <name>` | API + frontend + SEO in parallel |
| `api-and-sdk <name>` | Build API then generate SDK |
| `audit-batch <url1> <url2> ...` | Lighthouse audit multiple URLs |

## How to Route User Requests

When the user asks for something, map it to the right module and recipe:

| User says | Run |
|-----------|-----|
| "research X" | `just research topic X` |
| "deep research X" | `just research deep X` |
| "quick lookup on X" | `just research quick X` |
| "research X, Y, and Z" | `just research batch "X\|Y\|Z"` |
| "audit this site" | `just lighthouse audit <url>` |
| "audit these 5 sites" | `just audit-batch <url1> <url2> ...` |
| "build an API for X" | `just api build X` |
| "add a users endpoint" | `just api add-route users` |
| "generate SDK for X" | `just sdk build <source> X` |
| "build me an app" | `just vite build-app <name>` |
| "add a feature" | `just vite add-feature <name>` |
| "set up SEO" | `just seo all` |
| "run SEO meta tags" | `just seo meta` |
| "browse this page" | `just playwright skill <prompt>` |
| "QA test this" | `just playwright qa <prompt>` |
| "build full project" | `just project-setup <name>` |
| "build API and SDK" | `just api-and-sdk <name>` |

## Coordination Model

- **Single agent** — one Claude instance, no coordination needed
- **Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) — agents that talk to each other via `SendMessage` and `TaskList`. Used when agents within one workstream need to coordinate (e.g. research orchestrator managing 3 workers).
- **mprocs** — terminal multiplexer for running independent workstreams in parallel. Each pane is a separate Claude instance. Used when tasks don't need to communicate (e.g. researching 3 different topics, or auditing 5 URLs).
- **Teams inside mprocs** — the most powerful pattern. Each mprocs pane runs an orchestrated team. Multiple coordinated workstreams running in parallel.

## Adding New Recipes

When adding a recipe to any `skill.just`:

1. Use `+args` (not `args`) for multi-word parameters
2. Add a `#` comment above each recipe (shows in `just --list`)
3. Multi-agent recipes should depend on `ensure-mprocs`
4. Use shebang `#!/usr/bin/env bash` for multi-line recipes
5. Generate mprocs YAML via `mktemp` and clean up after

## Reference

- [just docs](https://github.com/casey/just)
- [mprocs docs](https://github.com/pvolok/mprocs)
- Install mprocs: `.claude/setup/install-mprocs.sh`
