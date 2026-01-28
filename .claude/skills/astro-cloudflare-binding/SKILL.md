---
name: astro-cloudflare:binding
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

## Astro 6 Environment Access

```typescript
// NEW in Astro 6 - use cloudflare:workers
import { env } from "cloudflare:workers";

const db = env.DB;        // D1Database
const bucket = env.BUCKET; // R2Bucket
const cache = env.CACHE;   // KVNamespace
```

## Workflow

1. Parse TYPE and NAME
2. Update wrangler.jsonc with binding config
3. Update website.config.ts features
4. Create helper file in src/lib/
5. Output CLI commands to create resource

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

### Helper: src/lib/db.ts

```typescript
import { env } from "cloudflare:workers";

export const db = () => env.${NAME};

// Query helpers
export async function query<T>(
  sql: string,
  params: unknown[] = []
): Promise<T[]> {
  const stmt = env.${NAME}.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  const { results } = await bound.all();
  return results as T[];
}

export async function queryOne<T>(
  sql: string,
  params: unknown[] = []
): Promise<T | null> {
  const stmt = env.${NAME}.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  return await bound.first() as T | null;
}

export async function execute(
  sql: string,
  params: unknown[] = []
): Promise<void> {
  const stmt = env.${NAME}.prepare(sql);
  const bound = params.length ? stmt.bind(...params) : stmt;
  await bound.run();
}

export async function batch(
  statements: { sql: string; params?: unknown[] }[]
): Promise<void> {
  const prepared = statements.map(({ sql, params = [] }) => {
    const stmt = env.${NAME}.prepare(sql);
    return params.length ? stmt.bind(...params) : stmt;
  });
  await env.${NAME}.batch(prepared);
}
```

### Migration: migrations/001_init.sql

```sql
-- Create initial tables
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
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

### Helper: src/lib/storage.ts

```typescript
import { env } from "cloudflare:workers";

export const bucket = () => env.${NAME};

// Upload file
export async function upload(
  key: string,
  data: ArrayBuffer | ReadableStream | string,
  contentType?: string
): Promise<void> {
  await env.${NAME}.put(key, data, {
    httpMetadata: contentType ? { contentType } : undefined,
  });
}

// Download file
export async function download(key: string): Promise<{
  data: ReadableStream | null;
  contentType: string | undefined;
} | null> {
  const object = await env.${NAME}.get(key);
  if (!object) return null;

  return {
    data: object.body,
    contentType: object.httpMetadata?.contentType,
  };
}

// Delete file
export async function remove(key: string): Promise<void> {
  await env.${NAME}.delete(key);
}

// List files
export async function list(
  prefix?: string,
  limit = 100
): Promise<string[]> {
  const { objects } = await env.${NAME}.list({ prefix, limit });
  return objects.map((o) => o.key);
}

// Check if exists
export async function exists(key: string): Promise<boolean> {
  const object = await env.${NAME}.head(key);
  return object !== null;
}

// Get signed URL (for public access)
export function getPublicUrl(key: string, baseUrl: string): string {
  return `${baseUrl}/api/files/${encodeURIComponent(key)}`;
}
```

### File API Endpoint

```typescript
// src/pages/api/files/[...path].ts
import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

export const GET: APIRoute = async ({ params }) => {
  const path = params.path;
  if (!path) {
    return new Response("Path required", { status: 400 });
  }

  const object = await env.${NAME}.get(path);
  if (!object) {
    return new Response("Not found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("Cache-Control", "public, max-age=31536000");

  return new Response(object.body, { headers });
};

export const PUT: APIRoute = async ({ params, request }) => {
  const path = params.path;
  if (!path) {
    return new Response("Path required", { status: 400 });
  }

  const contentType = request.headers.get("Content-Type");
  const body = await request.arrayBuffer();

  await env.${NAME}.put(path, body, {
    httpMetadata: contentType ? { contentType } : undefined,
  });

  return new Response(JSON.stringify({ key: path }), {
    headers: { "Content-Type": "application/json" },
  });
};

export const DELETE: APIRoute = async ({ params }) => {
  const path = params.path;
  if (!path) {
    return new Response("Path required", { status: 400 });
  }

  await env.${NAME}.delete(path);
  return new Response(null, { status: 204 });
};
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

### Helper: src/lib/cache.ts

```typescript
import { env } from "cloudflare:workers";

export const kv = () => env.${NAME};

// Get value
export async function get<T>(key: string): Promise<T | null> {
  const value = await env.${NAME}.get(key);
  if (!value) return null;
  return JSON.parse(value) as T;
}

// Set value with optional TTL
export async function set<T>(
  key: string,
  value: T,
  ttlSeconds?: number
): Promise<void> {
  await env.${NAME}.put(key, JSON.stringify(value), {
    expirationTtl: ttlSeconds,
  });
}

// Delete value
export async function del(key: string): Promise<void> {
  await env.${NAME}.delete(key);
}

// List keys
export async function keys(prefix?: string): Promise<string[]> {
  const { keys } = await env.${NAME}.list({ prefix });
  return keys.map((k) => k.name);
}

// Cache-aside pattern
export async function cached<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds = 3600
): Promise<T> {
  const existing = await get<T>(key);
  if (existing !== null) return existing;

  const fresh = await fetcher();
  await set(key, fresh, ttlSeconds);
  return fresh;
}

// Invalidate by prefix
export async function invalidatePrefix(prefix: string): Promise<void> {
  const allKeys = await keys(prefix);
  await Promise.all(allKeys.map((k) => del(k)));
}
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

## Update website.config.ts

```typescript
export const config = {
  // ... existing config
  features: {
    d1: ${TYPE === 'd1'},
    r2: ${TYPE === 'r2'},
    kv: ${TYPE === 'kv'},
  },
} as const;
```

## Generate Types

```bash
# Generate TypeScript types from wrangler.jsonc
wrangler types

# This creates worker-configuration.d.ts with binding types
```

## Output

```
## Binding Added

**Type**: ${TYPE.toUpperCase()}
**Name**: ${NAME}

### Files Modified
- wrangler.jsonc (binding config)
- website.config.ts (feature flag)
- src/lib/${TYPE === 'd1' ? 'db' : TYPE === 'r2' ? 'storage' : 'cache'}.ts (helper)

### Create Resource
\`\`\`bash
${TYPE === 'd1' ? `wrangler d1 create my-database` : ''}
${TYPE === 'r2' ? `wrangler r2 bucket create my-bucket` : ''}
${TYPE === 'kv' ? `wrangler kv namespace create ${NAME}` : ''}
\`\`\`

### Update wrangler.jsonc
Copy the ID from the CLI output into wrangler.jsonc

### Generate Types
\`\`\`bash
wrangler types
\`\`\`
```
