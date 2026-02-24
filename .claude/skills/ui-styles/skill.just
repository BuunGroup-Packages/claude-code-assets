# UI Styles — selectable design system presets
# Each style is a folder with STYLE.md, references/, and examples/

set quiet

# List ui-styles recipes
default:
    @just --list ui-styles

# ─── Single commands ─────────────────────────────────────

# List available styles
list:
    @echo "Available UI styles:"
    @echo "  destroy-dark  — Dark theme, purple/violet accents, glassmorphism"
    @echo "  modern        — Light + dark sections, lime CTAs, photo-heavy cards"
    @echo "  brutalist     — Raw, bold, high-contrast, oversized mono type"
    @echo "  corporate     — Professional, data-dense, neutral dashboards"

# Clone a website's style — see `just clone` for full options
clone-from +url:
    claude --dangerously-skip-permissions --model opus "Use @ui-clone to clone {{url}}"

# Apply a style to the current project — generates CSS in src/client/styles/
apply +style:
    claude --dangerously-skip-permissions --model sonnet "Read .claude/skills/ui-styles/{{style}}/STYLE.md and all files in .claude/skills/ui-styles/{{style}}/references/ then generate tokens.css, animations.css, and global.css in src/client/styles/ following that style's design system exactly."

# Preview a style — summarize its design system
preview +style:
    claude --dangerously-skip-permissions --model haiku "Read .claude/skills/ui-styles/{{style}}/STYLE.md and summarize: palette, fonts, component patterns, key effects."
