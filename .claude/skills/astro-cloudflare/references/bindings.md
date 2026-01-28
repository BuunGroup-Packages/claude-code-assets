# Cloudflare Bindings Reference

## wrangler.jsonc Configuration

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-app",
  "compatibility_date": "2026-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "main": "./dist/_worker.js/index.js",
  "assets": {
    "binding": "ASSETS",
    "directory": "./dist"
  },

  // D1 Database
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ],

  // R2 Storage
  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "my-bucket"
    }
  ],

  // KV Namespace
  "kv_namespaces": [
    {
      "binding": "CACHE",
      "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  ]
}
```

## D1 Database

### CLI Commands

```bash
# Create database
wrangler d1 create my-db

# Run migration
wrangler d1 execute my-db --file=./migrations/0001.sql

# Query locally
wrangler d1 execute my-db --local --command="SELECT * FROM users"
```

### Usage in Hono

```typescript
app.get("/users", async (c) => {
  const { results } = await c.env.DB.prepare(
    "SELECT * FROM users"
  ).all();
  return c.json(results);
});

app.get("/users/:id", async (c) => {
  const user = await c.env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  ).bind(c.req.param("id")).first();
  return c.json(user);
});

app.post("/users", async (c) => {
  const { name, email } = await c.req.json();
  const result = await c.env.DB.prepare(
    "INSERT INTO users (name, email) VALUES (?, ?) RETURNING *"
  ).bind(name, email).first();
  return c.json(result, 201);
});
```

### Batch Operations

```typescript
const batch = [
  c.env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Alice"),
  c.env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Bob"),
];
await c.env.DB.batch(batch);
```

## R2 Storage

### CLI Commands

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Upload file
wrangler r2 object put my-bucket/file.txt --file=./file.txt
```

### Usage in Hono

```typescript
// Upload
app.put("/files/:key", async (c) => {
  const key = c.req.param("key");
  const body = await c.req.arrayBuffer();
  const contentType = c.req.header("Content-Type");

  await c.env.BUCKET.put(key, body, {
    httpMetadata: { contentType },
  });

  return c.json({ success: true });
});

// Download
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

// List
app.get("/files", async (c) => {
  const prefix = c.req.query("prefix");
  const { objects } = await c.env.BUCKET.list({ prefix });
  return c.json(objects.map((o) => o.key));
});

// Delete
app.delete("/files/:key", async (c) => {
  await c.env.BUCKET.delete(c.req.param("key"));
  return c.json({ success: true });
});
```

## KV Namespace

### CLI Commands

```bash
# Create namespace
wrangler kv namespace create CACHE

# Write value
wrangler kv key put --namespace-id=xxx "key" "value"

# Read value
wrangler kv key get --namespace-id=xxx "key"
```

### Usage in Hono

```typescript
// Get
app.get("/cache/:key", async (c) => {
  const value = await c.env.CACHE.get(c.req.param("key"));
  if (!value) return c.json({ error: "Not found" }, 404);
  return c.json(JSON.parse(value));
});

// Set with TTL
app.put("/cache/:key", async (c) => {
  const key = c.req.param("key");
  const value = await c.req.json();
  const ttl = parseInt(c.req.query("ttl") || "3600");

  await c.env.CACHE.put(key, JSON.stringify(value), {
    expirationTtl: ttl,
  });

  return c.json({ success: true });
});

// Delete
app.delete("/cache/:key", async (c) => {
  await c.env.CACHE.delete(c.req.param("key"));
  return c.json({ success: true });
});

// List keys
app.get("/cache", async (c) => {
  const prefix = c.req.query("prefix");
  const { keys } = await c.env.CACHE.list({ prefix });
  return c.json(keys.map((k) => k.name));
});
```

## Type Definitions

```typescript
// functions/_lib/types.ts
import type {
  D1Database,
  R2Bucket,
  KVNamespace,
} from "@cloudflare/workers-types";

export type Bindings = {
  DB: D1Database;
  BUCKET: R2Bucket;
  CACHE: KVNamespace;
  ASSETS: Fetcher;
};
```

## Access in Astro

```typescript
// In .astro files or API routes
import { env } from "cloudflare:workers";

const db = env.DB;
const bucket = env.BUCKET;
const cache = env.CACHE;
```
