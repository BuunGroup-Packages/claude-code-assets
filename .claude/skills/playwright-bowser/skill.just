# Playwright Bowser — browser automation, QA, workflows
# Multi-agent recipes use mprocs by default

set quiet

default_prompt := "Get the current date, then go to XXXX, find the latest blog post by Simon, summarize it, and give it a rating out of 10."

default_qa_prompt := "Navigate to XXXX. Verify the front page loads with posts. Click 'More' to go to the next page. Verify page 2 loads with a new set of posts. Go back to page 1. Click into the first post's comments link. Verify the comments page loads and at least one comment is visible."

default_hop_demo_prompt := "m4 mac mini with top specs, flowers for valentines day, pack of 10 sketch notebooks, mechanical keyboard with brown switches, USB-C docking station, blue light blocking glasses, standing desk anti-fatigue mat, Anker wireless charging pad"

# List playwright-bowser recipes
default:
    @just --list playwright

# ─── mprocs helper ────────────────────────────────────────

[private]
ensure-mprocs:
    #!/usr/bin/env bash
    command -v mprocs &>/dev/null || .claude/setup/install-mprocs.sh

# ─── Single agent ─────────────────────────────────────────

# Playwright skill — direct (headless by default)
skill headed="true" prompt=default_prompt:
    claude --dangerously-skip-permissions --model opus "/playwright-bowser (headed: {{headed}}) {{prompt}}"

# Chrome skill — direct (requires --chrome)
chrome prompt=default_prompt:
    claude --dangerously-skip-permissions --model opus --chrome "/claude-bowser {{prompt}}"

# Playwright subagent — isolated browser session
agent headed="true" prompt=default_prompt:
    claude --dangerously-skip-permissions --model opus "Use a @playwright-bowser-agent to do this: (headed: {{headed}}) {{prompt}}"

# Chrome subagent (requires --chrome)
chrome-agent prompt=default_prompt:
    claude --dangerously-skip-permissions --model opus --chrome "Use a @claude-bowser-agent to do this: {{prompt}}"

# QA agent — single story validation
qa headed="true" prompt=default_qa_prompt:
    claude --dangerously-skip-permissions --model opus "Use a @bowser-qa-agent: (headed: {{headed}}) {{prompt}}"

# Summarize a blog's latest post (headless, no auth needed)
blog url="https://XXX/":
    claude --dangerously-skip-permissions --model opus "/bowser:hop-automate blog-summarizer \"{{url}}\" playwright headless"

# ─── Multi-agent (mprocs) ────────────────────────────────

# Run a saved browser automation workflow (requires --chrome)
hop workflow="amazon-add-to-cart" prompt="pack of 10 sketch notebooks" *flags="":
    export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 && claude --dangerously-skip-permissions --model opus --chrome "/bowser:hop-automate {{workflow}} {{prompt}} {{flags}}"

# UI Review — parallel QA agents via mprocs
ui-review headed="headed" filter="" *flags="": ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/ui-review-XXXX.yaml)
    cat > "$cfg" <<YAML
    procs:
      orchestrator:
        shell: "claude --dangerously-skip-permissions --model opus '/ui-review {{headed}} {{filter}} {{flags}}'"
        cwd: "$(pwd)"
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"

# Amazon add-to-cart — multiple items via mprocs
amazon prompt=default_hop_demo_prompt: ensure-mprocs
    #!/usr/bin/env bash
    cfg=$(mktemp /tmp/amazon-XXXX.yaml)
    IFS=',' read -ra ITEMS <<< "{{prompt}}"
    procs=""
    i=1
    for item in "${ITEMS[@]}"; do
      item=$(echo "$item" | xargs)
      procs="$procs
      item-$i:
        shell: \"claude --dangerously-skip-permissions --model opus --chrome '/bowser:hop-automate amazon-add-to-cart $item'\"
        cwd: \"$(pwd)\""
      i=$((i+1))
    done
    cat > "$cfg" <<YAML
    procs:$procs
    YAML
    mprocs --config "$cfg"
    rm -f "$cfg"
