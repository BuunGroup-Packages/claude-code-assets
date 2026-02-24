# Colors — modern

## Tokens

```css
:root {
  /* ── Background ── */
  --color-bg: #ffffff;
  --color-bg-dark: #1a2e1a;
  --color-surface: #f5f5f0;
  --color-surface-dark: #243524;
  --color-elevated: #ffffff;

  /* ── Borders ── */
  --color-border: #e5e5e0;
  --color-border-dark: rgba(255, 255, 255, 0.1);

  /* ── Brand ── */
  --color-primary: #1a2e1a;
  --color-primary-hover: #2a4a2a;
  --color-accent: #c8ee44;
  --color-accent-hover: #b8de34;

  /* ── Text ── */
  --color-text: #1a1a1a;
  --color-text-muted: #666666;
  --color-text-subtle: #999999;
  --color-text-inverse: #ffffff;
  --color-text-on-dark: rgba(255, 255, 255, 0.9);
  --color-text-muted-on-dark: rgba(255, 255, 255, 0.6);

  /* ── Status ── */
  --color-success: #22c55e;
  --color-error: #ef4444;
  --color-warning: #f59e0b;

  /* ── Shadows ── */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.12);
  --shadow-focus: 0 0 0 3px rgba(26, 46, 26, 0.15);
}
```

## Usage

| Use Case | Light Section | Dark Section |
|----------|---------------|--------------|
| Background | `--color-bg` | `--color-bg-dark` |
| Surface | `--color-surface` | `--color-surface-dark` |
| Body text | `--color-text` | `--color-text-on-dark` |
| Muted text | `--color-text-muted` | `--color-text-muted-on-dark` |
| CTA button | `--color-primary` bg | `--color-accent` bg |
| Border | `--color-border` | `--color-border-dark` |
