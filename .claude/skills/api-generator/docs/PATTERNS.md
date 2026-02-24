# API Generator — Patterns Reference

Condensed reference from `.claude/assets/best-practices/hono-cf-workers/`.
Sub-skills MUST follow these patterns exactly when generating code.

---

## 1. Core Architecture

- **App factory pattern**: `createApp()` in `app.ts`, exported from `index.ts`
- **Routes chain methods**: `new Hono().get(...).post(...)` — NEVER use separate `app.get()` calls (breaks RPC type inference)
- **Export route types**: `export type UsersRoute = typeof users` for RPC clients
- **Export AppType**: `export type AppType = ReturnType<typeof createApp>`

---

## 2. Type-Safe Bindings

```typescript
// src/types.ts — ALWAYS create this file
export type Bindings = {
  DB: D1Database
  KV: KVNamespace
  BUCKET: R2Bucket
  RATE_LIMITER: RateLimitBinding
  ENVIRONMENT: string
  API_VERSION: string
  API_KEY: string      // wrangler secret
  JWT_SECRET: string   // wrangler secret
}

export type Variables = {
  requestId: string
  userId: string | null
  startTime: number
}

export type AppEnv = { Bindings: Bindings; Variables: Variables }
export type AppContext = Context<AppEnv>
```

---

## 3. Middleware Order (Critical)

```typescript
app.use('*', requestIdMiddleware)       // 1. Request ID first
app.use('*', structuredLogger)          // 2. Logging
app.use('*', secureHeaders)             // 3. Security headers
app.use('/api/*', corsMiddleware)       // 4. CORS before auth
app.use('/api/*', rateLimitMiddleware)  // 5. Rate limit before auth
app.use('/api/*', authMiddleware)       // 6. Auth last
```

---

## 4. Route Pattern

Routes are thin — validate, call service, return response:

```typescript
const users = new Hono<AppEnv>()
  .get('/', zValidator('query', listUsersQuerySchema), async (c) => {
    const query = c.req.valid('query')
    const result = await UserService.list(c.env.DB, query)
    return paginated(c, result)
  })
  .post('/', zValidator('json', createUserSchema), async (c) => {
    const data = c.req.valid('json')
    const user = await UserService.create(c.env.DB, data)
    return success(c, user, 201)
  })

export default users
export type UsersRoute = typeof users
```

---

## 5. Schema Pattern (Single Source of Truth)

```typescript
// schemas/common.ts
export const uuidParam = z.object({
  id: z.string().uuid('Invalid UUID format'),
})

export const paginationQuery = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
})

// schemas/{resource}.ts
export const createUserSchema = z.object({ ... })
export const updateUserSchema = createUserSchema.partial()
export const listUsersQuerySchema = paginationQuery.extend({ ... })

// Inferred types
export type CreateUser = z.infer<typeof createUserSchema>
```

**Gotchas:**
- Query params are ALWAYS strings — use `z.coerce.number()` not `z.number()`
- Header keys are lowercased by Hono — use `authorization` not `Authorization`

---

## 6. Service Pattern (Framework-Agnostic)

```typescript
export class UserService {
  static async list(d1: D1Database, query: ListUsersQuery) {
    const db = getDb(d1)
    // Business logic here — no HTTP, no Hono context
    return { data, total, page: query.page, limit: query.limit }
  }

  static async create(d1: D1Database, data: CreateUser) {
    const db = getDb(d1)
    try {
      const [user] = await db.insert(schema.users).values(data).returning()
      return user
    } catch (error: any) {
      if (error.message?.includes('UNIQUE constraint failed')) {
        throw new ConflictError(`User with email '${data.email}' already exists`)
      }
      throw error
    }
  }
}
```

---

## 7. Error Hierarchy

```typescript
AppError (base) — code, statusCode, message, details
├── NotFoundError (404)
├── UnauthorizedError (401)
├── ForbiddenError (403)
├── ConflictError (409)
└── RateLimitError (429)
```

Global error handler returns consistent JSON envelope:
```json
{ "success": false, "error": { "code": "NOT_FOUND", "message": "..." } }
```

---

## 8. Response Helpers

```typescript
export function success<T>(c: Context, data: T, status = 200) {
  return c.json({ success: true, data }, status as any)
}

export function paginated<T>(c: Context, result: {
  data: T[]; total: number; page: number; limit: number
}) {
  return c.json({
    success: true, data: result.data,
    pagination: { page: result.page, limit: result.limit,
      total: result.total, totalPages: Math.ceil(result.total / result.limit) },
  })
}
```

---

## 9. Drizzle ORM + D1

```typescript
// db/schema.ts
export const users = sqliteTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
  updatedAt: text('updated_at').notNull().default(sql`(datetime('now'))`),
})

// db/index.ts
export function getDb(d1: D1Database) {
  return drizzle(d1, { schema })
}
```

**D1 Gotchas:**
- SQLite, not Postgres — no `ALTER COLUMN`, limited JOINs
- `datetime('now')` is UTC
- 10GB per database limit

---

## 10. Auth Patterns

**API Key (constant-time comparison):**
```typescript
const encoder = new TextEncoder()
const a = encoder.encode(apiKey)
const b = encoder.encode(expected)
if (!crypto.subtle.timingSafeEqual(a, b)) throw new UnauthorizedError()
```

**JWT:**
```typescript
import { jwt } from 'hono/jwt'
export function jwtAuth() {
  return createMiddleware<AppEnv>(async (c, next) => {
    return jwt({ secret: c.env.JWT_SECRET })(c, next)
  })
}
```

---

## 11. Rate Limiting

```typescript
const { success } = await c.env.RATE_LIMITER.limit({
  key: c.req.header('x-api-key') || c.req.header('cf-connecting-ip') || 'anonymous'
})
```

- Key on API keys or user IDs, NOT just IPs
- Rate limits are per CF location, eventually consistent
- Period must be 10 or 60 seconds

---

## 12. Testing with Cloudflare Vitest Pool

```typescript
// vitest.config.ts
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config'
export default defineWorkersConfig({
  test: {
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' },
        miniflare: {
          bindings: { ENVIRONMENT: 'test', API_KEY: 'test-api-key-12345' },
        },
      },
    },
  },
})
```

Test pattern:
```typescript
const app = createApp()
const res = await app.request('/api/users', {
  headers: { 'x-api-key': 'test-api-key-12345' }
}, env)
expect(res.status).toBe(200)
```

---

## 13. Wrangler Config

- Use `wrangler.jsonc` (JSON with comments)
- `compatibility_flags: ["nodejs_compat"]` — required for Drizzle
- `observability.enabled: true` — always in production
- Bindings NOT inheritable across environments — redeclare in each `env`
- Secrets via `wrangler secret put`, NEVER in config file
- Local secrets in `.dev.vars` (git-ignored)

---

## 14. Health Check (Required)

```typescript
.get('/health', (c) => c.json({
  status: 'ok', timestamp: new Date().toISOString(),
  version: c.env.API_VERSION, environment: c.env.ENVIRONMENT,
}))
.get('/ready', async (c) => {
  try { await c.env.DB.prepare('SELECT 1').first(); return c.json({ status: 'ready' }) }
  catch { return c.json({ status: 'not_ready' }, 503) }
})
```

---

## 15. Structured Logging

Always JSON — Workers Logs auto-indexes fields:
```typescript
console.log(JSON.stringify({
  level: 'info', method: c.req.method, path: c.req.path,
  status: c.res.status, duration_ms: Date.now() - start,
  request_id: c.get('requestId'), user_id: c.get('userId'),
}))
```

---

## 16. Dependencies

```json
{
  "dependencies": {
    "hono": "^4.7.0",
    "@hono/zod-validator": "^0.5.0",
    "zod": "^3.24.0",
    "drizzle-orm": "^0.38.0"
  },
  "devDependencies": {
    "@cloudflare/vitest-pool-workers": "^0.9.0",
    "@cloudflare/workers-types": "^4.20250401.0",
    "drizzle-kit": "^0.30.0",
    "vitest": "^3.0.0",
    "wrangler": "^4.0.0",
    "typescript": "^5.7.0"
  }
}
```
