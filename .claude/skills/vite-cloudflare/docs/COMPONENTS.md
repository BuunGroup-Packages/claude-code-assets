# Component Design Guidelines

## Component Structure

Every component follows co-located file organization:

```
ComponentName/
├── ComponentName.tsx    # Component logic
├── ComponentName.css    # Component styles
└── index.ts             # Barrel export
```

## CSS Naming Convention

BEM-inspired with component prefix:

```css
/* Block - the component itself */
.button { }

/* Element - a part of the component */
.button__icon { }
.button__label { }

/* Modifier - a variation */
.button--primary { }
.button--secondary { }
.button--large { }

/* State - dynamic states */
.button--is-loading { }
.button--is-disabled { }
```

## Component Template

```tsx
// ComponentName.tsx
import type { FC, ReactNode } from "react";
import "./ComponentName.css";

interface ComponentNameProps {
  children?: ReactNode;
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const ComponentName: FC<ComponentNameProps> = ({
  children,
  variant = "primary",
  size = "md",
  className = "",
}) => {
  const classes = [
    "component-name",
    `component-name--${variant}`,
    `component-name--${size}`,
    className,
  ].filter(Boolean).join(" ");

  return (
    <div className={classes}>
      {children}
    </div>
  );
};
```

## Component CSS Template

```css
/* ComponentName.css */

/* ========================================
   BASE STYLES
   ======================================== */
.component-name {
  /* Layout */
  display: flex;
  align-items: center;

  /* Box model */
  padding: var(--space-3) var(--space-4);

  /* Visual */
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);

  /* Typography */
  font-size: var(--text-md);
  color: var(--color-text);

  /* Animation */
  transition:
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}

/* ========================================
   ELEMENTS
   ======================================== */
.component-name__icon {
  margin-right: var(--space-2);
  color: var(--color-text-muted);
}

.component-name__label {
  flex: 1;
}

/* ========================================
   VARIANTS
   ======================================== */
.component-name--primary {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverse);
}

.component-name--secondary {
  background: transparent;
  border-color: var(--color-border-strong);
}

/* ========================================
   SIZES
   ======================================== */
.component-name--sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
}

.component-name--lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
}

/* ========================================
   STATES
   ======================================== */
.component-name:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
}

.component-name:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.component-name--is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.component-name--is-loading {
  position: relative;
  color: transparent;
}

.component-name--is-loading::after {
  content: "";
  position: absolute;
  inset: 0;
  margin: auto;
  width: 1rem;
  height: 1rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin var(--duration-slow) linear infinite;
}
```

## Common Components

### Button

```tsx
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  icon?: ReactNode;
}
```

### Card

```tsx
interface CardProps {
  children: ReactNode;
  padding?: "sm" | "md" | "lg";
  shadow?: "none" | "sm" | "md" | "lg";
  hoverable?: boolean;
}
```

### Input

```tsx
interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}
```

### Modal

```tsx
interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  size?: "sm" | "md" | "lg" | "full";
  children: ReactNode;
}
```

## Accessibility Checklist

- [ ] Focusable elements have visible focus states
- [ ] Interactive elements have appropriate cursor
- [ ] Color is not the only indicator of state
- [ ] Touch targets are at least 44x44px
- [ ] Form inputs have associated labels
- [ ] Error messages are announced to screen readers
- [ ] Modals trap focus and return focus on close
- [ ] `prefers-reduced-motion` is respected

## Responsive Patterns

```css
/* Mobile-first breakpoints */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }

/* Component-specific responsive */
.component-name {
  /* Mobile */
  flex-direction: column;
  padding: var(--space-3);
}

@media (min-width: 768px) {
  .component-name {
    /* Desktop */
    flex-direction: row;
    padding: var(--space-4) var(--space-6);
  }
}
```

## Export Pattern

```ts
// ComponentName/index.ts
export { ComponentName } from "./ComponentName";
export type { ComponentNameProps } from "./ComponentName";
```

```ts
// components/index.ts (barrel)
export { Button } from "./Button";
export { Card } from "./Card";
export { Input } from "./Input";
export { Modal } from "./Modal";
```
