---
name: seo
description: Full SEO implementation with auto-validation hooks. Meta tags, JSON-LD, AI crawlers, Core Web Vitals, sitemaps, assets, Lighthouse.
argument-hint: "[command] [framework]"
user-invokable: true
hooks:
  PostToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_meta_validate.py"
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_schema_validate.py"
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_ai_validate.py"
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_perf_validate.py"
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_sitemap_validate.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_assets_validate.py"
---

# SEO Orchestrator

Implement SEO by invoking the appropriate command(s). STOP after outputting the final report.

## Commands

| Command | Reference | Description |
|---------|-----------|-------------|
| `meta [framework]` | `references/meta.md` | Meta tags, OG, Twitter Cards |
| `schema [type]` | `references/schema.md` | JSON-LD structured data |
| `ai [action]` | `references/ai.md` | llms.txt, AI crawler config |
| `perf [target]` | `references/perf.md` | Core Web Vitals optimization |
| `sitemap [framework]` | `references/sitemap.md` | XML sitemap generation |
| `assets [logo] [color]` | `references/assets.md` | Favicons, OG images, manifests |
| `validate [url]` | `references/validate.md` | Lighthouse audit |
| `all [framework]` | all above | Full SEO setup |

## Agents

| Agent | What it does |
|-------|--------------|
| @seo-auditor | Read-only audit of current SEO state |
| @seo-research | Web search for latest SEO best practices |

## Workflow

1. Detect framework from package.json if not provided
2. Read the matching `references/*.md` for the command
3. Execute the command following reference patterns
4. Each edit auto-validates via PostToolUse hooks
5. If validation fails, fix issues before proceeding
6. For `all`, execute commands in sequence: meta, schema, ai, perf, sitemap, assets
7. For `validate`, use the `lighthouse` skill: `mkdir -p "$CLAUDE_PROJECT_DIR/lighthouse" && npx lighthouse <URL> --preset=desktop --output json --output html --output-path=$CLAUDE_PROJECT_DIR/lighthouse/report --chrome-flags="--headless --no-sandbox" --quiet`
8. For `assets`, run generator: `uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/generate_assets.py`
9. **For Vite projects**: set up post-build prerendering (see `references/meta/vite.md`). Without it, crawlers see an empty SPA shell and all SEO work is invisible.
10. **STOP** after outputting the final report

## Vite SPA Prerendering

Vite SPAs are client-rendered — crawlers see `<div id="root"></div>` with no content. For Vite projects, use the `puppeteer` skill to create `scripts/prerender-pages.mjs` (post-build headless Chrome rendering) and wire into the build script. See `references/meta/vite.md` for the full script, API mocking patterns, and setup.

## Validate Command

Uses the `lighthouse` skill (`npx lighthouse`) instead of Python scripts. Requires Node 22+ and Chrome. See `references/validate.md`.

## Completion

After executing all tasks, output this report then STOP:

```
## SEO Complete

**Command**: [COMMAND]
**Framework**: [detected or provided]

### Results
| Skill | Status |
|-------|--------|
| meta | pass / fail |
| schema | pass / fail |
| ai | pass / fail |
| perf | pass / fail |
| sitemap | pass / fail |
| assets | pass / fail |
| validate | score/100 |
```

**IMPORTANT**: Do not continue after outputting this report. The task is complete.
