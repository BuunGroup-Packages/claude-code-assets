# SDK Generator — TypeScript/Python SDKs from API docs
# Multi-agent recipes use mprocs by default

set quiet

# List SDK generator recipes
default:
    @just --list sdk

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single command ───────────────────────────────────────

# Analyze API source
analyze +source:
    claude --dangerously-skip-permissions --model opus "/api:sdk-generator analyze {{source}}"

# Scaffold empty SDK
init +name:
    claude --dangerously-skip-permissions --model haiku "/api:sdk-generator init {{name}}"

# Add resource class
add-resource +name:
    claude --dangerously-skip-permissions --model sonnet "/api:sdk-generator add-resource {{name}}"

# Generate core modules
core:
    claude --dangerously-skip-permissions --model sonnet "/api:sdk-generator core"

# Generate tests
tests:
    claude --dangerously-skip-permissions --model sonnet "/api:sdk-generator tests"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Full SDK build — analyze + generate + test via mprocs
build +args: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/sdk-build-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      analyzer:
        shell: "claude --dangerously-skip-permissions --model opus '/api:sdk-generator analyze {{args}}'"
        cwd: "$(pwd)"
      builder:
        shell: "claude --dangerously-skip-permissions --model opus '/api:sdk-generator build {{args}}'"
        cwd: "$(pwd)"
        autostart: false
      tests:
        shell: "claude --dangerously-skip-permissions --model sonnet '/api:sdk-generator tests'"
        cwd: "$(pwd)"
        autostart: false
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
