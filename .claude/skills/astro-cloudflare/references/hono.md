# Hono API Reference

> **Note**: Astro 6 recommends using **Astro Actions** for type-safe backend calls. Use Hono only when you need:
> - Custom middleware patterns
> - OpenAPI documentation
> - Complex routing logic
> - Integration with external Hono services

## When to Use What

| Use Case | Recommended |
|----------|-------------|
| Type-safe backend calls | Astro Actions |
| Form handling | Astro Actions |
| CRUD operations | Astro Actions |
| Webhooks | API Endpoints |
| External API integration | Hono or API Endpoints |
| Complex middleware | Hono |
| OpenAPI/Swagger | Hono |

## Hono with Astro 6

If you need Hono, create it as an API endpoint:

```typescript
// src/pages/api/[...path].ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

type Bindings = {
  DB: D1Database;
  BUCKET: R2Bucket;
  CACHE: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>()
  .basePath("/api")
  .use("*", logger())
  .use("*", cors())
  .get("/health", (c) => c.json({ status: "ok" }));

export const prerender = false;

export const ALL: APIRoute = async ({ request }) => {
  // Pass bindings from Astro 6 env
  return app.fetch(request, env);
};
```

## Hono Patterns

### Basic Routes

```typescript
const app = new Hono()
  .get("/users", (c) => c.json([]))
  .get("/users/:id", (c) => {
    const id = c.req.param("id");
    return c.json({ id });
  })
  .post("/users", async (c) => {
    const body = await c.req.json();
    return c.json(body, 201);
  })
  .delete("/users/:id", (c) => {
    return c.json({ deleted: true });
  });
```

### Validation with Zod

```typescript
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

app.post(
  "/users",
  zValidator("json", createUserSchema),
  async (c) => {
    const data = c.req.valid("json");
    return c.json(data, 201);
  }
);
```

### Middleware

```typescript
import { createMiddleware } from "hono/factory";

const authMiddleware = createMiddleware(async (c, next) => {
  const token = c.req.header("Authorization")?.replace("Bearer ", "");

  if (!token) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  // Validate token...
  c.set("userId", "user-id-from-token");
  await next();
});

app.use("/api/protected/*", authMiddleware);
```

### Error Handling

```typescript
import { HTTPException } from "hono/http-exception";

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  return c.json({ error: "Internal Server Error" }, 500);
});

// Throw errors
app.get("/error", () => {
  throw new HTTPException(404, { message: "Not Found" });
});
```

### RPC Client (Type-safe)

```typescript
// Define API
const app = new Hono()
  .get("/users", (c) => c.json([{ id: "1", name: "Alice" }]))
  .post("/users", async (c) => {
    const body = await c.req.json<{ name: string }>();
    return c.json({ id: "2", name: body.name }, 201);
  });

export type AppType = typeof app;

// Client usage
import { hc } from "hono/client";
import type { AppType } from "./api";

const client = hc<AppType>("http://localhost:4321");

const res = await client.users.$get();
const users = await res.json();
```

## D1 Integration

```typescript
app.get("/users", async (c) => {
  const { results } = await c.env.DB.prepare(
    "SELECT * FROM users"
  ).all();
  return c.json(results);
});

app.post("/users", async (c) => {
  const { name, email } = await c.req.json();
  const result = await c.env.DB.prepare(
    "INSERT INTO users (name, email) VALUES (?, ?) RETURNING *"
  ).bind(name, email).first();
  return c.json(result, 201);
});
```

## R2 Integration

```typescript
app.put("/files/:key", async (c) => {
  const key = c.req.param("key");
  const body = await c.req.arrayBuffer();
  const contentType = c.req.header("Content-Type");

  await c.env.BUCKET.put(key, body, {
    httpMetadata: { contentType },
  });

  return c.json({ success: true });
});

app.get("/files/:key", async (c) => {
  const key = c.req.param("key");
  const object = await c.env.BUCKET.get(key);

  if (!object) {
    return c.json({ error: "Not found" }, 404);
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);

  return new Response(object.body, { headers });
});
```

## KV Integration

```typescript
app.get("/cache/:key", async (c) => {
  const value = await c.env.CACHE.get(c.req.param("key"));
  if (!value) return c.json({ error: "Not found" }, 404);
  return c.json(JSON.parse(value));
});

app.put("/cache/:key", async (c) => {
  const key = c.req.param("key");
  const value = await c.req.json();
  const ttl = parseInt(c.req.query("ttl") || "3600");

  await c.env.CACHE.put(key, JSON.stringify(value), {
    expirationTtl: ttl,
  });

  return c.json({ success: true });
});
```

## References

- [Hono Documentation](https://hono.dev/)
- [Hono Cloudflare Workers](https://hono.dev/getting-started/cloudflare-workers)
- [Hono RPC](https://hono.dev/guides/rpc)
