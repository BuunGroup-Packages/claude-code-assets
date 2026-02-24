# Effects — destroy-dark

## Animated Gradient Border

Used on primary CTAs and premium features. Creates a flowing purple border.

```css
.gradient-border {
  position: relative;
  border: none;
}

.gradient-border::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: inherit;
  background: linear-gradient(90deg,
    rgba(139, 92, 246, 0.8),
    rgba(168, 85, 247, 0.9),
    rgba(139, 92, 246, 0.6),
    rgba(88, 28, 135, 0.8),
    rgba(139, 92, 246, 0.8));
  background-size: 300% 100%;
  animation: gradient-rotate 3s ease infinite;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

## Glassmorphism

Used on sticky headers and overlay panels.

```css
.glass {
  background: rgba(27, 27, 31, 0.8);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--color-border);
}
```

## Grid Background

Subtle grid overlay for hero sections and feature areas.

```css
.grid-bg {
  background-image:
    linear-gradient(rgba(139, 92, 246, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

## Radial Glow

Ambient lighting behind cards, hero elements, or CTAs.

```css
.radial-glow {
  position: relative;
}

.radial-glow::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.2) 0%, transparent 70%);
  pointer-events: none;
  z-index: -1;
}
```

## Drop Shadow Glow

For icons and small glowing elements.

```css
.icon-glow {
  filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.5));
}
```

## Custom Scrollbars

```css
/* Webkit */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #3a3a42 0%, #2a2a32 100%);
  border: 2px solid var(--color-bg);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.6) 0%, rgba(139, 92, 246, 0.4) 100%);
}

/* Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: #3a3a42 var(--color-bg);
}
```

## Skeleton Loading

```css
.skeleton {
  background: linear-gradient(90deg,
    var(--color-surface) 25%,
    var(--color-elevated) 50%,
    var(--color-surface) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
```
