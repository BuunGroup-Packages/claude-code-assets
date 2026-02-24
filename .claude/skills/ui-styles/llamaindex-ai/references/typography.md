# Typography — llamaindex-ai

## Font Stack

```css
:root {
  --font-sans: "OverusedGrotesk", system-ui, sans-serif;
  --font-mono: "IBMPlexMono", ui-monospace, monospace;
}
```

OverusedGrotesk is a variable font (weight 400–500) loaded from `/fonts/OverusedGrotesk-VF.woff2`. IBM Plex Mono Medium is used for code/technical labels. HubSpot forms load Inter as a fallback.

## Type Scale

```css
:root {
  --text-xs: 0.75rem;    /* 12px — mono labels, metadata */
  --text-sm: 0.875rem;   /* 14px — nav links, small body */
  --text-base: 1rem;     /* 16px — body text (most common) */
  --text-lg: 1.125rem;   /* 18px — large body */
  --text-xl: 1.5rem;     /* 24px — subheadings */
  --text-2xl: 2rem;      /* 32px — section subheads */
  --text-3xl: 2.4375rem; /* 39px — section headings */
  --text-4xl: 3.42rem;   /* 55px — page headings (h1/h2) */
  --text-hero: 4.92rem;  /* 79px — hero display text */
}
```

## Weights

```css
:root {
  --font-normal: 400;
  --font-medium: 500;
}
```

The site uses only two weights: 400 (body, nav) and 500 (headings, emphasis). No bold (700) outside of HubSpot form submit buttons.

## Line Heights

```css
:root {
  --leading-body: normal;      /* default for body text */
  --leading-heading: 1.1;      /* tight heading line-height */
  --leading-tight: 1.0;        /* very tight for hero text */
  --leading-relaxed: 1.65;     /* descriptive paragraphs */
}
```

## Letter Spacing

```css
:root {
  --tracking-body: 0;          /* body text — no adjustment */
  --tracking-label: 0.24px;    /* mono labels, overlines */
  --tracking-wide: 0.48px;     /* uppercase labels, badges */
  --tracking-tight: -0.72px;   /* medium headings */
  --tracking-tighter: -0.96px; /* large headings */
  --tracking-hero: -1.64px;    /* hero/display headings */
  --tracking-display: -2.36px; /* largest display text */
}
```

## Heading Styles

```css
h1 {
  font-family: var(--font-sans);
  font-size: var(--text-4xl);    /* ~55px */
  font-weight: var(--font-medium);
  line-height: var(--leading-heading);
  letter-spacing: var(--tracking-hero);
  color: var(--color-text);
}

h2 {
  font-family: var(--font-sans);
  font-size: var(--text-4xl);    /* ~55px — same as h1 */
  font-weight: var(--font-medium);
  line-height: var(--leading-heading);
  letter-spacing: var(--tracking-hero);
  color: var(--color-text);
}

h3 {
  font-family: var(--font-sans);
  font-size: var(--text-xl);     /* ~24px */
  font-weight: var(--font-normal);
  line-height: normal;
  letter-spacing: normal;
  color: var(--color-text);
}
```

## Special Text Styles

```css
/* Mono label — used for overlines, tags, code snippets */
.mono-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
}

/* Stat number — large display numbers */
.stat-number {
  font-family: var(--font-sans);
  font-size: var(--text-hero);
  font-weight: var(--font-medium);
  letter-spacing: var(--tracking-display);
  line-height: var(--leading-tight);
}
```
