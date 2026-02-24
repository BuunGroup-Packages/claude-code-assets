# Spacing — corporate

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
}
```

## Border Radius

Conservative, professional.

```css
:root {
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 100px;
}
```

## Layout

```css
:root {
  --sidebar-width: 240px;
  --header-height: 56px;
  --max-width: 1400px;
}

.app-layout {
  display: grid;
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-rows: var(--header-height) 1fr;
  min-height: 100vh;
}

.content {
  padding: var(--space-xl);
  overflow-y: auto;
}
```

## Breakpoints

| Name | Value |
|------|-------|
| Mobile | `max-width: 640px` |
| Tablet | `min-width: 768px` |
| Desktop | `min-width: 1024px` |
| Wide | `min-width: 1280px` |

At mobile, sidebar collapses to hamburger menu.
