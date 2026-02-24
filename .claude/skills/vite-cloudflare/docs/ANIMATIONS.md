# Animation System

## Principles

1. **Subtle** - Enhance, don't distract
2. **Fast** - 150-300ms for micro-interactions
3. **Purposeful** - Communicate state changes
4. **Performant** - Only animate `transform` and `opacity`

## Timing Tokens

```css
:root {
  /* Durations */
  --duration-instant: 50ms;
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  /* Easings */
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

## Utility Classes

```css
/* ========================================
   ENTRANCE ANIMATIONS
   ======================================== */

.fade-in {
  animation: fadeIn var(--duration-normal) var(--ease-out);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in-up {
  animation: fadeInUp var(--duration-normal) var(--ease-out);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-down {
  animation: fadeInDown var(--duration-normal) var(--ease-out);
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-left {
  animation: slideInLeft var(--duration-normal) var(--ease-out);
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.slide-in-right {
  animation: slideInRight var(--duration-normal) var(--ease-out);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.scale-in {
  animation: scaleIn var(--duration-fast) var(--ease-spring);
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.pop-in {
  animation: popIn var(--duration-fast) var(--ease-bounce);
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ========================================
   EXIT ANIMATIONS
   ======================================== */

.fade-out {
  animation: fadeOut var(--duration-fast) var(--ease-in) forwards;
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.scale-out {
  animation: scaleOut var(--duration-fast) var(--ease-in) forwards;
}

@keyframes scaleOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* ========================================
   LOADING ANIMATIONS
   ======================================== */

.spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin var(--duration-slow) linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pulse {
  animation: pulse 2s var(--ease-in-out) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    var(--color-surface-hover) 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ========================================
   INTERACTION STATES
   ======================================== */

.hover-lift {
  transition: transform var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.hover-scale {
  transition: transform var(--duration-fast) var(--ease-out);
}

.hover-scale:hover {
  transform: scale(1.02);
}

.press-scale {
  transition: transform var(--duration-instant) var(--ease-out);
}

.press-scale:active {
  transform: scale(0.98);
}

/* ========================================
   STAGGER ANIMATIONS
   ======================================== */

.stagger-children > * {
  animation: fadeInUp var(--duration-normal) var(--ease-out) backwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0ms; }
.stagger-children > *:nth-child(2) { animation-delay: 50ms; }
.stagger-children > *:nth-child(3) { animation-delay: 100ms; }
.stagger-children > *:nth-child(4) { animation-delay: 150ms; }
.stagger-children > *:nth-child(5) { animation-delay: 200ms; }
.stagger-children > *:nth-child(6) { animation-delay: 250ms; }
.stagger-children > *:nth-child(7) { animation-delay: 300ms; }
.stagger-children > *:nth-child(8) { animation-delay: 350ms; }

/* ========================================
   REDUCED MOTION
   ======================================== */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Component Transitions

```css
/* Button */
.btn {
  transition:
    transform var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn:active:not(:disabled) {
  transform: translateY(0);
}

/* Card */
.card {
  transition:
    transform var(--duration-normal) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

/* Input focus */
.input {
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
}

.input:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-focus);
}

/* Link */
.link {
  transition: color var(--duration-fast) var(--ease-out);
}

/* Modal backdrop */
.modal-backdrop {
  transition: opacity var(--duration-normal) var(--ease-out);
}

.modal-backdrop.entering { opacity: 0; }
.modal-backdrop.entered { opacity: 1; }
.modal-backdrop.exiting { opacity: 0; }

/* Modal content */
.modal-content {
  transition:
    opacity var(--duration-normal) var(--ease-out),
    transform var(--duration-normal) var(--ease-spring);
}

.modal-content.entering {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.modal-content.entered {
  opacity: 1;
  transform: scale(1) translateY(0);
}
```
