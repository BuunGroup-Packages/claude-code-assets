# Colors — destroy-dark

## Tokens

```css
:root {
  /* ── Background ── */
  --color-bg: #1b1b1f;
  --color-surface: #202127;
  --color-elevated: #2a2a32;
  --color-code-bg: #161618;

  /* ── Borders ── */
  --color-border: #2e2e32;
  --color-border-hover: #414146;

  /* ── Brand ── */
  --color-primary: #646cff;
  --color-primary-hover: #747bff;
  --color-accent: #8b5cf6;
  --color-accent-light: #a78bfa;
  --color-glow: #bd34fe;
  --color-deep: #370a7f;
  --color-cyan: #41d1ff;

  /* ── Text ── */
  --color-text: rgba(255, 255, 255, 0.95);
  --color-text-muted: rgba(235, 235, 245, 0.6);
  --color-text-subtle: rgba(235, 235, 245, 0.38);

  /* ── Status ── */
  --color-success: #42b883;
  --color-error: #ed4245;
  --color-warning: #fab005;

  /* ── Shadows ── */
  --shadow-subtle: 0 4px 12px rgba(0, 0, 0, 0.15);
  --shadow-medium: 0 20px 40px rgba(0, 0, 0, 0.3);
  --shadow-glow: 0 0 40px rgba(139, 92, 246, 0.2);
  --shadow-glow-strong: 0 0 20px rgba(139, 92, 246, 0.4), 0 0 40px rgba(139, 92, 246, 0.2);
  --shadow-focus: 0 0 0 3px rgba(139, 92, 246, 0.1);
}
```

## Selection

```css
::selection {
  background: rgba(139, 92, 246, 0.3);
  color: #fff;
}
```

## Usage

| Use Case | Token |
|----------|-------|
| Page background | `--color-bg` |
| Card / panel | `--color-surface` |
| Modal / elevated | `--color-elevated` |
| Code blocks | `--color-code-bg` |
| Primary actions | `--color-accent` |
| Links | `--color-primary` |
| Body text | `--color-text` |
| Secondary text | `--color-text-muted` |
| Placeholder | `--color-text-subtle` |
| Default border | `--color-border` |
| Hover border | `--color-border-hover` |
