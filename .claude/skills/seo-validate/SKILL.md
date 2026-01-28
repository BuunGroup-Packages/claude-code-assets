---
name: seo-validate
description: |
  Run full SEO validation with Lighthouse. Returns scores for Performance,
  Accessibility, Best Practices, SEO. Use for auditing, verifying implementation,
  or checking Lighthouse scores.
argument-hint: "[url] [target_score]"
allowed-tools: Bash, Read, Glob, Grep
---

# SEO Validation Suite

## Overview

Runs comprehensive Lighthouse audit in isolated context.
Returns detailed scores and actionable recommendations.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | url | Local dev URL (localhost only) | http://localhost:3000 |
| $2 | target_score | Minimum score (0-100) | 100 |

## Usage

```bash
/seo-validate                           # Defaults to localhost:3000
/seo-validate http://localhost:4321     # Astro default port
/seo-validate http://localhost:3000 95  # Custom target score
/seo-validate http://localhost:5173     # Vite default port
```

## IMPORTANT: Local Development Only

Lighthouse MUST run against your **local dev server**, NOT a remote/production URL:
- ✓ `http://localhost:3000`
- ✓ `http://localhost:4321`
- ✓ `http://127.0.0.1:3000`
- ✗ `https://mysite.com` (will be rejected)

Start your dev server first:
```bash
npm run dev    # Most frameworks
pnpm dev       # pnpm
yarn dev       # yarn
```

## Prerequisites

1. Dev server running at target URL
2. Playwright installed: `uv tool install playwright`
3. Chromium browser: `playwright install chromium`

## Validation Steps

### 1. Server Check

Verify dev server is accessible:
```bash
curl -s -o /dev/null -w "%{http_code}" $URL
```

If not 200, ask user to start dev server first.

### 2. Lighthouse Audit

Run the lighthouse script:
```bash
uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/lighthouse.py --url $URL --target $TARGET_SCORE
```

This outputs scores and issues. **After outputting results, STOP.**

## Score Targets

| Category | Target | Weight |
|----------|--------|--------|
| Performance | 100 | Core Web Vitals |
| Accessibility | 100 | WCAG 2.1 AA |
| Best Practices | 100 | Security, HTTPS |
| SEO | 100 | Meta, crawlability |

## Report Output

Reports are automatically saved to `reports/seo/lighthouse-{timestamp}.json`.

Lighthouse temp directories are cleaned up automatically:
- Windows: `AppData\Local\lighthouse.*`
- Linux/WSL: `/tmp/lighthouse.*`

## Output Format

Returns structured report:

```json
{
  "success": true,
  "url": "http://localhost:4321",
  "timestamp": "2025-01-22T10:30:00Z",
  "scores": {
    "performance": 100,
    "accessibility": 100,
    "bestPractices": 100,
    "seo": 100
  },
  "coreWebVitals": {
    "LCP": 1.2,
    "FID": 50,
    "CLS": 0.05,
    "INP": 120
  },
  "ai": {
    "llmsTxt": true,
    "robotsAllowsAI": true,
    "structuredData": true
  },
  "issues": [],
  "recommendations": []
}
```

## Failure Report

On scores below target:

```
✗ LIGHTHOUSE VALIDATION FAILED
URL: http://localhost:4321
Target: 100 | Achieved: Performance 85, SEO 92

============================================================
SCORE BREAKDOWN:
============================================================

Performance: 85/100 (FAIL - need +15)
  - LCP: 3.2s (target: <2.5s)
  - CLS: 0.15 (target: <0.1)
  
Accessibility: 100/100 (PASS)

Best Practices: 100/100 (PASS)

SEO: 92/100 (FAIL - need +8)
  - Missing meta description on 2 pages
  - Images missing alt text

============================================================
FIX INSTRUCTIONS:
============================================================

1. [LH_PERF] Performance at 85
   Rule: Performance score must be ≥100
   Fix: Optimize images, add lazy loading, preload fonts.

2. [LH_SEO] SEO at 92
   Rule: SEO score must be ≥100
   Fix: Add missing meta descriptions, fix image alt text.

============================================================
Run /seo-perf and /seo-meta to fix, then re-validate.
```

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| LH_PERF | error | Performance below target |
| LH_A11Y | error | Accessibility below target |
| LH_BEST | error | Best Practices below target |
| LH_SEO | error | SEO below target |
| LH_CONN | error | Cannot connect to URL |
| LH_TIME | error | Lighthouse timeout |

## Integration

After validation fails, run specific skills to fix:

| Issue | Skill |
|-------|-------|
| SEO score low | /seo-meta |
| Performance low | /seo-perf |
| Missing structured data | /seo-schema |
| AI crawler blocked | /seo-ai |

Then re-run `/seo-validate` to confirm fixes.

## Completion

After running Lighthouse and outputting results, STOP immediately. Do not continue or loop.
