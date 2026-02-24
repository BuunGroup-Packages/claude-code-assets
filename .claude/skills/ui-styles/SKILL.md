---
name: ui-styles
description: Selectable UI style presets for consistent theming. Each style has its own folder with references (typography, colors, spacing, components, animations) and example screenshots. Apply a named style when building apps with vite-cloudflare or any frontend skill. Keywords - ui, style, theme, design, tokens, colors, fonts.
---

# UI Styles

## Purpose

Apply a consistent, named UI style when building frontend apps. Each style is a complete design system with detailed reference docs that agents read to generate accurate CSS.

## Available Styles

| Style | Theme | Vibe | Font |
|-------|-------|------|------|
| `destroy-dark` | Dark | Purple glassmorphism, gradient borders, glow effects | Inter + JetBrains Mono |
| `modern` | Light + Dark sections | Clean SaaS, photo-heavy cards, lime accents | System stack |
| `brutalist` | Light | Raw, bold, high-contrast, oversized type | Mono / grotesque |
| `corporate` | Light | Professional, data-dense, neutral palette | General Sans / Inter |
| `llamaindex-ai` | Light | Clean SaaS, gradient accents (cyan→blue→pink→orange), editorial type | OverusedGrotesk + IBM Plex Mono |

## Folder Structure

Each style follows this layout:

```
<style-name>/
├── STYLE.md            # Overview — palette preview, fonts, vibe
├── references/
│   ├── colors.md       # Full color tokens + dark mode
│   ├── typography.md   # Font stack, scale, weights, features
│   ├── spacing.md      # Spacing scale, radii, containers
│   ├── components.md   # Button, Card, Input, Badge, Header CSS
│   ├── animations.md   # Keyframes, transitions, effects
│   └── effects.md      # (optional) Glassmorphism, gradients, glows
└── examples/           # Reference screenshots
```

## Usage

### With vite-cloudflare

```
Use @vite-cloudflare to build my-app with the destroy-dark style
```

The skill reads the style's `STYLE.md` and `references/` to generate `tokens.css`, `animations.css`, and component CSS.

### Standalone

```
Apply the modern style to this project
```

### Pre-Flight (for agents)

When applying a style, read these files in order:
1. `<style>/STYLE.md` — overview and palette
2. `<style>/references/colors.md` — exact color tokens
3. `<style>/references/typography.md` — font system
4. `<style>/references/components.md` — component patterns
5. `<style>/references/animations.md` — motion and transitions
6. `<style>/examples/` — visual reference (read screenshots)

## Adding a New Style

### Manual

1. Create `<name>/` folder with `STYLE.md`, `references/`, `examples/`
2. Add reference screenshots to `examples/`
3. Fill in reference docs following existing styles as templates
4. Add the style to the table above

### From a Live Website (ui-clone)

Use the `ui-clone` skill to automatically extract a website's design system into a new style preset:

```
/ui-clone https://llamaindex.ai          # full clone
/ui-clone quick https://stripe.com       # fast homepage-only
just clone full https://vercel.com       # via just
```

This creates a complete `ui-styles/<slug>/` preset with all reference files, ready to use with `just styles apply <slug>` or `@vite-cloudflare`.
