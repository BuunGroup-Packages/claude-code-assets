# Error Handling & Resilience

## Error Class Hierarchy

**TypeScript:**
```typescript
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

export class AuthenticationError extends APIError { /* 401 */ }
export class RateLimitError extends APIError {
  readonly retryAfter: number | null;
  constructor(body: ErrorBody, headers: Headers) {
    super(429, body, headers);
    this.retryAfter = parseRetryAfter(headers.get('retry-after'));
  }
}
export class BadRequestError extends APIError { /* 400 */ }
export class NotFoundError extends APIError { /* 404 */ }
export class InternalServerError extends APIError { /* 500 */ }
export class ConnectionError extends Error { /* Network failures */ }
export class TimeoutError extends Error { /* Request timeouts */ }
```

**Python:**
```python
class APIError(Exception):
    def __init__(self, message: str, *, status: int, code: str, request_id: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.request_id = request_id

class AuthenticationError(APIError): ...  # 401
class RateLimitError(APIError):           # 429
    def __init__(self, message: str, *, retry_after: float | None = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
class BadRequestError(APIError): ...      # 400
class NotFoundError(APIError): ...        # 404
class InternalServerError(APIError): ...  # 500
```

## Retry Logic with Exponential Backoff

```typescript
interface RetryConfig {
  maxRetries: number;          // Default: 2
  initialDelayMs: number;      // Default: 500
  maxDelayMs: number;          // Default: 8000
  backoffMultiplier: number;   // Default: 2
  retryableStatuses: number[]; // Default: [408, 429, 500, 502, 503, 504]
  jitter: boolean;             // Default: true
}

function calculateDelay(attempt: number, config: RetryConfig): number {
  const baseDelay = config.initialDelayMs * Math.pow(config.backoffMultiplier, attempt);
  const cappedDelay = Math.min(baseDelay, config.maxDelayMs);
  if (config.jitter) {
    const jitterRange = cappedDelay * 0.2;
    return cappedDelay - jitterRange + Math.random() * jitterRange * 2;
  }
  return cappedDelay;
}
```

**Rules:**
- Always respect `Retry-After` headers from 429 responses
- Only auto-retry idempotent requests (GET, PUT, DELETE) — POST requires idempotency keys
- Include jitter to prevent synchronized retry storms

## Timeouts

```typescript
const client = new MyAPI({
  timeout: {
    connectionMs: 5000,
    requestMs: 30000,
  },
});
```
