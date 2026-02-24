# Lighthouse — audit performance, accessibility, best-practices, seo

set quiet

default_url := "https://example.com"

# List lighthouse recipes
default:
    @just --list lighthouse

# ─── Skill (direct) ─────────────────────────────────────────

# Full audit — all categories
audit url=default_url preset="mobile" *flags="":
    claude --dangerously-skip-permissions --model opus "/lighthouse audit {{url}} {{ if preset == "desktop" { "desktop" } else { "" } }} {{flags}}"

# Performance-only audit
perf url=default_url preset="mobile":
    claude --dangerously-skip-permissions --model opus "/lighthouse perf {{url}} {{ if preset == "desktop" { "desktop" } else { "" } }}"

# Accessibility-only audit
a11y url=default_url:
    claude --dangerously-skip-permissions --model opus "/lighthouse a11y {{url}}"

# SEO-only audit
seo url=default_url:
    claude --dangerously-skip-permissions --model opus "/lighthouse seo {{url}}"

# Desktop audit + open report in browser
desktop url=default_url:
    claude --dangerously-skip-permissions --model opus "/lighthouse desktop {{url}}"

# Audit with performance budget
budget url=default_url budget_path="./budget.json":
    claude --dangerously-skip-permissions --model opus "/lighthouse budget {{url}} {{budget_path}}"

# Extract scores from JSON report
scores report="./lighthouse-report.report.json":
    claude --dangerously-skip-permissions --model opus "/lighthouse scores {{report}}"

# Batch audit multiple URLs
batch +urls:
    claude --dangerously-skip-permissions --model opus "/lighthouse batch {{urls}}"
