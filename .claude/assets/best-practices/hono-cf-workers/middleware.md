# Middleware Stack

## Execution Order (order matters!)

```typescript
app.use('*', requestIdMiddleware)       // 1. Assign request ID (used by all subsequent middleware)
app.use('*', structuredLogger)          // 2. Log request start, capture timing
app.use('*', secureHeaders)             // 3. Security headers on all responses
app.use('/api/*', corsMiddleware)       // 4. CORS (before auth — preflight needs to pass)
app.use('/api/*', rateLimitMiddleware)  // 5. Rate limit (before auth — reject early)
app.use('/api/*', authMiddleware)       // 6. Authentication (after CORS, before handlers)
```

## Request ID

```typescript
// src/middleware/request-id.ts
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

## CORS

```typescript
// src/middleware/cors.ts
import { cors } from 'hono/cors'

export const corsMiddleware = cors({
  origin: (origin) => {
    const allowed = ['https://app.example.com', 'https://admin.example.com']
    if (allowed.includes(origin)) return origin
    if (origin.endsWith('.example.com')) return origin
    return null
  },
  allowHeaders: ['Content-Type', 'Authorization', 'X-Request-Id'],
  allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  exposeHeaders: ['X-Request-Id', 'X-RateLimit-Remaining'],
  maxAge: 600,
  credentials: true,
})
```

**CORS Gotcha:** Register CORS middleware BEFORE route handlers. If using Vite for local dev with Cloudflare plugin, disable Vite's built-in CORS:
```typescript
export default defineConfig({ server: { cors: false } })
```

## Secure Headers

```typescript
import { secureHeaders } from 'hono/secure-headers'

export const secureHeadersMiddleware = secureHeaders({
  contentSecurityPolicy: false,
  crossOriginResourcePolicy: 'cross-origin',
  xContentTypeOptions: 'nosniff',
  xFrameOptions: 'DENY',
  referrerPolicy: 'strict-origin-when-cross-origin',
})
```

## Structured Logger

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
