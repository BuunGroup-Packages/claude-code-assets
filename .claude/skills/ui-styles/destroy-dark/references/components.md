# Components — destroy-dark

## Button — Primary

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 14px 28px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 1) 0%, rgba(168, 85, 247, 1) 50%, rgba(139, 92, 246, 0.9) 100%);
  color: #fff;
  font-weight: 600;
  font-size: var(--text-base);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  box-shadow: var(--shadow-glow-strong), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all var(--duration-normal) var(--ease-default);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.6), 0 0 60px rgba(139, 92, 246, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}
```

## Button — Secondary

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
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-default);
}

.btn-secondary:hover {
  background: rgba(139, 92, 246, 0.08);
  border-color: rgba(139, 92, 246, 0.5);
  transform: translateY(-2px);
}
```

## Button — Ghost

```css
.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 10px 16px;
  background: transparent;
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: var(--text-sm);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-default);
}

.btn-ghost:hover {
  color: var(--color-text);
  background: rgba(255, 255, 255, 0.05);
}
```

## Card

```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  transition: all var(--duration-smooth) var(--ease-default);
}

.card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.card--featured {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
  border-color: rgba(139, 92, 246, 0.25);
}
```

## Input

```css
.input {
  width: 100%;
  padding: 10px 14px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  transition: all var(--duration-fast) var(--ease-default);
}

.input:focus {
  outline: none;
  border-color: rgba(139, 92, 246, 0.6);
  box-shadow: var(--shadow-focus);
}

.input::placeholder {
  color: var(--color-text-subtle);
}
```

## Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  font-size: var(--text-xs);
  font-weight: 500;
  border-radius: var(--radius-full);
  background: rgba(139, 92, 246, 0.12);
  color: var(--color-accent-light);
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.badge--success {
  background: rgba(66, 184, 131, 0.12);
  color: var(--color-success);
  border-color: rgba(66, 184, 131, 0.2);
}

.badge--error {
  background: rgba(237, 66, 69, 0.12);
  color: var(--color-error);
  border-color: rgba(237, 66, 69, 0.2);
}
```

## Header

```css
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--wrapper-padding);
  background: rgba(27, 27, 31, 0.8);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border);
}
```

## Modal

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 200;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--color-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  z-index: 201;
  animation: scale-in 0.2s ease;
}
```
