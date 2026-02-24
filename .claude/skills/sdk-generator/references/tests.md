# Generate SDK Test Scaffolding

Generate comprehensive test files following the SDK testing pyramid:
- Unit tests for core modules (errors, retry, auth, HTTP client)
- Unit tests for each resource (mocked HTTP transport)
- Integration test fixtures (recorded HTTP responses)

Follow patterns from:
```
.claude/skills/sdk-generator/docs/PATTERNS.md
.claude/assets/best-practices/sdk/testing.md
```

## Workflow

1. Generate core unit tests (errors, retry, auth)
2. Generate HTTP client unit tests with mocked fetch
3. Generate resource tests for each resource
4. Generate integration test helper and fixtures
5. Generate example test for consumer usage

---

## TypeScript Test Files

### tests/unit/core/errors.test.ts

```typescript
import { describe, it, expect } from 'vitest';
import {
  APIError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  BadRequestError,
  mapStatusToError,
} from '../../../src/core/errors';

describe('Error Classes', () => {
  const mockHeaders = new Headers({ 'x-request-id': 'req_123' });
  const mockBody = { message: 'Something went wrong', code: 'error_code' };

  it('creates APIError with correct properties', () => {
    const error = new APIError(500, mockBody, mockHeaders);
    expect(error.status).toBe(500);
    expect(error.code).toBe('error_code');
    expect(error.message).toBe('Something went wrong');
    expect(error.requestId).toBe('req_123');
    expect(error.name).toBe('APIError');
    expect(error).toBeInstanceOf(Error);
  });

  it('creates AuthenticationError for 401', () => {
    const error = new AuthenticationError(mockBody, mockHeaders);
    expect(error.status).toBe(401);
    expect(error.name).toBe('AuthenticationError');
    expect(error).toBeInstanceOf(APIError);
  });

  it('creates RateLimitError with retryAfter', () => {
    const headers = new Headers({
      'x-request-id': 'req_123',
      'retry-after': '30',
    });
    const error = new RateLimitError(mockBody, headers);
    expect(error.status).toBe(429);
    expect(error.retryAfter).toBe(30000);
  });

  it('maps status codes to correct error types', () => {
    expect(mapStatusToError(400, mockBody, mockHeaders)).toBeInstanceOf(BadRequestError);
    expect(mapStatusToError(401, mockBody, mockHeaders)).toBeInstanceOf(AuthenticationError);
    expect(mapStatusToError(404, mockBody, mockHeaders)).toBeInstanceOf(NotFoundError);
    expect(mapStatusToError(429, mockBody, mockHeaders)).toBeInstanceOf(RateLimitError);
  });
});
```

### tests/unit/core/retry.test.ts

```typescript
import { describe, it, expect } from 'vitest';
import {
  calculateDelay,
  isRetryable,
  DEFAULT_RETRY_CONFIG,
} from '../../../src/core/retry';

describe('Retry Logic', () => {
  it('calculates exponential backoff', () => {
    const config = { ...DEFAULT_RETRY_CONFIG, jitter: false };
    expect(calculateDelay(0, config)).toBe(500);
    expect(calculateDelay(1, config)).toBe(1000);
    expect(calculateDelay(2, config)).toBe(2000);
  });

  it('caps delay at maxDelayMs', () => {
    const config = { ...DEFAULT_RETRY_CONFIG, jitter: false };
    expect(calculateDelay(10, config)).toBe(config.maxDelayMs);
  });

  it('adds jitter when enabled', () => {
    const delays = Array.from({ length: 100 }, () =>
      calculateDelay(0, DEFAULT_RETRY_CONFIG),
    );
    const unique = new Set(delays);
    expect(unique.size).toBeGreaterThan(1);
  });

  it('retries idempotent methods on retryable statuses', () => {
    expect(isRetryable('GET', 500, DEFAULT_RETRY_CONFIG)).toBe(true);
    expect(isRetryable('PUT', 503, DEFAULT_RETRY_CONFIG)).toBe(true);
    expect(isRetryable('DELETE', 429, DEFAULT_RETRY_CONFIG)).toBe(true);
  });

  it('does not retry POST requests', () => {
    expect(isRetryable('POST', 500, DEFAULT_RETRY_CONFIG)).toBe(false);
  });

  it('does not retry non-retryable statuses', () => {
    expect(isRetryable('GET', 400, DEFAULT_RETRY_CONFIG)).toBe(false);
    expect(isRetryable('GET', 401, DEFAULT_RETRY_CONFIG)).toBe(false);
    expect(isRetryable('GET', 404, DEFAULT_RETRY_CONFIG)).toBe(false);
  });
});
```

### tests/unit/core/auth.test.ts

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { resolveAuth, validateAuth } from '../../../src/core/auth';

describe('Auth', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it('uses explicit API key', () => {
    const auth = resolveAuth({ apiKey: 'sk_test_123' });
    expect(auth.apiKey).toBe('sk_test_123');
  });

  it('falls back to environment variable', () => {
    process.env.${ENV_VAR} = 'sk_env_456';
    const auth = resolveAuth({});
    expect(auth.apiKey).toBe('sk_env_456');
  });

  it('throws when no auth configured', () => {
    delete process.env.${ENV_VAR};
    expect(() => validateAuth(resolveAuth({}))).toThrow('Missing API key');
  });
});
```

Replace `${ENV_VAR}` with the actual env var name from the analysis.

### tests/unit/resources/{resource}.test.ts

For each resource, generate:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ${ResourceName}Resource } from '../../../src/resources/${resourceName}';
import type { HTTPClient } from '../../../src/core';

function createMockClient(): HTTPClient {
  return {
    request: vi.fn(),
  } as unknown as HTTPClient;
}

describe('${ResourceName}Resource', () => {
  let client: HTTPClient;
  let resource: ${ResourceName}Resource;

  beforeEach(() => {
    client = createMockClient();
    resource = new ${ResourceName}Resource(client);
  });

  describe('list', () => {
    it('sends GET request to /${resourcePath}', async () => {
      const mockResponse = {
        data: { data: [], has_more: false, next_cursor: null },
        status: 200,
        headers: new Headers(),
        requestId: 'req_123',
      };
      vi.mocked(client.request).mockResolvedValue(mockResponse);

      const result = await resource.list();

      expect(client.request).toHaveBeenCalledWith({
        method: 'GET',
        path: '/${resourcePath}',
        query: undefined,
      });
      expect(result.data).toEqual([]);
    });

    it('passes pagination params as query', async () => {
      const mockResponse = {
        data: { data: [], has_more: false, next_cursor: null },
        status: 200,
        headers: new Headers(),
        requestId: 'req_123',
      };
      vi.mocked(client.request).mockResolvedValue(mockResponse);

      await resource.list({ limit: 10, after: 'cursor_abc' });

      expect(client.request).toHaveBeenCalledWith(
        expect.objectContaining({
          query: expect.objectContaining({ limit: 10, after: 'cursor_abc' }),
        }),
      );
    });
  });

  describe('get', () => {
    it('sends GET request to /${resourcePath}/:id', async () => {
      const mockItem = { id: 'id_123', name: 'Test' };
      vi.mocked(client.request).mockResolvedValue({
        data: mockItem,
        status: 200,
        headers: new Headers(),
        requestId: 'req_123',
      });

      const result = await resource.get('id_123');

      expect(client.request).toHaveBeenCalledWith({
        method: 'GET',
        path: '/${resourcePath}/id_123',
      });
      expect(result).toEqual(mockItem);
    });
  });

  describe('create', () => {
    it('sends POST request with body', async () => {
      const params = { name: 'New Item' };
      const mockItem = { id: 'id_456', ...params };
      vi.mocked(client.request).mockResolvedValue({
        data: mockItem,
        status: 201,
        headers: new Headers(),
        requestId: 'req_123',
      });

      const result = await resource.create(params);

      expect(client.request).toHaveBeenCalledWith({
        method: 'POST',
        path: '/${resourcePath}',
        body: params,
      });
      expect(result.id).toBe('id_456');
    });
  });

  describe('update', () => {
    it('sends PUT request with body', async () => {
      const params = { name: 'Updated' };
      vi.mocked(client.request).mockResolvedValue({
        data: { id: 'id_123', ...params },
        status: 200,
        headers: new Headers(),
        requestId: 'req_123',
      });

      await resource.update('id_123', params);

      expect(client.request).toHaveBeenCalledWith({
        method: 'PUT',
        path: '/${resourcePath}/id_123',
        body: params,
      });
    });
  });

  describe('delete', () => {
    it('sends DELETE request', async () => {
      vi.mocked(client.request).mockResolvedValue({
        data: undefined,
        status: 204,
        headers: new Headers(),
        requestId: 'req_123',
      });

      await resource.delete('id_123');

      expect(client.request).toHaveBeenCalledWith({
        method: 'DELETE',
        path: '/${resourcePath}/id_123',
      });
    });
  });
});
```

### tests/integration/api.test.ts

```typescript
import { describe, it, expect } from 'vitest';

/**
 * Integration tests against a live or recorded API.
 *
 * To run against live API:
 *   ${ENV_VAR}=sk_test_xxx npm run test -- tests/integration/
 *
 * TODO: Add VCR/Polly.js recording for CI.
 */
describe.skip('Integration: ${API_NAME}', () => {
  // Unskip and configure when ready for integration testing

  it('lists resources', async () => {
    // const client = new ${ClientName}();
    // const page = await client.${resourceName}s.list({ limit: 1 });
    // expect(page.data).toBeDefined();
    // expect(Array.isArray(page.data)).toBe(true);
  });
});
```

### examples/basic-usage.ts

```typescript
import { ${ClientName} } from '../src';

async function main() {
  const client = new ${ClientName}();

  // List
  const page = await client.${resourceName}s.list({ limit: 10 });
  console.log('Items:', page.data.length);

  // Create
  // const item = await client.${resourceName}s.create({ name: 'Example' });
  // console.log('Created:', item.id);

  // Auto-paginate
  // for await (const item of client.${resourceName}s.listAutoPaging()) {
  //   console.log(item);
  // }
}

main().catch(console.error);
```

---

## Python Test Equivalents

Generate equivalent tests using `pytest` and `pytest-asyncio`:
- `tests/unit/core/test_errors.py`
- `tests/unit/core/test_retry.py`
- `tests/unit/core/test_auth.py`
- `tests/unit/resources/test_{resource}.py`
- `tests/integration/test_api.py`

Use `pytest-httpx` to mock HTTP responses.

---

## Output

```
## Test Scaffolding Generated

### Unit Tests
| File | Tests | Covers |
|------|-------|--------|
| core/errors.test.ts | {count} | Error class hierarchy |
| core/retry.test.ts | {count} | Backoff, jitter, retryable checks |
| core/auth.test.ts | {count} | Auth resolution, env vars |
| resources/{name}.test.ts | {count} | HTTP methods, params |

### Integration
| File | Status |
|------|--------|
| integration/api.test.ts | Scaffold (skipped) |

### Examples
| File | Description |
|------|-------------|
| basic-usage.ts | Quick start example |

### Run Tests
\`\`\`bash
npm test              # Run all unit tests
npm run test:watch    # Watch mode
\`\`\`
```
