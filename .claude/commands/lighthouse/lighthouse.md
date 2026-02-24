---
description: Run Lighthouse audits for performance, accessibility, best-practices, SEO
argument-hint: "[command] [url] [flags]"
---

# Lighthouse

Parse the command from `$ARGUMENTS` and execute using the `lighthouse` skill.

## Command Routing

| Pattern | Description |
|---------|-------------|
| `audit <url>` | Full audit — all categories, HTML + JSON output |
| `audit <url> desktop` | Full audit with desktop preset |
| `perf <url>` | Performance-only audit |
| `a11y <url>` | Accessibility-only audit |
| `seo <url>` | SEO-only audit |
| `desktop <url>` | Desktop audit, opens report in browser |
| `budget <url> [budget.json]` | Audit with performance budget |
| `scores [report.json]` | Extract scores from existing JSON report |
| `batch <url1> <url2> ...` | Batch audit multiple URLs |

## Execution

1. Parse `$ARGUMENTS` to extract the command, URL, and any extra flags
2. Invoke the `lighthouse` skill to run the appropriate `npx lighthouse` command
3. Default to headless (`--chrome-flags="--headless --no-sandbox"`) and `--quiet`
4. Output reports to `./lighthouse-report` (or `./lighthouse-reports/` for batch)
5. If no command matches, show the help table
