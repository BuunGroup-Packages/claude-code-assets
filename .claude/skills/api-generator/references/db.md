# Generate Database Layer

Generate Drizzle ORM table definitions and initial migration SQL for Cloudflare D1.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

1. Read database schema section from the plan
2. Add table definition to src/db/schema.ts
3. Generate migration SQL in drizzle/migrations/
4. Ensure foreign keys and indexes are included

## Table Definition Pattern

### src/db/schema.ts

```typescript
import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core'
import { sql } from 'drizzle-orm'

export const ${resource} = sqliteTable('${resource}', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  // Fields from plan's database schema section
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  role: text('role', { enum: ['admin', 'member', 'viewer'] }).notNull().default('member'),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
  updatedAt: text('updated_at').notNull().default(sql`(datetime('now'))`),
})
```

## Type Mapping (Plan -> Drizzle)

| Plan Type | Drizzle Column | SQLite Type |
|-----------|---------------|-------------|
| string | `text('col')` | TEXT |
| string (unique) | `text('col').unique()` | TEXT UNIQUE |
| string (enum) | `text('col', { enum: [...] })` | TEXT |
| integer | `integer('col')` | INTEGER |
| float/real | `real('col')` | REAL |
| boolean | `integer('col', { mode: 'boolean' })` | INTEGER |
| uuid (PK) | `text('id').primaryKey().$defaultFn(...)` | TEXT PK |
| datetime | `text('col').default(sql\`(datetime('now'))\`)` | TEXT |
| foreign key | `text('col').references(() => other.id)` | TEXT FK |

## Relationship Patterns

### Foreign Key with Cascade Delete

```typescript
export const orders = sqliteTable('orders', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  userId: text('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  total: real('total').notNull(),
  status: text('status', { enum: ['pending', 'paid', 'shipped', 'delivered'] })
    .notNull().default('pending'),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
})
```

## Migration SQL

### drizzle/migrations/0000_create_{resource}.sql

```sql
CREATE TABLE IF NOT EXISTS ${resource} (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'member',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_${resource}_created_at ON ${resource}(created_at);
CREATE INDEX IF NOT EXISTS idx_${resource}_email ON ${resource}(email);
```

Add indexes for:
- Foreign key columns (always)
- Columns used in WHERE clauses (from list query filters)
- Columns used in ORDER BY (typically created_at)
- Unique columns (automatically indexed by UNIQUE constraint)

## D1 Gotchas

- SQLite, not Postgres — no `ALTER COLUMN`, limited `JOIN` syntax
- `datetime('now')` returns UTC — document this for consumers
- 10GB per database limit — plan sharding for large datasets
- No `RETURNING *` on some operations — use `RETURNING` with specific columns
- TEXT for all string types including UUIDs and datetimes
- INTEGER for booleans (0/1 via Drizzle's `mode: 'boolean'`)

## Output

```
## Database Schema Generated

### Tables
| Table | Columns | Indexes | Relationships |
|-------|---------|---------|---------------|
| ${resource} | {count} | {count} | {list} |

### Migration
- drizzle/migrations/0000_create_${resource}.sql

### Run Migration
\`\`\`bash
npm run db:migrate:local
\`\`\`
```
