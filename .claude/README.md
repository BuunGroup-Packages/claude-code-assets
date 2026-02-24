# Claude Code Assets

Reusable skills, commands, and justfile recipes for Claude Code.

## Prerequisites

- [just](https://github.com/casey/just) 1.19+ (`brew install just` or `cargo install just`)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

## Quick Start

```bash
cd .claude

# List all available commands
just

# List a skill module's recipes
just lighthouse
```

## Architecture

```
.claude/
  justfile              ← root: top-level recipes + mod declarations
  commands/             ← /slash commands (route args to skills)
  skills/
    <skill>/
      SKILL.md          ← what Claude reads (instructions + reference)
      skill.just        ← reusable just recipes (invoke claude + command)
      docs/             ← extended reference (reduced token load)
```

Four layers, each building on the last:

| Layer | What | How | Example |
|-------|------|-----|---------|
| **Skill** | Capability | Claude reads SKILL.md | `/lighthouse audit https://example.com` |
| **Command** | Routing | commands/*.md parses args, invokes skill | `/lighthouse perf https://example.com desktop` |
| **Justfile** | Reusability | skill.just invokes `claude /command` | `just lighthouse perf https://example.com` |
| **Composition** | Chaining | Root justfile composes recipes | `just automate-amazon "keyboards, monitors"` |

### Flow

```
just lighthouse audit https://example.com
  -> claude --dangerously-skip-permissions --model opus "/lighthouse audit https://example.com"
    -> Claude reads commands/lighthouse.md (routing)
      -> Claude reads skills/lighthouse/SKILL.md (instructions)
        -> runs: npx lighthouse https://example.com ...
```

## Skill Modules

Each skill can expose a `skill.just` file with reusable recipes. The root justfile registers them with `mod`:

```just
mod lighthouse 'skills/lighthouse/skill.just'
mod seo        'skills/seo/skill.just'
```

Recipes are namespaced: `just <module> <recipe> [args]`

### lighthouse

| Recipe | Usage |
|--------|-------|
| `just lighthouse audit <url> [desktop]` | Full audit, all categories |
| `just lighthouse perf <url> [desktop]` | Performance only |
| `just lighthouse a11y <url>` | Accessibility only |
| `just lighthouse seo <url>` | SEO only |
| `just lighthouse desktop <url>` | Desktop + opens report |
| `just lighthouse budget <url> [budget.json]` | Audit with budget |
| `just lighthouse scores [report.json]` | Extract scores from report |
| `just lighthouse batch <url1> <url2> ...` | Batch audit URLs |

### Top-Level Recipes

| Recipe | Description |
|--------|-------------|
| `just test-playwright-skill` | Playwright skill direct |
| `just test-chrome-skill` | Chrome skill direct |
| `just test-playwright-agent` | Playwright subagent |
| `just test-chrome-agent` | Chrome subagent |
| `just test-qa` | QA agent validation |
| `just hop [workflow] [prompt]` | Browser automation workflow |
| `just ui-review` | Parallel user story validation |
| `just automate-amazon [prompt]` | Amazon add-to-cart |
| `just summarize-blog [url]` | Summarize latest blog post |

## Adding a New Skill Module

1. Create `skills/<name>/skill.just` with recipes that invoke `claude /command`:
   ```just
   audit url:
       claude --dangerously-skip-permissions --model opus "/my-skill audit {{url}}"
   ```

2. Create `commands/<name>.md` to route arguments to the skill:
   ```markdown
   ---
   description: What this command does
   argument-hint: "[command] [args]"
   ---
   Parse $ARGUMENTS and invoke the skill.
   ```

3. Register the module in the root justfile:
   ```just
   mod my-skill 'skills/my-skill/skill.just'
   ```

4. Run: `just my-skill audit https://example.com`
