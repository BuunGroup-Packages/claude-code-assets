# Research — web search, data gathering, cross-validation
# Teams for coordination, mprocs for parallel independent workstreams

set quiet

# List research recipes
default:
    @just --list research

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single agent ─────────────────────────────────────────

# Quick single-agent research
quick +topic:
    claude --dangerously-skip-permissions --model sonnet "Use a @research-agent to research: {{topic}}"

# ─── Orchestrated team ────────────────────────────────────

# Research a topic — orchestrator manages coordinated agent team
topic +topic:
    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --model opus "Use a @research-orchestrator to research: {{topic}}"

# Research with reference images for each item
images +topic:
    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --model opus "Use a @research-orchestrator to research (with images): {{topic}}"

# Deep research — orchestrator + browser + images
deep +topic:
    CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --model opus "Use a @research-orchestrator to research (with browser support and images): {{topic}}"

# ─── Image collection (standalone) ───────────────────────

# Download images for an existing research JSON file
download-images +json_path:
    claude --dangerously-skip-permissions --model sonnet "Use a @research-image-agent to download images for: {{json_path}}"

# ─── mprocs (parallel independent topics) ────────────────

# Research multiple topics in parallel — each gets its own orchestrator
batch +topics: ensure-mprocs
    #!/usr/bin/env bash
    mkdir -p "$CLAUDE_PROJECT_DIR/research"
    cfg=$(mktemp /tmp/research-batch-XXXX.yaml)
    IFS='|' read -ra ITEMS <<< "{{topics}}"
    procs="procs:"
    for item in "${ITEMS[@]}"; do
      item=$(echo "$item" | xargs)
      slug=$(echo "$item" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 20)
      procs="$procs
      $slug:
        shell: \"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions --model opus 'Use a @research-orchestrator to research: $item'\"
        cwd: \"$(pwd)\""
    done
    echo "$procs" > "$cfg"
    mprocs --config "$cfg"
    rm -f "$cfg"
