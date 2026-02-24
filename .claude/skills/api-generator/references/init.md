# Initialize API Project

Scaffold a production-ready Hono + Cloudflare Workers project.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
.claude/assets/best-practices/hono-cf-workers/project-structure.md
```

## Workflow

1. Create project root directory
2. Create directory structure
3. Generate wrangler.jsonc
4. Generate package.json
5. Generate tsconfig.json
6. Generate vitest.config.ts with Cloudflare pool
7. Generate drizzle.config.ts
8. Generate src/index.ts entry point
9. Generate src/app.ts app factory
10. Generate src/types.ts with bindings
11. Generate src/lib/errors.ts
12. Generate src/lib/response.ts
13. Generate src/routes/health.ts
14. Generate .dev.vars template
15. Generate .gitignore
16. Generate .github/workflows/deploy.yml

## Directory Structure

```
{API_NAME}/
├── src/
│   ├── index.ts
│   ├── app.ts
│   ├── types.ts
│   ├── middleware/
│   ├── routes/
│   │   ├── index.ts
│   │   └── health.ts
│   ├── schemas/
│   │   ├── index.ts
│   │   └── common.ts
│   ├── services/
│   ├── db/
│   │   ├── index.ts
│   │   └── schema.ts
│   └── lib/
│       ├── errors.ts
│       └── response.ts
├── tests/
│   ├── env.d.ts
│   ├── setup.ts
│   ├── routes/
│   └── services/
├── drizzle/
│   └── migrations/
├── wrangler.jsonc
├── drizzle.config.ts
├── vitest.config.ts
├── tsconfig.json
├── package.json
├── .dev.vars
├── .gitignore
└── .github/
    └── workflows/
        └── deploy.yml
```

## File Templates

### package.json

```json
{
  "name": "${API_NAME}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wrangler dev",
    "dev:remote": "wrangler dev --remote",
    "deploy": "wrangler deploy",
    "deploy:staging": "wrangler deploy --env staging",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src/",
    "test": "vitest run",
    "test:watch": "vitest",
    "db:generate": "drizzle-kit generate",
    "db:migrate:local": "wrangler d1 migrations apply ${API_NAME}-db --local",
    "db:migrate:prod": "wrangler d1 migrations apply ${API_NAME}-db --remote",
    "db:studio": "drizzle-kit studio",
    "cf-typegen": "wrangler types"
  },
  "dependencies": {
    "hono": "^4.7.0",
    "@hono/zod-validator": "^0.5.0",
    "zod": "^3.24.0",
    "drizzle-orm": "^0.38.0"
  },
  "devDependencies": {
    "@cloudflare/vitest-pool-workers": "^0.9.0",
    "@cloudflare/workers-types": "^4.20250401.0",
    "drizzle-kit": "^0.30.0",
    "vitest": "^3.0.0",
    "wrangler": "^4.0.0",
    "typescript": "^5.7.0"
  }
}
```

### wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "${API_NAME}",
  "main": "src/index.ts",
  "compatibility_date": "2025-04-01",
  "compatibility_flags": ["nodejs_compat"],
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  },
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "${API_NAME}-db",
      "database_id": "YOUR_DATABASE_ID",
      "migrations_dir": "drizzle/migrations"
    }
  ],
  "vars": {
    "ENVIRONMENT": "production",
    "API_VERSION": "v1",
    "LOG_LEVEL": "info"
  }
}
```

Adapt bindings based on the plan. Include KV, R2, and rate limiters only if required.

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types/2023-07-01"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### vitest.config.ts

```typescript
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
            API_VERSION: 'v1',
            API_KEY: 'test-api-key-12345',
            JWT_SECRET: 'test-jwt-secret',
          },
        },
      },
    },
  },
})
```

### drizzle.config.ts

```typescript
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  dialect: 'sqlite',
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
})
```

### src/index.ts

```typescript
import { createApp } from './app'

const app = createApp()

export default app
export type { AppType } from './app'
```

### src/app.ts

```typescript
import { Hono } from 'hono'
import type { AppEnv } from './types'
import { errorHandler } from './middleware/error-handler'
import { routes } from './routes'

export function createApp() {
  const app = new Hono<AppEnv>()

  // Global error handler
  app.onError(errorHandler)

  // 404 handler
  app.notFound((c) => {
    return c.json({
      success: false,
      error: { code: 'NOT_FOUND', message: `Route not found: ${c.req.method} ${c.req.path}` },
    }, 404)
  })

  // Mount routes
  app.route('/api', routes)

  return app
}

export type AppType = ReturnType<typeof createApp>
```

Note: Middleware is NOT added here during init. Middleware is added in Phase 3.

### src/types.ts

```typescript
import type { Context } from 'hono'

export type Bindings = {
  DB: D1Database
  ENVIRONMENT: string
  API_VERSION: string
  LOG_LEVEL: string
  API_KEY: string
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

Adapt Bindings based on the plan's bindings table.

### src/lib/errors.ts

```typescript
export class AppError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super('NOT_FOUND', 404, id ? `${resource} '${id}' not found` : `${resource} not found`)
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super('UNAUTHORIZED', 401, message)
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super('FORBIDDEN', 403, message)
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super('CONFLICT', 409, message)
  }
}

export class RateLimitError extends AppError {
  constructor() {
    super('RATE_LIMITED', 429, 'Too many requests')
  }
}
```

### src/lib/response.ts

```typescript
import type { Context } from 'hono'

export function success<T>(c: Context, data: T, status: number = 200) {
  return c.json({ success: true, data }, status as any)
}

export function paginated<T>(
  c: Context,
  result: { data: T[]; total: number; page: number; limit: number }
) {
  return c.json({
    success: true,
    data: result.data,
    pagination: {
      page: result.page,
      limit: result.limit,
      total: result.total,
      totalPages: Math.ceil(result.total / result.limit),
    },
  })
}
```

### src/middleware/error-handler.ts

```typescript
import type { ErrorHandler } from 'hono'
import { HTTPException } from 'hono/http-exception'
import type { AppEnv } from '../types'
import { AppError } from '../lib/errors'

export const errorHandler: ErrorHandler<AppEnv> = (err, c) => {
  const requestId = c.get('requestId')

  if (err instanceof AppError) {
    console.log(JSON.stringify({
      level: 'warn', error_code: err.code,
      message: err.message, request_id: requestId,
    }))
    return c.json({
      success: false,
      error: { code: err.code, message: err.message, ...(err.details && { details: err.details }) },
    }, err.statusCode as any)
  }

  if (err instanceof HTTPException) {
    return c.json({
      success: false,
      error: { code: 'HTTP_ERROR', message: err.message },
    }, err.status)
  }

  console.error(JSON.stringify({
    level: 'error', error: err.message, stack: err.stack,
    request_id: requestId, path: c.req.path, method: c.req.method,
  }))

  return c.json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
  }, 500)
}
```

### src/routes/index.ts

```typescript
import { Hono } from 'hono'
import type { AppEnv } from '../types'
import health from './health'

const routes = new Hono<AppEnv>()

routes.route('/', health)

export { routes }
```

### src/routes/health.ts

```typescript
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
    } catch {
      return c.json({ status: 'not_ready', database: 'disconnected' }, 503)
    }
  })

export default health
```

### src/schemas/common.ts

```typescript
import { z } from 'zod'

export const uuidParam = z.object({
  id: z.string().uuid('Invalid UUID format'),
})

export const paginationQuery = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
})
```

### src/db/index.ts

```typescript
import { drizzle } from 'drizzle-orm/d1'
import * as schema from './schema'

export function getDb(d1: D1Database) {
  return drizzle(d1, { schema })
}

export type Database = ReturnType<typeof getDb>
export { schema }
```

### src/db/schema.ts

```typescript
// Tables will be added by db generation step
```

### tests/env.d.ts

```typescript
declare module 'cloudflare:test' {
  interface ProvidedEnv extends Env {}
}
```

### tests/setup.ts

```typescript
import { env } from 'cloudflare:test'
```

Full migration setup will be added by test generation step.

### .dev.vars

```
API_KEY=dev-key-12345
JWT_SECRET=dev-jwt-secret
```

### .gitignore

```
node_modules/
dist/
.wrangler/
.dev.vars
*.tsbuildinfo
```

### .github/workflows/deploy.yml

```yaml
name: Deploy API
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npm run typecheck
      - run: npm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: d1 migrations apply ${API_NAME}-db --remote
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy
```

## Output

```
## API Project Initialized

**Name**: {API_NAME}
**Stack**: Hono + Cloudflare Workers + D1 + Drizzle ORM

### Structure
{DIRECTORY_TREE}

### Next Steps
\`\`\`bash
cd {API_NAME}
npm install
npx wrangler d1 create {API_NAME}-db
# Update wrangler.jsonc with database_id
npm run dev
\`\`\`
```
