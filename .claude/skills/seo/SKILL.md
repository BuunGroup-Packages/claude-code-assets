---
name: seo
model: opus
description: Full SEO implementation. Orchestrates meta, schema, ai, perf skills.
argument-hint: "[command] [framework]"
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/generate_report.py"
---

# SEO Orchestrator

## Variables

COMMAND: $1 (meta, schema, ai, perf, validate, all)
FRAMEWORK: $2 (astro, vite, tanstack, nextjs, auto)

## Instructions

Implement SEO by invoking the appropriate skill(s).

## Workflow

1. Detect framework from package.json if FRAMEWORK is "auto" or not provided
2. Execute skill(s) based on COMMAND:
   - `meta` → /seo-meta FRAMEWORK
   - `schema` → /seo-schema Organization
   - `ai` → /seo-ai llms-txt
   - `perf` → /seo-perf all
   - `validate` → /seo-validate http://localhost:4321
   - `all` → execute all above in sequence
3. Each skill self-validates via PostToolUse hooks
4. If any skill fails validation, fix issues before proceeding

## Skills

| Command | Skill | What it does |
|---------|-------|--------------|
| meta | /seo-meta | Meta tags, Open Graph, Twitter Cards |
| schema | /seo-schema | JSON-LD structured data |
| ai | /seo-ai | llms.txt, AI crawler config |
| perf | /seo-perf | Core Web Vitals optimization |
| validate | /seo-validate | Full Lighthouse audit |

## Report

After completing:

## SEO Complete

**Command**: [COMMAND]
**Framework**: [detected or provided]
**Skills executed**: [list of skills run]
**Validation**: [pass/fail per skill]
