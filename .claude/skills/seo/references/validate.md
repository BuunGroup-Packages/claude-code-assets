# SEO Validation Suite

## Overview

Runs comprehensive Lighthouse audit using the `lighthouse` skill (`npx lighthouse`).
Returns detailed scores and actionable recommendations.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | url | Dev URL | http://localhost:3000 |
| $2 | target_score | Minimum score (0-100) | 100 |
| $3 | preset | mobile, desktop | desktop |

## Usage

```bash
/seo validate                           # Defaults to localhost:3000
/seo validate http://localhost:4321     # Astro default port
/seo validate http://localhost:3000 95  # Custom target score
/seo validate http://localhost:5173     # Vite default port
```

## Prerequisites

1. Dev server running at target URL
2. Node 22+ and Google Chrome installed

## Validation Steps

### 1. Server Check

Verify dev server is accessible:
```bash
curl -s -o /dev/null -w "%{http_code}" $URL
```

If not 200, ask user to start dev server first.

### 2. Run Lighthouse Audit

Use `npx lighthouse` directly (from the `lighthouse` skill):

```bash
npx lighthouse "$URL" \
  --preset=desktop \
  --output json --output html \
  --output-path=./lighthouse-report \
  --chrome-flags="--headless --no-sandbox" \
  --quiet
```

### 3. Extract Scores

Parse the JSON report:
```bash
node -e "
const r = require('./lighthouse-report.report.json');
const c = r.categories;
Object.keys(c).forEach(k => console.log(k + ': ' + Math.round(c[k].score * 100)));
"
```

### 4. Evaluate Against Target

Compare each category score against TARGET_SCORE. Report pass/fail per category.

**After outputting results, STOP.**

## Score Targets

| Category | Target | Weight |
|----------|--------|--------|
| Performance | 100 | Core Web Vitals (FCP, SI, LCP, TBT, CLS) |
| Accessibility | 100 | WCAG 2.1 AA |
| Best Practices | 100 | Security, HTTPS |
| SEO | 100 | Meta, crawlability |

## JSON Result Structure

```
lhr.categories.performance.score      # 0-1 (multiply by 100)
lhr.categories.accessibility.score
lhr.categories['best-practices'].score
lhr.categories.seo.score
lhr.audits[id].score                  # 0-1 or null
lhr.audits[id].numericValue           # raw metric (ms, bytes, etc.)
lhr.audits[id].displayValue           # formatted string
```

## Failure Report

On scores below target:

```
LIGHTHOUSE VALIDATION FAILED
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
   Fix: Optimize images, add lazy loading, preload fonts.

2. [LH_SEO] SEO at 92
   Fix: Add missing meta descriptions, fix image alt text.

============================================================
Run /seo perf and /seo meta to fix, then re-validate.
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

After validation fails, run specific commands to fix:

| Issue | Command |
|-------|---------|
| SEO score low | /seo meta |
| Performance low | /seo perf |
| Missing structured data | /seo schema |
| AI crawler blocked | /seo ai |

Then re-run `/seo validate` to confirm fixes.

## Completion

After running Lighthouse and outputting results, STOP immediately. Do not continue or loop.
