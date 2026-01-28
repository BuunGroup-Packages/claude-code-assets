---
name: astro-cloudflare:component
model: haiku
description: |
  Add React island component with co-located CSS.
  Supports shared or page-specific components.
argument-hint: "<name> [path]"
---

# Add React Island Component

## Variables

NAME: $1 (required, PascalCase)
PATH: $2 (optional, defaults to src/components)

## Detect Location

| PATH contains | Type | Import from |
|---------------|------|-------------|
| `_components` | Co-located | `./_components` |
| `src/components` | Shared | `@/components` |

## Files Created

```
${PATH}/
├── ${NAME}.tsx
├── ${NAME}.css
└── index.ts (update barrel export)
```

---

## Island Hydration Guide

| Directive | Ship JS | When | Use For |
|-----------|---------|------|---------|
| `client:load` | Yes | Immediate | Critical interactivity |
| `client:idle` | Yes | requestIdleCallback | Forms, non-critical |
| `client:visible` | Yes | IntersectionObserver | Below fold |
| `client:media` | Yes | Media query match | Responsive |
| `client:only="react"` | Yes | Never SSR | Client-only libs |
| *(none)* | No | Never | Static display |

---

## CRITICAL: Prop Limitations

**Functions CANNOT be passed to hydrated components!**

Serializable props only:
- Primitives: `string`, `number`, `boolean`, `null`, `undefined`
- Objects: plain objects, `Date`, `Map`, `Set`, `RegExp`, `BigInt`, `URL`
- Arrays and typed arrays

```astro
<!-- WRONG - functions don't serialize -->
<Button client:load onClick={() => console.log('click')} />

<!-- CORRECT - handle events inside the component -->
<Button client:load />

<!-- CORRECT - pass data, not callbacks -->
<UserCard client:visible user={userData} />
```

---

## Component Templates

### Display Island (client:visible)

For components that display data but aren't immediately interactive.

```tsx
// ${PATH}/${NAME}.tsx
import type { FC } from "react";
import "./${NAME}.css";

interface ${NAME}Props {
  items: Array<{ id: string; name: string; value: number }>;
}

export const ${NAME}: FC<${NAME}Props> = ({ items }) => {
  return (
    <div className="${kebab(NAME)} fade-in">
      {items.map((item) => (
        <div key={item.id} className="${kebab(NAME)}__item">
          <span className="${kebab(NAME)}__name">{item.name}</span>
          <span className="${kebab(NAME)}__value">{item.value}</span>
        </div>
      ))}
    </div>
  );
};
```

**Usage:** `<${NAME} client:visible items={items} />`

### Interactive Island (client:load)

For components requiring immediate interactivity. Events handled internally.

```tsx
// ${PATH}/${NAME}.tsx
import { useState, type FC } from "react";
import { actions } from "astro:actions";
import "./${NAME}.css";

interface ${NAME}Props {
  initialValue?: string;
  redirectTo?: string;  // Pass URL string, not function
}

export const ${NAME}: FC<${NAME}Props> = ({ initialValue = "", redirectTo }) => {
  const [value, setValue] = useState(initialValue);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const { error } = await actions.myFeature.submit({ value });
    if (!error) {
      setSubmitted(true);
      if (redirectTo) {
        window.location.href = redirectTo;
      }
    }
  };

  if (submitted) {
    return <div className="${kebab(NAME)} ${kebab(NAME)}--success">Submitted!</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="${kebab(NAME)}">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="${kebab(NAME)}__input"
        placeholder="Enter value..."
      />
      <button type="submit" className="${kebab(NAME)}__button">
        Submit
      </button>
    </form>
  );
};
```

**Usage:** `<${NAME} client:load redirectTo="/success" />`

### Form Island with Actions (client:idle)

For form components that can wait for browser idle.

```tsx
// ${PATH}/${NAME}.tsx
import { actions } from "astro:actions";
import { useActionState } from "react";
import { withState } from "@astrojs/react/actions";
import type { FC } from "react";
import "./${NAME}.css";

interface ${NAME}Props {
  // Only serializable props!
  defaultName?: string;
  featureId?: string;
}

export const ${NAME}: FC<${NAME}Props> = ({ defaultName = "", featureId }) => {
  const [state, action, pending] = useActionState(
    withState(actions.yourFeature.create),
    { data: undefined, error: undefined }
  );

  return (
    <form action={action} className="${kebab(NAME)}">
      {featureId && <input type="hidden" name="featureId" value={featureId} />}

      <div className="${kebab(NAME)}__field">
        <label htmlFor="${kebab(NAME)}-input">Name</label>
        <input
          id="${kebab(NAME)}-input"
          name="name"
          type="text"
          required
          disabled={pending}
          defaultValue={defaultName}
        />
      </div>

      <button
        type="submit"
        disabled={pending}
        className="${kebab(NAME)}__submit"
      >
        {pending ? "Submitting..." : "Submit"}
      </button>

      {state.error && (
        <div className="${kebab(NAME)}__error" role="alert">
          {state.error.message}
        </div>
      )}

      {state.data && (
        <div className="${kebab(NAME)}__success" role="status">
          Created successfully!
        </div>
      )}
    </form>
  );
};
```

**Usage:** `<${NAME} client:idle featureId="123" />`

### Data-Fetching Island with Hook

For components that fetch their own data.

```tsx
// ${PATH}/${NAME}.tsx
import type { FC } from "react";
import { use${NAME}Data } from "../_hooks";
import "./${NAME}.css";

interface ${NAME}Props {
  // Pass initial data from server, not callbacks
  initialData?: Array<{ id: string; name: string }>;
}

export const ${NAME}: FC<${NAME}Props> = ({ initialData }) => {
  const { data, loading, error, refetch } = use${NAME}Data(initialData);

  if (loading) {
    return (
      <div className="${kebab(NAME)} ${kebab(NAME)}--loading">
        <div className="${kebab(NAME)}__spinner" />
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="${kebab(NAME)} ${kebab(NAME)}--error">
        <p>Error: {error.message}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div className="${kebab(NAME)}">
      <div className="${kebab(NAME)}__header">
        <h3>${NAME}</h3>
        <button onClick={refetch} className="${kebab(NAME)}__refresh">
          ↻
        </button>
      </div>
      <div className="${kebab(NAME)}__content">
        {data?.map((item) => (
          <div key={item.id} className="${kebab(NAME)}__item">
            {item.name}
          </div>
        ))}
      </div>
    </div>
  );
};
```

**Usage:** `<${NAME} client:visible initialData={serverData} />`

---

## Passing Children (React)

React receives children via the `children` prop:

```astro
---
import { Card } from "./_components";
---

<Card client:load>
  <h2>Title</h2>
  <p>Content passed as children</p>
</Card>
```

```tsx
// Card.tsx
import type { FC, ReactNode } from "react";

interface CardProps {
  children: ReactNode;
}

export const Card: FC<CardProps> = ({ children }) => {
  return <div className="card">{children}</div>;
};
```

### Named Slots

Use `slot` attribute in Astro, access as props in React:

```astro
<MySidebar client:load>
  <h2 slot="title">Menu</h2>
  <p>Default slot content</p>
</MySidebar>
```

```tsx
// MySidebar.tsx - slots become camelCase props
interface MySidebarProps {
  children: ReactNode;
  title: ReactNode;  // slot="title" becomes title prop
}

export const MySidebar: FC<MySidebarProps> = ({ children, title }) => {
  return (
    <aside>
      <header>{title}</header>
      <main>{children}</main>
    </aside>
  );
};
```

---

## CSS Template

```css
/* ${PATH}/${NAME}.css */

/* Base */
.${kebab(NAME)} {
  padding: 1.5rem;
  background: var(--color-surface, #fff);
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* States */
.${kebab(NAME)}--loading {
  opacity: 0.7;
  pointer-events: none;
}

.${kebab(NAME)}--error {
  border: 1px solid var(--color-error, #dc2626);
}

.${kebab(NAME)}--success {
  background: #f0fdf4;
  border: 1px solid #16a34a;
}

/* Elements */
.${kebab(NAME)}__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.${kebab(NAME)}__content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.${kebab(NAME)}__item {
  padding: 0.75rem;
  background: var(--color-bg, #f9fafb);
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.${kebab(NAME)}__item:hover {
  transform: translateX(4px);
}

/* Form elements */
.${kebab(NAME)}__field {
  margin-bottom: 1rem;
}

.${kebab(NAME)}__field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.${kebab(NAME)}__field input,
.${kebab(NAME)}__field textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border, #e5e7eb);
  border-radius: 0.5rem;
  font-size: 1rem;
}

.${kebab(NAME)}__field input:focus,
.${kebab(NAME)}__field textarea:focus {
  outline: none;
  border-color: var(--color-primary, #0066ff);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.${kebab(NAME)}__submit {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary, #0066ff);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.${kebab(NAME)}__submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
}

.${kebab(NAME)}__submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Feedback */
.${kebab(NAME)}__error {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.${kebab(NAME)}__success {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

/* Animations */
.${kebab(NAME)} {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Spinner */
.${kebab(NAME)}__spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid var(--color-border, #e5e7eb);
  border-top-color: var(--color-primary, #0066ff);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## Limitations

1. **No functions in props** - Cannot pass callbacks to hydrated islands
2. **No .astro imports** - React components cannot import Astro components
3. **Islands are isolated** - Each island hydrates independently
4. **Children serialization** - Children must be valid React nodes

---

## Update Barrel Export

If adding to existing `_components/`:

```typescript
// ${PATH}/index.ts
export { ExistingComponent } from "./ExistingComponent";
export { ${NAME} } from "./${NAME}";  // Add this line
```

---

## Usage in Astro Pages

```astro
---
// Co-located import
import { ${NAME} } from "./_components";

// OR shared import
import { ${NAME} } from "@/components";

// Server-side data fetch
const serverData = await fetchData();
---

<!-- Pass data, not functions -->
<${NAME} client:load initialData={serverData} />
<${NAME} client:idle featureId="123" />
<${NAME} client:visible items={items} />
<${NAME} />  <!-- Static, no JS shipped -->
```

---

## Output

```
## Island Created

**Name**: ${NAME}
**Path**: ${PATH}/${NAME}.tsx
**CSS**: ${PATH}/${NAME}.css
**Type**: ${PATH.includes('_components') ? 'Co-located' : 'Shared'}

### Files
- ${PATH}/${NAME}.tsx
- ${PATH}/${NAME}.css
- ${PATH}/index.ts (updated)

### Hydration Options
\`\`\`astro
<${NAME} client:load />     <!-- Critical UI -->
<${NAME} client:idle />     <!-- Forms -->
<${NAME} client:visible />  <!-- Below fold -->
\`\`\`

### Remember
- No functions in props!
- Pass data from server
- Handle events inside component
```
