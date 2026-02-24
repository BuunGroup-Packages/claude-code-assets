# Animations — brutalist

## Philosophy

Minimal animation. Brutalism favors instant state changes over smooth transitions. When animation exists, it's abrupt and intentional.

## Timing

```css
:root {
  --duration-instant: 0;
  --duration-fast: 0.1s;
  --ease-default: step-end;
}
```

## Hover States

Instant color inversion, no easing.

```css
.interactive {
  transition: none;
}

.interactive:hover {
  background: var(--color-inverted);
  color: var(--color-text-inverse);
}
```

## Entrance

If used at all, simple hard cuts.

```css
@keyframes hard-cut {
  from { opacity: 0; }
  to { opacity: 1; }
}

.entrance {
  animation: hard-cut 0.1s step-end;
}
```

## Reduced Motion

Already minimal, but respect the preference.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
  }
}
```
