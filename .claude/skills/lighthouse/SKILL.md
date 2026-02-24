---
name: lighthouse
description: Run Lighthouse audits via CLI for performance, accessibility, best-practices, and SEO scoring. Headless by default. Outputs HTML/JSON/CSV reports. Keywords - lighthouse, audit, performance, accessibility, seo, core web vitals, page speed.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Lighthouse CLI

## Purpose

Run Google Lighthouse audits from the CLI. Produces scores for performance, accessibility, best-practices, and SEO. Headless by default, outputs HTML/JSON/CSV reports.

## Key Details

- **Requires** Node 22+ and Google Chrome installed
- **Headless by default** — no `--chrome-flags` needed for CI
- **Four categories** — `performance`, `accessibility`, `best-practices`, `seo`
- **Three output formats** — `html` (visual), `json` (machine-readable), `csv`
- **Mobile by default** — use `--preset=desktop` for desktop scoring + emulation
- **Token-efficient** — parse JSON output programmatically, skip verbose logs with `--quiet`

## Quick Reference

```
# Basic audit (mobile, all categories, HTML report)
npx lighthouse <url>

# Desktop audit, open report in browser
npx lighthouse <url> --preset=desktop --view

# JSON output, specific categories
npx lighthouse <url> --only-categories=performance,seo --output json --output-path=./report.json --quiet

# Multiple output formats at once
npx lighthouse <url> --output json --output html --output-path=./report

# CI-friendly headless
npx lighthouse <url> --chrome-flags="--headless --no-sandbox" --output json --output-path=./report.json --quiet

# Accessibility only
npx lighthouse <url> --only-categories=accessibility --view

# With auth header
npx lighthouse <url> --extra-headers='{"Authorization":"Bearer TOKEN"}'

# Performance budget
npx lighthouse <url> --budget-path=./budget.json

# No throttling (real network conditions)
npx lighthouse <url> --throttling-method=provided --screenEmulation.disabled --no-emulatedUserAgent

# Save trace data for debugging
npx lighthouse <url> --save-assets
```

## Workflow

1. **Run the audit** with appropriate flags for the task:
```bash
npx lighthouse <url> --preset=desktop --output json --output html --output-path=./lighthouse-report --quiet
```

2. **Parse JSON results** to extract scores:
```bash
# Extract category scores from JSON report
node -e "
const r = require('./lighthouse-report.report.json');
const c = r.categories;
Object.keys(c).forEach(k => console.log(k + ': ' + Math.round(c[k].score * 100)));
"
```

3. **Review HTML report** for detailed diagnostics:
```bash
# Open in browser
npx lighthouse <url> --view
```

4. **Fix issues** identified in the audit, then re-run to verify improvements.

## Common Flags

```
Output:     --output [html|json|csv], --output-path <path>, --view, --quiet, --verbose
Categories: --only-categories=performance,accessibility,best-practices,seo
Audits:     --only-audits [ids], --skip-audits [ids], --list-all-audits
Device:     --preset=desktop, --form-factor [mobile|desktop]
Emulation:  --screenEmulation.width=N, --screenEmulation.height=N, --screenEmulation.disabled
Throttling: --throttling-method [simulate|devtools|provided], --throttling.cpuSlowdownMultiplier=N
Network:    --extra-headers '<json>', --blocked-url-patterns [patterns]
Chrome:     --chrome-flags="<flags>", --port <N>, --disable-storage-reset
Budget:     --budget-path <path>
Artifacts:  -G (gather only), -A (audit only), -GA (both), --save-assets
```

## Scoring

Scores range 0-100. Categories:
- **Performance** — weighted average of FCP, SI, LCP, TBT, CLS
- **Accessibility** — weighted pass/fail per WCAG audit
- **Best Practices** — equal weight per audit
- **SEO** — equal weight per audit

## JSON Result Structure

```
lhr.categories.performance.score      # 0-1 (multiply by 100)
lhr.categories.accessibility.score
lhr.categories['best-practices'].score
lhr.categories.seo.score
lhr.audits[id].score                  # 0-1 or null
lhr.audits[id].numericValue           # raw metric (ms, bytes, etc.)
lhr.audits[id].displayValue           # formatted string
lhr.audits[id].details                # detailed findings
lhr.finalDisplayedUrl                 # final URL after redirects
lhr.runWarnings                       # array of warnings
```

## Performance Budget (budget.json)

```json
[{
  "path": "/*",
  "resourceSizes": [
    {"resourceType": "script", "budget": 125},
    {"resourceType": "total", "budget": 300}
  ],
  "timings": [
    {"metric": "interactive", "budget": 3000}
  ]
}]
```

Resource types: `document`, `font`, `image`, `media`, `script`, `stylesheet`, `third-party`, `total`

## Full Reference

See [docs/lighthouse-cli.md](docs/lighthouse-cli.md) for complete flag reference, Node API, user flows, CI config, and throttling details.
