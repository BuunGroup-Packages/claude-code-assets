# Spacing System

## Spacing Scale

```css
:root {
  /* Base unit: 4px (0.25rem) */
  --space-0: 0;
  --space-px: 1px;
  --space-0.5: 0.125rem;  /* 2px */
  --space-1: 0.25rem;     /* 4px */
  --space-1.5: 0.375rem;  /* 6px */
  --space-2: 0.5rem;      /* 8px */
  --space-2.5: 0.625rem;  /* 10px */
  --space-3: 0.75rem;     /* 12px */
  --space-3.5: 0.875rem;  /* 14px */
  --space-4: 1rem;        /* 16px */
  --space-5: 1.25rem;     /* 20px */
  --space-6: 1.5rem;      /* 24px */
  --space-7: 1.75rem;     /* 28px */
  --space-8: 2rem;        /* 32px */
  --space-9: 2.25rem;     /* 36px */
  --space-10: 2.5rem;     /* 40px */
  --space-11: 2.75rem;    /* 44px */
  --space-12: 3rem;       /* 48px */
  --space-14: 3.5rem;     /* 56px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
  --space-28: 7rem;       /* 112px */
  --space-32: 8rem;       /* 128px */
}
```

## Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-2xl: 1rem;     /* 16px */
  --radius-3xl: 1.5rem;   /* 24px */
  --radius-full: 9999px;
}
```

## Container Widths

```css
:root {
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
}

.container {
  width: 100%;
  max-width: var(--container-xl);
  margin-inline: auto;
  padding-inline: var(--space-4);
}

@media (min-width: 640px) {
  .container { padding-inline: var(--space-6); }
}

@media (min-width: 1024px) {
  .container { padding-inline: var(--space-8); }
}
```

## Component Spacing Guidelines

| Component | Padding | Gap |
|-----------|---------|-----|
| Button (sm) | `--space-2` `--space-3` | - |
| Button (md) | `--space-2.5` `--space-4` | - |
| Button (lg) | `--space-3` `--space-6` | - |
| Card | `--space-4` to `--space-6` | - |
| Form field | `--space-2` `--space-3` | - |
| Form group | - | `--space-4` |
| List items | - | `--space-2` to `--space-3` |
| Section | `--space-12` to `--space-20` | - |
| Stack | - | `--space-4` |
| Inline | - | `--space-2` |

## Layout Utilities

```css
/* Stack (vertical spacing) */
.stack {
  display: flex;
  flex-direction: column;
}

.stack > * + * {
  margin-top: var(--stack-gap, var(--space-4));
}

.stack-sm { --stack-gap: var(--space-2); }
.stack-md { --stack-gap: var(--space-4); }
.stack-lg { --stack-gap: var(--space-6); }
.stack-xl { --stack-gap: var(--space-8); }

/* Inline (horizontal spacing) */
.inline {
  display: flex;
  flex-wrap: wrap;
  gap: var(--inline-gap, var(--space-2));
  align-items: center;
}

.inline-sm { --inline-gap: var(--space-1); }
.inline-md { --inline-gap: var(--space-2); }
.inline-lg { --inline-gap: var(--space-4); }

/* Grid */
.grid {
  display: grid;
  gap: var(--grid-gap, var(--space-4));
}

.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3,
  .grid-cols-4 {
    grid-template-columns: 1fr;
  }
}
```

## Section Spacing

```css
.section {
  padding-block: var(--space-16);
}

.section-sm {
  padding-block: var(--space-8);
}

.section-lg {
  padding-block: var(--space-24);
}
```
