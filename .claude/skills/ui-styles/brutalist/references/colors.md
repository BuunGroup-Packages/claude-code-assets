# Colors — brutalist

## Tokens

```css
:root {
  /* ── Background ── */
  --color-bg: #ffffff;
  --color-surface: #f0f0f0;
  --color-elevated: #ffffff;
  --color-inverted: #000000;

  /* ── Borders ── */
  --color-border: #000000;
  --border-width: 2px;
  --border-width-thick: 4px;

  /* ── Brand ── */
  --color-primary: #000000;
  --color-accent: #ff0000;
  --color-accent-alt: #0000ff;

  /* ── Text ── */
  --color-text: #000000;
  --color-text-muted: #666666;
  --color-text-inverse: #ffffff;

  /* ── Status ── */
  --color-success: #00ff00;
  --color-error: #ff0000;
  --color-warning: #ffff00;

  /* ── No shadows ── */
}
```

## Hover States

Color inversion instead of subtle shifts.

```css
.interactive:hover {
  background: var(--color-inverted);
  color: var(--color-text-inverse);
}
```
