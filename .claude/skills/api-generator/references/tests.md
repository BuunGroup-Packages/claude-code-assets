# Generate Test Suite

Generate comprehensive tests using Vitest with the Cloudflare Workers pool.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
.claude/assets/best-practices/hono-cf-workers/testing.md
```

## Workflow

1. Update tests/setup.ts with D1 migration setup
2. Generate route integration tests for each resource
3. Generate service unit tests for each resource
4. Generate health check tests

## Test Setup

### tests/setup.ts

```typescript
import { env } from 'cloudflare:test'

// D1 migrations are applied automatically by the Cloudflare Vitest pool
// when migrations_dir is configured in wrangler.jsonc.
// For manual setup, use applyD1Migrations:

// import { applyD1Migrations } from 'cloudflare:test'
// import { readD1Migrations } from '@cloudflare/vitest-pool-workers/config'
// const migrations = await readD1Migrations('drizzle/migrations')
// await applyD1Migrations(env.DB, migrations)
```

### tests/env.d.ts

```typescript
declare module 'cloudflare:test' {
  interface ProvidedEnv {
    DB: D1Database
    ENVIRONMENT: string
    API_VERSION: string
    API_KEY: string
    JWT_SECRET: string
  }
}
```

## Route Integration Tests

### tests/routes/{resource}.test.ts

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { env } from 'cloudflare:test'
import { createApp } from '../../src/app'

const app = createApp()
const AUTH_HEADER = { 'x-api-key': 'test-api-key-12345' }

describe('GET /api/${resource}', () => {
  it('returns paginated list', async () => {
    const res = await app.request(
      '/api/${resource}',
      { headers: AUTH_HEADER },
      env
    )
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.success).toBe(true)
    expect(Array.isArray(body.data)).toBe(true)
    expect(body.pagination).toBeDefined()
    expect(body.pagination.page).toBe(1)
  })

  it('respects pagination params', async () => {
    const res = await app.request(
      '/api/${resource}?page=1&limit=5',
      { headers: AUTH_HEADER },
      env
    )
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.pagination.limit).toBe(5)
  })

  it('rejects without auth', async () => {
    const res = await app.request('/api/${resource}', {}, env)
    expect(res.status).toBe(401)
  })
})

describe('POST /api/${resource}', () => {
  it('creates a ${resource}', async () => {
    const res = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          // Valid create payload from plan's schema
          name: 'Test ${Resource}',
          email: 'test@example.com',
        }),
      },
      env
    )

    expect(res.status).toBe(201)
    const body = await res.json() as any
    expect(body.success).toBe(true)
    expect(body.data.id).toBeDefined()
    expect(body.data.name).toBe('Test ${Resource}')
  })

  it('rejects invalid payload', async () => {
    const res = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      },
      env
    )

    expect(res.status).toBe(400)
    const body = await res.json() as any
    expect(body.success).toBe(false)
  })

  it('rejects without auth', async () => {
    const res = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Test' }),
      },
      env
    )
    expect(res.status).toBe(401)
  })
})

describe('GET /api/${resource}/:id', () => {
  it('returns 404 for non-existent ID', async () => {
    const res = await app.request(
      '/api/${resource}/00000000-0000-0000-0000-000000000000',
      { headers: AUTH_HEADER },
      env
    )
    expect(res.status).toBe(404)
  })

  it('returns item after creation', async () => {
    // Create first
    const createRes = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Fetch Test', email: 'fetch@example.com' }),
      },
      env
    )
    const created = (await createRes.json() as any).data

    // Then fetch
    const res = await app.request(
      `/api/${resource}/${created.id}`,
      { headers: AUTH_HEADER },
      env
    )
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.data.id).toBe(created.id)
  })
})

describe('PUT /api/${resource}/:id', () => {
  it('updates an existing ${resource}', async () => {
    // Create first
    const createRes = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Original', email: 'update@example.com' }),
      },
      env
    )
    const created = (await createRes.json() as any).data

    // Update
    const res = await app.request(
      `/api/${resource}/${created.id}`,
      {
        method: 'PUT',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Updated' }),
      },
      env
    )
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.data.name).toBe('Updated')
  })

  it('returns 404 for non-existent ID', async () => {
    const res = await app.request(
      '/api/${resource}/00000000-0000-0000-0000-000000000000',
      {
        method: 'PUT',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Nope' }),
      },
      env
    )
    expect(res.status).toBe(404)
  })
})

describe('DELETE /api/${resource}/:id', () => {
  it('deletes an existing ${resource}', async () => {
    // Create first
    const createRes = await app.request(
      '/api/${resource}',
      {
        method: 'POST',
        headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'To Delete', email: 'delete@example.com' }),
      },
      env
    )
    const created = (await createRes.json() as any).data

    // Delete
    const res = await app.request(
      `/api/${resource}/${created.id}`,
      { method: 'DELETE', headers: AUTH_HEADER },
      env
    )
    expect(res.status).toBe(204)
  })
})
```

Adapt the test payloads based on the plan's actual schema fields.

## Service Unit Tests

### tests/services/{resource}.service.test.ts

```typescript
import { describe, it, expect } from 'vitest'
import { env } from 'cloudflare:test'
import { ${Resource}Service } from '../../src/services/${resource}.service'

describe('${Resource}Service', () => {
  it('creates and retrieves a ${resource}', async () => {
    const item = await ${Resource}Service.create(env.DB, {
      name: 'Service Test',
      email: 'service@example.com',
    })
    expect(item.id).toBeDefined()

    const fetched = await ${Resource}Service.getById(env.DB, item.id)
    expect(fetched?.name).toBe('Service Test')
  })

  it('lists with pagination', async () => {
    const result = await ${Resource}Service.list(env.DB, {
      page: 1, limit: 10, sort: 'desc',
    })
    expect(result.data).toBeDefined()
    expect(result.total).toBeGreaterThanOrEqual(0)
    expect(result.page).toBe(1)
  })

  it('updates a ${resource}', async () => {
    const item = await ${Resource}Service.create(env.DB, {
      name: 'Before Update',
      email: 'before@example.com',
    })

    const updated = await ${Resource}Service.update(env.DB, item.id, {
      name: 'After Update',
    })
    expect(updated.name).toBe('After Update')
  })

  it('throws NotFoundError on update of non-existent', async () => {
    await expect(
      ${Resource}Service.update(env.DB, 'non-existent-id', { name: 'Nope' })
    ).rejects.toThrow('not found')
  })

  it('deletes a ${resource}', async () => {
    const item = await ${Resource}Service.create(env.DB, {
      name: 'To Delete',
      email: 'todelete@example.com',
    })

    await ${Resource}Service.delete(env.DB, item.id)
    const fetched = await ${Resource}Service.getById(env.DB, item.id)
    expect(fetched).toBeNull()
  })

  it('throws on duplicate unique field', async () => {
    await ${Resource}Service.create(env.DB, {
      name: 'First',
      email: 'dupe@example.com',
    })
    await expect(
      ${Resource}Service.create(env.DB, {
        name: 'Second',
        email: 'dupe@example.com',
      })
    ).rejects.toThrow('already exists')
  })
})
```

## Health Check Tests

### tests/routes/health.test.ts

```typescript
import { describe, it, expect } from 'vitest'
import { env } from 'cloudflare:test'
import { createApp } from '../../src/app'

const app = createApp()

describe('GET /api/health', () => {
  it('returns ok status', async () => {
    const res = await app.request('/api/health', {}, env)
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.status).toBe('ok')
    expect(body.version).toBeDefined()
    expect(body.environment).toBe('test')
  })
})

describe('GET /api/ready', () => {
  it('reports database connectivity', async () => {
    const res = await app.request('/api/ready', {}, env)
    expect(res.status).toBe(200)

    const body = await res.json() as any
    expect(body.status).toBe('ready')
  })
})
```

## 404 Test

```typescript
describe('404', () => {
  it('returns structured error for unknown routes', async () => {
    const res = await app.request('/api/nonexistent', {}, env)
    expect(res.status).toBe(404)

    const body = await res.json() as any
    expect(body.success).toBe(false)
    expect(body.error.code).toBe('NOT_FOUND')
  })
})
```

## Output

```
## Tests Generated

### Route Tests
| File | Tests | Covers |
|------|-------|--------|
| routes/health.test.ts | 2 | Health + ready endpoints |
| routes/${resource}.test.ts | {count} | Full CRUD + auth + validation |

### Service Tests
| File | Tests | Covers |
|------|-------|--------|
| services/${resource}.service.test.ts | {count} | CRUD + errors + constraints |

### Run
\`\`\`bash
npm test
npm run test:watch
\`\`\`
```
