---
description: Run just recipes — route requests to the right skill module and recipe
argument-hint: "[module] [recipe] [args]"
---

# Just

Route user requests to the correct just module and recipe. Read `.claude/justfile` to discover available modules and recipes.

## Pre-Flight

1. Read `.claude/justfile` to see available modules and cross-skill recipes
2. Read the relevant `skill.just` if you need recipe details

## Command Routing

### Modules

| Pattern | Description |
|---------|-------------|
| `research topic <topic>` | Orchestrated research team on a topic |
| `research deep <topic>` | Deep research with browser support |
| `research quick <topic>` | Single-agent quick research |
| `research batch "<t1>\|<t2>\|<t3>"` | Multiple topics in parallel (mprocs) |
| `lighthouse audit <url>` | Full Lighthouse audit |
| `lighthouse perf <url>` | Performance-only audit |
| `lighthouse batch <url1> <url2>` | Batch audit multiple URLs |
| `playwright skill <prompt>` | Direct browser automation |
| `playwright agent <prompt>` | Browser subagent |
| `playwright qa <prompt>` | QA user story validation |
| `api build <name>` | Full API generation (mprocs) |
| `api plan <context>` | Architecture plan |
| `api add-route <resource>` | Add route module |
| `sdk build <source> <name>` | Full SDK generation (mprocs) |
| `sdk analyze <source>` | Analyze API docs |
| `seo all` | Full SEO setup (mprocs) |
| `seo meta` | Meta tags only |
| `seo validate <url>` | Lighthouse SEO audit |
| `vite build-app <name>` | Full app scaffold (mprocs) |
| `vite add-feature <name>` | Add feature (mprocs) |
| `vite component <name>` | Add React component |

### Cross-Skill Recipes

| Pattern | Description |
|---------|-------------|
| `research-and-audit <url> <topic>` | Research + Lighthouse in parallel |
| `project-setup <name>` | API + frontend + SEO in parallel |
| `api-and-sdk <name>` | Build API then generate SDK |
| `audit-batch <url1> <url2> ...` | Audit multiple URLs in parallel |

## Execution

1. Parse `$ARGUMENTS` to determine the module and recipe
2. Run the recipe from the `.claude/` directory: `just --justfile .claude/justfile <module> <recipe> <args>`
3. If no arguments, run `just --justfile .claude/justfile` to list all available modules
4. If only a module is given, run `just --justfile .claude/justfile <module>` to list its recipes

## Smart Routing

If the user doesn't specify a module, infer it:

| User says | Route to |
|-----------|----------|
| "research X" | `research topic X` |
| "look up X" | `research quick X` |
| "audit example.com" | `lighthouse audit example.com` |
| "build an API" | `api build <name>` |
| "generate SDK" | `sdk build <source> <name>` |
| "set up SEO" | `seo all` |
| "build me an app" | `vite build-app <name>` |
| "browse example.com" | `playwright skill browse example.com` |
| "QA test this" | `playwright qa <prompt>` |
