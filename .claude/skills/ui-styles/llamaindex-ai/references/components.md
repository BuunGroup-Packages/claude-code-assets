# Components — llamaindex-ai

## Button — Primary

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 12px 32px;
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-family: var(--font-sans);
  font-weight: 700;
  font-size: var(--text-xs);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.075s, color 0.075s;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}
```

## Button — Nav

```css
.btn-nav {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 0;
  background: transparent;
  color: var(--color-text);
  font-family: var(--font-sans);
  font-weight: var(--font-normal);
  font-size: var(--text-sm);
  border: none;
  cursor: pointer;
  transition: color 0.15s;
}

.btn-nav:hover {
  color: var(--color-text-muted);
}
```

## Button — Gradient CTA

```css
.btn-gradient {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 12px 32px;
  background: var(--color-accent-gradient);
  color: var(--color-text);
  font-family: var(--font-sans);
  font-weight: var(--font-medium);
  font-size: var(--text-base);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
}
```

## Card (Impact/Testimonial)

```css
.card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-lg);
  padding: 0;
  background: transparent;
  color: var(--color-text);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  border: none;
}

.card img {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-full);
  object-fit: cover;
}
```

## Header

```css
.header {
  display: block;
  width: 100%;
  max-width: var(--max-width);
  margin-inline: auto;
  padding: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: var(--text-base);
}

.header-grid {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 52px;
}

.header-nav {
  display: flex;
  gap: var(--space-2xl);
  align-items: center;
}
```

## Announcement Bar

```css
.announcement-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  background: var(--color-accent-gradient);
  color: var(--color-text);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-decoration: none;
}
```

## Section

```css
.section {
  display: grid;
  grid-template-columns: [full-start] var(--wrapper-padding) [content-start] var(--max-width) [content-end] var(--wrapper-padding) [full-end];
  padding-block: var(--space-4xl);
}

.section > * {
  grid-column: content;
}

.section-white {
  background: var(--color-bg);
}

.section-light {
  background: var(--color-surface);
}
```

## Section — Hero

```css
.hero {
  padding-top: var(--space-3xl);
  padding-bottom: var(--space-6xl);
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3xl);
}

.hero h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-medium);
  letter-spacing: var(--tracking-hero);
  line-height: var(--leading-heading);
}
```

## Input

```css
.input {
  padding: var(--space-md);
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  border: 1px solid var(--color-border);
  border-radius: 0;
  outline: none;
  transition: border-color 0.15s;
}

.input:focus {
  border-color: var(--color-primary);
}

/* Rounded variant (form inputs) */
.input-rounded {
  border-radius: var(--radius-md);
  padding: 12px 10px;
}
```

## Footer

```css
.footer {
  padding: var(--space-lg);
  background: transparent;
  color: var(--color-text);
  font-size: var(--text-base);
}

.footer a {
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.15s;
}

.footer a:hover {
  color: var(--color-text-muted);
}
```

## Logo Bar / Partner Grid

```css
.logo-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3xl);
  align-items: center;
  justify-content: center;
}

.logo-bar img {
  max-width: 144px;
  height: auto;
  filter: grayscale(100%);
  opacity: 0.7;
  transition: opacity 0.15s, filter 0.15s;
}

.logo-bar img:hover {
  filter: grayscale(0%);
  opacity: 1;
}
```

## Stats Grid

```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-3xl);
}

.stat {
  text-align: center;
}

.stat-number {
  font-family: var(--font-sans);
  font-size: var(--text-hero);
  font-weight: var(--font-medium);
  letter-spacing: var(--tracking-display);
  line-height: var(--leading-tight);
}

.stat-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wide);
  color: var(--color-text-muted);
  text-transform: uppercase;
}
```

## Dropdown / Mega Menu

```css
.dropdown {
  display: flex;
  gap: var(--space-3xl);
  padding: var(--space-2xl);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
}

.dropdown-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) 0;
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.075s, background 0.075s;
}

.dropdown-link:hover {
  color: var(--color-text-muted);
}
```
