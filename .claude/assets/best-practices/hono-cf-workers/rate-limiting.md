# Rate Limiting

## Native Cloudflare Rate Limiting

```typescript
// src/middleware/rate-limit.ts
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
    return c.json({ success: false, error: { code: 'RATE_LIMITED', message: 'Too many requests' } }, 429)
  }
  await next()
})
```

## Using `@elithrar/workers-hono-rate-limit`

```typescript
import { rateLimit, RateLimitBinding, RateLimitKeyFunc } from '@elithrar/workers-hono-rate-limit'

const getKey: RateLimitKeyFunc = (c) => c.req.header('authorization') || ''
app.use('/api/*', (c, next) => rateLimit(c.env.RATE_LIMITER, getKey)(c, next))
```

## Best Practices

- Key on API keys, user IDs, or tenant IDs — NOT IP addresses (shared by many users)
- Rate limits are per Cloudflare location, eventually consistent (not exact counters)
- Use separate limiters for different tiers (free/paid) and sensitivity levels (login vs. read)
- Period must be 10 or 60 seconds
