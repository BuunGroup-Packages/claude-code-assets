# SDK Generator — Patterns Reference

Condensed reference from `.claude/assets/best-practices/sdk/`.
Sub-skills MUST follow these patterns exactly when generating code.

---

## 1. Resource-Oriented Client (Gold Standard)

Every SDK uses the resource-oriented pattern. The client exposes resources as properties
that mirror the API's URL structure.

```typescript
// Consumer experience
const client = new MyAPI({ apiKey: process.env.MY_API_KEY });
const user = await client.users.create({ name: "Sacha" });
const orders = await client.users.orders.list("user_123");
```

Implementation pattern:

```typescript
// client.ts
export class MyAPIClient {
  readonly users: UsersResource;
  readonly orders: OrdersResource;

  constructor(options: ClientOptions = {}) {
    const httpClient = new HTTPClient({
      baseURL: options.baseURL ?? 'https://api.example.com/v1',
      apiKey: options.apiKey ?? process.env.MY_API_KEY,
      timeout: options.timeout ?? { connectionMs: 5000, requestMs: 30000 },
      retry: options.retry ?? { maxRetries: 2 },
    });

    this.users = new UsersResource(httpClient);
    this.orders = new OrdersResource(httpClient);
  }
}
```

---

## 2. Naming Conventions

| Convention | TypeScript | Python |
|---|---|---|
| Methods | `camelCase` | `snake_case` |
| Classes | `PascalCase` | `PascalCase` |
| Constants | `UPPER_CASE` | `UPPER_CASE` |
| Files | `kebab-case.ts` | `snake_case.py` |
| Internal modules | N/A | `_prefixed.py` |

---

## 3. Error Hierarchy

Always generate this error class tree:

```
APIError (base)
├── AuthenticationError (401)
├── PermissionError (403)
├── NotFoundError (404)
├── BadRequestError (400)
├── RateLimitError (429) — includes retryAfter
├── InternalServerError (500)
├── ConnectionError — network failures
└── TimeoutError — request timeouts
```

Every error includes: `status`, `code`, `message`, `requestId`, `headers`.

---

## 4. Retry with Exponential Backoff

Default config:
- maxRetries: 2
- initialDelayMs: 500
- maxDelayMs: 8000
- backoffMultiplier: 2
- jitter: true (±20%)
- retryableStatuses: [408, 429, 500, 502, 503, 504]

Rules:
- Always respect `Retry-After` headers
- Only auto-retry idempotent methods (GET, PUT, DELETE)
- POST requires `Idempotency-Key` header for safe retry

---

## 5. Authentication Patterns

Support multiple auth strategies:
- API Key (header: `Authorization: Bearer <key>` or `X-API-Key: <key>`)
- Bearer token (OAuth2 access tokens)
- OAuth2 client credentials flow

Auto-detect from environment variables. Never log credentials.

---

## 6. HTTP Client Headers

Every request includes:
```
Authorization: Bearer {apiKey}
Content-Type: application/json
Accept: application/json
User-Agent: {sdk-name}/{language}/{version}
X-SDK-Version: {version}
X-SDK-Language: {language}
```

---

## 7. Auto-Pagination (AsyncIterable)

```typescript
async *listAutoPaging(params?: ListParams): AsyncIterable<T> {
  let cursor = params?.after;
  do {
    const page = await this.list({ ...params, after: cursor });
    for (const item of page.data) {
      yield item;
    }
    cursor = page.next_cursor ?? undefined;
  } while (cursor);
}
```

---

## 8. Type Strategy

- **Request params**: Separate interface per operation (e.g., `CreateUserParams`)
- **Response models**: Mirror API schema (e.g., `User`)
- **Paginated responses**: Generic `Page<T>` wrapper
- **Enums/Literals**: Use string unions, not TS enums
- **ReadOnly fields**: Mark server-assigned fields as `readonly`
- **Zod schemas**: Generate alongside interfaces for runtime validation

---

## 9. Barrel Exports

Use explicit named re-exports (never `export *`):

```typescript
// src/index.ts
export { MyAPIClient } from './client';
export type { ClientOptions } from './client';
export type { User, Order, CreateUserParams } from './types';
export { APIError, AuthenticationError, RateLimitError } from './core/errors';
```

---

## 10. TSDoc Standard

Every public method includes:
- `@param` — parameter description
- `@returns` — return type description
- `@throws` — exception types
- `@example` — usage example with fenced code block
- `@see` — link to API reference
- `@public` or `@internal` — visibility

---

## 11. Package Configuration

TypeScript `package.json` must include:
- `"type": "module"`
- `"exports"` with `import`, `require`, `types` conditions
- `"files": ["dist"]`
- `"engines": { "node": ">=18" }`

Python `pyproject.toml` must include:
- `requires-python = ">=3.9"`
- `build-system` with hatchling
- `[project.optional-dependencies]` for dev deps

---

## 12. Testing Pyramid

- **Unit tests**: Mock HTTP transport, test serialization, error mapping, retry, validation
- **Integration tests**: Recorded HTTP fixtures (VCR pattern)
- **E2E tests**: Placeholder for live API testing

Test every:
- Resource method produces correct HTTP request
- Error responses map to correct exception types
- Retry triggers on appropriate status codes
- Pagination terminates correctly
- Auth headers set properly
- Input validation rejects bad data
