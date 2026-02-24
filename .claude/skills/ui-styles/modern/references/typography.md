# Typography — modern

## Font Stack

```css
:root {
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace;
}
```

No custom web fonts — system stack for fast loading and native feel.

## Type Scale

```css
:root {
  --text-xs: 0.75rem;    /* 12px — overlines, captions */
  --text-sm: 0.875rem;   /* 14px — small body, metadata */
  --text-base: 1rem;     /* 16px — body text */
  --text-lg: 1.125rem;   /* 18px — large body, descriptions */
  --text-xl: 1.25rem;    /* 20px — subheadings */
  --text-2xl: 1.5rem;    /* 24px — section subheads */
  --text-3xl: clamp(1.875rem, 4vw, 2.5rem);  /* section headings */
  --text-hero: clamp(2.5rem, 6vw, 4rem);      /* hero headings */
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
  --leading-body: 1.6;
  --leading-heading: 1.15;
  --leading-tight: 1.25;
}
```

## Heading Styles

```css
h1 {
  font-size: var(--text-hero);
  font-weight: var(--font-bold);
  line-height: var(--leading-heading);
  letter-spacing: -0.02em;
}

h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-heading);
  letter-spacing: -0.01em;
}

h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
}
```

## Overline

Used above section headings in lime color.

```css
.overline {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-accent);
}
```

## Stats Numbers

Large display numbers for metrics sections.

```css
.stat-number {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: var(--font-bold);
  letter-spacing: -0.02em;
  line-height: 1;
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-top: 8px;
}
```
