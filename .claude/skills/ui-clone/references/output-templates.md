# Output Templates

Exact markdown templates for each output file. These match the existing ui-styles format (modern, brutalist, corporate, destroy-dark). Replace `{placeholders}` with extracted data.

## STYLE.md

```markdown
# Style: {slug}

{1-2 sentence vibe description based on extracted colors, typography, and layout patterns.}

## Vibe

{2-3 sentences describing the feel: color mood, typography personality, layout rhythm, overall aesthetic.}

## Palette Preview

| Role | Value | Description |
|------|-------|-------------|
| Background | `{bg-color}` | {description} |
| Surface | `{surface-color}` | {description} |
| Primary | `{primary-color}` | {description} |
| Accent | `{accent-color}` | {description} |
| Text | `{text-color}` | {description} |
| Text muted | `{text-muted}` | {description} |
| Border | `{border-color}` | {description} |

## Fonts

{Font description — custom web fonts or system stack.}

```css
--font-sans: {primary-font-stack};
--font-mono: {mono-font-stack};
```

## Key Patterns

- **{Pattern 1}** — {description}
- **{Pattern 2}** — {description}
- **{Pattern 3}** — {description}
- **{Pattern 4}** — {description}
- **{Pattern 5}** — {description}

## References

- `references/colors.md` — full color tokens
- `references/typography.md` — font system and scale
- `references/spacing.md` — spacing, radii, containers
- `references/components.md` — component patterns
- `references/animations.md` — transitions and motion

## Examples

See `examples/` for reference screenshots.
Source: {original-url}
```

## references/colors.md

```markdown
# Colors — {slug}

## Tokens

```css
:root {
  /* ── Background ── */
  --color-bg: {value};
  --color-bg-alt: {value};
  --color-surface: {value};
  --color-elevated: {value};

  /* ── Borders ── */
  --color-border: {value};
  --color-border-subtle: {value};

  /* ── Brand ── */
  --color-primary: {value};
  --color-primary-hover: {value};
  --color-accent: {value};
  --color-accent-hover: {value};

  /* ── Text ── */
  --color-text: {value};
  --color-text-muted: {value};
  --color-text-subtle: {value};
  --color-text-inverse: {value};

  /* ── Status ── */
  --color-success: {value};
  --color-error: {value};
  --color-warning: {value};

  /* ── Shadows ── */
  --shadow-sm: {value};
  --shadow-md: {value};
  --shadow-lg: {value};
}
```

## Usage

| Use Case | Token |
|----------|-------|
| Page background | `--color-bg` |
| Card/section surface | `--color-surface` |
| Body text | `--color-text` |
| Secondary text | `--color-text-muted` |
| CTA button background | `--color-primary` |
| Accent highlights | `--color-accent` |
| Dividers | `--color-border` |
```

Note: If the site has dark mode sections or a dark theme, add a `/* ── Dark Mode ── */` section with dark variants (e.g., `--color-bg-dark`, `--color-text-on-dark`).

## references/typography.md

```markdown
# Typography — {slug}

## Font Stack

```css
:root {
  --font-sans: {sans-stack};
  --font-mono: {mono-stack};
}
```

{Note about font loading: custom web fonts vs system stack, Google Fonts links if applicable.}

## Type Scale

```css
:root {
  --text-xs: {value};    /* {px} — captions, overlines */
  --text-sm: {value};    /* {px} — small body, metadata */
  --text-base: {value};  /* {px} — body text */
  --text-lg: {value};    /* {px} — large body */
  --text-xl: {value};    /* {px} — subheadings */
  --text-2xl: {value};   /* {px} — section subheads */
  --text-3xl: {value};   /* section headings */
  --text-hero: {value};  /* hero headings */
}
```

## Weights

```css
:root {
  --font-normal: {value};
  --font-medium: {value};
  --font-semibold: {value};
  --font-bold: {value};
}
```

## Line Heights

```css
:root {
  --leading-body: {value};
  --leading-heading: {value};
  --leading-tight: {value};
}
```

## Heading Styles

```css
h1 {
  font-size: var(--text-hero);
  font-weight: var(--font-bold);
  line-height: var(--leading-heading);
  letter-spacing: {value};
}

h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-heading);
  letter-spacing: {value};
}

h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
}
```

{Add any special text styles found: overlines, stat numbers, labels, etc.}
```

## references/spacing.md

```markdown
# Spacing — {slug}

## Scale

```css
:root {
  --space-xs: {value};
  --space-sm: {value};
  --space-md: {value};
  --space-lg: {value};
  --space-xl: {value};
  --space-2xl: {value};
  --space-3xl: {value};
  --space-4xl: {value};
}
```

## Border Radius

```css
:root {
  --radius-sm: {value};
  --radius-md: {value};
  --radius-lg: {value};
  --radius-xl: {value};
  --radius-full: {value};
}
```

## Layout

```css
:root {
  --max-width: {value};
  --wrapper-padding: {value};
}

.container {
  width: 100%;
  max-width: var(--max-width);
  margin-inline: auto;
  padding-inline: var(--wrapper-padding);
}
```

## Breakpoints

| Name | Value |
|------|-------|
| Mobile | `{value}` |
| Tablet | `{value}` |
| Desktop | `{value}` |
| Wide | `{value}` |

## Section Spacing

```css
.section {
  padding-block: var(--space-4xl);
}

@media (max-width: 640px) {
  .section { padding-block: var(--space-3xl); }
}
```

## Component Spacing

| Component | Padding |
|-----------|---------|
| Button | `{value}` |
| Card | `{value}` |
| Section | `{value}` |
| Input | `{value}` |
```

## references/components.md

```markdown
# Components — {slug}

## Button — Primary

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: {value};
  padding: {value};
  background: var(--color-primary);
  color: {value};
  font-weight: {value};
  font-size: {value};
  border: {value};
  border-radius: {value};
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  {hover-styles}
}
```

## Button — Secondary

```css
.btn-secondary {
  {extracted-styles}
}
```

## Card

```css
.card {
  {extracted-styles}
}
```

## Header

```css
.header {
  {extracted-styles}
}
```

## Section

```css
.section {
  {extracted-styles}
}
```

## Footer

```css
.footer {
  {extracted-styles}
}
```

{Add additional components as detected: inputs, badges, logo bar, stats grid, etc.}
```

Include only components that were actually detected. Each component should have complete, usable CSS with token references.

## references/animations.md

```markdown
# Animations — {slug}

## Timing

```css
:root {
  --duration-fast: {value};
  --duration-normal: {value};
  --duration-smooth: {value};
  --ease-default: {value};
}
```

## Keyframes

```css
{For each detected @keyframes rule:}

@keyframes {name} {
  {frames}
}
```

## Hover States

```css
.btn:hover {
  {extracted-hover-styles}
}

.card:hover {
  {extracted-hover-styles}
}

a:hover {
  {extracted-hover-styles}
}
```

## Transitions

Common transitions found on the site:

```css
{List of transition values with context}
```

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
```

Always include the reduced motion media query, even if the source site doesn't have one.

## clone-report.json

```json
{
  "slug": "{slug}",
  "sourceUrl": "{url}",
  "extractedAt": "{ISO timestamp}",
  "pagesVisited": ["{url1}", "{url2}"],
  "raw": {
    "colors": { /* full extractColors() output */ },
    "typography": { /* full extractTypography() output */ },
    "spacing": { /* full extractSpacing() output */ },
    "layout": { /* full extractLayout() output */ },
    "components": { /* full detectComponents() output */ },
    "animations": { /* full extractAnimations() output */ },
    "icons": { /* full detectIcons() output */ }
  },
  "mapped": {
    "palette": { /* grouped color palette */ },
    "typeScale": { /* mapped token scale */ },
    "spacingScale": { /* mapped spacing tokens */ }
  },
  "screenshots": [
    "examples/full-page.png",
    "examples/header.png",
    "examples/hero.png",
    "examples/footer.png"
  ],
  "screenshotsDir": ".claude/skills/ui-styles/{slug}/examples/",
  "outputFiles": [
    "STYLE.md",
    "references/colors.md",
    "references/typography.md",
    "references/spacing.md",
    "references/components.md",
    "references/animations.md",
    "examples/*.png"
  ]
}
```
