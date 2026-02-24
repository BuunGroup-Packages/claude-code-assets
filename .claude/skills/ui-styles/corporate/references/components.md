# Components — corporate

## Button — Primary

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 8px 16px;
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-weight: 500;
  font-size: var(--text-base);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}
```

## Button — Secondary

```css
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 8px 16px;
  background: var(--color-bg);
  color: var(--color-text);
  font-weight: 500;
  font-size: var(--text-base);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background: var(--color-elevated);
  border-color: var(--color-border-strong);
}
```

## Card — Dashboard

```css
.card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-xs);
}

.card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
}

.card__title {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text);
}
```

## Sidebar

```css
.sidebar {
  background: var(--color-sidebar);
  color: var(--color-text-inverse);
  padding: var(--space-lg) var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.sidebar__item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
}

.sidebar__item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--color-text-inverse);
}

.sidebar__item--active {
  background: var(--color-accent);
  color: var(--color-text-inverse);
}
```

## Input

```css
.input {
  width: 100%;
  padding: 8px 12px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  color: var(--color-text);
  transition: border-color 0.15s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: var(--shadow-focus);
}
```

## Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  border-radius: var(--radius-full);
}
```

## Data Table

```css
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.table th {
  text-align: left;
  padding: var(--space-sm) var(--space-md);
  font-weight: var(--font-medium);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

.table td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.table tr:hover td {
  background: var(--color-surface);
}
```

## Kanban Column

```css
.kanban {
  display: flex;
  gap: var(--space-xl);
  overflow-x: auto;
}

.kanban__column {
  min-width: 280px;
  flex-shrink: 0;
}

.kanban__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-lg);
  font-weight: var(--font-semibold);
}

.kanban__card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin-bottom: var(--space-sm);
}
```
