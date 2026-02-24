---
name: ui-clone
description: Clone a website's visual design system — colors, typography, spacing, layout, components, animations — and produce a reusable ui-styles preset. Keywords - clone, extract, design system, scrape, visual, style, theme.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user-invokable: true
---

# UI Clone

## Purpose

Visit a live website, extract its complete visual design system, capture reference screenshots, and produce a structured `ui-styles/<slug>/` preset that other skills (vite-cloudflare, etc.) can consume directly.

## Commands

| Command | Description |
|---------|-------------|
| `clone <url>` | Full extraction — homepage + auto-detect key pages |
| `clone <url> --pages="/about,/pricing"` | Full extraction + specified additional pages |
| `quick <url>` | Homepage only, fast extraction |

Default: if no command keyword, treat as `clone`.

## Pre-Flight

1. Read `references/extraction-workflow.md` (or `quick-workflow.md` for `quick`)
2. Read `references/page-evaluate.md` for all extraction scripts
3. Read `references/output-templates.md` for output file formats
4. Read the `puppeteer` skill SKILL.md for Puppeteer API patterns

## Workflow (clone)

1. **Parse URL** — derive site slug (e.g., `https://llamaindex.ai` -> `llamaindex-ai`)
2. **Create output dirs**:
   - `.claude/skills/ui-styles/<slug>/references/`
   - `.claude/skills/ui-styles/<slug>/examples/`
   - `$CLAUDE_PROJECT_DIR/ui-clones/<slug>/`
3. **Launch Puppeteer** — 1440x900 viewport, 2x device scale factor
4. **Navigate** — `goto(url, { waitUntil: 'networkidle2' })`
5. **Dismiss cookie banners** — click common consent selectors
6. **Run extraction scripts** — via `page.evaluate()` (from `references/page-evaluate.md`):
   - `extractColors()` — backgrounds, text colors, borders, shadows, CSS custom properties
   - `extractTypography()` — font families, sizes, weights, line-heights, letter-spacings
   - `extractSpacing()` — margins, paddings, gaps, border-radii, max-widths
   - `extractLayout()` — flex/grid containers, breakpoints from stylesheets
   - `detectComponents()` — header, hero, buttons, cards, forms, footer
   - `extractAnimations()` — transitions, keyframes from stylesheets
   - `detectIcons()` — icon libraries, inline SVGs, sprites
7. **Capture screenshots**:
   - Full-page: `page.screenshot({ fullPage: true })`
   - Header: element screenshot of `header, nav, [role="banner"]`
   - Hero: first large section / `[class*="hero"]`
   - Footer: `footer, [role="contentinfo"]`
   - Cards / buttons: if detected, element-level screenshots
8. **Additional pages** (if `--pages` or auto-detected):
   - Navigate to each page, repeat extraction + screenshots
   - Merge new color/typography/spacing tokens into main data
9. **Post-process** extracted data:
   - Group raw colors into palette (primary, accent, neutral, semantic) via HSL analysis
   - Map sizes to token scale (`--text-xs` through `--text-hero`, `--space-xs` through `--space-4xl`)
   - Deduplicate and normalize values
10. **Write output files** (using templates from `references/output-templates.md`):
    - `.claude/skills/ui-styles/<slug>/STYLE.md`
    - `.claude/skills/ui-styles/<slug>/references/colors.md`
    - `.claude/skills/ui-styles/<slug>/references/typography.md`
    - `.claude/skills/ui-styles/<slug>/references/spacing.md`
    - `.claude/skills/ui-styles/<slug>/references/components.md`
    - `.claude/skills/ui-styles/<slug>/references/animations.md`
    - `$CLAUDE_PROJECT_DIR/ui-clones/<slug>/clone-report.json`
11. **Update** `.claude/skills/ui-styles/SKILL.md` — add new style to the available styles table

## Workflow (quick)

Streamlined homepage-only extraction. See `references/quick-workflow.md`.

1. Parse URL, create dirs
2. Launch Puppeteer, navigate, dismiss cookies
3. Run all extraction scripts on homepage only
4. Capture screenshots: full-page, header, hero, footer only
5. Post-process and write all output files
6. Update ui-styles table

## Output Structure

```
.claude/skills/ui-styles/<slug>/         <- style preset (used by vite-cloudflare)
  STYLE.md
  references/
    colors.md
    typography.md
    spacing.md
    components.md
    animations.md
  examples/                              <- reference screenshots live WITH the preset
    full-page.png
    header.png
    hero.png
    footer.png
    cards.png          (if found)
    buttons.png        (if found)
    <page-slug>.png    (additional pages)

$CLAUDE_PROJECT_DIR/ui-clones/<slug>/    <- raw extraction data
  clone-report.json
```

## Slug Derivation

Strip protocol and path, replace dots with hyphens, lowercase:
- `https://llamaindex.ai` -> `llamaindex-ai`
- `https://www.stripe.com/pricing` -> `stripe-com`
- `https://vercel.com` -> `vercel-com`

## Cookie Banner Dismissal

Try these selectors in order, click first match:
```
[class*="cookie"] button[class*="accept"]
[id*="cookie"] button[class*="accept"]
button[id*="accept-cookies"]
[class*="consent"] button:first-of-type
[class*="banner"] button[class*="close"]
```

## Error Handling

- If Puppeteer fails to launch: check that `puppeteer` is installed, suggest `npm i puppeteer`
- If page times out: retry once with `waitUntil: 'domcontentloaded'`
- If extraction returns empty: fall back to stylesheet-only extraction (parse CSS files)
- Always write whatever data was collected — partial output is better than none

## References

- `references/page-evaluate.md` — all extraction scripts
- `references/extraction-workflow.md` — full pipeline details
- `references/quick-workflow.md` — fast pipeline details
- `references/output-templates.md` — output file format templates
