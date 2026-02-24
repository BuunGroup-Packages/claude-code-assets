# Route Architecture

## App Factory

```typescript
// src/app.ts
import { Hono } from 'hono'
import type { AppEnv } from './types'
import { corsMiddleware } from './middleware/cors'
import { errorHandler } from './middleware/error-handler'
import { requestIdMiddleware } from './middleware/request-id'
import { structuredLogger } from './middleware/logger'
import { routes } from './routes'

export function createApp() {
  const app = new Hono<AppEnv>()

  app.use('*', requestIdMiddleware)
  app.use('*', structuredLogger)
  app.use('/api/*', corsMiddleware)
  app.onError(errorHandler)

  app.notFound((c) => {
    return c.json(
      {
        success: false,
        error: { code: 'NOT_FOUND', message: `Route not found: ${c.req.method} ${c.req.path}` },
      },
      404
    )
  })

  app.route('/api', routes)
  return app
}

export type AppType = ReturnType<typeof createApp>
```

## Entry Point

```typescript
// src/index.ts
import { createApp } from './app'

const app = createApp()
export default app
export type { AppType } from './app'
```

## Route Modules (chain, don't use controllers)

```typescript
// src/routes/users.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import type { AppEnv } from '../types'
import { createUserSchema, updateUserSchema, listUsersQuerySchema } from '../schemas/users'
import { UserService } from '../services/user.service'
import { success, paginated } from '../lib/response'

// IMPORTANT: Chain methods for RPC type inference
const users = new Hono<AppEnv>()
  .get('/', zValidator('query', listUsersQuerySchema), async (c) => {
    const query = c.req.valid('query')
    const result = await UserService.list(c.env.DB, query)
    return paginated(c, result)
  })
  .get('/:id', zValidator('param', z.object({ id: z.string().uuid() })), async (c) => {
    const { id } = c.req.valid('param')
    const user = await UserService.getById(c.env.DB, id)
    if (!user) {
      return c.json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } }, 404)
    }
    return success(c, user)
  })
  .post('/', zValidator('json', createUserSchema), async (c) => {
    const data = c.req.valid('json')
    const user = await UserService.create(c.env.DB, data)
    return success(c, user, 201)
  })
  .put('/:id',
    zValidator('param', z.object({ id: z.string().uuid() })),
    zValidator('json', updateUserSchema),
    async (c) => {
      const { id } = c.req.valid('param')
      const data = c.req.valid('json')
      const user = await UserService.update(c.env.DB, id, data)
      return success(c, user)
    }
  )
  .delete('/:id', zValidator('param', z.object({ id: z.string().uuid() })), async (c) => {
    const { id } = c.req.valid('param')
    await UserService.delete(c.env.DB, id)
    return c.json({ success: true }, 204)
  })

export default users
export type UsersRoute = typeof users
```

## Route Barrel

```typescript
// src/routes/index.ts
import { Hono } from 'hono'
import type { AppEnv } from '../types'
import users from './users'
import orders from './orders'
import health from './health'

const routes = new Hono<AppEnv>()
routes.route('/users', users)
routes.route('/orders', orders)
routes.route('/health', health)
export { routes }
```

## Health Check

```typescript
// src/routes/health.ts
import { Hono } from 'hono'
import type { AppEnv } from '../types'

const health = new Hono<AppEnv>()
  .get('/health', (c) => {
    return c.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      version: c.env.API_VERSION,
      environment: c.env.ENVIRONMENT,
    })
  })
  .get('/ready', async (c) => {
    try {
      await c.env.DB.prepare('SELECT 1').first()
      return c.json({ status: 'ready', database: 'connected' })
    } catch (error) {
      return c.json({ status: 'not_ready', database: 'disconnected' }, 503)
    }
  })

export default health
```
