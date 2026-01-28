---
name: vite-cloudflare:init
model: haiku
description: |
  Initialize Vite 6 + React + Cloudflare Workers + Hono project.
  Sets up complete stack with TypeScript, React Router, co-located structure.
argument-hint: "<project-name> [--minimal]"
---

# Initialize Vite + Cloudflare Project

## Variables

NAME: $1 (required, project name)
MINIMAL: --minimal skips example components

## Workflow

1. Create project directory
2. Initialize package.json
3. Create configuration files
4. Create directory structure
5. Add starter files
6. Output next steps

---

## package.json

```json
{
  "name": "${NAME}",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "vite build && wrangler deploy",
    "types": "wrangler types",
    "db:migrate": "wrangler d1 execute DB --file=./migrations/001_init.sql",
    "db:migrate:local": "wrangler d1 execute DB --local --file=./migrations/001_init.sql"
  },
  "dependencies": {
    "hono": "^4.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router": "^7.0.0"
  },
  "devDependencies": {
    "@cloudflare/vite-plugin": "^1.0.0",
    "@cloudflare/workers-types": "^4.0.0",
    "@hono/zod-validator": "^0.4.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.7.0",
    "vite": "^6.0.0",
    "wrangler": "^4.0.0",
    "zod": "^3.0.0"
  }
}
```

---

## vite.config.ts

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
  build: {
    outDir: "dist/client",
  },
});
```

---

## wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "${NAME}",
  "compatibility_date": "2025-05-21",
  "compatibility_flags": ["nodejs_compat"],
  "main": "src/worker/index.ts",
  "assets": {
    "directory": "./dist/client",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application"
  }

  // Uncomment to add bindings:
  // "d1_databases": [
  //   { "binding": "DB", "database_name": "${NAME}-db", "database_id": "YOUR_ID" }
  // ],
  // "r2_buckets": [
  //   { "binding": "BUCKET", "bucket_name": "${NAME}-bucket" }
  // ],
  // "kv_namespaces": [
  //   { "binding": "CACHE", "id": "YOUR_ID" }
  // ]
}
```

---

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/client/*"],
      "@worker/*": ["src/worker/*"]
    }
  },
  "include": ["src/client/**/*"],
  "references": [{ "path": "./tsconfig.worker.json" }]
}
```

---

## tsconfig.worker.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "strict": true,
    "types": ["@cloudflare/workers-types"],
    "baseUrl": ".",
    "paths": {
      "@worker/*": ["src/worker/*"]
    }
  },
  "include": ["src/worker/**/*"]
}
```

---

## Directory Structure

```
${NAME}/
├── src/
│   ├── client/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── router.tsx
│   │   ├── pages/
│   │   │   └── Home/
│   │   │       ├── HomePage.tsx
│   │   │       └── HomePage.css
│   │   ├── components/
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   └── Button.css
│   │   │   └── index.ts
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── styles/
│   │       ├── global.css
│   │       └── animations.css
│   └── worker/
│       ├── index.ts
│       ├── routes/
│       │   └── index.ts
│       └── lib/
│           └── types.ts
├── public/
│   └── favicon.svg
├── migrations/
│   └── .gitkeep
├── index.html
├── vite.config.ts
├── wrangler.jsonc
├── tsconfig.json
├── tsconfig.worker.json
├── package.json
└── .gitignore
```

---

## index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${NAME}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/client/main.tsx"></script>
  </body>
</html>
```

---

## src/client/main.tsx

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router";
import { router } from "./router";
import "./styles/global.css";
import "./styles/animations.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
```

---

## src/client/router.tsx

```tsx
import { createBrowserRouter } from "react-router";
import { App } from "./App";
import { HomePage } from "./pages/Home/HomePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      // Add more routes here
    ],
  },
]);
```

---

## src/client/App.tsx

```tsx
import { Outlet } from "react-router";
import "./App.css";

export function App() {
  return (
    <div className="app">
      <header className="app-header">
        <nav>
          <a href="/">${NAME}</a>
        </nav>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
```

---

## src/client/App.css

```css
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--color-border);
}

.app-header nav a {
  font-weight: 600;
  color: var(--color-text);
  text-decoration: none;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
```

---

## src/client/pages/Home/HomePage.tsx

```tsx
import { useState, useEffect } from "react";
import { Button } from "@/components";
import "./HomePage.css";

export function HomePage() {
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => setMessage(data.status))
      .catch(() => setMessage("API unavailable"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="home-page fade-in">
      <h1>Welcome to ${NAME}</h1>
      <p>Vite 6 + React + Cloudflare Workers + Hono</p>
      <p className="api-status">
        API Status: {loading ? "Checking..." : message}
      </p>
      <Button onClick={() => alert("Hello!")}>Get Started</Button>
    </div>
  );
}
```

---

## src/client/pages/Home/HomePage.css

```css
.home-page {
  text-align: center;
  padding: 4rem 0;
}

.home-page h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.home-page p {
  color: var(--color-text-muted);
  margin-bottom: 1rem;
}

.api-status {
  font-family: monospace;
  background: var(--color-surface);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  display: inline-block;
  margin-bottom: 2rem;
}
```

---

## src/client/components/Button/Button.tsx

```tsx
import type { FC, ReactNode, ButtonHTMLAttributes } from "react";
import "./Button.css";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary";
}

export const Button: FC<ButtonProps> = ({
  children,
  variant = "primary",
  className = "",
  ...props
}) => (
  <button className={`btn btn-${variant} ${className}`.trim()} {...props}>
    {children}
  </button>
);
```

---

## src/client/components/Button/Button.css

```css
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}
```

---

## src/client/components/index.ts

```typescript
export { Button } from "./Button/Button";
```

---

## src/client/lib/api.ts

```typescript
const API_BASE = "/api";

class ApiError extends Error {
  constructor(
    message: string,
    public status: number
  ) {
    super(message);
    this.name = "ApiError";
  }
}

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
    const error = await res.json().catch(() => ({ message: "Request failed" }));
    throw new ApiError(error.message, res.status);
  }

  return res.json();
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint),

  post: <T>(endpoint: string, data: unknown) =>
    request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  put: <T>(endpoint: string, data: unknown) =>
    request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: "DELETE" }),
};
```

---

## src/client/styles/global.css

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --font-sans: system-ui, -apple-system, sans-serif;
  --color-bg: #ffffff;
  --color-surface: #f9fafb;
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-primary: #0066ff;
  --color-border: #e5e7eb;
  --color-error: #dc2626;
  --color-success: #16a34a;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
}

a {
  color: var(--color-primary);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

---

## src/client/styles/animations.css

```css
.fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.scale-in {
  animation: scaleIn 0.2s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
```

---

## src/worker/index.ts

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

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
  .get("/health", (c) => {
    return c.json({
      status: "ok",
      timestamp: new Date().toISOString(),
    });
  });

export default app;
```

---

## src/worker/lib/types.ts

```typescript
export type Bindings = {
  DB: D1Database;
  BUCKET: R2Bucket;
  CACHE: KVNamespace;
  ASSETS: Fetcher;
};
```

---

## .gitignore

```
node_modules/
dist/
.wrangler/
.dev.vars
*.local
```

---

## Output

```
## Project Initialized

**Name**: ${NAME}
**Stack**: Vite 6 + React 19 + Cloudflare Workers + Hono

### Structure
- src/client/ — React SPA
- src/worker/ — Hono API

### Created Files
- vite.config.ts
- wrangler.jsonc
- tsconfig.json / tsconfig.worker.json
- src/client/main.tsx, App.tsx, router.tsx
- src/worker/index.ts
- Component: Button
- Page: Home

### Next Steps
\`\`\`bash
cd ${NAME}
npm install
npm run dev
\`\`\`

### Add Features
\`\`\`bash
/vite-cloudflare api users
/vite-cloudflare page dashboard --with-components
/vite-cloudflare binding d1 DB
\`\`\`
```
