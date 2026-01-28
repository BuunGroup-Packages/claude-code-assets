---
name: vite-cloudflare:api
model: haiku
description: |
  Add Hono API route to Cloudflare Workers.
  Type-safe with Zod validation, D1/R2/KV bindings.
argument-hint: "<resource-name>"
---

# Add Hono API Route

## Variables

NAME: $1 (required, e.g., users, posts, secrets)

## Workflow

1. Create route file in src/worker/routes/
2. Add route to main worker index
3. Create TypeScript types
4. Output usage example

---

## Route File Structure

```
src/worker/routes/${NAME}.ts
```

---

## Basic CRUD Route

```typescript
// src/worker/routes/${NAME}.ts
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";
import type { Bindings } from "../lib/types";

// Validation schemas
const create${pascal(NAME)}Schema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional(),
});

const update${pascal(NAME)}Schema = create${pascal(NAME)}Schema.partial();

// Route handler
export const ${NAME} = new Hono<{ Bindings: Bindings }>()

  // GET /${NAME} - List all
  .get("/", async (c) => {
    const { results } = await c.env.DB.prepare(
      "SELECT * FROM ${NAME} ORDER BY created_at DESC"
    ).all();
    return c.json(results);
  })

  // GET /${NAME}/:id - Get one
  .get("/:id", async (c) => {
    const id = c.req.param("id");
    const item = await c.env.DB.prepare(
      "SELECT * FROM ${NAME} WHERE id = ?"
    ).bind(id).first();

    if (!item) {
      return c.json({ error: "Not found" }, 404);
    }
    return c.json(item);
  })

  // POST /${NAME} - Create
  .post("/", zValidator("json", create${pascal(NAME)}Schema), async (c) => {
    const data = c.req.valid("json");
    const id = crypto.randomUUID();

    const result = await c.env.DB.prepare(
      `INSERT INTO ${NAME} (id, name, description, created_at)
       VALUES (?, ?, ?, datetime('now'))
       RETURNING *`
    ).bind(id, data.name, data.description ?? null).first();

    return c.json(result, 201);
  })

  // PUT /${NAME}/:id - Update
  .put("/:id", zValidator("json", update${pascal(NAME)}Schema), async (c) => {
    const id = c.req.param("id");
    const data = c.req.valid("json");

    const existing = await c.env.DB.prepare(
      "SELECT * FROM ${NAME} WHERE id = ?"
    ).bind(id).first();

    if (!existing) {
      return c.json({ error: "Not found" }, 404);
    }

    const result = await c.env.DB.prepare(
      `UPDATE ${NAME}
       SET name = COALESCE(?, name),
           description = COALESCE(?, description),
           updated_at = datetime('now')
       WHERE id = ?
       RETURNING *`
    ).bind(data.name ?? null, data.description ?? null, id).first();

    return c.json(result);
  })

  // DELETE /${NAME}/:id - Delete
  .delete("/:id", async (c) => {
    const id = c.req.param("id");

    const existing = await c.env.DB.prepare(
      "SELECT * FROM ${NAME} WHERE id = ?"
    ).bind(id).first();

    if (!existing) {
      return c.json({ error: "Not found" }, 404);
    }

    await c.env.DB.prepare(
      "DELETE FROM ${NAME} WHERE id = ?"
    ).bind(id).run();

    return c.json({ deleted: true });
  });
```

---

## Route with R2 Storage

```typescript
// src/worker/routes/${NAME}.ts
import { Hono } from "hono";
import type { Bindings } from "../lib/types";

export const ${NAME} = new Hono<{ Bindings: Bindings }>()

  // Upload file
  .put("/:key", async (c) => {
    const key = c.req.param("key");
    const contentType = c.req.header("Content-Type") || "application/octet-stream";
    const body = await c.req.arrayBuffer();

    await c.env.BUCKET.put(`${NAME}/${key}`, body, {
      httpMetadata: { contentType },
    });

    return c.json({ key, uploaded: true });
  })

  // Download file
  .get("/:key", async (c) => {
    const key = c.req.param("key");
    const object = await c.env.BUCKET.get(`${NAME}/${key}`);

    if (!object) {
      return c.json({ error: "Not found" }, 404);
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("Cache-Control", "public, max-age=31536000");

    return new Response(object.body, { headers });
  })

  // Delete file
  .delete("/:key", async (c) => {
    const key = c.req.param("key");
    await c.env.BUCKET.delete(`${NAME}/${key}`);
    return c.json({ deleted: true });
  })

  // List files
  .get("/", async (c) => {
    const prefix = c.req.query("prefix") || "";
    const { objects } = await c.env.BUCKET.list({
      prefix: `${NAME}/${prefix}`,
      limit: 100,
    });
    return c.json(objects.map((o) => ({
      key: o.key.replace(`${NAME}/`, ""),
      size: o.size,
      uploaded: o.uploaded,
    })));
  });
```

---

## Route with KV Cache

```typescript
// src/worker/routes/${NAME}.ts
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";
import type { Bindings } from "../lib/types";

const cacheSchema = z.object({
  value: z.unknown(),
  ttl: z.number().int().positive().optional(),
});

export const ${NAME} = new Hono<{ Bindings: Bindings }>()

  // Get cached value
  .get("/:key", async (c) => {
    const key = c.req.param("key");
    const value = await c.env.CACHE.get(`${NAME}:${key}`);

    if (!value) {
      return c.json({ error: "Not found" }, 404);
    }

    return c.json(JSON.parse(value));
  })

  // Set cached value
  .put("/:key", zValidator("json", cacheSchema), async (c) => {
    const key = c.req.param("key");
    const { value, ttl } = c.req.valid("json");

    await c.env.CACHE.put(
      `${NAME}:${key}`,
      JSON.stringify(value),
      ttl ? { expirationTtl: ttl } : undefined
    );

    return c.json({ cached: true });
  })

  // Delete cached value
  .delete("/:key", async (c) => {
    const key = c.req.param("key");
    await c.env.CACHE.delete(`${NAME}:${key}`);
    return c.json({ deleted: true });
  });
```

---

## Route with Authentication

```typescript
// src/worker/routes/${NAME}.ts
import { Hono } from "hono";
import { HTTPException } from "hono/http-exception";
import type { Bindings } from "../lib/types";

// Auth middleware
const requireAuth = async (c: any, next: any) => {
  const token = c.req.header("Authorization")?.replace("Bearer ", "");

  if (!token) {
    throw new HTTPException(401, { message: "Unauthorized" });
  }

  // Validate token (implement your logic)
  const user = await validateToken(token, c.env);
  if (!user) {
    throw new HTTPException(401, { message: "Invalid token" });
  }

  c.set("user", user);
  await next();
};

export const ${NAME} = new Hono<{ Bindings: Bindings }>()

  // Public route
  .get("/public", (c) => c.json({ message: "Public" }))

  // Protected routes
  .use("/*", requireAuth)

  .get("/me", (c) => {
    const user = c.get("user");
    return c.json(user);
  })

  .get("/", async (c) => {
    const user = c.get("user");
    const { results } = await c.env.DB.prepare(
      "SELECT * FROM ${NAME} WHERE user_id = ?"
    ).bind(user.id).all();
    return c.json(results);
  });
```

---

## Register Route in Worker

```typescript
// src/worker/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { ${NAME} } from "./routes/${NAME}";  // Add import
import type { Bindings } from "./lib/types";

const app = new Hono<{ Bindings: Bindings }>()
  .basePath("/api")
  .use("*", logger())
  .use("*", cors())
  .get("/health", (c) => c.json({ status: "ok" }))
  .route("/${NAME}", ${NAME});  // Add route

export default app;
```

---

## Migration for D1

```sql
-- migrations/00X_create_${NAME}.sql
CREATE TABLE IF NOT EXISTS ${NAME} (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_${NAME}_created_at ON ${NAME}(created_at);
```

---

## Client API Integration

```typescript
// src/client/lib/api.ts - Add to existing api object

export const api = {
  // ... existing

  ${NAME}: {
    list: () => request<${pascal(NAME)}[]>("/${NAME}"),
    get: (id: string) => request<${pascal(NAME)}>(`/${NAME}/${id}`),
    create: (data: Create${pascal(NAME)}) =>
      request<${pascal(NAME)}>("/${NAME}", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Update${pascal(NAME)}) =>
      request<${pascal(NAME)}>(`/${NAME}/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<{ deleted: boolean }>(`/${NAME}/${id}`, {
        method: "DELETE",
      }),
  },
};
```

---

## TypeScript Types

```typescript
// src/client/types/${NAME}.ts
export interface ${pascal(NAME)} {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface Create${pascal(NAME)} {
  name: string;
  description?: string;
}

export interface Update${pascal(NAME)} {
  name?: string;
  description?: string;
}
```

---

## Output

```
## API Route Created

**Resource**: ${NAME}
**Path**: /api/${NAME}

### Endpoints
- GET    /api/${NAME}      — List all
- GET    /api/${NAME}/:id  — Get one
- POST   /api/${NAME}      — Create
- PUT    /api/${NAME}/:id  — Update
- DELETE /api/${NAME}/:id  — Delete

### Files
- src/worker/routes/${NAME}.ts
- src/worker/index.ts (updated)
- migrations/00X_create_${NAME}.sql

### Client Usage
\`\`\`typescript
import { api } from "@/lib/api";

const items = await api.${NAME}.list();
const item = await api.${NAME}.create({ name: "Test" });
\`\`\`

### Run Migration
\`\`\`bash
npm run db:migrate:local
\`\`\`
```
