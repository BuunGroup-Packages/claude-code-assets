---
name: vite-cloudflare:binding
model: haiku
description: |
  Configure Cloudflare D1, R2, or KV bindings in wrangler.jsonc.
  Creates helper files and TypeScript types.
argument-hint: "<type> <name>"
---

# Add Cloudflare Binding

## Variables

TYPE: $1 (required: d1, r2, kv)
NAME: $2 (required: binding name, e.g., DB, BUCKET, CACHE)

## Workflow

1. Update wrangler.jsonc with binding
2. Update src/worker/lib/types.ts
3. Create helper file
4. Output CLI commands

---

## D1 Database

### wrangler.jsonc

```jsonc
{
  "d1_databases": [
    {
      "binding": "${NAME}",
      "database_name": "my-database",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

### Helper: src/worker/lib/db.ts

```typescript
// src/worker/lib/db.ts

export async function query<T>(
  db: D1Database,
  sql: string,
  params: unknown[] = []
): Promise<T[]> {
  const stmt = db.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  const { results } = await bound.all();
  return results as T[];
}

export async function queryOne<T>(
  db: D1Database,
  sql: string,
  params: unknown[] = []
): Promise<T | null> {
  const stmt = db.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  return (await bound.first()) as T | null;
}

export async function execute(
  db: D1Database,
  sql: string,
  params: unknown[] = []
): Promise<D1Result> {
  const stmt = db.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  return bound.run();
}

export async function batch(
  db: D1Database,
  statements: { sql: string; params?: unknown[] }[]
): Promise<D1Result[]> {
  const prepared = statements.map(({ sql, params = [] }) => {
    const stmt = db.prepare(sql);
    return params.length ? stmt.bind(...params) : stmt;
  });
  return db.batch(prepared);
}
```

### Usage in Hono Route

```typescript
import { query, queryOne } from "../lib/db";

app.get("/users", async (c) => {
  const users = await query(c.env.DB, "SELECT * FROM users");
  return c.json(users);
});

app.get("/users/:id", async (c) => {
  const user = await queryOne(
    c.env.DB,
    "SELECT * FROM users WHERE id = ?",
    [c.req.param("id")]
  );
  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});
```

### Migration Template

```sql
-- migrations/001_init.sql
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

### CLI Commands

```bash
# Create database
wrangler d1 create my-database

# Run migration locally
wrangler d1 execute ${NAME} --local --file=./migrations/001_init.sql

# Run migration in production
wrangler d1 execute ${NAME} --file=./migrations/001_init.sql

# Query database
wrangler d1 execute ${NAME} --local --command="SELECT * FROM users"
```

---

## R2 Storage

### wrangler.jsonc

```jsonc
{
  "r2_buckets": [
    {
      "binding": "${NAME}",
      "bucket_name": "my-bucket"
    }
  ]
}
```

### Helper: src/worker/lib/storage.ts

```typescript
// src/worker/lib/storage.ts

export async function upload(
  bucket: R2Bucket,
  key: string,
  data: ArrayBuffer | ReadableStream | string,
  contentType?: string
): Promise<R2Object> {
  return bucket.put(key, data, {
    httpMetadata: contentType ? { contentType } : undefined,
  });
}

export async function download(
  bucket: R2Bucket,
  key: string
): Promise<{ data: ReadableStream; contentType?: string } | null> {
  const object = await bucket.get(key);
  if (!object) return null;

  return {
    data: object.body,
    contentType: object.httpMetadata?.contentType,
  };
}

export async function remove(bucket: R2Bucket, key: string): Promise<void> {
  await bucket.delete(key);
}

export async function list(
  bucket: R2Bucket,
  prefix?: string,
  limit = 100
): Promise<{ key: string; size: number }[]> {
  const { objects } = await bucket.list({ prefix, limit });
  return objects.map((o) => ({ key: o.key, size: o.size }));
}

export async function exists(bucket: R2Bucket, key: string): Promise<boolean> {
  const object = await bucket.head(key);
  return object !== null;
}

export function getSignedUrl(key: string, baseUrl: string): string {
  return `${baseUrl}/api/files/${encodeURIComponent(key)}`;
}
```

### Usage in Hono Route

```typescript
import { upload, download, remove, list } from "../lib/storage";

app.put("/files/:key", async (c) => {
  const key = c.req.param("key");
  const body = await c.req.arrayBuffer();
  const contentType = c.req.header("Content-Type");

  await upload(c.env.BUCKET, key, body, contentType);
  return c.json({ key, uploaded: true });
});

app.get("/files/:key", async (c) => {
  const key = c.req.param("key");
  const result = await download(c.env.BUCKET, key);

  if (!result) return c.json({ error: "Not found" }, 404);

  return new Response(result.data, {
    headers: {
      "Content-Type": result.contentType || "application/octet-stream",
      "Cache-Control": "public, max-age=31536000",
    },
  });
});

app.get("/files", async (c) => {
  const prefix = c.req.query("prefix");
  const files = await list(c.env.BUCKET, prefix);
  return c.json(files);
});
```

### CLI Commands

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Upload file
wrangler r2 object put my-bucket/test.txt --file=./test.txt

# List objects
wrangler r2 object list my-bucket
```

---

## KV Namespace

### wrangler.jsonc

```jsonc
{
  "kv_namespaces": [
    {
      "binding": "${NAME}",
      "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  ]
}
```

### Helper: src/worker/lib/cache.ts

```typescript
// src/worker/lib/cache.ts

export async function get<T>(kv: KVNamespace, key: string): Promise<T | null> {
  const value = await kv.get(key);
  if (!value) return null;
  return JSON.parse(value) as T;
}

export async function set<T>(
  kv: KVNamespace,
  key: string,
  value: T,
  ttlSeconds?: number
): Promise<void> {
  await kv.put(key, JSON.stringify(value), {
    expirationTtl: ttlSeconds,
  });
}

export async function del(kv: KVNamespace, key: string): Promise<void> {
  await kv.delete(key);
}

export async function keys(
  kv: KVNamespace,
  prefix?: string
): Promise<string[]> {
  const { keys } = await kv.list({ prefix });
  return keys.map((k) => k.name);
}

export async function cached<T>(
  kv: KVNamespace,
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds = 3600
): Promise<T> {
  const existing = await get<T>(kv, key);
  if (existing !== null) return existing;

  const fresh = await fetcher();
  await set(kv, key, fresh, ttlSeconds);
  return fresh;
}
```

### Usage in Hono Route

```typescript
import { get, set, del, cached } from "../lib/cache";

app.get("/cache/:key", async (c) => {
  const value = await get(c.env.CACHE, c.req.param("key"));
  if (!value) return c.json({ error: "Not found" }, 404);
  return c.json(value);
});

app.put("/cache/:key", async (c) => {
  const key = c.req.param("key");
  const value = await c.req.json();
  const ttl = parseInt(c.req.query("ttl") || "3600");

  await set(c.env.CACHE, key, value, ttl);
  return c.json({ cached: true });
});

// Cache-aside pattern
app.get("/users/:id", async (c) => {
  const id = c.req.param("id");

  const user = await cached(
    c.env.CACHE,
    `user:${id}`,
    async () => {
      const result = await c.env.DB.prepare(
        "SELECT * FROM users WHERE id = ?"
      ).bind(id).first();
      return result;
    },
    300 // 5 minutes
  );

  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});
```

### CLI Commands

```bash
# Create namespace
wrangler kv namespace create ${NAME}

# Write value
wrangler kv key put --namespace-id=xxx "key" "value"

# Read value
wrangler kv key get --namespace-id=xxx "key"

# List keys
wrangler kv key list --namespace-id=xxx
```

---

## Update Types

```typescript
// src/worker/lib/types.ts
export type Bindings = {
  DB: D1Database;      // Add if d1
  BUCKET: R2Bucket;    // Add if r2
  CACHE: KVNamespace;  // Add if kv
  ASSETS: Fetcher;
};
```

---

## Generate Types

```bash
# Generate TypeScript types from wrangler.jsonc
wrangler types
```

---

## Output

```
## Binding Added

**Type**: ${TYPE.toUpperCase()}
**Name**: ${NAME}

### Files Modified
- wrangler.jsonc
- src/worker/lib/types.ts
- src/worker/lib/${TYPE === 'd1' ? 'db' : TYPE === 'r2' ? 'storage' : 'cache'}.ts

### Create Resource
\`\`\`bash
${TYPE === 'd1' ? 'wrangler d1 create my-database' : ''}
${TYPE === 'r2' ? 'wrangler r2 bucket create my-bucket' : ''}
${TYPE === 'kv' ? `wrangler kv namespace create ${NAME}` : ''}
\`\`\`

### Update wrangler.jsonc
Copy the ID from CLI output into wrangler.jsonc

### Generate Types
\`\`\`bash
wrangler types
\`\`\`
```
