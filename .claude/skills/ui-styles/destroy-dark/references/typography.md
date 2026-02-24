# Typography — destroy-dark

## Font Stack

```css
:root {
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
  --font-feature: 'cv02', 'cv03', 'cv04', 'cv11';
}
```

## Type Scale

```css
:root {
  --text-xs: 11px;
  --text-sm: 13px;
  --text-base: 15px;
  --text-lg: 17px;
  --text-xl: 22px;
  --text-hero: clamp(2.5rem, 6vw, 4rem);
  --text-section: clamp(2rem, 5vw, 3rem);
}
```

## Line Heights

```css
:root {
  --leading-body: 1.7;
  --leading-heading: 1.15;
  --leading-desc: 1.6;
}
```

## Letter Spacing

```css
:root {
  --tracking-body: -0.01em;
  --tracking-heading: -0.02em;
  --tracking-hero: -0.03em;
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

## Base Styles

```css
html {
  font-size: clamp(14px, 1vw + 12px, 18px);
}

body {
  font-family: var(--font-sans);
  font-feature-settings: var(--font-feature);
  color: var(--color-text);
  line-height: var(--leading-body);
  letter-spacing: var(--tracking-body);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 {
  line-height: var(--leading-heading);
  letter-spacing: var(--tracking-heading);
  font-weight: var(--font-semibold);
}

h1 { font-size: var(--text-hero); letter-spacing: var(--tracking-hero); font-weight: var(--font-bold); }
h2 { font-size: var(--text-section); }
h3 { font-size: var(--text-xl); }

code, pre {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
}
```
