# SEO Module

Self-validating SEO implementation for Claude Code.

## Quick Start

```bash
# 1. Install dependencies
cd .claude/setup && make

# 2. Start your dev server
npm run dev

# 3. Run full SEO implementation
/seo all astro
```

## Commands

### Full Implementation

```bash
# Implement everything (meta + schema + ai + perf) then validate
/seo all astro
/seo all nextjs
/seo all vite
```

### Audit First (Read-Only)

```bash
# See what's missing before making changes
@seo-auditor Audit this project for SEO issues
```

### Individual Skills

```bash
# Meta tags (title, description, Open Graph, Twitter Cards)
/seo meta astro
/seo meta nextjs src/app/layout.tsx

# JSON-LD structured data
/seo schema Organization
/seo schema Article src/layouts/BlogPost.astro
/seo schema LocalBusiness

# AI SEO (llms.txt, robots.txt for AI crawlers)
/seo ai llms-txt
/seo ai robots

# Performance (images, fonts, Core Web Vitals)
/seo perf all
/seo perf images
/seo perf fonts

# Lighthouse validation
/seo validate http://localhost:4321
/seo validate http://localhost:3000 95
```

## Example Workflow

### New Astro Project

```bash
# Start dev server in terminal
npm run dev

# In Claude Code:
/seo all astro

# Claude will:
# 1. Add meta tags to src/layouts/Layout.astro
# 2. Add Organization JSON-LD schema
# 3. Create public/llms.txt
# 4. Configure public/robots.txt for AI crawlers
# 5. Optimize images with width/height/lazy
# 6. Run Lighthouse to verify 100 scores
```

### Existing Next.js App

```bash
# Audit first to see current state
@seo-auditor Check SEO status

# Fix specific issues
/seo meta nextjs
/seo schema Organization

# Validate
/seo validate http://localhost:3000
```

### Fix Specific Issues

```bash
# Only missing meta tags
/seo meta

# Only JSON-LD
/seo schema Product

# Only performance
/seo perf images
```

## Supported Frameworks

| Framework | Layout File |
|-----------|-------------|
| Astro | `src/layouts/Layout.astro` |
| Next.js | `src/app/layout.tsx` |
| Vite + React | `index.html` or `src/App.tsx` |
| TanStack Start | `src/routes/__root.tsx` |

## Validation

Each skill auto-validates via PostToolUse hooks. Errors include:

```
✗ META VALIDATION FAILED
File: src/layouts/Layout.astro
Errors: 2

1. [META004] Missing meta description
   Fix: Add <meta name="description" content="...">

2. [META011] Missing og:image
   Fix: Add <meta property="og:image" content="https://...">
```

## Error Codes

| Prefix | Category |
|--------|----------|
| META0xx | Meta tags |
| SCHEMA0xx | JSON-LD |
| AI0xx | AI SEO |
| PERF0xx | Performance |
| LH_xxx | Lighthouse |
