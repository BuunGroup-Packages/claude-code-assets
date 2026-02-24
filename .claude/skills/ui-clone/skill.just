# UI Clone — extract a website's visual design system into a ui-styles preset

set quiet

# List ui-clone recipes
default:
    @just --list clone

# ─── Single commands ─────────────────────────────────────

# Full clone — homepage + auto-detect key pages
full +url:
    claude --dangerously-skip-permissions --model opus "Use @ui-clone to clone {{url}}"

# Quick clone — homepage only, fast extraction
quick +url:
    claude --dangerously-skip-permissions --model opus "Use @ui-clone to quick {{url}}"

# Full clone with specific additional pages
pages url +pages:
    claude --dangerously-skip-permissions --model opus 'Use @ui-clone to clone {{url}} --pages="{{pages}}"'
