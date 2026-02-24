# Generate Route Modules

Generate thin Hono route modules that validate input, call services, and return responses.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

1. Read the resource's endpoint definitions from the plan
2. Generate route file with chained methods (critical for RPC)
3. Wire Zod validators from schemas
4. Delegate to service layer
5. Use response helpers (success/paginated)
6. Export route type for RPC clients
7. Update routes/index.ts barrel to mount the new route

## Route File Pattern

### src/routes/{resource}.ts

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import type { AppEnv } from '../types'
import {
  create${Resource}Schema,
  update${Resource}Schema,
  list${Resource}QuerySchema,
} from '../schemas/${resource}'
import { uuidParam } from '../schemas/common'
import { ${Resource}Service } from '../services/${resource}.service'
import { success, paginated } from '../lib/response'

// IMPORTANT: Chain methods for RPC type inference
const ${resource} = new Hono<AppEnv>()
  .get(
    '/',
    zValidator('query', list${Resource}QuerySchema),
    async (c) => {
      const query = c.req.valid('query')
      const result = await ${Resource}Service.list(c.env.DB, query)
      return paginated(c, result)
    }
  )
  .get(
    '/:id',
    zValidator('param', uuidParam),
    async (c) => {
      const { id } = c.req.valid('param')
      const item = await ${Resource}Service.getById(c.env.DB, id)
      if (!item) {
        return c.json(
          { success: false, error: { code: 'NOT_FOUND', message: '${Resource} not found' } },
          404
        )
      }
      return success(c, item)
    }
  )
  .post(
    '/',
    zValidator('json', create${Resource}Schema),
    async (c) => {
      const data = c.req.valid('json')
      const item = await ${Resource}Service.create(c.env.DB, data)
      return success(c, item, 201)
    }
  )
  .put(
    '/:id',
    zValidator('param', uuidParam),
    zValidator('json', update${Resource}Schema),
    async (c) => {
      const { id } = c.req.valid('param')
      const data = c.req.valid('json')
      const item = await ${Resource}Service.update(c.env.DB, id, data)
      return success(c, item)
    }
  )
  .delete(
    '/:id',
    zValidator('param', uuidParam),
    async (c) => {
      const { id } = c.req.valid('param')
      await ${Resource}Service.delete(c.env.DB, id)
      return c.json({ success: true }, 204)
    }
  )

export default ${resource}
export type ${Resource}Route = typeof ${resource}
```

## Adaptation Rules

1. **Only generate endpoints from the plan.** If the plan has no DELETE, don't generate delete.
2. **Chain ALL methods** on a single `new Hono()` instance — NEVER use separate `app.get()` calls.
3. **Always export the route type** — `export type ${Resource}Route = typeof ${resource}`
4. **Use `zValidator`** for all input sources (json, query, param, header).
5. **Delegate to services** — routes NEVER contain business logic.
6. **Use response helpers** — `success()` for single items, `paginated()` for lists.
7. **Use `uuidParam`** from common schemas for `:id` path params.
8. **For nested resources** (e.g., `/users/:userId/orders`), accept parent ID as a param.
9. **For custom actions** (e.g., `/users/:id/archive`), name the operation clearly.

## Non-CRUD Endpoints

For custom operations from the plan:

```typescript
  .post(
    '/:id/archive',
    zValidator('param', uuidParam),
    async (c) => {
      const { id } = c.req.valid('param')
      const item = await ${Resource}Service.archive(c.env.DB, id)
      return success(c, item)
    }
  )
```

## Route Barrel

### Update src/routes/index.ts

```typescript
import { Hono } from 'hono'
import type { AppEnv } from '../types'
import health from './health'
import ${resource} from './${resource}'

const routes = new Hono<AppEnv>()

routes.route('/', health)
routes.route('/${resource}', ${resource})

export { routes }
```

## Output

```
## Route Generated

**Resource**: ${resource}
**Path**: /api/${resource}

### Endpoints
| Method | Path | Validator | Service Method |
|--------|------|-----------|---------------|
| GET | /api/${resource} | query: list schema | list |
| GET | /api/${resource}/:id | param: uuid | getById |
| POST | /api/${resource} | json: create schema | create |
| PUT | /api/${resource}/:id | param + json: update | update |
| DELETE | /api/${resource}/:id | param: uuid | delete |

### Files
- src/routes/${resource}.ts (created)
- src/routes/index.ts (updated)

### RPC Type
\`\`\`typescript
export type ${Resource}Route = typeof ${resource}
\`\`\`
```
