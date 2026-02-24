# OpenAPI Documentation (Auto-Generated)

## Option A: `chanfana` (Cloudflare's Official Library)

Best for class-based endpoint patterns with automatic Swagger/ReDoc UI.

```typescript
import { Hono } from 'hono'
import { fromHono, OpenAPIRoute, contentJson } from 'chanfana'
import { z } from 'zod'
import type { AppEnv, AppContext } from './types'

class ListUsers extends OpenAPIRoute {
  schema = {
    tags: ['Users'],
    summary: 'List all users',
    request: {
      query: z.object({
        page: z.number().int().min(1).default(1),
        limit: z.number().int().min(1).max(100).default(20),
      }),
    },
    responses: {
      '200': {
        description: 'Successful response',
        ...contentJson(z.object({
          success: z.literal(true),
          data: z.array(z.object({
            id: z.string().uuid(),
            name: z.string(),
            email: z.string().email(),
          })),
        })),
      },
    },
  }

  async handle(c: AppContext) {
    const data = await this.getValidatedData<typeof this.schema>()
    return c.json({ success: true, data: [] })
  }
}

const app = new Hono<AppEnv>()
const openapi = fromHono(app, {
  docs_url: '/docs',
  redoc_url: '/redocs',
  openapi_url: '/openapi.json',
  schema: {
    info: { title: 'My API', version: '1.0.0' },
    servers: [
      { url: 'https://api.example.com', description: 'Production' },
      { url: 'http://localhost:8787', description: 'Local development' },
    ],
  },
})

openapi.get('/api/users', ListUsers)
export default app
```

## Option B: `@hono/zod-openapi` (Hono-Native)

Best for maintaining Hono's idiomatic chained route patterns.

```typescript
import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'
import type { AppEnv } from './types'

const app = new OpenAPIHono<AppEnv>()

const getUserRoute = createRoute({
  method: 'get',
  path: '/api/users/{id}',
  tags: ['Users'],
  request: {
    params: z.object({
      id: z.string().uuid().openapi({ param: { name: 'id', in: 'path' } }),
    }),
  },
  responses: {
    200: { content: { 'application/json': { schema: userResponseSchema } }, description: 'User found' },
    404: { content: { 'application/json': { schema: errorResponseSchema } }, description: 'User not found' },
  },
})

app.openapi(getUserRoute, async (c) => {
  const { id } = c.req.valid('param')
})

app.doc('/openapi.json', { openapi: '3.1.0', info: { title: 'My API', version: '1.0.0' } })
app.get('/docs', swaggerUI({ url: '/openapi.json' }))
```

## Comparison

| Feature | chanfana | @hono/zod-openapi |
|---------|---------|-------------------|
| Style | Class-based endpoints | Functional/chained routes |
| Maintained by | Cloudflare | Hono community |
| Swagger/ReDoc | Built-in auto-serve | Manual setup |
| Validation | Built-in from schema | Uses zValidator |
| RPC compatibility | Requires adapter | Native Hono RPC |
| Best for | Cloudflare-first APIs | Type-safe full-stack |
