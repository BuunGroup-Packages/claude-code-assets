# Animations — llamaindex-ai

## Timing

```css
:root {
  --duration-fast: 0.075s;
  --duration-normal: 0.15s;
  --duration-smooth: 0.3s;
  --ease-default: ease-out;
  --ease-interactive: ease-in-out;
}
```

The site uses very fast transitions (75ms) as default, creating snappy, responsive interactions.

## Common Transitions

```css
/* Default interactive transition — buttons, links */
.interactive {
  transition: color var(--duration-fast), background var(--duration-fast);
}

/* Text-only color change — nav links, descriptive text */
.text-hover {
  transition: color var(--duration-normal);
}

/* Transform animations — icons, decorative elements */
.transform-hover {
  transition: transform var(--duration-fast) var(--ease-interactive);
}

/* Opacity animations — fade in/out */
.fade {
  transition: opacity var(--duration-fast) var(--ease-default);
}

/* Shadow animations — cards, elevated elements */
.shadow-hover {
  transition: box-shadow 0.2s;
}

/* Combined opacity + transform — dropdown items, reveal animations */
.reveal {
  transition: opacity var(--duration-fast) var(--ease-default),
              transform var(--duration-fast) var(--ease-interactive);
}

/* Height collapse — accordions, expandable sections */
.collapse {
  transition: height var(--duration-smooth);
}

/* Gradient color transitions — gradient border/bg accents */
.gradient-transition {
  transition: --from-color var(--duration-normal) var(--ease-interactive),
              --to-color var(--duration-normal) var(--ease-interactive);
}
```

## Hover States

```css
/* Button hover */
.btn:hover {
  background: var(--color-primary-hover);
}

/* Nav link hover */
a:hover {
  color: var(--color-text-muted);
}

/* Card hover — subtle shadow */
.card:hover {
  box-shadow: var(--shadow-md);
}

/* Logo hover — remove grayscale */
.logo:hover {
  filter: grayscale(0%);
  opacity: 1;
}
```

## Keyframes

No custom @keyframes were detected on the homepage. Animations primarily use CSS transitions. For scroll-triggered reveals, consider:

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-in {
  animation: fadeInUp var(--duration-smooth) var(--ease-default) forwards;
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
