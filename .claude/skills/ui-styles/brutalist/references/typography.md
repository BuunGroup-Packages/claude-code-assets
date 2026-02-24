# Typography — brutalist

## Font Stack

```css
:root {
  --font-sans: 'Space Grotesk', 'Arial Black', Helvetica, sans-serif;
  --font-mono: 'Space Mono', 'Courier New', monospace;
}
```

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

## Type Scale

Oversized, dramatic range.

```css
:root {
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
  --text-hero: clamp(4rem, 10vw, 8rem);
  --text-section: clamp(2.5rem, 6vw, 5rem);
}
```

## Weights

Only two: regular and bold.

```css
:root {
  --font-normal: 400;
  --font-bold: 700;
}
```

## Heading Styles

```css
h1 {
  font-size: var(--text-hero);
  font-weight: var(--font-bold);
  line-height: 0.9;
  letter-spacing: -0.04em;
  text-transform: uppercase;
}

h2 {
  font-size: var(--text-section);
  font-weight: var(--font-bold);
  line-height: 0.95;
  letter-spacing: -0.03em;
}
```

## Labels

```css
.label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}
```
