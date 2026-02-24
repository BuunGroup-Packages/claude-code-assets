# Spacing — llamaindex-ai

## Scale

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 48px;
  --space-4xl: 80px;
  --space-5xl: 120px;
  --space-6xl: 160px;
}
```

## Border Radius

```css
:root {
  --radius-sm: 0px;       /* default — most elements have no radius */
  --radius-md: 6px;       /* form inputs, small buttons */
  --radius-lg: 12px;      /* cards, panels */
  --radius-full: 50%;     /* avatars, circular elements */
}
```

The site is notably flat — most elements use 0px border-radius, giving it a sharp, editorial feel.

## Layout

```css
:root {
  --max-width: 1360px;
  --max-width-narrow: 700px;
  --max-width-wide: 1440px;
  --wrapper-padding: 40px;
}

.container {
  width: 100%;
  max-width: var(--max-width);
  margin-inline: auto;
  padding-inline: var(--wrapper-padding);
}
```

### Grid Template

The site uses a named-line CSS Grid for full-bleed sections:

```css
.section {
  display: grid;
  grid-template-columns: [full-start] var(--wrapper-padding) [content-start] var(--max-width) [content-end] var(--wrapper-padding) [full-end];
}

/* Content spans content track */
.section > * {
  grid-column: content;
}

/* Full-bleed elements span full track */
.section > .full-bleed {
  grid-column: full;
}
```

## Breakpoints

| Name | Value |
|------|-------|
| Mobile | `480px` |
| Tablet | `768px` |
| Desktop | `1200px` |
| Wide | `1440px` |

Key breakpoints from the extracted media queries: 480, 768, 900, 1200, 1376, 1500px.

## Section Spacing

```css
.section {
  padding-block: var(--space-4xl);  /* 80px */
}

.section-hero {
  padding-top: var(--space-3xl);    /* 48px */
  padding-bottom: var(--space-6xl); /* 160px */
}

.section-tight {
  padding-block: var(--space-3xl);  /* 48px */
}

@media (max-width: 768px) {
  .section { padding-block: var(--space-3xl); }
}
```

## Component Spacing

| Component | Padding |
|-----------|---------|
| Button | `12px 32px` |
| Card | `32px` |
| Section | `80px 0` to `100px 0` |
| Section (hero) | `48px 0 160px` |
| Input | `12px` |
| Nav gap | `32px` |
| Content grid gap | `48px` |
