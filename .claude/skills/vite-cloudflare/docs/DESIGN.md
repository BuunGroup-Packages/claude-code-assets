# Vite + Cloudflare Design System

## Overview

This design system provides consistent styling patterns for Vite + React + Cloudflare Workers applications.

## Design Principles

1. **Clean & Minimal** - Focus on content, reduce visual noise
2. **Fast Loading** - CSS-only animations, no heavy libraries
3. **Accessible** - WCAG 2.1 AA compliant color contrasts
4. **Responsive** - Mobile-first, fluid layouts
5. **Dark Mode Ready** - CSS custom properties for theming

## File Structure

```
docs/
├── DESIGN.md          # This file - overview
├── COLORS.md          # Color palette & tokens
├── TYPOGRAPHY.md      # Font system
├── SPACING.md         # Spacing scale
├── ANIMATIONS.md      # Animation patterns
└── COMPONENTS.md      # Component guidelines
```

## Quick Start

Import the design tokens in your global CSS:

```css
/* src/client/styles/global.css */
@import "./tokens.css";
@import "./animations.css";
```

## CSS Architecture

```
src/client/styles/
├── global.css         # Reset + base styles
├── tokens.css         # Design tokens (colors, spacing, etc.)
├── animations.css     # Animation utilities
└── utilities.css      # Utility classes (optional)
```

## Component Pattern

Every component follows co-located CSS:

```
Button/
├── Button.tsx         # Component logic
├── Button.css         # Component styles
└── index.ts           # Export
```

## Naming Convention

BEM-inspired with component prefix:

```css
.component-name { }                    /* Block */
.component-name__element { }           /* Element */
.component-name--modifier { }          /* Modifier */
.component-name--state-loading { }     /* State */
```

## Related Docs

- [Colors](./COLORS.md) - Full color palette
- [Typography](./TYPOGRAPHY.md) - Font system
- [Spacing](./SPACING.md) - Spacing scale
- [Animations](./ANIMATIONS.md) - Motion design
- [Components](./COMPONENTS.md) - Component patterns
