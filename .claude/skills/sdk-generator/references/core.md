# Generate SDK Core Infrastructure

Generate the core modules that every SDK needs. These are the foundational building
blocks that resource classes depend on.

Follow patterns from:
```
.claude/skills/sdk-generator/docs/PATTERNS.md
.claude/assets/best-practices/sdk/errors.md and .claude/assets/best-practices/sdk/http-client.md
```

## Workflow

1. Generate error class hierarchy
2. Generate HTTP client abstraction
3. Generate authentication handler
4. Generate retry logic
5. Generate pagination helpers
6. Generate barrel exports
7. Generate main client class

---

## TypeScript Core Modules

### src/core/errors.ts

```typescript
export interface ErrorBody {
  message: string;
  code: string;
  type?: string;
}

function parseRetryAfter(value: string | null): number | null {
  if (!value) return null;
  const seconds = Number(value);
  if (!Number.isNaN(seconds)) return seconds * 1000;
  const date = Date.parse(value);
  if (!Number.isNaN(date)) return date - Date.now();
  return null;
}

export class APIError extends Error {
  readonly status: number;
  readonly code: string;
  readonly requestId: string;
  readonly headers: Headers;

  constructor(status: number, body: ErrorBody, headers: Headers) {
    super(body.message);
    this.name = 'APIError';
    this.status = status;
    this.code = body.code;
    this.requestId = headers.get('x-request-id') ?? '';
    this.headers = headers;
  }
}

export class AuthenticationError extends APIError {
  constructor(body: ErrorBody, headers: Headers) {
    super(401, body, headers);
    this.name = 'AuthenticationError';
  }
}

export class PermissionError extends APIError {
  constructor(body: ErrorBody, headers: Headers) {
    super(403, body, headers);
    this.name = 'PermissionError';
  }
}

export class NotFoundError extends APIError {
  constructor(body: ErrorBody, headers: Headers) {
    super(404, body, headers);
    this.name = 'NotFoundError';
  }
}

export class BadRequestError extends APIError {
  constructor(body: ErrorBody, headers: Headers) {
    super(400, body, headers);
    this.name = 'BadRequestError';
  }
}

export class RateLimitError extends APIError {
  readonly retryAfter: number | null;

  constructor(body: ErrorBody, headers: Headers) {
    super(429, body, headers);
    this.name = 'RateLimitError';
    this.retryAfter = parseRetryAfter(headers.get('retry-after'));
  }
}

export class InternalServerError extends APIError {
  constructor(body: ErrorBody, headers: Headers) {
    super(500, body, headers);
    this.name = 'InternalServerError';
  }
}

export class ConnectionError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = 'ConnectionError';
  }
}

export class TimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
  }
}

export function mapStatusToError(
  status: number,
  body: ErrorBody,
  headers: Headers,
): APIError {
  switch (status) {
    case 400: return new BadRequestError(body, headers);
    case 401: return new AuthenticationError(body, headers);
    case 403: return new PermissionError(body, headers);
    case 404: return new NotFoundError(body, headers);
    case 429: return new RateLimitError(body, headers);
    case 500: return new InternalServerError(body, headers);
    default: return new APIError(status, body, headers);
  }
}
```

### src/core/retry.ts

```typescript
export interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableStatuses: number[];
  jitter: boolean;
}

export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 2,
  initialDelayMs: 500,
  maxDelayMs: 8000,
  backoffMultiplier: 2,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  jitter: true,
};

export function calculateDelay(attempt: number, config: RetryConfig): number {
  const baseDelay = config.initialDelayMs * Math.pow(config.backoffMultiplier, attempt);
  const cappedDelay = Math.min(baseDelay, config.maxDelayMs);

  if (config.jitter) {
    const jitterRange = cappedDelay * 0.2;
    return cappedDelay - jitterRange + Math.random() * jitterRange * 2;
  }
  return cappedDelay;
}

export function isRetryable(method: string, status: number, config: RetryConfig): boolean {
  const idempotentMethods = ['GET', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'];
  if (!idempotentMethods.includes(method.toUpperCase())) return false;
  return config.retryableStatuses.includes(status);
}

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

### src/core/http-client.ts

```typescript
import { VERSION } from '../version';
import { mapStatusToError, ConnectionError, TimeoutError } from './errors';
import type { ErrorBody } from './errors';
import { DEFAULT_RETRY_CONFIG, calculateDelay, isRetryable, sleep } from './retry';
import type { RetryConfig } from './retry';

export interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  path: string;
  headers?: Record<string, string>;
  body?: unknown;
  query?: Record<string, string | number | boolean | undefined>;
  timeout?: number;
  signal?: AbortSignal;
  idempotencyKey?: string;
}

export interface APIResponse<T> {
  data: T;
  status: number;
  headers: Headers;
  requestId: string;
}

export interface HTTPClientOptions {
  baseURL: string;
  apiKey?: string;
  bearerToken?: string;
  timeout?: number;
  retry?: Partial<RetryConfig>;
  headers?: Record<string, string>;
}

export class HTTPClient {
  private readonly baseURL: string;
  private readonly apiKey: string | undefined;
  private readonly bearerToken: string | undefined;
  private readonly timeout: number;
  private readonly retryConfig: RetryConfig;
  private readonly customHeaders: Record<string, string>;

  constructor(options: HTTPClientOptions) {
    this.baseURL = options.baseURL.replace(/\/+$/, '');
    this.apiKey = options.apiKey;
    this.bearerToken = options.bearerToken;
    this.timeout = options.timeout ?? 30000;
    this.retryConfig = { ...DEFAULT_RETRY_CONFIG, ...options.retry };
    this.customHeaders = options.headers ?? {};
  }

  async request<T>(config: RequestConfig): Promise<APIResponse<T>> {
    const url = this.buildURL(config.path, config.query);
    const headers = this.buildHeaders(config.headers, config.idempotencyKey);

    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= this.retryConfig.maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(
          () => controller.abort(),
          config.timeout ?? this.timeout,
        );

        const response = await fetch(url, {
          method: config.method,
          headers,
          body: config.body ? JSON.stringify(config.body) : undefined,
          signal: config.signal ?? controller.signal,
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          const body = await response.json().catch(() => ({
            message: response.statusText,
            code: 'unknown_error',
          })) as ErrorBody;

          const error = mapStatusToError(response.status, body, response.headers);

          if (attempt < this.retryConfig.maxRetries &&
              isRetryable(config.method, response.status, this.retryConfig)) {
            const retryAfter = response.headers.get('retry-after');
            const delay = retryAfter
              ? Number(retryAfter) * 1000
              : calculateDelay(attempt, this.retryConfig);
            await sleep(delay);
            lastError = error;
            continue;
          }

          throw error;
        }

        const data = response.status === 204
          ? (undefined as T)
          : (await response.json() as T);

        return {
          data,
          status: response.status,
          headers: response.headers,
          requestId: response.headers.get('x-request-id') ?? '',
        };
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') {
          throw new TimeoutError(`Request timed out after ${config.timeout ?? this.timeout}ms`);
        }
        if (error instanceof TypeError && error.message.includes('fetch')) {
          if (attempt < this.retryConfig.maxRetries) {
            await sleep(calculateDelay(attempt, this.retryConfig));
            lastError = new ConnectionError('Network request failed', error);
            continue;
          }
          throw new ConnectionError('Network request failed', error);
        }
        throw error;
      }
    }

    throw lastError ?? new Error('Request failed after retries');
  }

  private buildURL(
    path: string,
    query?: Record<string, string | number | boolean | undefined>,
  ): string {
    const url = new URL(`${this.baseURL}${path}`);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value !== undefined) {
          url.searchParams.set(key, String(value));
        }
      }
    }
    return url.toString();
  }

  private buildHeaders(
    custom?: Record<string, string>,
    idempotencyKey?: string,
  ): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'User-Agent': `${SDK_NAME}/typescript/${VERSION}`,
      'X-SDK-Version': VERSION,
      'X-SDK-Language': 'typescript',
      ...this.customHeaders,
      ...custom,
    };

    // Auth: adapt based on AUTH_STRATEGY from analysis
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    } else if (this.bearerToken) {
      headers['Authorization'] = `Bearer ${this.bearerToken}`;
    }

    if (idempotencyKey) {
      headers['Idempotency-Key'] = idempotencyKey;
    }

    return headers;
  }
}
```

IMPORTANT: Replace `SDK_NAME` in the `User-Agent` header with the actual SDK name from context.
Adapt the auth header pattern based on the analysis report's AUTH_STRATEGY.

### src/core/pagination.ts

```typescript
export interface Page<T> {
  data: T[];
  has_more: boolean;
  next_cursor: string | null;
}

export interface PaginationParams {
  limit?: number;
  after?: string;
}
```

Adapt the `Page` interface fields based on the analysis report's PAGINATION_STRATEGY.

### src/core/auth.ts

```typescript
export interface AuthConfig {
  apiKey?: string;
  bearerToken?: string;
}

export function resolveAuth(config: AuthConfig): AuthConfig {
  return {
    apiKey: config.apiKey ?? process.env.${ENV_VAR},
    bearerToken: config.bearerToken,
  };
}

export function validateAuth(config: AuthConfig): void {
  if (!config.apiKey && !config.bearerToken) {
    throw new Error(
      'Missing API key. Pass { apiKey } to the constructor or set the ${ENV_VAR} environment variable.',
    );
  }
}
```

Replace `${ENV_VAR}` with the actual env var name from the analysis report.

### src/core/index.ts

```typescript
export { HTTPClient } from './http-client';
export type { HTTPClientOptions, RequestConfig, APIResponse } from './http-client';
export { DEFAULT_RETRY_CONFIG } from './retry';
export type { RetryConfig } from './retry';
export type { Page, PaginationParams } from './pagination';
export { resolveAuth, validateAuth } from './auth';
export type { AuthConfig } from './auth';
export {
  APIError,
  AuthenticationError,
  PermissionError,
  NotFoundError,
  BadRequestError,
  RateLimitError,
  InternalServerError,
  ConnectionError,
  TimeoutError,
} from './errors';
```

### src/client.ts

```typescript
import { HTTPClient } from './core/http-client';
import { resolveAuth, validateAuth } from './core/auth';
import type { RetryConfig } from './core/retry';
// Resource imports will be added by resources generation step

export interface ClientOptions {
  apiKey?: string;
  bearerToken?: string;
  baseURL?: string;
  timeout?: number;
  retry?: Partial<RetryConfig>;
  headers?: Record<string, string>;
}

export class ${ClientName} {
  private readonly _httpClient: HTTPClient;
  // Resource properties will be added by resources generation step

  constructor(options: ClientOptions = {}) {
    const auth = resolveAuth({
      apiKey: options.apiKey,
      bearerToken: options.bearerToken,
    });
    validateAuth(auth);

    this._httpClient = new HTTPClient({
      baseURL: options.baseURL ?? '${BASE_URL}',
      apiKey: auth.apiKey,
      bearerToken: auth.bearerToken,
      timeout: options.timeout,
      retry: options.retry,
      headers: options.headers,
    });

    // Resource initialization will be added by resources generation step
  }
}
```

Replace `${ClientName}` with PascalCase API name + "Client" (e.g., `MyAPIClient`).
Replace `${BASE_URL}` with the base URL from the analysis report.

---

## Python Core Modules

Generate equivalent Python modules following the same patterns:

- `_core/_errors.py` -- Exception hierarchy with `APIError` base class
- `_core/_retry.py` -- Retry with exponential backoff and jitter
- `_core/_http_client.py` -- `httpx.AsyncClient` wrapper with retry
- `_core/_pagination.py` -- `Page[T]` generic Pydantic model
- `_core/_auth.py` -- Auth resolution from env vars
- `_core/__init__.py` -- Public re-exports
- `_client.py` -- Main client class

Use `httpx` for HTTP, `pydantic` for models, Google-style docstrings.
Prefix internal modules with `_`.

---

## Output

```
## Core Infrastructure Generated

### Modules
- core/errors.ts -- Error class hierarchy (9 error types)
- core/retry.ts -- Exponential backoff with jitter
- core/http-client.ts -- Transport abstraction with retry
- core/pagination.ts -- Page<T> generic type
- core/auth.ts -- Auth resolution from env vars
- core/index.ts -- Barrel exports
- client.ts -- Main client class (awaiting resources)
```
