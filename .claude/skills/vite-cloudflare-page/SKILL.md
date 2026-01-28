---
name: vite-cloudflare:page
model: haiku
description: |
  Add React Router page with co-located structure.
  Creates _components/, _hooks/, _types/, _utils/ with barrel exports.
argument-hint: "<name> [--with-components]"
---

# Add React Router Page

## Variables

NAME: $1 (required, e.g., dashboard, settings, profile)
WITH_COMPONENTS: --with-components creates full co-location structure

## Co-location Structure

```
src/client/pages/${NAME}/
├── ${NAME}Page.tsx           # Page component
├── ${NAME}Page.css           # Page styles
├── _components/              # Page-specific components
│   ├── ${NAME}Header.tsx
│   ├── ${NAME}Header.css
│   ├── ${NAME}Content.tsx
│   ├── ${NAME}Content.css
│   └── index.ts              # Barrel export
├── _hooks/                   # Page-specific hooks
│   ├── use${NAME}.ts
│   └── index.ts
├── _types/                   # Page-specific types
│   ├── ${NAME}.ts
│   └── index.ts
└── _utils/                   # Page-specific utils
    └── index.ts
```

---

## Page Template

### Basic Page

```tsx
// src/client/pages/${NAME}/${NAME}Page.tsx
import "./${NAME}Page.css";

export function ${NAME}Page() {
  return (
    <div className="${kebab(NAME)}-page fade-in">
      <h1>${titleCase(NAME)}</h1>
      <p>Welcome to the ${NAME} page.</p>
    </div>
  );
}
```

### Page with Data Fetching

```tsx
// src/client/pages/${NAME}/${NAME}Page.tsx
import { use${NAME} } from "./_hooks";
import { ${NAME}Header, ${NAME}Content } from "./_components";
import "./${NAME}Page.css";

export function ${NAME}Page() {
  const { data, loading, error, refetch } = use${NAME}();

  if (loading) {
    return (
      <div className="${kebab(NAME)}-page ${kebab(NAME)}-page--loading">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="${kebab(NAME)}-page ${kebab(NAME)}-page--error">
        <p>Error: {error.message}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div className="${kebab(NAME)}-page fade-in">
      <${NAME}Header data={data} />
      <${NAME}Content data={data} onRefresh={refetch} />
    </div>
  );
}
```

### Page with URL Params

```tsx
// src/client/pages/${NAME}/${NAME}Page.tsx
import { useParams } from "react-router";
import { use${NAME}Detail } from "./_hooks";
import { ${NAME}Detail } from "./_components";
import "./${NAME}Page.css";

export function ${NAME}DetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = use${NAME}Detail(id!);

  if (loading) {
    return <div className="${kebab(NAME)}-page--loading">Loading...</div>;
  }

  if (error || !data) {
    return <div className="${kebab(NAME)}-page--error">Not found</div>;
  }

  return (
    <div className="${kebab(NAME)}-page fade-in">
      <${NAME}Detail item={data} />
    </div>
  );
}
```

---

## Page CSS

```css
/* src/client/pages/${NAME}/${NAME}Page.css */

.${kebab(NAME)}-page {
  padding: 2rem 0;
}

.${kebab(NAME)}-page h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.${kebab(NAME)}-page--loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  gap: 1rem;
}

.${kebab(NAME)}-page--error {
  text-align: center;
  padding: 2rem;
  color: var(--color-error);
}

.${kebab(NAME)}-page--error button {
  margin-top: 1rem;
}

/* Spinner */
.${kebab(NAME)}-page .spinner {
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
```

---

## Co-located Components

### _components/index.ts

```typescript
// src/client/pages/${NAME}/_components/index.ts
export { ${NAME}Header } from "./${NAME}Header";
export { ${NAME}Content } from "./${NAME}Content";
```

### Header Component

```tsx
// src/client/pages/${NAME}/_components/${NAME}Header.tsx
import type { FC } from "react";
import type { ${NAME}Data } from "../_types";
import "./${NAME}Header.css";

interface ${NAME}HeaderProps {
  data: ${NAME}Data | null;
}

export const ${NAME}Header: FC<${NAME}HeaderProps> = ({ data }) => {
  return (
    <header className="${kebab(NAME)}-header">
      <h1>{data?.title || "${titleCase(NAME)}"}</h1>
      <p>{data?.description}</p>
    </header>
  );
};
```

### Content Component

```tsx
// src/client/pages/${NAME}/_components/${NAME}Content.tsx
import type { FC } from "react";
import type { ${NAME}Data } from "../_types";
import "./${NAME}Content.css";

interface ${NAME}ContentProps {
  data: ${NAME}Data | null;
  onRefresh?: () => void;
}

export const ${NAME}Content: FC<${NAME}ContentProps> = ({ data, onRefresh }) => {
  return (
    <div className="${kebab(NAME)}-content">
      <div className="${kebab(NAME)}-content__header">
        <h2>Content</h2>
        {onRefresh && (
          <button onClick={onRefresh} className="${kebab(NAME)}-content__refresh">
            ↻
          </button>
        )}
      </div>
      <div className="${kebab(NAME)}-content__body">
        {data?.items?.map((item) => (
          <div key={item.id} className="${kebab(NAME)}-content__item">
            {item.name}
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## Co-located Hook

```typescript
// src/client/pages/${NAME}/_hooks/use${NAME}.ts
import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api";
import type { ${NAME}Data } from "../_types";

export function use${NAME}() {
  const [data, setData] = useState<${NAME}Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetch${NAME} = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.get<${NAME}Data>("/${NAME}");
      setData(result);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch${NAME}();
  }, [fetch${NAME}]);

  return { data, loading, error, refetch: fetch${NAME} };
}

// Hook with ID parameter
export function use${NAME}Detail(id: string) {
  const [data, setData] = useState<${NAME}Item | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true);
      try {
        const result = await api.get<${NAME}Item>(`/${NAME}/${id}`);
        setData(result);
      } catch (e) {
        setError(e as Error);
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  return { data, loading, error };
}
```

```typescript
// src/client/pages/${NAME}/_hooks/index.ts
export { use${NAME}, use${NAME}Detail } from "./use${NAME}";
```

---

## Co-located Types

```typescript
// src/client/pages/${NAME}/_types/${NAME}.ts
export interface ${NAME}Data {
  title: string;
  description?: string;
  items: ${NAME}Item[];
}

export interface ${NAME}Item {
  id: string;
  name: string;
  createdAt: string;
}

export type ${NAME}Status = "pending" | "active" | "completed";
```

```typescript
// src/client/pages/${NAME}/_types/index.ts
export type { ${NAME}Data, ${NAME}Item, ${NAME}Status } from "./${NAME}";
```

---

## Co-located Utils

```typescript
// src/client/pages/${NAME}/_utils/index.ts
import type { ${NAME}Item } from "../_types";

export function format${NAME}Date(dateString: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(dateString));
}

export function sort${NAME}Items(
  items: ${NAME}Item[],
  order: "asc" | "desc" = "desc"
): ${NAME}Item[] {
  return [...items].sort((a, b) => {
    const comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
    return order === "asc" ? comparison : -comparison;
  });
}
```

---

## Register Route

```tsx
// src/client/router.tsx
import { createBrowserRouter } from "react-router";
import { App } from "./App";
import { HomePage } from "./pages/Home/HomePage";
import { ${NAME}Page } from "./pages/${NAME}/${NAME}Page";  // Add import

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "${kebab(NAME)}", element: <${NAME}Page /> },  // Add route
      // For detail page:
      // { path: "${kebab(NAME)}/:id", element: <${NAME}DetailPage /> },
    ],
  },
]);
```

---

## Add Navigation Link

```tsx
// src/client/App.tsx
<nav>
  <a href="/">Home</a>
  <a href="/${kebab(NAME)}">${titleCase(NAME)}</a>  {/* Add link */}
</nav>
```

---

## Output

```
## Page Created

**Name**: ${NAME}
**Path**: src/client/pages/${NAME}/
**Route**: /${kebab(NAME)}

### Structure
\`\`\`
src/client/pages/${NAME}/
├── ${NAME}Page.tsx
├── ${NAME}Page.css
${WITH_COMPONENTS ? `├── _components/
│   ├── ${NAME}Header.tsx
│   ├── ${NAME}Content.tsx
│   └── index.ts
├── _hooks/
│   ├── use${NAME}.ts
│   └── index.ts
├── _types/
│   ├── ${NAME}.ts
│   └── index.ts
└── _utils/
    └── index.ts` : ''}
\`\`\`

### Route Added
\`\`\`tsx
{ path: "${kebab(NAME)}", element: <${NAME}Page /> }
\`\`\`

### Next Steps
- Add to router.tsx
- Add navigation link
- Add API route: \`/vite-cloudflare api ${NAME}\`
```
