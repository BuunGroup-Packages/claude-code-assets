# Generate Middleware Stack

Generate the full middleware stack following the critical execution order.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
.claude/assets/best-practices/hono-cf-workers/middleware.md
```

## Workflow

1. Generate request-id middleware
2. Generate structured logger middleware
3. Generate CORS middleware
4. Generate rate-limit middleware
5. Generate auth middleware (based on AUTH_STRATEGY)
6. Update app.ts to mount all middleware in correct order

## CRITICAL: Middleware Execution Order

The order in `app.ts` MUST be:

```typescript
app.use('*', requestIdMiddleware)       // 1. First — used by all subsequent
app.use('*', structuredLogger)          // 2. Timing + log
app.use('/api/*', corsMiddleware)       // 3. Before auth — preflight must pass
app.use('/api/*', rateLimitMiddleware)  // 4. Before auth — reject early
app.use('/api/*', authMiddleware)       // 5. Last — after CORS and rate limit
```

## File Templates

### src/middleware/request-id.ts

```typescript
import { createMiddleware } from 'hono/factory'
import type { AppEnv } from '../types'

export const requestIdMiddleware = createMiddleware<AppEnv>(async (c, next) => {
  const requestId = c.req.header('x-request-id') || crypto.randomUUID()
  c.set('requestId', requestId)
  c.set('startTime', Date.now())
  await next()
  c.header('X-Request-Id', requestId)
})
```

### src/middleware/logger.ts

```typescript
import { createMiddleware } from 'hono/factory'
import type { AppEnv } from '../types'

export const structuredLogger = createMiddleware<AppEnv>(async (c, next) => {
  const start = Date.now()
  await next()
  const duration = Date.now() - start

  console.log(JSON.stringify({
    level: c.res.status >= 500 ? 'error' : c.res.status >= 400 ? 'warn' : 'info',
    method: c.req.method,
    path: c.req.path,
    status: c.res.status,
    duration_ms: duration,
    request_id: c.get('requestId'),
    user_id: c.get('userId'),
    user_agent: c.req.header('user-agent'),
    cf_ray: c.req.header('cf-ray'),
  }))
})
```

### src/middleware/cors.ts

```typescript
import { cors } from 'hono/cors'

export const corsMiddleware = cors({
  origin: (origin) => {
    const allowed = [
      // Replace with actual origins from plan
      'https://app.example.com',
      'https://admin.example.com',
    ]
    if (allowed.includes(origin)) return origin
    // Allow subdomains
    if (origin.endsWith('.example.com')) return origin
    // Allow localhost in development
    if (origin.startsWith('http://localhost:')) return origin
    return null
  },
  allowHeaders: ['Content-Type', 'Authorization', 'X-API-Key', 'X-Request-Id'],
  allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  exposeHeaders: ['X-Request-Id', 'X-RateLimit-Remaining'],
  maxAge: 600,
  credentials: true,
})
```

### src/middleware/rate-limit.ts

```typescript
import { createMiddleware } from 'hono/factory'
import type { AppEnv } from '../types'

export const rateLimitMiddleware = createMiddleware<AppEnv>(async (c, next) => {
  const key = c.req.header('x-api-key')
    || c.req.header('cf-connecting-ip')
    || 'anonymous'

  const { success } = await c.env.RATE_LIMITER.limit({ key })

  if (!success) {
    return c.json({
      success: false,
      error: { code: 'RATE_LIMITED', message: 'Too many requests. Please try again later.' },
    }, 429)
  }

  await next()
})

export const strictRateLimit = createMiddleware<AppEnv>(async (c, next) => {
  const key = c.req.header('cf-connecting-ip') || 'anonymous'
  const { success } = await c.env.RATE_LIMITER_STRICT.limit({ key })

  if (!success) {
    return c.json({
      success: false,
      error: { code: 'RATE_LIMITED', message: 'Too many requests' },
    }, 429)
  }
  await next()
})
```

Only generate rate-limit middleware if the plan includes rate limiter bindings.
If no rate limiter bindings, skip this file entirely.

### src/middleware/auth.ts — API Key Strategy

```typescript
import { createMiddleware } from 'hono/factory'
import type { AppEnv } from '../types'
import { UnauthorizedError } from '../lib/errors'

export const authMiddleware = createMiddleware<AppEnv>(async (c, next) => {
  const apiKey = c.req.header('x-api-key')
    || c.req.header('authorization')?.replace('Bearer ', '')

  if (!apiKey) {
    throw new UnauthorizedError('Missing API key')
  }

  const expected = c.env.API_KEY
  const encoder = new TextEncoder()
  const a = encoder.encode(apiKey)
  const b = encoder.encode(expected)

  if (a.byteLength !== b.byteLength || !crypto.subtle.timingSafeEqual(a, b)) {
    throw new UnauthorizedError('Invalid API key')
  }

  await next()
})
```

### src/middleware/auth.ts — JWT Strategy

```typescript
import { createMiddleware } from 'hono/factory'
import { jwt } from 'hono/jwt'
import type { AppEnv } from '../types'

export const authMiddleware = createMiddleware<AppEnv>(async (c, next) => {
  const jwtMiddleware = jwt({ secret: c.env.JWT_SECRET })
  return jwtMiddleware(c, next)
})

export const optionalAuth = createMiddleware<AppEnv>(async (c, next) => {
  const token = c.req.header('authorization')?.replace('Bearer ', '')
  if (token) {
    try {
      const jwtMiddleware = jwt({ secret: c.env.JWT_SECRET })
      await jwtMiddleware(c, async () => {})
      const payload = c.get('jwtPayload' as any)
      c.set('userId', payload?.sub || null)
    } catch {
      c.set('userId', null)
    }
  } else {
    c.set('userId', null)
  }
  await next()
})
```

Choose the auth strategy based on the plan. If "Both", generate both API key
and JWT middleware and let the plan dictate which endpoints use which.

### Update app.ts

After generating all middleware, update `src/app.ts` to import and mount them:

```typescript
import { Hono } from 'hono'
import type { AppEnv } from './types'
import { requestIdMiddleware } from './middleware/request-id'
import { structuredLogger } from './middleware/logger'
import { corsMiddleware } from './middleware/cors'
import { rateLimitMiddleware } from './middleware/rate-limit'
import { authMiddleware } from './middleware/auth'
import { errorHandler } from './middleware/error-handler'
import { routes } from './routes'

export function createApp() {
  const app = new Hono<AppEnv>()

  // Middleware (order is critical!)
  app.use('*', requestIdMiddleware)
  app.use('*', structuredLogger)
  app.use('/api/*', corsMiddleware)
  app.use('/api/*', rateLimitMiddleware)
  app.use('/api/*', authMiddleware)

  // Error handler
  app.onError(errorHandler)

  // 404
  app.notFound((c) => {
    return c.json({
      success: false,
      error: { code: 'NOT_FOUND', message: `Route not found: ${c.req.method} ${c.req.path}` },
    }, 404)
  })

  // Routes
  app.route('/api', routes)

  return app
}

export type AppType = ReturnType<typeof createApp>
```

## Output

```
## Middleware Generated

| Order | Middleware | Scope | File |
|-------|-----------|-------|------|
| 1 | request-id | * | middleware/request-id.ts |
| 2 | structured-logger | * | middleware/logger.ts |
| 3 | cors | /api/* | middleware/cors.ts |
| 4 | rate-limit | /api/* | middleware/rate-limit.ts |
| 5 | auth ({strategy}) | /api/* | middleware/auth.ts |

### Updated
- app.ts — Middleware mounted in correct order
```
