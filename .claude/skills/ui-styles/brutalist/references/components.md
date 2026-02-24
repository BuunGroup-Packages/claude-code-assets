# Components — brutalist

## Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 12px 24px;
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-family: var(--font-mono);
  font-weight: var(--font-bold);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border: var(--border-width) solid var(--color-primary);
  border-radius: var(--radius-none);
  cursor: pointer;
  transition: none;
}

.btn:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
}

.btn--outline {
  background: transparent;
  color: var(--color-primary);
}

.btn--outline:hover {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}
```

## Card

```css
.card {
  border: var(--border-width) solid var(--color-border);
  padding: var(--space-lg);
  border-radius: var(--radius-none);
}

.card:hover {
  border-width: var(--border-width-thick);
  padding: calc(var(--space-lg) - 2px); /* compensate for thicker border */
}
```

## Input

```css
.input {
  width: 100%;
  padding: 12px 16px;
  background: var(--color-bg);
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--radius-none);
  font-family: var(--font-mono);
  font-size: var(--text-base);
  color: var(--color-text);
}

.input:focus {
  outline: var(--border-width-thick) solid var(--color-accent);
  outline-offset: 0;
}
```

## Divider

Thick horizontal rules.

```css
hr {
  border: none;
  border-top: var(--border-width-thick) solid var(--color-border);
  margin: var(--space-2xl) 0;
}
```

## Header

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--wrapper-padding);
  border-bottom: var(--border-width-thick) solid var(--color-border);
}
```
