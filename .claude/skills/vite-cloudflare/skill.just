# Vite + React + Cloudflare Workers + Hono
# Multi-agent recipes use mprocs by default

set quiet

# List vite-cloudflare recipes
default:
    @just --list vite

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single command ───────────────────────────────────────

# Scaffold project
init +name:
    claude --dangerously-skip-permissions --model haiku "/vite:vite-cloudflare init {{name}}"

# Add React component
component +args:
    claude --dangerously-skip-permissions --model haiku "/vite:vite-cloudflare component {{args}}"

# Add React Router page
page +args:
    claude --dangerously-skip-permissions --model haiku "/vite:vite-cloudflare page {{args}}"

# Add D1/R2/KV binding
binding +args:
    claude --dangerously-skip-permissions --model haiku "/vite:vite-cloudflare binding {{args}}"

# Add Hono API route (delegates to api-generator)
api +resource:
    claude --dangerously-skip-permissions --model sonnet "/vite:vite-cloudflare api {{resource}}"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Full app build — parallel frontend + API via mprocs
build-app +name: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/vite-build-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      frontend:
        shell: "claude --dangerously-skip-permissions --model sonnet '/vite:vite-cloudflare build-app {{name}}'"
        cwd: "$(pwd)"
      api:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator init {{name}}'"
        cwd: "$(pwd)"
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"

# Full app build with a UI style — applies style tokens + components
build-styled style +name: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/vite-styled-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      frontend:
        shell: "claude --dangerously-skip-permissions --model sonnet '/vite:vite-cloudflare build-app {{name}} with the {{style}} style'"
        cwd: "$(pwd)"
      api:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator init {{name}}'"
        cwd: "$(pwd)"
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"

# Add feature — parallel page + component + API via mprocs
add-feature +name: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/vite-feature-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      page:
        shell: "claude --dangerously-skip-permissions --model sonnet '/vite:vite-cloudflare page {{name}} --with-components'"
        cwd: "$(pwd)"
      api-route:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator add-route {{name}}'"
        cwd: "$(pwd)"
      api-schema:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator add-schema {{name}}'"
        cwd: "$(pwd)"
      api-service:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:api-generator add-service {{name}}'"
        cwd: "$(pwd)"
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
