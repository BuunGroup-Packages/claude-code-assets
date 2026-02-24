# RPC Client (End-to-End Type Safety)

Hono's killer feature: share API types between server and client with zero code generation.

## Server (routes must be chained)

```typescript
const users = new Hono<AppEnv>()
  .get('/', zValidator('query', listUsersQuerySchema), async (c) => {
    return c.json({ success: true, data: users })
  })
  .post('/', zValidator('json', createUserSchema), async (c) => {
    return c.json({ success: true, data: user }, 201)
  })

export default users
export type UsersRoute = typeof users
```

## Client Usage

```typescript
import { hc } from 'hono/client'
import type { AppType } from '../server/src/app'

const client = hc<AppType>('https://api.example.com')

// Fully typed — IDE auto-completes paths, params, and response types
const res = await client.api.users.$get({
  query: { page: '1', limit: '20', search: 'sacha' },
})
const { data, pagination } = await res.json()

// Create user
const createRes = await client.api.users.$post({
  json: { name: 'Sacha', email: 'sacha@example.com', role: 'admin' },
})

// Cloudflare Service Bindings (Worker-to-Worker)
const internalClient = hc<AppType>('http://internal', {
  fetch: c.env.MY_OTHER_WORKER.fetch.bind(c.env.MY_OTHER_WORKER),
})
```

## Monorepo Setup

```
my-monorepo/
├── packages/
│   ├── api/              # Hono API (Cloudflare Worker)
│   └── web/              # Frontend — tsconfig references: [{ path: "../api" }]
└── tsconfig.base.json
```

**Performance tip:** Pre-compile the RPC type to avoid slow IDE inference:

```typescript
// packages/api/src/client.ts
import { hc } from 'hono/client'
import { app } from './app'

export type Client = ReturnType<typeof hc<typeof app>>
export const hcWithType = (...args: Parameters<typeof hc>): Client =>
  hc<typeof app>(...args)
```
