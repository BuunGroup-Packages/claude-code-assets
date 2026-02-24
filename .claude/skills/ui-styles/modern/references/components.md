# Components — modern

## Button — Primary (Dark)

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 14px 28px;
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-weight: 600;
  font-size: var(--text-base);
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

## Button — Accent (Lime)

Used on dark sections.

```css
.btn-accent {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 14px 28px;
  background: var(--color-accent);
  color: var(--color-primary);
  font-weight: 600;
  font-size: var(--text-base);
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-accent:hover {
  background: var(--color-accent-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

## Button — Secondary (Outline)

```css
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 14px 28px;
  background: transparent;
  color: var(--color-text);
  font-weight: 500;
  font-size: var(--text-base);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--color-surface);
  border-color: var(--color-text-muted);
}
```

## Card — Photo

Full-bleed image card with gradient overlay text.

```css
.card-photo {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 4/3;
}

.card-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-photo__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 40%, rgba(0, 0, 0, 0.6) 100%);
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: var(--color-text-inverse);
}

.card-photo__title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
}

.card-photo__desc {
  font-size: var(--text-sm);
  color: rgba(255, 255, 255, 0.8);
  margin-top: var(--space-xs);
}
```

## Card — Feature

Used in feature grid sections.

```css
.card-feature {
  background: var(--color-surface-dark);
  border-radius: var(--radius-lg);
  overflow: hidden;
  padding: var(--space-lg);
  color: var(--color-text-on-dark);
}

.card-feature__label {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  margin-bottom: var(--space-xs);
}

.card-feature__desc {
  font-size: var(--text-sm);
  color: var(--color-text-muted-on-dark);
}
```

## Section — Alternating

```css
.section-light {
  background: var(--color-bg);
  color: var(--color-text);
  padding-block: var(--space-4xl);
}

.section-dark {
  background: var(--color-bg-dark);
  color: var(--color-text-on-dark);
  padding-block: var(--space-4xl);
}
```

## Logo Bar

Scrolling brand logos in dark section.

```css
.logo-bar {
  background: var(--color-surface-dark);
  padding: var(--space-lg) 0;
  overflow: hidden;
}

.logo-bar__track {
  display: flex;
  gap: var(--space-2xl);
  animation: marquee 30s linear infinite;
}

.logo-bar img {
  height: 24px;
  opacity: 0.7;
  filter: brightness(0) invert(1);
}
```

## Stats Grid

```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-xl);
  text-align: center;
}
```

## Header

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--wrapper-padding);
  background: var(--color-bg);
}

.header-dark {
  background: var(--color-bg-dark);
  color: var(--color-text-on-dark);
}
```

## Star Rating

```css
.stars {
  display: inline-flex;
  gap: 2px;
  color: var(--color-accent);
  font-size: var(--text-lg);
}
```
