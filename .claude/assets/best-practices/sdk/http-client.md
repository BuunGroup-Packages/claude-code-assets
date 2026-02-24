# HTTP Client & Transport Layer

## Transport Abstraction

Decouple your SDK from any specific HTTP client library:

```typescript
export interface HTTPClient {
  request<T>(config: RequestConfig): Promise<APIResponse<T>>;
}

export interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  url: string;
  headers?: Record<string, string>;
  body?: unknown;
  query?: Record<string, string | number | boolean | undefined>;
  timeout?: number;
  signal?: AbortSignal;
}

export interface APIResponse<T> {
  data: T;
  status: number;
  headers: Headers;
  requestId: string;
}
```

**Why abstract:**
- Consumers can swap in their own HTTP client (corporate proxy, custom TLS, mocking)
- Testability — mock the transport without touching network
- Platform flexibility — works in Node.js, Bun, Deno, and browsers

## Default Headers

```typescript
private buildHeaders(custom: Record<string, string> = {}): Record<string, string> {
  return {
    'Authorization': `Bearer ${this.apiKey}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': `my-sdk/typescript/${VERSION}`,
    'X-SDK-Version': VERSION,
    'X-SDK-Language': 'typescript',
    ...custom,
  };
}
```

Always include `User-Agent` with SDK language and version — helps API providers debug and track adoption.
