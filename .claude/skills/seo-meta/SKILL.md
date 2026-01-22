---
name: seo-meta
description: |
  Implement SEO meta tags: title, description, Open Graph, Twitter Cards,
  canonical URLs, viewport. Auto-validates via PostToolUse hook. Use when
  adding or fixing meta tags, implementing social sharing, or setting up
  head management. Supports Astro, Vite, TanStack Start, Next.js.
argument-hint: "[framework] [file]"
hooks:
  PostToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_meta_validate.py"
---

# SEO Meta Tags

## Overview

Implements all required meta tags for SEO and social sharing.
PostToolUse hook validates every edit automatically.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | framework | astro, vite, tanstack, nextjs | Auto-detect |
| $2 | file | Target file path | Layout file |

## Usage

```bash
/seo-meta astro src/layouts/Layout.astro
/seo-meta nextjs
```

## Required Tags

| Tag | Max Length | Error Code |
|-----|------------|------------|
| `<title>` | 60 chars | META001-003 |
| `<meta name="description">` | 160 chars | META004-006 |
| `<link rel="canonical">` | - | META007 |
| `<meta name="viewport">` | - | META008 |
| `<meta property="og:title">` | 60 chars | META009 |
| `<meta property="og:description">` | 160 chars | META010 |
| `<meta property="og:image">` | Absolute URL | META011-012 |
| `<meta property="og:url">` | - | META013 |
| `<meta name="twitter:card">` | - | META014 |

## Implementation

Select framework reference:

- **Astro**: See [references/astro.md](references/astro.md)
- **Vite/React**: See [references/vite.md](references/vite.md)
- **TanStack Start**: See [references/tanstack.md](references/tanstack.md)
- **Next.js**: See [references/nextjs.md](references/nextjs.md)

## Validation

PostToolUse hook runs `post_meta_validate.py` after every edit.

**On failure**, returns:
```
✗ META VALIDATION FAILED
File: src/layouts/Layout.astro
Errors: 2 | Warnings: 1

============================================================
FIX INSTRUCTIONS (execute in order):
============================================================

1. [META004] <meta name="description"> at line 12
   Rule: Page must have meta description
   Expected: <meta name="description" content="...">
   Fix: Add inside <head>. 150-160 chars recommended.

2. [META011] <meta property="og:image">
   Rule: Page must have Open Graph image
   Expected: <meta property="og:image" content="https://...">
   Fix: Add absolute URL. Image should be 1200x630px.

============================================================
After fixing, save file. Validation re-runs automatically.
```

**On success**, returns:
```
✓ META validation passed for src/layouts/Layout.astro
```

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| META001 | error | Missing title |
| META002 | error | Title too long (>60) |
| META003 | warning | Title too short (<10) |
| META004 | error | Missing description |
| META005 | warning | Description too long (>160) |
| META006 | warning | Description too short (<120) |
| META007 | error | Missing canonical |
| META008 | error | Missing viewport |
| META009 | error | Missing og:title |
| META010 | error | Missing og:description |
| META011 | error | Missing og:image |
| META012 | error | og:image not absolute URL |
| META013 | error | Missing og:url |
| META014 | error | Missing twitter:card |
| META015 | warning | Missing robots directive |
