# Authentication & Security

## API Key Auth

```typescript
// src/middleware/auth.ts
import { createMiddleware } from 'hono/factory'
import type { AppEnv } from '../types'
import { UnauthorizedError } from '../lib/errors'

export const apiKeyAuth = createMiddleware<AppEnv>(async (c, next) => {
  const apiKey = c.req.header('x-api-key') || c.req.header('authorization')?.replace('Bearer ', '')
  if (!apiKey) throw new UnauthorizedError('Missing API key')

  // Constant-time comparison to prevent timing attacks
  const expected = c.env.API_KEY
  if (apiKey.length !== expected.length) throw new UnauthorizedError('Invalid API key')

  const encoder = new TextEncoder()
  const a = encoder.encode(apiKey)
  const b = encoder.encode(expected)
  if (!crypto.subtle.timingSafeEqual(a, b)) throw new UnauthorizedError('Invalid API key')

  await next()
})
```

## JWT Auth

```typescript
import { jwt } from 'hono/jwt'

export function jwtAuth() {
  return createMiddleware<AppEnv>(async (c, next) => {
    const jwtMiddleware = jwt({ secret: c.env.JWT_SECRET })
    return jwtMiddleware(c, next)
  })
}
```

## Optional Auth

```typescript
export const optionalAuth = createMiddleware<AppEnv>(async (c, next) => {
  const token = c.req.header('authorization')?.replace('Bearer ', '')
  if (token) {
    try {
      const payload = await verifyJWT(token, c.env.JWT_SECRET)
      c.set('userId', payload.sub)
    } catch {
      c.set('userId', null)
    }
  } else {
    c.set('userId', null)
  }
  await next()
})
```

## Security Rules

- Never log secrets: `console.log(\`Auth present: ${!!c.req.header('authorization')}\`)`
- Use `wrangler secret put` for sensitive values, not `vars`
- HTTPS is enforced by default on Cloudflare
- Use `c.env.MY_SECRET`, not `process.env` (not available in Workers by default)
