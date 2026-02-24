# Hono + Cloudflare Workers Best Practices

Topic files for building production APIs with Hono on Cloudflare Workers.

| File | Topic |
|------|-------|
| [project-structure.md](project-structure.md) | File layout, entry point, app factory |
| [wrangler-config.md](wrangler-config.md) | `wrangler.jsonc` setup, environments, secrets |
| [types-bindings.md](types-bindings.md) | Type-safe bindings, variables, `AppEnv` |
| [routes.md](routes.md) | Route architecture, chaining, barrel, health checks |
| [validation.md](validation.md) | Zod schemas, custom error formatting, gotchas |
| [openapi.md](openapi.md) | chanfana vs `@hono/zod-openapi`, auto-generated docs |
| [middleware.md](middleware.md) | Execution order, CORS, request-id, logger, secure headers |
| [errors.md](errors.md) | Error classes, global handler, response helpers |
| [database.md](database.md) | D1 + Drizzle ORM schema, service layer, migrations |
| [auth.md](auth.md) | API key, JWT, optional auth, security practices |
| [rate-limiting.md](rate-limiting.md) | Native CF rate limiting, `@elithrar` helper |
| [rpc-client.md](rpc-client.md) | End-to-end type safety, monorepo setup |
| [testing.md](testing.md) | Vitest + CF pool, route tests, service tests |
| [observability.md](observability.md) | Workers Logs, structured logging, OpenTelemetry |
| [deployment.md](deployment.md) | CI/CD, GitHub Actions, package scripts |
| [checklist.md](checklist.md) | Production checklist, gotchas, limits |
