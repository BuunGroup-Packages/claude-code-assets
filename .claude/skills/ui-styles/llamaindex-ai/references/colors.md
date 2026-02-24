# Colors — llamaindex-ai

## Tokens

```css
:root {
  /* ── Background ── */
  --color-bg: #ffffff;
  --color-bg-alt: #f5f5f5;
  --color-surface: #f5f5f5;
  --color-elevated: #ffffff;

  /* ── Borders ── */
  --color-border: #e7e7e7;
  --color-border-subtle: rgba(0, 0, 0, 0.08);

  /* ── Brand ── */
  --color-primary: #000000;
  --color-primary-hover: #333333;
  --color-accent-gradient: linear-gradient(139.49deg, #37d7fa 9.62%, #4b72fe 39.56%, #ff8df2 60.52%, #ff8705 84.47%);
  --color-accent-gradient-vertical: linear-gradient(0deg, #8aeaff 0%, #83a3ff 33.33%, #fca6f3 66.67%, #fba647 100%);
  --color-accent-gradient-soft: linear-gradient(359.8deg, #f5f5f5 3.29%, #92aeff 39.66%, #96e7f9 94.22%);

  /* ── Text ── */
  --color-text: #000000;
  --color-text-muted: #7f7f7f;
  --color-text-subtle: #5f5f5f;
  --color-text-inverse: #ffffff;
  --color-text-on-light: #f5f5f5;

  /* ── Status ── */
  --color-success: #22c55e;
  --color-error: #e51520;
  --color-warning: #f59e0b;

  /* ── Shadows ── */
  --shadow-sm: none;
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
}
```

## Gradient Library

The brand relies heavily on gradients instead of solid accent colors:

```css
/* Diagonal rainbow — primary brand gradient (CTAs, hero accents) */
.gradient-brand {
  background: linear-gradient(139.49deg, #37d7fa 9.62%, #4b72fe 39.56%, #ff8df2 60.52%, #ff8705 84.47%);
}

/* Vertical rainbow — decorative stripes, border accents */
.gradient-vertical {
  background: linear-gradient(0deg, #8aeaff 0%, #83a3ff 33.33%, #fca6f3 66.67%, #fba647 100%);
}

/* Soft blue — section backgrounds, hero overlays */
.gradient-soft {
  background: linear-gradient(359.8deg, #f5f5f5 3.29%, #92aeff 39.66%, #96e7f9 94.22%);
}

/* Blue horizontal — announcement bar, badges */
.gradient-blue {
  background: linear-gradient(270deg, #92aeff 25%, #12d4ff 90%);
}

/* Pink-cyan diagonal — card accents */
.gradient-pink-cyan {
  background: linear-gradient(221.53deg, #51dbf7 0%, #f7a8ea 100%);
}

/* Orange-pink diagonal — card accents alt */
.gradient-orange-pink {
  background: linear-gradient(221.53deg, #ff8705 0%, #ff8df2 100%);
}
```

## Usage

| Use Case | Token |
|----------|-------|
| Page background | `--color-bg` |
| Alternate section background | `--color-bg-alt` |
| Card/section surface | `--color-surface` |
| Body text | `--color-text` |
| Secondary text | `--color-text-muted` |
| Descriptive text | `--color-text-subtle` |
| CTA button background | `--color-primary` |
| Brand accent | `--color-accent-gradient` |
| Dividers | `--color-border` |
| Subtle separators | `--color-border-subtle` |
