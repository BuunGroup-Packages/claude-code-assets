# Core Web Vitals Optimization

## Overview

Optimizes for Lighthouse Performance 100 score.
PostToolUse hook validates every edit automatically.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | target | images, fonts, preload, all | all |
| $2 | file | Target file path | Auto-select |

## Usage

```bash
/seo perf images
/seo perf fonts src/styles/global.css
/seo perf all
```

## Core Web Vitals

| Metric | Target | Impact |
|--------|--------|--------|
| LCP | <2.5s | Largest Contentful Paint |
| FID | <100ms | First Input Delay |
| CLS | <0.1 | Cumulative Layout Shift |
| INP | <200ms | Interaction to Next Paint |

## Image Optimization

### Required Attributes

```html
<img
  src="/image.webp"
  alt="Descriptive text"
  width="800"
  height="600"
  loading="lazy"
/>
```

| Attribute | Error Code | Purpose |
|-----------|------------|---------|
| width + height | PERF001 | Prevents CLS |
| alt | PERF002 | Accessibility + SEO |
| loading="lazy" | PERF003 | Deferred loading |

### Modern Formats

```html
<picture>
  <source srcset="/image.avif" type="image/avif">
  <source srcset="/image.webp" type="image/webp">
  <img src="/image.jpg" alt="..." width="800" height="600">
</picture>
```

| Format | Error Code | Savings |
|--------|------------|---------|
| AVIF | PERF004 | ~50% vs JPEG |
| WebP | PERF004 | ~30% vs JPEG |

## Font Optimization

### font-display Required

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* REQUIRED */
}
```

| Property | Error Code | Purpose |
|----------|------------|---------|
| font-display: swap | PERF006 | Prevents FOIT |

### Preload Critical Fonts

```html
<link
  rel="preload"
  href="/fonts/custom.woff2"
  as="font"
  type="font/woff2"
  crossorigin
>
```

| Attribute | Error Code | Purpose |
|-----------|------------|---------|
| rel="preload" | PERF005 | Early fetch |
| crossorigin | Required | CORS for fonts |

## Render-Blocking Resources

### Scripts

```html
<!-- BAD: Render-blocking -->
<script src="/script.js"></script>

<!-- GOOD: Deferred -->
<script src="/script.js" defer></script>

<!-- GOOD: Async -->
<script src="/script.js" async></script>

<!-- GOOD: Module (deferred by default) -->
<script type="module" src="/script.js"></script>
```

| Attribute | Error Code | Purpose |
|-----------|------------|---------|
| defer | PERF007 | Execute after parse |
| async | PERF007 | Execute when ready |
| type="module" | PERF007 | Deferred by default |

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| PERF001 | error | Image missing width/height |
| PERF002 | error | Image missing alt |
| PERF003 | warning | Image missing loading="lazy" |
| PERF004 | warning | Image not modern format |
| PERF005 | warning | Font not preloaded |
| PERF006 | error | @font-face missing font-display |
| PERF007 | warning | Render-blocking script |
| PERF008 | warning | Missing theme-color meta |
