# Type-Safe Bindings & Environment

```typescript
// src/types.ts
import type { Context } from 'hono'

export type Bindings = {
  DB: D1Database
  KV: KVNamespace
  BUCKET: R2Bucket
  RATE_LIMITER: RateLimitBinding
  RATE_LIMITER_STRICT: RateLimitBinding
  ENVIRONMENT: string
  API_VERSION: string
  LOG_LEVEL: string
  API_KEY: string        // Set via `wrangler secret put`
  JWT_SECRET: string     // Set via `wrangler secret put`
}

export interface RateLimitBinding {
  limit(options: { key: string }): Promise<{ success: boolean }>
}

export type Variables = {
  requestId: string
  userId: string | null
  startTime: number
}

export type AppEnv = {
  Bindings: Bindings
  Variables: Variables
}

export type AppContext = Context<AppEnv>
```

## Why This Matters

- Every `c.env.DB`, `c.env.API_KEY`, `c.get('userId')` is fully typed
- TypeScript catches missing bindings at compile time, not at runtime in production
- Single source of truth — change the type here, see errors everywhere
