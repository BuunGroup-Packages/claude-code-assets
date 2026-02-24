# Style: corporate

Professional, data-dense, neutral palette. Clean dashboards, structured layouts, and subtle accents. Prioritizes readability and information density.

## Vibe

Polished, trustworthy, functional. Neutral backgrounds with subtle warm tints. Clean card-based layouts with data visualizations. Professional typography with tight spacing. Minimal decoration — the data speaks.

## Palette Preview

| Role | Value | Description |
|------|-------|-------------|
| Background | `#ffffff` | White |
| Surface | `#f6f7ed` | Warm off-white |
| Elevated | `#f4f4f4` | Light gray |
| Primary | `#1f1f1f` | Near-black |
| Accent | `#2563eb` | Blue (links, active) |
| Accent alt | `#10b981` | Teal/green (success, charts) |
| Text | `#1f1f1f` | Near-black |
| Text muted | `#6b7280` | Mid-gray |
| Border | `#e5e7eb` | Light gray |

## Fonts

General Sans or Inter — professional, readable, geometric.

```css
--font-sans: 'General Sans', 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'SF Mono', monospace;
```

```html
<!-- General Sans from fontshare.com, or fallback to Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## Key Patterns

- **Card-based dashboards** — Bordered cards with data widgets, charts, KPIs
- **Sidebar navigation** — Vertical nav with icons, active state highlight
- **Data tables** — Clean rows with hover highlights, status badges
- **KPI cards** — Large numbers with small labels and trend indicators
- **Subtle shadows** — Very light drop shadows, no glow effects
- **Muted accents** — Blue for active/links, green for success/positive
- **Serif accent** — Optional serif/italic for marketing headings
- **Kanban boards** — Column-based task/pipeline views

## References

- `references/colors.md`
- `references/typography.md`
- `references/spacing.md`
- `references/components.md`
- `references/animations.md`

## Status

Skeleton — add example screenshots to `examples/` and flesh out references.
