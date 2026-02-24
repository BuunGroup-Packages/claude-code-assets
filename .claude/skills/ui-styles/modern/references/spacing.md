# Spacing — modern

## Scale

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;
}
```

## Border Radius

Generous rounding throughout — pill buttons, rounded cards.

```css
:root {
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 100px;
}
```

## Layout

```css
:root {
  --max-width: 1280px;
  --wrapper-padding: 24px;
}

.container {
  width: 100%;
  max-width: var(--max-width);
  margin-inline: auto;
  padding-inline: var(--wrapper-padding);
}
```

## Breakpoints

| Name | Value |
|------|-------|
| Mobile | `max-width: 480px` |
| Tablet | `min-width: 640px` |
| Desktop | `min-width: 1024px` |
| Wide | `min-width: 1280px` |

## Section Spacing

Generous vertical padding creates airy feel.

```css
.section {
  padding-block: var(--space-4xl);
}

.section-sm {
  padding-block: var(--space-3xl);
}

@media (max-width: 640px) {
  .section { padding-block: var(--space-3xl); }
}
```

## Component Spacing

| Component | Padding |
|-----------|---------|
| Button (pill) | `14px 28px` |
| Card (photo) | `var(--space-lg)` overlay padding |
| Section | `var(--space-4xl)` block |
| Logo bar | `var(--space-lg)` block |
| Stats grid | `var(--space-xl)` gap |
