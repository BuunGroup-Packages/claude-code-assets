# Typography System

## Font Stack

```css
:root {
  /* System font stack - fast loading, native feel */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, "Helvetica Neue", Arial, sans-serif;

  /* Monospace for code */
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo,
               Consolas, "Liberation Mono", monospace;

  /* Optional: Custom fonts (load via @font-face) */
  --font-display: var(--font-sans);
}
```

## Type Scale

```css
:root {
  /* Base size */
  --text-base: 1rem;      /* 16px */

  /* Scale (1.25 ratio - Major Third) */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-md: 1rem;        /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  --text-6xl: 3.75rem;    /* 60px */
}
```

## Line Heights

```css
:root {
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}
```

## Font Weights

```css
:root {
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

## Typography Classes

```css
/* Headings */
.heading-1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.025em;
}

.heading-2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
}

.heading-3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
}

.heading-4 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
}

/* Body text */
.body-large {
  font-size: var(--text-lg);
  line-height: var(--leading-relaxed);
}

.body {
  font-size: var(--text-md);
  line-height: var(--leading-normal);
}

.body-small {
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
}

/* Utility */
.caption {
  font-size: var(--text-xs);
  line-height: var(--leading-normal);
  color: var(--color-text-muted);
}

.overline {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--color-surface);
  padding: 0.125em 0.375em;
  border-radius: 0.25rem;
}
```

## Responsive Typography

```css
/* Fluid typography - scales with viewport */
html {
  font-size: clamp(14px, 1vw + 12px, 18px);
}

/* Or explicit breakpoints */
@media (max-width: 640px) {
  .heading-1 { font-size: var(--text-3xl); }
  .heading-2 { font-size: var(--text-2xl); }
}
```

## Usage in Components

```tsx
// Typography component (optional)
interface TextProps {
  as?: "h1" | "h2" | "h3" | "h4" | "p" | "span";
  variant?: "heading-1" | "heading-2" | "body" | "caption";
  children: React.ReactNode;
}

export const Text: FC<TextProps> = ({
  as: Component = "p",
  variant = "body",
  children
}) => (
  <Component className={variant}>{children}</Component>
);
```

## Best Practices

1. **Hierarchy** - Use max 3-4 heading levels per page
2. **Line length** - Aim for 50-75 characters for body text
3. **Contrast** - Ensure text meets WCAG AA (4.5:1 for body, 3:1 for large)
4. **Spacing** - Use margin-bottom on headings, not margin-top on paragraphs
