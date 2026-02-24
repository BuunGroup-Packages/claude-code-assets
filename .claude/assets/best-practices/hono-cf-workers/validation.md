# Validation with Zod

## Schema Definitions (Single Source of Truth)

```typescript
// src/schemas/common.ts
import { z } from 'zod'

export const uuidParam = z.object({
  id: z.string().uuid('Invalid UUID format'),
})

export const paginationQuery = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
})

export const errorResponseSchema = z.object({
  success: z.literal(false),
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.record(z.unknown()).optional(),
  }),
})

export const successResponseSchema = <T extends z.ZodType>(dataSchema: T) =>
  z.object({ success: z.literal(true), data: dataSchema })

export const paginatedResponseSchema = <T extends z.ZodType>(itemSchema: T) =>
  z.object({
    success: z.literal(true),
    data: z.array(itemSchema),
    pagination: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
      totalPages: z.number(),
    }),
  })
```

```typescript
// src/schemas/users.ts
import { z } from 'zod'
import { paginationQuery } from './common'

export const createUserSchema = z.object({
  name: z.string().min(1).max(255),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'viewer']).default('member'),
})

export const updateUserSchema = createUserSchema.partial()

export const listUsersQuerySchema = paginationQuery.extend({
  search: z.string().optional(),
  role: z.enum(['admin', 'member', 'viewer']).optional(),
})

export type CreateUser = z.infer<typeof createUserSchema>
export type UpdateUser = z.infer<typeof updateUserSchema>
export type ListUsersQuery = z.infer<typeof listUsersQuerySchema>
```

## Custom Validation Error Formatting

```typescript
import { zValidator } from '@hono/zod-validator'
import type { ZodSchema } from 'zod'
import type { ValidationTargets } from 'hono'

export function validate<
  Target extends keyof ValidationTargets,
  Schema extends ZodSchema
>(target: Target, schema: Schema) {
  return zValidator(target, schema, (result, c) => {
    if (!result.success) {
      return c.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Request validation failed',
            details: result.error.flatten().fieldErrors,
          },
        },
        400
      )
    }
  })
}
```

## Gotchas

- **Header names:** Hono normalises header keys to lowercase. Use `value['authorization']` not `value['Authorization']`
- **Query params are always strings:** Use `z.coerce.number()` for numeric query params, not `z.number()`
