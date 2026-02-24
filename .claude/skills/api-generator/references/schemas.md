# Generate Zod Schemas

Generate Zod schemas that serve as the single source of truth for validation AND OpenAPI docs.

Follow patterns from:
```
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

1. Read the resource's schema definition from the plan
2. Generate create schema with all writable fields
3. Generate update schema as `.partial()` of create
4. Generate list query schema extending `paginationQuery`
5. Export inferred TypeScript types
6. Update schemas/index.ts barrel

## Schema File Pattern

### src/schemas/{resource}.ts

```typescript
import { z } from 'zod'
import { paginationQuery } from './common'

// ── Create Schema ──
export const create${Resource}Schema = z.object({
  // Fields from plan, with appropriate Zod validators
  name: z.string().min(1).max(255),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'viewer']).default('member'),
})

// ── Update Schema (all fields optional) ──
export const update${Resource}Schema = create${Resource}Schema.partial()

// ── List Query Schema (pagination + filters) ──
export const list${Resource}QuerySchema = paginationQuery.extend({
  search: z.string().optional(),
  // Add filter fields from the plan
})

// ── Inferred Types ──
export type Create${Resource} = z.infer<typeof create${Resource}Schema>
export type Update${Resource} = z.infer<typeof update${Resource}Schema>
export type List${Resource}Query = z.infer<typeof list${Resource}QuerySchema>
```

## Type Mapping

| Plan Type | Zod Validator |
|-----------|---------------|
| string | `z.string()` |
| string (min/max) | `z.string().min(1).max(255)` |
| email | `z.string().email()` |
| uuid | `z.string().uuid()` |
| url | `z.string().url()` |
| integer | `z.number().int()` |
| float/real | `z.number()` |
| boolean | `z.boolean()` |
| enum | `z.enum(['a', 'b', 'c'])` |
| date-time | `z.string().datetime()` |
| optional | `.optional()` |
| default | `.default(value)` |
| nullable | `.nullable()` |
| array | `z.array(itemSchema)` |

## Gotchas

- Query params are ALWAYS strings — use `z.coerce.number()` for numeric query params
- Header keys are lowercased by Hono — validate with lowercase keys
- Use `.default()` for fields with defaults to match DB schema
- `paginationQuery` already handles `page`, `limit`, `sort` — just `.extend()` it

## Barrel Export

### src/schemas/index.ts

```typescript
export { uuidParam, paginationQuery } from './common'
export {
  create${Resource}Schema,
  update${Resource}Schema,
  list${Resource}QuerySchema,
} from './${resource}'
export type {
  Create${Resource},
  Update${Resource},
  List${Resource}Query,
} from './${resource}'
// ... repeat for each resource
```

## Output

```
## Schemas Generated

### {Resource}
| Schema | Fields | File |
|--------|--------|------|
| create{Resource}Schema | {count} fields | schemas/{resource}.ts |
| update{Resource}Schema | Partial of create | schemas/{resource}.ts |
| list{Resource}QuerySchema | pagination + {count} filters | schemas/{resource}.ts |

### Types Exported
- Create{Resource}
- Update{Resource}
- List{Resource}Query
```
