# Typography — corporate

## Font Stack

```css
:root {
  --font-sans: 'General Sans', 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
  --font-serif: 'Georgia', 'Times New Roman', serif; /* optional: marketing headings */
}
```

## Type Scale

Compact, information-dense.

```css
:root {
  --text-xs: 0.75rem;    /* 12px — badges, captions */
  --text-sm: 0.8125rem;  /* 13px — table data, metadata */
  --text-base: 0.875rem; /* 14px — body text (dense) */
  --text-lg: 1rem;       /* 16px — subheadings */
  --text-xl: 1.125rem;   /* 18px — section headings */
  --text-2xl: 1.5rem;    /* 24px — page titles */
  --text-3xl: 2rem;       /* 32px — marketing headers */
  --text-stat: clamp(2rem, 4vw, 3rem); /* KPI numbers */
}
```

## Weights

```css
:root {
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

## Line Heights

```css
:root {
  --leading-tight: 1.25;
  --leading-body: 1.5;
  --leading-relaxed: 1.6;
}
```

## Base Styles

```css
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text);
  line-height: var(--leading-body);
  -webkit-font-smoothing: antialiased;
}

h1 { font-size: var(--text-2xl); font-weight: var(--font-semibold); line-height: var(--leading-tight); }
h2 { font-size: var(--text-xl); font-weight: var(--font-semibold); }
h3 { font-size: var(--text-lg); font-weight: var(--font-medium); }
```

## KPI Numbers

```css
.stat-number {
  font-size: var(--text-stat);
  font-weight: var(--font-bold);
  letter-spacing: -0.02em;
  line-height: 1;
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-trend {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.stat-trend--up { color: var(--color-success); }
.stat-trend--down { color: var(--color-error); }
```
