# Style: llamaindex-ai

Clean, modern SaaS aesthetic with bold gradient accents on a crisp white canvas. OverusedGrotesk gives it a distinctive, slightly editorial edge.

## Vibe

Predominantly white with light gray (#f5f5f5) section alternation. The brand identity relies on vivid multi-stop gradients — cyan to blue to pink to orange — used as accent strokes, CTA backgrounds, and decorative elements. Typography is tight and confident: OverusedGrotesk with negative letter-spacing on headings, IBM Plex Mono for code/labels. Layout uses CSS Grid with generous whitespace and strong vertical rhythm.

## Palette Preview

| Role | Value | Description |
|------|-------|-------------|
| Background | `#ffffff` | Pure white base |
| Surface | `#f5f5f5` | Light gray alternate sections |
| Primary | `#000000` | Black — buttons, text, borders |
| Accent | `linear-gradient(139.49deg, #37d7fa, #4b72fe, #ff8df2, #ff8705)` | Brand gradient (cyan → blue → pink → orange) |
| Text | `#000000` | Primary text color |
| Text muted | `#7f7f7f` | Secondary/descriptive text |
| Border | `#e7e7e7` | Light gray borders and dividers |

## Fonts

OverusedGrotesk variable font for all body/heading text. IBM Plex Mono for code snippets and technical labels.

```css
--font-sans: "OverusedGrotesk", system-ui, sans-serif;
--font-mono: "IBMPlexMono", ui-monospace, monospace;
```

## Key Patterns

- **Grid sections** — Full-width CSS Grid with `[full-start] 40px [content-start] 1360px [content-end] 40px [full-end]` column template
- **Gradient accents** — Multi-stop gradients (cyan → blue → pink → orange) on CTAs, borders, and decorative elements
- **Tight headings** — Large font sizes (55–79px) with negative letter-spacing (-1.6 to -2.4px) and font-weight 500
- **Alternating sections** — White (#fff) and light (#f5f5f5) section backgrounds with generous vertical padding (80–160px)
- **Minimal borders** — 1px solid #e7e7e7 dividers, very few border-radius (mostly 0px, occasional 12px)
- **Fast transitions** — 75ms default duration for color/background, ease-out for opacity/transform

## References

- `references/colors.md` — full color tokens
- `references/typography.md` — font system and scale
- `references/spacing.md` — spacing, radii, containers
- `references/components.md` — component patterns
- `references/animations.md` — transitions and motion

## Examples

See `examples/` for reference screenshots.
Source: https://www.llamaindex.ai/
