# Animations — destroy-dark

## Timing Tokens

```css
:root {
  --duration-fast: 0.15s;
  --duration-normal: 0.2s;
  --duration-smooth: 0.3s;
  --ease-default: ease;
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

## Keyframes

```css
/* Gradient border rotation — for animated gradient borders */
@keyframes gradient-rotate {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Floating element — hero sections, decorative */
@keyframes hero-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

/* Pulse glow — status indicators */
@keyframes pulse-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Scale entrance — modals, popovers */
@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

/* Fade up entrance — cards, list items */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Shimmer — skeleton loading */
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Status ping — online indicators */
@keyframes status-ping {
  75%, 100% { transform: scale(2); opacity: 0; }
}

/* Marquee — logo scrollers */
@keyframes marquee {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(-25%, 0, 0); }
}
```

## Component Transitions

```css
/* All interactive elements */
.interactive {
  transition: all var(--duration-normal) var(--ease-default);
}

/* Hover lift — buttons, cards */
.hover-lift:hover {
  transform: translateY(-2px);
}

/* Hover lift strong — featured cards */
.hover-lift-strong:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

/* Stagger children — list animations */
.stagger > *:nth-child(1) { animation-delay: 0ms; }
.stagger > *:nth-child(2) { animation-delay: 50ms; }
.stagger > *:nth-child(3) { animation-delay: 100ms; }
.stagger > *:nth-child(4) { animation-delay: 150ms; }
.stagger > *:nth-child(5) { animation-delay: 200ms; }
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
