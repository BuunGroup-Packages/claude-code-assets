---
name: vite-cloudflare:component
model: haiku
description: |
  Add React component with co-located CSS.
  Supports shared or page-specific components.
argument-hint: "<name> [path]"
---

# Add React Component

## Variables

NAME: $1 (required, PascalCase)
PATH: $2 (optional, defaults to src/client/components)

## Detect Location

| PATH contains | Type | Import from |
|---------------|------|-------------|
| `_components` | Co-located | `./_components` |
| `components` | Shared | `@/components` |

## Files Created

```
${PATH}/${NAME}/
├── ${NAME}.tsx
├── ${NAME}.css
└── index.ts (or update parent barrel)
```

---

## Component Templates

### Basic Component

```tsx
// ${PATH}/${NAME}/${NAME}.tsx
import type { FC, ReactNode } from "react";
import "./${NAME}.css";

interface ${NAME}Props {
  children?: ReactNode;
  className?: string;
}

export const ${NAME}: FC<${NAME}Props> = ({
  children,
  className = "",
}) => {
  return (
    <div className={`${kebab(NAME)} ${className}`.trim()}>
      {children}
    </div>
  );
};
```

### Interactive Component

```tsx
// ${PATH}/${NAME}/${NAME}.tsx
import { useState, type FC } from "react";
import "./${NAME}.css";

interface ${NAME}Props {
  initialValue?: string;
  onChange?: (value: string) => void;
}

export const ${NAME}: FC<${NAME}Props> = ({
  initialValue = "",
  onChange,
}) => {
  const [value, setValue] = useState(initialValue);

  const handleChange = (newValue: string) => {
    setValue(newValue);
    onChange?.(newValue);
  };

  return (
    <div className="${kebab(NAME)}">
      <input
        type="text"
        value={value}
        onChange={(e) => handleChange(e.target.value)}
        className="${kebab(NAME)}__input"
      />
    </div>
  );
};
```

### Form Component

```tsx
// ${PATH}/${NAME}/${NAME}.tsx
import { useState, type FC, type FormEvent } from "react";
import { api } from "@/lib/api";
import "./${NAME}.css";

interface ${NAME}Props {
  onSuccess?: () => void;
}

export const ${NAME}: FC<${NAME}Props> = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData);

    try {
      await api.post("/endpoint", data);
      onSuccess?.();
      e.currentTarget.reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="${kebab(NAME)}">
      <div className="${kebab(NAME)}__field">
        <label htmlFor="${kebab(NAME)}-name">Name</label>
        <input
          id="${kebab(NAME)}-name"
          name="name"
          type="text"
          required
          disabled={loading}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="${kebab(NAME)}__submit"
      >
        {loading ? "Submitting..." : "Submit"}
      </button>

      {error && (
        <div className="${kebab(NAME)}__error" role="alert">
          {error}
        </div>
      )}
    </form>
  );
};
```

### List Component with Data Fetching

```tsx
// ${PATH}/${NAME}/${NAME}.tsx
import { useState, useEffect, type FC } from "react";
import { api } from "@/lib/api";
import "./${NAME}.css";

interface Item {
  id: string;
  name: string;
}

interface ${NAME}Props {
  initialItems?: Item[];
}

export const ${NAME}: FC<${NAME}Props> = ({ initialItems }) => {
  const [items, setItems] = useState<Item[]>(initialItems ?? []);
  const [loading, setLoading] = useState(!initialItems);
  const [error, setError] = useState<string | null>(null);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<Item[]>("/items");
      setItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!initialItems) {
      fetchItems();
    }
  }, [initialItems]);

  if (loading) {
    return <div className="${kebab(NAME)} ${kebab(NAME)}--loading">Loading...</div>;
  }

  if (error) {
    return (
      <div className="${kebab(NAME)} ${kebab(NAME)}--error">
        <p>{error}</p>
        <button onClick={fetchItems}>Retry</button>
      </div>
    );
  }

  return (
    <div className="${kebab(NAME)}">
      <div className="${kebab(NAME)}__header">
        <h3>Items</h3>
        <button onClick={fetchItems} className="${kebab(NAME)}__refresh">↻</button>
      </div>
      <ul className="${kebab(NAME)}__list">
        {items.map((item) => (
          <li key={item.id} className="${kebab(NAME)}__item">
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

### Component with Hook

```tsx
// ${PATH}/${NAME}/${NAME}.tsx
import type { FC } from "react";
import { use${NAME}Data } from "../_hooks/use${NAME}Data";
import "./${NAME}.css";

interface ${NAME}Props {
  id?: string;
}

export const ${NAME}: FC<${NAME}Props> = ({ id }) => {
  const { data, loading, error, refetch } = use${NAME}Data(id);

  if (loading) {
    return (
      <div className="${kebab(NAME)} ${kebab(NAME)}--loading">
        <div className="${kebab(NAME)}__spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="${kebab(NAME)} ${kebab(NAME)}--error">
        <p>{error.message}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div className="${kebab(NAME)} fade-in">
      <h3>{data?.name}</h3>
      <p>{data?.description}</p>
    </div>
  );
};
```

---

## CSS Template

```css
/* ${PATH}/${NAME}/${NAME}.css */

/* Base */
.${kebab(NAME)} {
  padding: 1.5rem;
  background: var(--color-surface);
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* States */
.${kebab(NAME)}--loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100px;
}

.${kebab(NAME)}--error {
  border: 1px solid var(--color-error);
  color: var(--color-error);
}

/* Header */
.${kebab(NAME)}__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* List */
.${kebab(NAME)}__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.${kebab(NAME)}__item {
  padding: 0.75rem;
  background: var(--color-bg);
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.${kebab(NAME)}__item:hover {
  transform: translateX(4px);
}

/* Form */
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
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  font-size: 1rem;
}

.${kebab(NAME)}__field input:focus,
.${kebab(NAME)}__field textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.${kebab(NAME)}__submit {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
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

.${kebab(NAME)}__error {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef2f2;
  color: var(--color-error);
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

/* Spinner */
.${kebab(NAME)}__spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Animation */
.${kebab(NAME)}.fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Refresh button */
.${kebab(NAME)}__refresh {
  padding: 0.5rem;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 1rem;
}

.${kebab(NAME)}__refresh:hover {
  background: var(--color-surface);
}
```

---

## Export Patterns

### Component index.ts

```typescript
// ${PATH}/${NAME}/index.ts
export { ${NAME} } from "./${NAME}";
```

### Update shared barrel

```typescript
// src/client/components/index.ts
export { Button } from "./Button/Button";
export { ${NAME} } from "./${NAME}/${NAME}";  // Add
```

### Co-located barrel

```typescript
// src/client/pages/Dashboard/_components/index.ts
export { ${NAME} } from "./${NAME}";
```

---

## Usage

```tsx
// Shared component
import { ${NAME} } from "@/components";

// Co-located component
import { ${NAME} } from "./_components";

// Use in JSX
<${NAME} />
<${NAME} className="custom" />
<${NAME} onSuccess={() => refetch()} />
```

---

## Output

```
## Component Created

**Name**: ${NAME}
**Path**: ${PATH}/${NAME}/
**Type**: ${PATH.includes('_components') ? 'Co-located' : 'Shared'}

### Files
- ${PATH}/${NAME}/${NAME}.tsx
- ${PATH}/${NAME}/${NAME}.css
- ${PATH}/${NAME}/index.ts

### Import
\`\`\`tsx
import { ${NAME} } from "${PATH.includes('_components') ? './_components' : '@/components'}";
\`\`\`

### Add Hook
\`\`\`bash
/vite-cloudflare hook use${NAME}Data ${PATH.replace('_components', '_hooks')}
\`\`\`
```
