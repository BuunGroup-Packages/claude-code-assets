# Database Layer (D1 + Drizzle ORM)

## Schema Definition

```typescript
// src/db/schema.ts
import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core'
import { sql } from 'drizzle-orm'

export const users = sqliteTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  role: text('role', { enum: ['admin', 'member', 'viewer'] }).notNull().default('member'),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
  updatedAt: text('updated_at').notNull().default(sql`(datetime('now'))`),
})

export const orders = sqliteTable('orders', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  userId: text('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  total: real('total').notNull(),
  status: text('status', { enum: ['pending', 'paid', 'shipped', 'delivered'] }).notNull().default('pending'),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
})
```

## DB Client Factory

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/d1'
import * as schema from './schema'

export function getDb(d1: D1Database) {
  return drizzle(d1, { schema })
}

export type Database = ReturnType<typeof getDb>
export { schema }
```

## Service Layer

```typescript
// src/services/user.service.ts
import { eq, like, sql, desc, asc } from 'drizzle-orm'
import { getDb, schema } from '../db'
import type { CreateUser, UpdateUser, ListUsersQuery } from '../schemas/users'
import { NotFoundError, ConflictError } from '../lib/errors'

export class UserService {
  static async list(d1: D1Database, query: ListUsersQuery) {
    const db = getDb(d1)
    const { page, limit, sort, search, role } = query
    const offset = (page - 1) * limit

    let where = undefined
    if (search) where = like(schema.users.name, `%${search}%`)
    if (role) {
      const roleCondition = eq(schema.users.role, role)
      where = where ? sql`${where} AND ${roleCondition}` : roleCondition
    }

    const [data, countResult] = await Promise.all([
      db.select().from(schema.users).where(where)
        .orderBy(sort === 'asc' ? asc(schema.users.createdAt) : desc(schema.users.createdAt))
        .limit(limit).offset(offset),
      db.select({ count: sql<number>`count(*)` }).from(schema.users).where(where),
    ])

    return { data, total: countResult[0].count, page, limit }
  }

  static async getById(d1: D1Database, id: string) {
    const db = getDb(d1)
    const [user] = await db.select().from(schema.users).where(eq(schema.users.id, id)).limit(1)
    return user || null
  }

  static async create(d1: D1Database, data: CreateUser) {
    const db = getDb(d1)
    try {
      const [user] = await db.insert(schema.users).values(data).returning()
      return user
    } catch (error: any) {
      if (error.message?.includes('UNIQUE constraint failed')) {
        throw new ConflictError(`User with email '${data.email}' already exists`)
      }
      throw error
    }
  }

  static async update(d1: D1Database, id: string, data: UpdateUser) {
    const db = getDb(d1)
    const [user] = await db.update(schema.users)
      .set({ ...data, updatedAt: new Date().toISOString() })
      .where(eq(schema.users.id, id)).returning()
    if (!user) throw new NotFoundError('User', id)
    return user
  }

  static async delete(d1: D1Database, id: string) {
    const db = getDb(d1)
    const result = await db.delete(schema.users).where(eq(schema.users.id, id)).returning()
    if (result.length === 0) throw new NotFoundError('User', id)
  }
}
```

## Drizzle Kit Configuration

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  dialect: 'sqlite',
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
  driver: 'd1-http',
  dbCredentials: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
    databaseId: process.env.CLOUDFLARE_DATABASE_ID!,
    token: process.env.CLOUDFLARE_API_TOKEN!,
  },
})
```

## Migration Commands

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate:local": "wrangler d1 migrations apply my-api-db --local",
    "db:migrate:staging": "wrangler d1 migrations apply my-api-db-staging --env staging --remote",
    "db:migrate:prod": "wrangler d1 migrations apply my-api-db --remote",
    "db:studio": "drizzle-kit studio"
  }
}
```
