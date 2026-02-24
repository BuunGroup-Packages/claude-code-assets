---
description: Clone a website's visual design system into a reusable ui-styles preset
argument-hint: "<url> [--pages='/about,/pricing']"
---

# UI Clone

Parse the command from `$ARGUMENTS` and execute using the `ui-clone` skill.

## Pre-Flight

Read these before starting extraction:
- `.claude/skills/ui-clone/SKILL.md`
- `.claude/skills/ui-clone/references/extraction-workflow.md` (or `quick-workflow.md`)
- `.claude/skills/ui-clone/references/page-evaluate.md`
- `.claude/skills/ui-clone/references/output-templates.md`
- `.claude/skills/puppeteer/SKILL.md`

## Command Routing

| Pattern | Reference | Description |
|---------|-----------|-------------|
| `clone <url>` | `references/extraction-workflow.md` | Full extraction (homepage + key pages) |
| `clone <url> --pages="..."` | `references/extraction-workflow.md` | Full extraction + specified pages |
| `quick <url>` | `references/quick-workflow.md` | Homepage only, fast extraction |

## Execution

1. Parse `$ARGUMENTS` to extract the command keyword and URL
2. Read pre-flight docs
3. Follow the appropriate workflow reference
4. Write output to `ui-styles/<slug>/` and `$CLAUDE_PROJECT_DIR/ui-clones/<slug>/`
5. Update `ui-styles/SKILL.md` table

## Default Behavior

If no command keyword, treat as `clone`:
```
/ui-clone https://llamaindex.ai                         -> clone https://llamaindex.ai
/ui-clone clone https://llamaindex.ai                   -> clone https://llamaindex.ai
/ui-clone quick https://stripe.com                      -> quick https://stripe.com
/ui-clone clone https://vercel.com --pages="/pricing"   -> clone with extra pages
```
