# Testing Strategy

## Testing Pyramid

```
                ┌─────────────┐
                │  E2E Tests  │  ← Live API (nightly, staging)
               ┌┴─────────────┴┐
               │ Integration    │  ← Recorded HTTP fixtures
              ┌┴───────────────┴┐
              │   Unit Tests     │  ← Mocked transport, pure logic
              └─────────────────┘
```

- **Unit tests:** Serialization, error mapping, retry logic, validation — mock the HTTP layer
- **Integration tests:** Recorded HTTP fixtures (VCR / Polly.js pattern) for full request/response cycles
- **E2E tests:** Real (staging) API on CI nightly — catches API drift

## What to Test

- Every resource method produces correct HTTP requests (method, URL, headers, body)
- Error responses map to the correct exception types
- Retry logic triggers on appropriate status codes and respects `Retry-After`
- Pagination iterators terminate correctly
- Authentication headers are set properly
- Input validation rejects invalid data before network calls
- Streaming events parse correctly
