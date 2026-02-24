# Generate SDK Resources & Types

Generate resource classes and type definitions based on the API analysis report.
Each API resource group becomes a resource class with methods matching the API endpoints.

Follow patterns from:
```
.claude/skills/sdk-generator/docs/PATTERNS.md
.claude/assets/best-practices/sdk/architecture.md and .claude/assets/best-practices/sdk/types.md
```

## Workflow

1. Parse the analysis report's Resources section
2. For each resource, generate a resource class file
3. Generate type definitions for all request/response models
4. Generate barrel exports for resources and types
5. Update client.ts to wire in resource instances
6. Update src/index.ts to export new types

---

## TypeScript Resource Pattern

### src/resources/{resource}.ts

For each resource in the analysis report, generate:

```typescript
import type { HTTPClient, APIResponse, Page, PaginationParams } from '../core';

// Import types specific to this resource
import type {
  ${ResourceName},
  Create${ResourceName}Params,
  Update${ResourceName}Params,
  List${ResourceName}Params,
} from '../types';

export class ${ResourceName}Resource {
  constructor(private readonly _client: HTTPClient) {}

  /**
   * List all ${resourceName}s.
   *
   * @param params - Pagination and filter parameters
   * @returns A page of ${resourceName} objects
   *
   * @example
   * ```typescript
   * const page = await client.${resourceName}s.list({ limit: 10 });
   * console.log(page.data);
   * ```
   */
  async list(params?: List${ResourceName}Params): Promise<Page<${ResourceName}>> {
    const response = await this._client.request<Page<${ResourceName}>>({
      method: 'GET',
      path: '/${resourcePath}',
      query: params as Record<string, string | number | boolean | undefined>,
    });
    return response.data;
  }

  /**
   * Auto-paginate through all ${resourceName}s.
   *
   * @param params - Pagination and filter parameters
   * @returns An async iterable of ${resourceName} objects
   *
   * @example
   * ```typescript
   * for await (const item of client.${resourceName}s.listAutoPaging()) {
   *   console.log(item);
   * }
   * ```
   */
  async *listAutoPaging(params?: List${ResourceName}Params): AsyncIterable<${ResourceName}> {
    let cursor = params?.after;
    do {
      const page = await this.list({ ...params, after: cursor });
      for (const item of page.data) {
        yield item;
      }
      cursor = page.next_cursor ?? undefined;
    } while (cursor);
  }

  /**
   * Retrieve a single ${resourceName} by ID.
   */
  async get(id: string): Promise<${ResourceName}> {
    const response = await this._client.request<${ResourceName}>({
      method: 'GET',
      path: `/${resourcePath}/${id}`,
    });
    return response.data;
  }

  /**
   * Create a new ${resourceName}.
   */
  async create(params: Create${ResourceName}Params): Promise<${ResourceName}> {
    const response = await this._client.request<${ResourceName}>({
      method: 'POST',
      path: '/${resourcePath}',
      body: params,
    });
    return response.data;
  }

  /**
   * Update an existing ${resourceName}.
   */
  async update(id: string, params: Update${ResourceName}Params): Promise<${ResourceName}> {
    const response = await this._client.request<${ResourceName}>({
      method: 'PUT',
      path: `/${resourcePath}/${id}`,
      body: params,
    });
    return response.data;
  }

  /**
   * Delete a ${resourceName}.
   */
  async delete(id: string): Promise<void> {
    await this._client.request<void>({
      method: 'DELETE',
      path: `/${resourcePath}/${id}`,
    });
  }
}
```

### Adaptation Rules

1. **Only generate methods that exist in the analysis report.** If the API has no DELETE endpoint for a resource, do not generate a `delete` method.
2. **Match the HTTP method and path exactly** from the analysis report.
3. **Add path parameters** as method arguments (e.g., `get(userId: string, orderId: string)` for nested resources).
4. **Add query parameters** as optional fields in the list params type.
5. **For non-CRUD operations**, name the method after the `operationId` from the analysis (e.g., `archive`, `publish`, `invite`).
6. **Include TSDoc** for every public method with `@param`, `@returns`, `@throws`, `@example`.
7. **For paginated endpoints**, always include both `list()` and `listAutoPaging()`.
8. **For non-paginated list endpoints**, only generate `list()` returning an array.

---

## TypeScript Type Definitions

### src/types/models.ts

For each resource model in the analysis report:

```typescript
/** A ${resourceName} in the system. */
export interface ${ResourceName} {
  /** Unique identifier (server-assigned) */
  readonly id: string;
  // ... fields from analysis, with TSDoc comments
  /** ISO 8601 creation timestamp */
  readonly created_at: string;
}
```

### src/types/api.ts

For each resource, generate request parameter types:

```typescript
/** Parameters for creating a new ${resourceName}. */
export interface Create${ResourceName}Params {
  // ... writable fields from analysis
}

/** Parameters for updating a ${resourceName}. All fields optional. */
export interface Update${ResourceName}Params {
  // ... same fields as Create, all optional (Partial)
}

/** Parameters for listing ${resourceName}s. */
export interface List${ResourceName}Params {
  /** Maximum results per page (1-100) */
  limit?: number;
  /** Cursor for pagination */
  after?: string;
  // ... additional filter fields from analysis
}
```

### Type Mapping

| API/OpenAPI Type | TypeScript Type |
|-----------------|-----------------|
| `string` | `string` |
| `string` (format: email) | `string` |
| `string` (format: date-time) | `string` |
| `string` (format: uuid) | `string` |
| `string` (format: uri) | `string` |
| `integer` / `number` | `number` |
| `boolean` | `boolean` |
| `array` of T | `T[]` |
| `enum` | String union: `'a' \| 'b' \| 'c'` |
| `object` (known schema) | Named interface |
| `object` (unknown) | `Record<string, unknown>` |
| nullable | `T \| null` |
| optional | `T \| undefined` (with `?:`) |
| readOnly | `readonly` prefix |

### src/types/index.ts

```typescript
// Models
export type { ${ResourceName} } from './models';
// ... all models

// API params
export type {
  Create${ResourceName}Params,
  Update${ResourceName}Params,
  List${ResourceName}Params,
} from './api';
// ... all params
```

### src/resources/index.ts

```typescript
export { ${ResourceName}Resource } from './${resourceName}';
// ... all resources
```

---

## Wire Resources into Client

After generating resources, update `src/client.ts`:

```typescript
import { ${ResourceName}Resource } from './resources/${resourceName}';
// ... for each resource

export class ${ClientName} {
  readonly ${resourceName}s: ${ResourceName}Resource;
  // ... for each resource

  constructor(options: ClientOptions = {}) {
    // ... existing auth + HTTP client setup

    this.${resourceName}s = new ${ResourceName}Resource(this._httpClient);
    // ... for each resource
  }
}
```

Update `src/index.ts` to export all new types:

```typescript
export { ${ClientName} } from './client';
export type { ClientOptions } from './client';

// Types
export type { ${ResourceName}, Create${ResourceName}Params, /*...*/ } from './types';

// Resources (for advanced usage)
export { ${ResourceName}Resource } from './resources';

// Errors
export {
  APIError,
  AuthenticationError,
  // ...
} from './core/errors';
```

---

## Python Resource Pattern

Generate equivalent Python resource classes:

```python
class ${ResourceName}Resource:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    async def list(self, *, limit: int = 20, after: str | None = None) -> Page[${ResourceName}]:
        ...

    async def list_auto_paging(self, **kwargs) -> AsyncIterator[${ResourceName}]:
        ...

    async def get(self, id: str) -> ${ResourceName}:
        ...

    async def create(self, params: Create${ResourceName}Params) -> ${ResourceName}:
        ...

    async def update(self, id: str, params: Update${ResourceName}Params) -> ${ResourceName}:
        ...

    async def delete(self, id: str) -> None:
        ...
```

Use Pydantic `BaseModel` for all types with `model_config = {"frozen": True}` for response models.

---

## Output

```
## Resources & Types Generated

### Resources
| Resource | Methods | File |
|----------|---------|------|
| {ResourceName} | list, get, create, update, delete | resources/{name}.ts |

### Types
| Type | Kind | File |
|------|------|------|
| {ResourceName} | Response model | types/models.ts |
| Create{ResourceName}Params | Request params | types/api.ts |

### Updated
- client.ts -- Added resource properties
- src/index.ts -- Added exports
```
