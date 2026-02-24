# Research — web search, data gathering, cross-validation
# Multi-agent recipes use mprocs by default

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

# Quick single-agent research (no orchestration)
quick +topic:
    claude --dangerously-skip-permissions --model sonnet "Use a @research-agent to research: {{topic}}"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Research a topic — 3 agents in parallel via mprocs
topic +topic: ensure-mprocs
    #!/usr/bin/env bash
    mkdir -p ./research
    cfg=$(mktemp /tmp/research-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      discover:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: broad discovery — cast a wide net, find the main items, lists, and overviews): {{topic}}'"
        cwd: "$(pwd)"
      deep-dive:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: deep dive — find detailed breakdowns, expert analysis, and primary sources): {{topic}}'"
        cwd: "$(pwd)"
      contrarian:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: contrarian — find alternative perspectives, criticisms, lesser-known entries, and things the mainstream lists miss): {{topic}}'"
        cwd: "$(pwd)"
      synthesizer:
        shell: "claude --dangerously-skip-permissions --model opus 'Read all JSON files in ./research/, merge into a single deduplicated list. Recalculate confidence: found by 3+ agents = high, 2 = medium, 1 = low. Write merged result to ./research/merged.json and print a summary table.'"
        cwd: "$(pwd)"
        autostart: false
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"

# Deep research — 3 agents + browser agent via mprocs
deep +topic: ensure-mprocs
    #!/usr/bin/env bash
    mkdir -p ./research
    cfg=$(mktemp /tmp/research-deep-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      discover:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: broad discovery — cast a wide net, find the main items, lists, and overviews): {{topic}}'"
        cwd: "$(pwd)"
      deep-dive:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: deep dive — find detailed breakdowns, expert analysis, and primary sources): {{topic}}'"
        cwd: "$(pwd)"
      contrarian:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @research-agent to research (strategy: contrarian — find alternative perspectives, criticisms, lesser-known entries, and things the mainstream lists miss): {{topic}}'"
        cwd: "$(pwd)"
      browser:
        shell: "claude --dangerously-skip-permissions --model sonnet 'Use a @playwright-bowser-agent to visit key pages about this topic and extract detailed data that may require JS rendering. Save findings to ./research/browser_findings.json: {{topic}}'"
        cwd: "$(pwd)"
      synthesizer:
        shell: "claude --dangerously-skip-permissions --model opus 'Read all JSON files in ./research/, merge into a single deduplicated list. Recalculate confidence: found by 3+ agents = high, 2 = medium, 1 = low. Write merged result to ./research/merged.json and print a summary table.'"
        cwd: "$(pwd)"
        autostart: false
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
