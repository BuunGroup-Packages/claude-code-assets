# Spacing — destroy-dark

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

```css
:root {
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
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

@media (max-width: 480px) {
  :root { --wrapper-padding: 16px; }
}
```

## Breakpoints

| Name | Value | Use |
|------|-------|-----|
| Mobile | `max-width: 480px` | Stack layouts, reduce padding |
| Tablet | `min-width: 640px` | Two-column grids |
| Desktop | `min-width: 1024px` | Full layout |
| Wide | `min-width: 1312px` | Decorative elements |

## Component Spacing

| Component | Padding | Gap |
|-----------|---------|-----|
| Button | `14px 28px` | `8px` (icon gap) |
| Card | `var(--space-lg)` | — |
| Input | `10px 14px` | — |
| Badge | `6px 12px` | — |
| Section | `var(--space-3xl) 0` | — |
| Header | `0 var(--wrapper-padding)` | — |
