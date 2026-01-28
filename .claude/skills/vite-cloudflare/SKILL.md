---
name: vite-cloudflare
model: sonnet
description: |
  Build Vite 6 + React + Cloudflare Workers apps with Hono API.
  TypeScript-first, co-located components, CSS animations.
  Orchestrates init, api, component, binding, page sub-skills.
argument-hint: "[command] [args]"
---

# Vite 6 + React + Cloudflare Workers + Hono

## Stack Overview

| Layer | Technology |
|-------|------------|
| Build | Vite 6 + @cloudflare/vite-plugin |
| UI | React 19 (SPA) |
| Routing | React Router 7 |
| API | Hono (Cloudflare Workers) |
| Database | Cloudflare D1 |
| Storage | Cloudflare R2 |
| Cache | Cloudflare KV |
| Styling | CSS (no Framer Motion) |

## Commands

| Command | Sub-skill | What it does |
|---------|-----------|--------------|
| init | /vite-cloudflare:init | Scaffold new project |
| api | /vite-cloudflare:api | Add Hono API route |
| component | /vite-cloudflare:component | Add React component |
| binding | /vite-cloudflare:binding | Configure D1/R2/KV |
| page | /vite-cloudflare:page | Add React Router page |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare Workers                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Hono API (/api/*)           │  Static Assets (Vite)   ││
│  │  - /api/users                │  - index.html           ││
│  │  - /api/posts                │  - assets/*.js          ││
│  │  - Bindings: D1, R2, KV      │  - assets/*.css         ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   React SPA       │
                    │   (Client-side)   │
                    │   - React Router  │
                    │   - fetch(/api/*) │
                    └───────────────────┘
```

### Key Concepts

1. **SPA Architecture** - React runs entirely on client, no SSR by default
2. **API Layer** - Hono handles all `/api/*` routes in Workers
3. **Static Assets** - Vite builds to static files served by Workers
4. **Bindings** - D1/R2/KV accessed only in Hono (not React)

---

## Project Structure

```
project/
├── src/
│   ├── client/                   # React SPA
│   │   ├── main.tsx              # Entry point
│   │   ├── App.tsx               # Root component
│   │   ├── router.tsx            # React Router config
│   │   ├── pages/                # Route pages
│   │   │   ├── Home/
│   │   │   │   ├── HomePage.tsx
│   │   │   │   ├── HomePage.css
│   │   │   │   ├── _components/
│   │   │   │   ├── _hooks/
│   │   │   │   └── _types/
│   │   │   └── Dashboard/
│   │   │       ├── DashboardPage.tsx
│   │   │       └── _components/
│   │   ├── components/           # Shared components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   └── Button.css
│   │   │   └── index.ts
│   │   ├── hooks/                # Shared hooks
│   │   ├── types/                # Shared types
│   │   └── lib/
│   │       └── api.ts            # API client (fetch wrapper)
│   │
│   └── worker/                   # Hono API (Cloudflare Workers)
│       ├── index.ts              # Worker entry
│       ├── routes/
│       │   ├── users.ts
│       │   ├── posts.ts
│       │   └── index.ts
│       ├── middleware/
│       │   └── auth.ts
│       └── lib/
│           ├── db.ts             # D1 helpers
│           ├── storage.ts        # R2 helpers
│           └── cache.ts          # KV helpers
│
├── public/                       # Static assets
├── index.html                    # Vite entry HTML
├── vite.config.ts
├── wrangler.jsonc
├── tsconfig.json
├── tsconfig.worker.json
└── package.json
```

---

## Configuration Files

### vite.config.ts

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { cloudflare } from "@cloudflare/vite-plugin";
import path from "path";

export default defineConfig({
  plugins: [react(), cloudflare()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src/client"),
      "@worker": path.resolve(__dirname, "./src/worker"),
    },
  },
});
```

### wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-app",
  "compatibility_date": "2025-05-21",
  "compatibility_flags": ["nodejs_compat"],
  "main": "src/worker/index.ts",
  "assets": {
    "directory": "./dist/client",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application"
  }
}
```

### tsconfig.worker.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "types": ["@cloudflare/workers-types"],
    "lib": ["ES2022"],
    "moduleResolution": "bundler"
  },
  "include": ["src/worker/**/*"]
}
```

---

## Hono API Pattern

### Worker Entry

```typescript
// src/worker/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { users } from "./routes/users";
import { posts } from "./routes/posts";

type Bindings = {
  DB: D1Database;
  BUCKET: R2Bucket;
  CACHE: KVNamespace;
  ASSETS: Fetcher;
};

const app = new Hono<{ Bindings: Bindings }>()
  .basePath("/api")
  .use("*", logger())
  .use("*", cors())
  .get("/health", (c) => c.json({ status: "ok" }))
  .route("/users", users)
  .route("/posts", posts);

export default app;
```

### Route Module

```typescript
// src/worker/routes/users.ts
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

type Bindings = {
  DB: D1Database;
};

export const users = new Hono<{ Bindings: Bindings }>()
  .get("/", async (c) => {
    const { results } = await c.env.DB.prepare(
      "SELECT * FROM users"
    ).all();
    return c.json(results);
  })
  .get("/:id", async (c) => {
    const user = await c.env.DB.prepare(
      "SELECT * FROM users WHERE id = ?"
    ).bind(c.req.param("id")).first();

    if (!user) return c.json({ error: "Not found" }, 404);
    return c.json(user);
  })
  .post(
    "/",
    zValidator("json", z.object({
      name: z.string().min(1),
      email: z.string().email(),
    })),
    async (c) => {
      const { name, email } = c.req.valid("json");
      const result = await c.env.DB.prepare(
        "INSERT INTO users (name, email) VALUES (?, ?) RETURNING *"
      ).bind(name, email).first();
      return c.json(result, 201);
    }
  );
```

---

## React Client Pattern

### API Client

```typescript
// src/client/lib/api.ts
const API_BASE = "/api";

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.message || `HTTP ${res.status}`);
  }

  return res.json();
}

export const api = {
  users: {
    list: () => request<User[]>("/users"),
    get: (id: string) => request<User>(`/users/${id}`),
    create: (data: CreateUser) =>
      request<User>("/users", {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
};
```

### React Hook

```typescript
// src/client/pages/Dashboard/_hooks/useUsers.ts
import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api";
import type { User } from "../_types";

export function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.users.list();
      setUsers(data);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, loading, error, refetch: fetchUsers };
}
```

### Page Component

```tsx
// src/client/pages/Dashboard/DashboardPage.tsx
import { useUsers } from "./_hooks/useUsers";
import { UserList, CreateUserForm } from "./_components";
import "./DashboardPage.css";

export function DashboardPage() {
  const { users, loading, error, refetch } = useUsers();

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error.message}</div>;

  return (
    <div className="dashboard-page fade-in">
      <h1>Dashboard</h1>
      <CreateUserForm onSuccess={refetch} />
      <UserList users={users} />
    </div>
  );
}
```

---

## Co-located Design

```
src/client/pages/Dashboard/
├── DashboardPage.tsx         # Page component
├── DashboardPage.css         # Page styles
├── _components/              # Page-specific components
│   ├── UserList.tsx
│   ├── UserList.css
│   ├── CreateUserForm.tsx
│   ├── CreateUserForm.css
│   └── index.ts              # Barrel export
├── _hooks/                   # Page-specific hooks
│   ├── useUsers.ts
│   └── index.ts
├── _types/                   # Page-specific types
│   ├── user.ts
│   └── index.ts
└── _utils/                   # Page-specific utils
    └── index.ts
```

### Barrel Exports

```typescript
// _components/index.ts
export { UserList } from "./UserList";
export { CreateUserForm } from "./CreateUserForm";

// _hooks/index.ts
export { useUsers } from "./useUsers";

// _types/index.ts
export type { User, CreateUser } from "./user";
```

---

## CSS Animations

```css
/* src/client/styles/animations.css */
.fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-in {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { transform: translateX(-20px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

---

## Usage Examples

```bash
# Create project
/vite-cloudflare init my-app

# Add API route
/vite-cloudflare api users

# Add page with co-location
/vite-cloudflare page dashboard --with-components

# Add shared component
/vite-cloudflare component Button

# Add binding
/vite-cloudflare binding d1 DB
```

---

## Development

```bash
# Install dependencies
npm install

# Generate binding types
wrangler types

# Start dev server (Vite + Workers runtime)
npm run dev

# Preview production build
npm run build && npm run preview

# Deploy to Cloudflare
npm run deploy
```

---

## Key Differences from Astro

| Aspect | Astro | Vite + React |
|--------|-------|--------------|
| Rendering | Islands (partial hydration) | Full SPA (client-side) |
| API | Astro Actions | Hono routes |
| Routing | File-based | React Router |
| SSR | Built-in | Manual setup |
| Bundle | Per-island | Single bundle |

---

## Output

After executing command:

```
## Vite + Cloudflare

**Command**: [COMMAND]
**Result**: [description]

### Files
- [list]

### Next Steps
- [actions]
```
