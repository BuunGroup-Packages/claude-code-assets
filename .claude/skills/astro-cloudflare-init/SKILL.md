---
name: astro-cloudflare:init
model: haiku
description: |
  Initialize new Astro 6 + Cloudflare Workers project with Hono API.
  Sets up complete stack: React, D1, R2, KV, TypeScript, CSS animations.
argument-hint: "<project-name> [--minimal]"
---

# Initialize Astro 6 + Cloudflare Project

## Variables

NAME: $1 (required, project name)
MINIMAL: --minimal flag skips example components

## Workflow

1. Create project directory
2. Initialize package.json with dependencies
3. Create configuration files
4. Create directory structure
5. Add starter files
6. Output next steps

## package.json

```json
{
  "name": "${NAME}",
  "type": "module",
  "scripts": {
    "dev": "wrangler types && astro dev",
    "build": "wrangler types && astro check && astro build",
    "preview": "astro build && astro preview",
    "deploy": "astro build && wrangler deploy",
    "db:migrate": "wrangler d1 execute DB --file=./migrations/001_init.sql",
    "db:migrate:local": "wrangler d1 execute DB --local --file=./migrations/001_init.sql"
  },
  "dependencies": {
    "astro": "^6.0.0",
    "@astrojs/cloudflare": "^12.0.0",
    "@astrojs/react": "^4.4.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.7.0",
    "wrangler": "^4.0.0"
  }
}
```

## astro.config.ts

```typescript
import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";
import react from "@astrojs/react";

export default defineConfig({
  output: "server",
  adapter: cloudflare(),
  integrations: [react()],
});
```

## wrangler.jsonc (Astro 6)

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "${NAME}",
  "compatibility_date": "2025-05-21",
  "compatibility_flags": ["nodejs_compat"],
  "main": "@astrojs/cloudflare/entrypoints/server"

  // Uncomment and configure as needed:
  // "d1_databases": [
  //   {
  //     "binding": "DB",
  //     "database_name": "${NAME}-db",
  //     "database_id": "YOUR_DATABASE_ID"
  //   }
  // ],
  // "r2_buckets": [
  //   {
  //     "binding": "BUCKET",
  //     "bucket_name": "${NAME}-bucket"
  //   }
  // ],
  // "kv_namespaces": [
  //   {
  //     "binding": "CACHE",
  //     "id": "YOUR_KV_ID"
  //   }
  // ]
}
```

## tsconfig.json

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/layouts/*": ["src/layouts/*"]
    }
  }
}
```

## website.config.ts

```typescript
export const config = {
  site: {
    name: "${NAME}",
    url: "https://${NAME}.workers.dev",
    description: "Built with Astro 6 + Cloudflare Workers",
  },
  meta: {
    ogImage: "/og-image.png",
    twitterHandle: "@handle",
  },
  features: {
    d1: false,
    r2: false,
    kv: false,
  },
} as const;

export type SiteConfig = typeof config;
```

## Directory Structure

```
${NAME}/
├── src/
│   ├── pages/
│   │   ├── index.astro
│   │   └── api/
│   │       └── health.ts
│   ├── actions/
│   │   └── index.ts
│   ├── components/
│   │   └── Button.tsx
│   ├── layouts/
│   │   └── Layout.astro
│   └── styles/
│       ├── global.css
│       └── animations.css
├── public/
│   └── favicon.svg
├── migrations/
│   └── .gitkeep
├── website.config.ts
├── astro.config.ts
├── wrangler.jsonc
├── tsconfig.json
├── package.json
└── .gitignore
```

## src/layouts/Layout.astro

```astro
---
import "@/styles/global.css";
import "@/styles/animations.css";
import { config } from "../../website.config";

interface Props {
  title: string;
  description?: string;
}

const { title, description = config.site.description } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title} | {config.site.name}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

## src/pages/index.astro

```astro
---
import Layout from "@/layouts/Layout.astro";
import { Button } from "@/components/Button";
---

<Layout title="Home">
  <main class="container fade-in">
    <h1>Welcome to ${NAME}</h1>
    <p>Built with Astro 6 + Cloudflare Workers</p>
    <Button client:load>Get Started</Button>
  </main>
</Layout>
```

## src/actions/index.ts (Astro 6 Actions)

```typescript
import { defineAction } from "astro:actions";
import { z } from "astro/zod";

export const server = {
  // Example action
  echo: defineAction({
    input: z.object({
      message: z.string(),
    }),
    handler: async (input) => {
      return { echo: input.message };
    },
  }),
};
```

## src/pages/api/health.ts

```typescript
import type { APIRoute } from "astro";

export const GET: APIRoute = () => {
  return new Response(
    JSON.stringify({
      status: "ok",
      timestamp: new Date().toISOString(),
    }),
    {
      headers: { "Content-Type": "application/json" },
    }
  );
};
```

## src/components/Button.tsx

```tsx
import type { FC, ReactNode } from "react";
import "./Button.css";

interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
}

export const Button: FC<ButtonProps> = ({
  children,
  onClick,
  variant = "primary",
}) => (
  <button className={`btn btn-${variant}`} onClick={onClick}>
    {children}
  </button>
);
```

## src/components/Button.css

```css
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary {
  background: #0066ff;
  color: white;
}

.btn-secondary {
  background: #e5e7eb;
  color: #1f2937;
}
```

## src/styles/global.css

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
  --color-text: #1f2937;
  --color-primary: #0066ff;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
```

## src/styles/animations.css

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

## .gitignore

```
node_modules/
dist/
.wrangler/
.dev.vars
.astro/
```

## Output

```
## Project Initialized

**Name**: ${NAME}
**Stack**: Astro 6 + Cloudflare Workers + React 19

### Created Files
- astro.config.ts
- wrangler.jsonc (v6 entrypoint)
- tsconfig.json
- website.config.ts
- src/layouts/Layout.astro
- src/pages/index.astro
- src/pages/api/health.ts
- src/actions/index.ts
- src/components/Button.tsx
- src/styles/global.css
- src/styles/animations.css

### Next Steps
\`\`\`bash
cd ${NAME}
npm install
npm run dev
\`\`\`

### Add Bindings
\`\`\`bash
/astro-cloudflare binding d1 DB
/astro-cloudflare binding r2 BUCKET
/astro-cloudflare binding kv CACHE
\`\`\`
```
