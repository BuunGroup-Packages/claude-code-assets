# SEO — meta tags, JSON-LD, AI crawlers, performance, sitemaps, assets
# Multi-agent recipes use mprocs by default

set quiet

# List SEO recipes
default:
    @just --list seo

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single command ───────────────────────────────────────

# Meta tags, Open Graph, Twitter Cards
meta +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo meta {{args}}"

# JSON-LD structured data
schema +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo schema {{args}}"

# llms.txt, AI crawler config
ai +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo ai {{args}}"

# Core Web Vitals optimization
perf +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo perf {{args}}"

# XML sitemap generation
sitemap +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo sitemap {{args}}"

# Favicons, OG images, manifests
assets +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo assets {{args}}"

# Lighthouse audit
validate +args="":
    claude --dangerously-skip-permissions --model opus "/seo:seo validate {{args}}"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Full SEO setup — audit + research + implement in parallel via mprocs
all +args="": ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/seo-all-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      auditor:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @seo-auditor to audit the current SEO state of this project. Write findings to $CLAUDE_PROJECT_DIR/seo/audit.md'"
        cwd: "$(pwd)"
      researcher:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @seo-research agent to research latest SEO best practices for this project. Write findings to $CLAUDE_PROJECT_DIR/seo/research.md'"
        cwd: "$(pwd)"
      implementer:
        shell: "claude --dangerously-skip-permissions --model opus '/seo:seo all {{args}}'"
        cwd: "$(pwd)"
        autostart: false
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
