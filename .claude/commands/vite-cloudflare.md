---
description: Build Vite 6 + React + Cloudflare Workers apps with Hono
argument-hint: "<command> [args]"
---

# Vite + React + Cloudflare + Hono

Run `/vite-cloudflare $ARGUMENTS` to use this stack.

## Commands

| Command | Description |
|---------|-------------|
| init NAME | Create new project |
| api RESOURCE | Add Hono API route |
| component NAME [path] | Add React component |
| page NAME [--with-components] | Add React Router page |
| binding TYPE NAME | Add D1/R2/KV binding |

## Examples

```bash
# Initialize project
/vite-cloudflare init my-app

# Add API route
/vite-cloudflare api users
/vite-cloudflare api posts

# Add component
/vite-cloudflare component Button
/vite-cloudflare component UserCard src/client/pages/Dashboard/_components

# Add page
/vite-cloudflare page dashboard --with-components
/vite-cloudflare page settings

# Add binding
/vite-cloudflare binding d1 DB
/vite-cloudflare binding r2 BUCKET
/vite-cloudflare binding kv CACHE
```

## Stack

| Layer | Technology |
|-------|------------|
| Build | Vite 6 + @cloudflare/vite-plugin |
| UI | React 19 (SPA) |
| Routing | React Router 7 |
| API | Hono |
| Database | Cloudflare D1 |
| Storage | Cloudflare R2 |
| Cache | Cloudflare KV |

## Architecture

```
┌─────────────────────────────────────────────┐
│           Cloudflare Workers                │
│  ┌──────────────────┬────────────────────┐ │
│  │   Hono API       │   Static Assets    │ │
│  │   /api/*         │   (Vite build)     │ │
│  │   D1, R2, KV     │                    │ │
│  └──────────────────┴────────────────────┘ │
└─────────────────────────────────────────────┘
              ↓ fetch()
┌─────────────────────────────────────────────┐
│              React SPA                       │
│              (Client-side)                   │
└─────────────────────────────────────────────┘
```

## Key Pattern

```typescript
// Worker: src/worker/index.ts
import { Hono } from "hono";

const app = new Hono()
  .basePath("/api")
  .get("/users", async (c) => {
    const { results } = await c.env.DB.prepare("SELECT * FROM users").all();
    return c.json(results);
  });

export default app;

// Client: src/client/lib/api.ts
const users = await fetch("/api/users").then(r => r.json());
```
