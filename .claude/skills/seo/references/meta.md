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
/seo meta astro src/layouts/Layout.astro
/seo meta nextjs
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

- **Astro**: See [meta/astro.md](meta/astro.md)
- **Vite/React**: See [meta/vite.md](meta/vite.md) — **requires post-build prerendering** (Vite SPAs serve empty `<div id="root">` to crawlers)
- **TanStack Start**: See [meta/tanstack.md](meta/tanstack.md)
- **Next.js**: See [meta/nextjs.md](meta/nextjs.md)

### Vite SPA Warning

Vite SPAs are client-rendered only. Crawlers (Google, social platforms, AI bots) see no meta tags, no content, no JSON-LD — just the shell HTML. **All SEO work is invisible without prerendering.** The Vite reference includes a Puppeteer post-build prerender script that captures fully-rendered HTML per route. This is mandatory for Vite projects.

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

============================================================
After fixing, save file. Validation re-runs automatically.
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
| META016 | error | Non-descriptive link text |

## Link Text Requirements

Links must have descriptive text for SEO and accessibility. Avoid generic text:

**Bad (triggers META016):**
- "Learn more"
- "Click here"
- "Read more"
- "Here"
- "More info"

**Good:**
- "Learn more about our painting courses"
- "View our gallery of student artwork"
- "Read our guide to watercolor techniques"

The validation checks `<a>`, `<Link>`, and `<NavLink>` elements.
