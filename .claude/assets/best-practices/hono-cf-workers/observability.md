# Observability & Logging

## Workers Logs (Native Cloudflare)

```jsonc
// wrangler.jsonc
"observability": {
  "enabled": true,
  "head_sampling_rate": 1
}
```

## Structured Logging

```typescript
// Always log as structured JSON — Workers Logs auto-indexes fields
console.log(JSON.stringify({
  level: 'info',
  event: 'user_created',
  user_id: user.id,
  email: user.email,
  request_id: c.get('requestId'),
  duration_ms: Date.now() - c.get('startTime'),
}))

// For errors, include stack traces
console.error(JSON.stringify({
  level: 'error',
  event: 'database_error',
  error: err.message,
  stack: err.stack,
  request_id: c.get('requestId'),
  path: c.req.path,
}))
```

## OpenTelemetry Tracing (Beta)

```jsonc
"observability": {
  "enabled": true,
  "head_sampling_rate": 1,
  "traces": { "enabled": true }
}
```

Compatible with Honeycomb, Grafana Cloud, Axiom, Datadog.

## Useful Dashboard Queries

```sql
-- P90 latency by endpoint
SELECT percentile(duration_ms, 90), path GROUP BY path

-- Error rate over time
SELECT count(*) WHERE level = 'error' GROUP BY time(1h)

-- Slowest requests
SELECT * WHERE duration_ms > 1000 ORDER BY duration_ms DESC LIMIT 50
```
