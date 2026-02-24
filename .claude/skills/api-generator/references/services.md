# Generate Service Layer

Generate framework-agnostic service classes containing all business logic.
Services accept `D1Database` (not Hono context) and return typed data.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

1. Read the resource's endpoints and schema from the plan
2. Generate service class with static methods
3. Implement Drizzle ORM queries for each operation
4. Handle unique constraint violations -> ConflictError
5. Handle not-found -> NotFoundError
6. Return paginated results for list operations

## Service File Pattern

### src/services/{resource}.service.ts

```typescript
import { eq, like, sql, desc, asc } from 'drizzle-orm'
import { getDb, schema } from '../db'
import type { Create${Resource}, Update${Resource}, List${Resource}Query } from '../schemas/${resource}'
import { NotFoundError, ConflictError } from '../lib/errors'

export class ${Resource}Service {
  /**
   * List ${resource}s with pagination, sorting, and filtering.
   */
  static async list(d1: D1Database, query: List${Resource}Query) {
    const db = getDb(d1)
    const { page, limit, sort } = query
    const offset = (page - 1) * limit

    // Build where conditions from query filters
    let where = undefined
    // Add filter logic based on plan's query schema fields

    const [data, countResult] = await Promise.all([
      db.select()
        .from(schema.${resource})
        .where(where)
        .orderBy(sort === 'asc' ? asc(schema.${resource}.createdAt) : desc(schema.${resource}.createdAt))
        .limit(limit)
        .offset(offset),
      db.select({ count: sql<number>`count(*)` })
        .from(schema.${resource})
        .where(where),
    ])

    return { data, total: countResult[0].count, page, limit }
  }

  /**
   * Get a single ${resource} by ID.
   */
  static async getById(d1: D1Database, id: string) {
    const db = getDb(d1)
    const [item] = await db.select()
      .from(schema.${resource})
      .where(eq(schema.${resource}.id, id))
      .limit(1)
    return item || null
  }

  /**
   * Create a new ${resource}.
   */
  static async create(d1: D1Database, data: Create${Resource}) {
    const db = getDb(d1)
    try {
      const [item] = await db.insert(schema.${resource})
        .values(data)
        .returning()
      return item
    } catch (error: any) {
      if (error.message?.includes('UNIQUE constraint failed')) {
        throw new ConflictError('${Resource} with this value already exists')
      }
      throw error
    }
  }

  /**
   * Update an existing ${resource}.
   */
  static async update(d1: D1Database, id: string, data: Update${Resource}) {
    const db = getDb(d1)
    const [item] = await db.update(schema.${resource})
      .set({ ...data, updatedAt: new Date().toISOString() })
      .where(eq(schema.${resource}.id, id))
      .returning()

    if (!item) throw new NotFoundError('${Resource}', id)
    return item
  }

  /**
   * Delete a ${resource}.
   */
  static async delete(d1: D1Database, id: string) {
    const db = getDb(d1)
    const result = await db.delete(schema.${resource})
      .where(eq(schema.${resource}.id, id))
      .returning()
    if (result.length === 0) throw new NotFoundError('${Resource}', id)
  }
}
```

## Adaptation Rules

1. **Services accept `D1Database`** — never Hono `Context`. This makes them testable without HTTP.
2. **Use `getDb(d1)` factory** — creates a Drizzle instance per request (stateless).
3. **Throw AppError subclasses** — never return HTTP status codes from services.
4. **Handle UNIQUE constraint** -> `ConflictError` with a helpful message.
5. **Handle not-found** -> `NotFoundError` with resource name and ID.
6. **List always returns `{ data, total, page, limit }`** — for the `paginated()` helper.
7. **Add search/filter logic** based on the plan's list query schema.
8. **For related resources**, accept parent ID and filter by foreign key.
9. **For custom operations** (archive, publish, etc.), add specific methods.
10. **Always set `updatedAt`** on update operations.

## Search/Filter Pattern

When the plan includes search or filter fields:

```typescript
// Build where conditions
let where = undefined

if (query.search) {
  where = like(schema.${resource}.name, `%${query.search}%`)
}

if (query.status) {
  const statusCondition = eq(schema.${resource}.status, query.status)
  where = where ? sql`${where} AND ${statusCondition}` : statusCondition
}

if (query.userId) {
  const userCondition = eq(schema.${resource}.userId, query.userId)
  where = where ? sql`${where} AND ${userCondition}` : userCondition
}
```

## Relationship Pattern

For resources with foreign keys (e.g., orders belong to users):

```typescript
static async listByUser(d1: D1Database, userId: string, query: ListOrdersQuery) {
  const db = getDb(d1)
  const where = eq(schema.orders.userId, userId)
  // ... same pagination pattern with additional where clause
}
```

## Output

```
## Service Generated

**Resource**: ${Resource}
**File**: src/services/${resource}.service.ts

### Methods
| Method | Args | Returns | Throws |
|--------|------|---------|--------|
| list | D1Database, query | { data, total, page, limit } | -- |
| getById | D1Database, id | Item | null | -- |
| create | D1Database, data | Item | ConflictError |
| update | D1Database, id, data | Item | NotFoundError |
| delete | D1Database, id | void | NotFoundError |
```
