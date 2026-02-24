# API Generator — Hono + Cloudflare Workers APIs
# Multi-agent recipes use mprocs by default

set quiet

# List API generator recipes
default:
    @just --list api

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single command ───────────────────────────────────────

# Architecture plan
plan +args:
    claude --dangerously-skip-permissions --model opus "/api:api-generator plan {{args}}"

# Scaffold empty project
init +name:
    claude --dangerously-skip-permissions --model haiku "/api:api-generator init {{name}}"

# Add route module
add-route +resource:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator add-route {{resource}}"

# Add service layer
add-service +resource:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator add-service {{resource}}"

# Add Zod schemas
add-schema +resource:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator add-schema {{resource}}"

# Add middleware
add-middleware +type:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator add-middleware {{type}}"

# Add Drizzle table
add-db +resource:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator add-db {{resource}}"

# Generate tests
tests:
    claude --dangerously-skip-permissions --model sonnet "/api:api-generator tests"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Full API build — parallel phases via mprocs
build +args: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/api-build-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      planner:
        shell: "claude --dangerously-skip-permissions --model opus '/api:api-generator plan {{args}}'"
        cwd: "$(pwd)"
      builder:
        shell: "claude --dangerously-skip-permissions --model opus '/api:api-generator build {{args}}'"
        cwd: "$(pwd)"
        autostart: false
      tests:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator tests'"
        cwd: "$(pwd)"
        autostart: false
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
