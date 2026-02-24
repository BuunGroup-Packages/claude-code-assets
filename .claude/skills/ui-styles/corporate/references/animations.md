# Animations — corporate

## Timing

Subtle, professional. No flashy effects.

```css
:root {
  --duration-fast: 0.15s;
  --duration-normal: 0.2s;
  --ease-default: ease;
}
```

## Transitions

```css
/* Standard interactive transition */
.interactive {
  transition: all var(--duration-fast) var(--ease-default);
}

/* Table row highlight */
.table tr {
  transition: background var(--duration-fast) var(--ease-default);
}

/* Sidebar item */
.sidebar__item {
  transition: background var(--duration-fast) var(--ease-default),
              color var(--duration-fast) var(--ease-default);
}
```

## Keyframes

```css
/* Fade in — modals, dropdowns */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide down — dropdowns, notifications */
@keyframes slide-down {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Scale in — modals */
@keyframes scale-in {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}
```

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
