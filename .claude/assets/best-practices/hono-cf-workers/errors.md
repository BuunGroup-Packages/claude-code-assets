# Error Handling

## Custom Error Classes

```typescript
// src/lib/errors.ts
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

## Global Error Handler

```typescript
// src/middleware/error-handler.ts
import type { ErrorHandler } from 'hono'
import { HTTPException } from 'hono/http-exception'
import type { AppEnv } from '../types'
import { AppError } from '../lib/errors'

export const errorHandler: ErrorHandler<AppEnv> = (err, c) => {
  const requestId = c.get('requestId')

  if (err instanceof AppError) {
    console.log(JSON.stringify({
      level: 'warn', error_code: err.code, message: err.message, request_id: requestId,
    }))
    return c.json({
      success: false,
      error: { code: err.code, message: err.message, ...(err.details && { details: err.details }) },
    }, err.statusCode as any)
  }

  if (err instanceof HTTPException) {
    return c.json({ success: false, error: { code: 'HTTP_ERROR', message: err.message } }, err.status)
  }

  console.error(JSON.stringify({
    level: 'error', error: err.message, stack: err.stack, request_id: requestId,
    path: c.req.path, method: c.req.method,
  }))
  return c.json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } }, 500)
}
```

## Response Helpers

```typescript
// src/lib/response.ts
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
