# Color System

## Design Tokens

```css
:root {
  /* ========================================
     BRAND COLORS
     ======================================== */
  --color-primary: #0066ff;
  --color-primary-hover: #0052cc;
  --color-primary-light: #e6f0ff;

  --color-secondary: #6366f1;
  --color-secondary-hover: #4f46e5;

  --color-accent: #f59e0b;
  --color-accent-hover: #d97706;

  /* ========================================
     SEMANTIC COLORS
     ======================================== */
  --color-success: #16a34a;
  --color-success-light: #dcfce7;
  --color-success-dark: #15803d;

  --color-warning: #f59e0b;
  --color-warning-light: #fef3c7;
  --color-warning-dark: #b45309;

  --color-error: #dc2626;
  --color-error-light: #fee2e2;
  --color-error-dark: #b91c1c;

  --color-info: #0ea5e9;
  --color-info-light: #e0f2fe;
  --color-info-dark: #0284c7;

  /* ========================================
     NEUTRAL COLORS (Light Mode)
     ======================================== */
  --color-bg: #ffffff;
  --color-bg-subtle: #f9fafb;
  --color-surface: #f3f4f6;
  --color-surface-hover: #e5e7eb;

  --color-border: #e5e7eb;
  --color-border-strong: #d1d5db;

  --color-text: #1f2937;
  --color-text-secondary: #4b5563;
  --color-text-muted: #6b7280;
  --color-text-disabled: #9ca3af;
  --color-text-inverse: #ffffff;

  /* ========================================
     SHADOWS
     ======================================== */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04);

  /* Focus ring */
  --shadow-focus: 0 0 0 3px rgba(0, 102, 255, 0.3);
}
```

## Dark Mode

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f172a;
    --color-bg-subtle: #1e293b;
    --color-surface: #334155;
    --color-surface-hover: #475569;

    --color-border: #334155;
    --color-border-strong: #475569;

    --color-text: #f1f5f9;
    --color-text-secondary: #cbd5e1;
    --color-text-muted: #94a3b8;
    --color-text-disabled: #64748b;

    --color-primary-light: #1e3a5f;
    --color-success-light: #14532d;
    --color-warning-light: #422006;
    --color-error-light: #450a0a;
    --color-info-light: #0c4a6e;

    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.4);
    --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.5);
  }
}
```

## Manual Dark Mode Toggle

```css
[data-theme="dark"] {
  --color-bg: #0f172a;
  --color-bg-subtle: #1e293b;
  /* ... same as @media above */
}
```

```tsx
// Toggle dark mode
function toggleTheme() {
  const current = document.documentElement.dataset.theme;
  document.documentElement.dataset.theme = current === "dark" ? "light" : "dark";
}
```

## Color Usage Guidelines

| Use Case | Token |
|----------|-------|
| Page background | `--color-bg` |
| Card/panel background | `--color-surface` |
| Primary buttons | `--color-primary` |
| Body text | `--color-text` |
| Secondary text | `--color-text-secondary` |
| Placeholder text | `--color-text-muted` |
| Borders | `--color-border` |
| Success messages | `--color-success` |
| Error messages | `--color-error` |
| Warnings | `--color-warning` |

## Contrast Ratios

All color combinations meet WCAG 2.1 AA:

| Combination | Ratio |
|-------------|-------|
| `--color-text` on `--color-bg` | 14.5:1 |
| `--color-text-secondary` on `--color-bg` | 7.5:1 |
| `--color-text-muted` on `--color-bg` | 4.6:1 |
| `--color-text-inverse` on `--color-primary` | 4.8:1 |
