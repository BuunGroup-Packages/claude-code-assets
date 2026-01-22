---
name: seo
model: opus
description: Full SEO implementation. Orchestrates meta, schema, ai, perf skills.
argument-hint: "[command] [framework]"
---

# SEO Orchestrator

## Variables

COMMAND: $1 (meta, schema, ai, perf, sitemap, assets, validate, all)
FRAMEWORK: $2 (astro, vite, tanstack, nextjs, auto)

## Instructions

Implement SEO by invoking the appropriate skill(s). STOP after outputting the final report.

## Workflow

1. Detect framework from package.json if FRAMEWORK is "auto" or not provided
2. Execute skill(s) based on COMMAND:
   - `meta` → /seo-meta FRAMEWORK
   - `schema` → /seo-schema Organization
   - `ai` → /seo-ai llms-txt
   - `perf` → /seo-perf all
   - `sitemap` → /seo-sitemap FRAMEWORK
   - `assets` → Run: `uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/generate_assets.py`
   - `validate` → Run: `uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/lighthouse.py --url <URL>`
   - `all` → execute all above in sequence
3. Each skill self-validates via PostToolUse hooks
4. If any skill fails validation, fix issues before proceeding
5. **STOP** after outputting the final report - do not continue

## Skills

| Command | Skill | What it does |
|---------|-------|--------------|
| meta | /seo-meta | Meta tags, Open Graph, Twitter Cards |
| schema | /seo-schema | JSON-LD structured data |
| ai | /seo-ai | llms.txt, AI crawler config |
| perf | /seo-perf | Core Web Vitals optimization |
| sitemap | /seo-sitemap | XML sitemap generation |
| assets | /seo-assets | Favicons, OG images, manifests |
| validate | /seo-validate | Full Lighthouse audit |

## Agents

| Agent | What it does |
|-------|--------------|
| @seo-auditor | Read-only audit of current SEO state |
| @seo-research | Web search for latest SEO best practices |

## Completion

After executing all tasks, output this report then STOP immediately:

```
## SEO Complete

**Command**: [COMMAND]
**Framework**: [detected or provided]

### Results
| Skill | Status |
|-------|--------|
| meta | ✓ / ✗ |
| schema | ✓ / ✗ |
| ai | ✓ / ✗ |
| perf | ✓ / ✗ |
| sitemap | ✓ / ✗ |
| assets | ✓ / ✗ |
| validate | score/100 |
```

**IMPORTANT**: Do not continue after outputting this report. The task is complete.
