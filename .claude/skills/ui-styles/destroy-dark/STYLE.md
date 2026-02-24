# Style: destroy-dark

Dark theme with purple/violet accents, glassmorphism, animated gradient borders, and glow effects. Extracted from destroy.network.

## Vibe

Moody, premium, developer-oriented. Deep charcoal backgrounds with purple energy. Glassmorphism headers, animated gradient borders on CTAs, radial glow effects, grid overlays. Everything floats and glows subtly.

## Palette Preview

| Role | Value | Description |
|------|-------|-------------|
| Background | `#1b1b1f` | Deep charcoal |
| Surface | `#202127` | Slightly lighter |
| Elevated | `#2a2a32` | Cards, modals |
| Primary | `#646cff` | Blue-violet |
| Accent | `#8b5cf6` | Purple (main brand) |
| Glow | `#bd34fe` | Magenta glow |
| Cyan | `#41d1ff` | Secondary accent |
| Text | `rgba(255,255,255,0.95)` | Near-white |
| Muted | `rgba(235,235,245,0.6)` | Subdued text |

## Fonts

- **Sans:** Inter (400, 500, 600, 700) — body, UI, headings
- **Mono:** JetBrains Mono (400, 500) — code, badges, data

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## Key Effects

- **Glassmorphism** — `backdrop-filter: blur(8px)` on headers and overlays
- **Animated gradient borders** — flowing purple gradient on CTAs using `mask-composite`
- **Radial glow** — `radial-gradient(circle, rgba(139,92,246,0.2), transparent 70%)`
- **Grid overlay** — 40px grid with `rgba(139,92,246,0.04)` lines
- **Hover lift** — `translateY(-2px)` to `translateY(-4px)` on interactive elements
- **Custom scrollbars** — Purple gradient thumb on hover

## References

- `references/colors.md` — full color tokens
- `references/typography.md` — font system and scale
- `references/spacing.md` — spacing, radii, containers
- `references/components.md` — button, card, input, badge, header
- `references/animations.md` — keyframes, transitions
- `references/effects.md` — glassmorphism, gradients, glows, scrollbars
