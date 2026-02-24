# Animations — modern

## Timing

```css
:root {
  --duration-fast: 0.15s;
  --duration-normal: 0.2s;
  --duration-smooth: 0.3s;
  --ease-default: ease;
}
```

## Keyframes

```css
/* Marquee — logo bar scroll */
@keyframes marquee {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(-50%, 0, 0); }
}

/* Fade in — general entrance */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Fade in up — cards, list items */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Scale in — modals, popovers */
@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
```

## Hover States

Minimal, clean hover transitions.

```css
/* Button hover — subtle lift */
.btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Card hover — slight lift */
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Link hover — color shift */
a:hover {
  opacity: 0.8;
}
```

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
