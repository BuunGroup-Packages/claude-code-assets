# Testing

## Vitest Configuration

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
          bindings: {
            ENVIRONMENT: 'test',
            API_KEY: 'test-api-key-12345',
            JWT_SECRET: 'test-jwt-secret',
          },
        },
      },
    },
  },
})
```

## Test Environment Types

```typescript
// tests/env.d.ts
declare module 'cloudflare:test' {
  interface ProvidedEnv extends Env {}
}
```

## D1 Migration Setup

```typescript
// tests/setup.ts
import { applyD1Migrations, env } from 'cloudflare:test'
import { readD1Migrations } from '@cloudflare/vitest-pool-workers/config'
import path from 'node:path'

const migrations = await readD1Migrations(path.join(__dirname, '../drizzle/migrations'))

export async function setup() {
  await applyD1Migrations(env.DB, migrations)
}

await setup()
```

## Route Tests (Integration)

```typescript
import { describe, it, expect } from 'vitest'
import { env } from 'cloudflare:test'
import { createApp } from '../../src/app'

const app = createApp()

describe('GET /api/users', () => {
  it('returns empty list initially', async () => {
    const res = await app.request('/api/users', { headers: { 'x-api-key': 'test-api-key-12345' } }, env)
    expect(res.status).toBe(200)
    const body = await res.json()
    expect(body.success).toBe(true)
    expect(body.data).toEqual([])
  })

  it('rejects without auth', async () => {
    const res = await app.request('/api/users', {}, env)
    expect(res.status).toBe(401)
  })
})

describe('POST /api/users', () => {
  it('creates a user', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': 'test-api-key-12345' },
      body: JSON.stringify({ name: 'Sacha', email: 'sacha@example.com', role: 'admin' }),
    }, env)
    expect(res.status).toBe(201)
    const body = await res.json()
    expect(body.success).toBe(true)
    expect(body.data.name).toBe('Sacha')
  })

  it('rejects invalid email', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': 'test-api-key-12345' },
      body: JSON.stringify({ name: 'Test', email: 'not-an-email' }),
    }, env)
    expect(res.status).toBe(400)
    const body = await res.json()
    expect(body.error.code).toBe('VALIDATION_ERROR')
  })
})
```

## Service Tests (Unit)

```typescript
import { describe, it, expect } from 'vitest'
import { env } from 'cloudflare:test'
import { UserService } from '../../src/services/user.service'

describe('UserService', () => {
  it('creates and retrieves a user', async () => {
    const user = await UserService.create(env.DB, {
      name: 'Test', email: 'test@example.com', role: 'member',
    })
    expect(user.id).toBeDefined()
    const fetched = await UserService.getById(env.DB, user.id)
    expect(fetched?.name).toBe('Test')
  })

  it('throws ConflictError on duplicate email', async () => {
    await UserService.create(env.DB, { name: 'First', email: 'dupe@example.com', role: 'member' })
    await expect(
      UserService.create(env.DB, { name: 'Second', email: 'dupe@example.com', role: 'member' })
    ).rejects.toThrow('already exists')
  })
})
```
