---
name: astro-cloudflare:page
model: haiku
description: |
  Add new Astro page with full co-location structure.
  Creates _components/, _hooks/, _types/, _utils/ with barrel exports.
argument-hint: "<name> [--with-components] [--dynamic] [--static]"
---

# Add Astro Page with Co-location

## Variables

NAME: $1 (required, e.g., dashboard, secrets, settings)
WITH_COMPONENTS: --with-components creates full co-location structure
DYNAMIC: --dynamic creates [id].astro for dynamic routes
STATIC: --static sets prerender = true

## Co-location Structure

```
src/pages/${NAME}/
├── index.astro               # Page entry
├── [id].astro                # Dynamic route (if --dynamic)
├── _components/              # React islands
│   ├── ${NAME}Hero.tsx
│   ├── ${NAME}Hero.css
│   ├── ${NAME}Form.tsx
│   ├── ${NAME}Form.css
│   └── index.ts              # Barrel export
├── _hooks/                   # React hooks
│   ├── use${NAME}.ts
│   └── index.ts
├── _types/                   # TypeScript types
│   ├── ${NAME}.ts
│   └── index.ts
└── _utils/                   # Utilities
    ├── helpers.ts
    └── index.ts
```

---

## Barrel Exports

### _components/index.ts

```typescript
// src/pages/${NAME}/_components/index.ts
export { ${NAME}Hero } from "./${NAME}Hero";
export { ${NAME}Form } from "./${NAME}Form";
export { ${NAME}List } from "./${NAME}List";
```

### _hooks/index.ts

```typescript
// src/pages/${NAME}/_hooks/index.ts
export { use${NAME} } from "./use${NAME}";
export { use${NAME}Form } from "./use${NAME}Form";
```

### _types/index.ts

```typescript
// src/pages/${NAME}/_types/index.ts
export type { ${NAME}Item, ${NAME}FormData, ${NAME}State } from "./${NAME}";
```

### _utils/index.ts

```typescript
// src/pages/${NAME}/_utils/index.ts
export { format${NAME}, validate${NAME} } from "./helpers";
```

---

## Page Templates

### SSR Page with Islands

```astro
---
// src/pages/${NAME}/index.astro
import Layout from "@/layouts/Layout.astro";
import { ${NAME}Hero, ${NAME}Form, ${NAME}List } from "./_components";
import type { ${NAME}Item } from "./_types";
import { actions } from "astro:actions";

export const prerender = false;

// Server-side data fetch
const { data: items } = await Astro.callAction(actions.${NAME}.list, {});
---

<Layout title="${titleCase(NAME)}">
  <main class="page-${NAME}">
    <!-- Static header -->
    <header class="page-header fade-in">
      <h1>${titleCase(NAME)}</h1>
      <p>Manage your ${NAME} here.</p>
    </header>

    <!-- Island: Hero (immediate) -->
    <${NAME}Hero client:load />

    <!-- Island: Form (idle) -->
    <section class="form-section">
      <h2>Create New</h2>
      <${NAME}Form client:idle />
    </section>

    <!-- Island: List (visible) -->
    <section class="list-section">
      <h2>All ${titleCase(NAME)}</h2>
      <${NAME}List client:visible items={items} />
    </section>
  </main>
</Layout>

<style>
  .page-${NAME} {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .page-header {
    margin-bottom: 2rem;
  }

  .page-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .form-section,
  .list-section {
    margin-top: 3rem;
  }

  section h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--color-border);
  }
</style>
```

### Dynamic Route Page

```astro
---
// src/pages/${NAME}/[id].astro
import Layout from "@/layouts/Layout.astro";
import { ${NAME}Detail, ${NAME}Actions } from "./_components";
import { actions } from "astro:actions";

export const prerender = false;

const { id } = Astro.params;

const { data: item, error } = await Astro.callAction(
  actions.${NAME}.getById,
  { id: id! }
);

if (error || !item) {
  return Astro.redirect("/404");
}
---

<Layout title={item.name}>
  <main class="page-${NAME}-detail fade-in">
    <nav class="breadcrumb">
      <a href="/${NAME}">${titleCase(NAME)}</a>
      <span>/</span>
      <span>{item.name}</span>
    </nav>

    <!-- Island: Detail view -->
    <${NAME}Detail client:load item={item} />

    <!-- Island: Actions (delete, edit) -->
    <${NAME}Actions client:idle itemId={item.id} />
  </main>
</Layout>

<style>
  .page-${NAME}-detail {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  .breadcrumb {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    color: var(--color-text-muted);
  }

  .breadcrumb a {
    color: var(--color-primary);
  }
</style>
```

### Static Page

```astro
---
// src/pages/${NAME}/index.astro
import Layout from "@/layouts/Layout.astro";
import { ${NAME}Content } from "./_components";

export const prerender = true; // Static at build time
---

<Layout title="${titleCase(NAME)}">
  <main class="page-${NAME} fade-in">
    <h1>${titleCase(NAME)}</h1>

    <!-- Static content, no hydration needed -->
    <${NAME}Content />
  </main>
</Layout>
```

---

## Co-located Component Templates

### Hero Component (Island)

```tsx
// src/pages/${NAME}/_components/${NAME}Hero.tsx
import type { FC } from "react";
import "./${NAME}Hero.css";

interface ${NAME}HeroProps {
  title?: string;
  subtitle?: string;
}

export const ${NAME}Hero: FC<${NAME}HeroProps> = ({
  title = "${titleCase(NAME)}",
  subtitle = "Welcome to the ${NAME} section",
}) => {
  return (
    <section className="${kebab(NAME)}-hero fade-in">
      <h1 className="${kebab(NAME)}-hero__title">{title}</h1>
      <p className="${kebab(NAME)}-hero__subtitle">{subtitle}</p>
    </section>
  );
};
```

### Form Component (Island)

```tsx
// src/pages/${NAME}/_components/${NAME}Form.tsx
import { actions } from "astro:actions";
import { useActionState } from "react";
import { withState } from "@astrojs/react/actions";
import type { FC } from "react";
import type { ${NAME}FormData } from "../_types";
import "./${NAME}Form.css";

export const ${NAME}Form: FC = () => {
  const [state, action, pending] = useActionState(
    withState(actions.${NAME}.create),
    { data: undefined, error: undefined }
  );

  return (
    <form action={action} className="${kebab(NAME)}-form">
      <div className="${kebab(NAME)}-form__field">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          required
          placeholder="Enter name"
        />
      </div>

      <div className="${kebab(NAME)}-form__field">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          rows={3}
          placeholder="Enter description"
        />
      </div>

      <button
        type="submit"
        disabled={pending}
        className="${kebab(NAME)}-form__submit"
      >
        {pending ? "Creating..." : "Create"}
      </button>

      {state.error && (
        <p className="${kebab(NAME)}-form__error">{state.error.message}</p>
      )}

      {state.data && (
        <p className="${kebab(NAME)}-form__success">
          Created successfully!
        </p>
      )}
    </form>
  );
};
```

### List Component (Island)

```tsx
// src/pages/${NAME}/_components/${NAME}List.tsx
import type { FC } from "react";
import { use${NAME} } from "../_hooks";
import type { ${NAME}Item } from "../_types";
import "./${NAME}List.css";

interface ${NAME}ListProps {
  items?: ${NAME}Item[];
}

export const ${NAME}List: FC<${NAME}ListProps> = ({ items: initialItems }) => {
  const { items, loading, error, refetch } = use${NAME}(initialItems);

  if (loading) {
    return <div className="${kebab(NAME)}-list ${kebab(NAME)}-list--loading">Loading...</div>;
  }

  if (error) {
    return <div className="${kebab(NAME)}-list ${kebab(NAME)}-list--error">{error.message}</div>;
  }

  if (!items?.length) {
    return <div className="${kebab(NAME)}-list ${kebab(NAME)}-list--empty">No items yet.</div>;
  }

  return (
    <div className="${kebab(NAME)}-list">
      <ul className="${kebab(NAME)}-list__items">
        {items.map((item) => (
          <li key={item.id} className="${kebab(NAME)}-list__item fade-in">
            <a href={`/${NAME}/${item.id}`}>
              <span className="${kebab(NAME)}-list__name">{item.name}</span>
              <span className="${kebab(NAME)}-list__date">
                {new Date(item.createdAt).toLocaleDateString()}
              </span>
            </a>
          </li>
        ))}
      </ul>
      <button onClick={refetch} className="${kebab(NAME)}-list__refresh">
        Refresh
      </button>
    </div>
  );
};
```

---

## Co-located Hook Template

```typescript
// src/pages/${NAME}/_hooks/use${NAME}.ts
import { useState, useEffect, useCallback } from "react";
import { actions } from "astro:actions";
import type { ${NAME}Item } from "../_types";

export function use${NAME}(initialItems?: ${NAME}Item[]) {
  const [items, setItems] = useState<${NAME}Item[]>(initialItems ?? []);
  const [loading, setLoading] = useState(!initialItems);
  const [error, setError] = useState<Error | null>(null);

  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const { data, error } = await actions.${NAME}.list();
      if (error) throw new Error(error.message);
      setItems(data ?? []);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!initialItems) {
      fetchItems();
    }
  }, [initialItems, fetchItems]);

  return {
    items,
    loading,
    error,
    refetch: fetchItems,
    setItems,
  };
}
```

---

## Co-located Types Template

```typescript
// src/pages/${NAME}/_types/${NAME}.ts
export interface ${NAME}Item {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ${NAME}FormData {
  name: string;
  description?: string;
}

export interface ${NAME}State {
  items: ${NAME}Item[];
  loading: boolean;
  error: Error | null;
}

export type ${NAME}SortField = "name" | "createdAt" | "updatedAt";
export type ${NAME}SortOrder = "asc" | "desc";
```

---

## Co-located Utils Template

```typescript
// src/pages/${NAME}/_utils/helpers.ts
import type { ${NAME}Item, ${NAME}SortField, ${NAME}SortOrder } from "../_types";

export function format${NAME}Date(date: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
}

export function sort${NAME}Items(
  items: ${NAME}Item[],
  field: ${NAME}SortField,
  order: ${NAME}SortOrder
): ${NAME}Item[] {
  return [...items].sort((a, b) => {
    const aVal = a[field];
    const bVal = b[field];
    const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    return order === "asc" ? comparison : -comparison;
  });
}

export function filter${NAME}Items(
  items: ${NAME}Item[],
  query: string
): ${NAME}Item[] {
  const lower = query.toLowerCase();
  return items.filter(
    (item) =>
      item.name.toLowerCase().includes(lower) ||
      item.description?.toLowerCase().includes(lower)
  );
}
```

---

## Output

```
## Page Created

**Name**: ${NAME}
**URL**: /${NAME}
**Type**: ${STATIC ? 'Static' : 'SSR'}

### Structure
\`\`\`
src/pages/${NAME}/
├── index.astro
${DYNAMIC ? '├── [id].astro' : ''}
├── _components/
│   ├── ${NAME}Hero.tsx
│   ├── ${NAME}Form.tsx
│   ├── ${NAME}List.tsx
│   └── index.ts
├── _hooks/
│   ├── use${NAME}.ts
│   └── index.ts
├── _types/
│   ├── ${NAME}.ts
│   └── index.ts
└── _utils/
    ├── helpers.ts
    └── index.ts
\`\`\`

### Islands
- \`${NAME}Hero\` - client:load (immediate)
- \`${NAME}Form\` - client:idle (deferred)
- \`${NAME}List\` - client:visible (lazy)

### Usage
\`\`\`astro
import { ${NAME}Hero, ${NAME}Form } from "./_components";
import type { ${NAME}Item } from "./_types";

<${NAME}Hero client:load />
<${NAME}Form client:idle />
\`\`\`

### Add Actions
\`\`\`bash
/astro-cloudflare api ${NAME}.create
/astro-cloudflare api ${NAME}.list
/astro-cloudflare api ${NAME}.getById
\`\`\`
```
