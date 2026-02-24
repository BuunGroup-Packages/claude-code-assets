# Project Structure

```
my-api/
├── src/
│   ├── index.ts                 # Entry point — mounts app, exports default
│   ├── app.ts                   # Creates and configures the Hono app
│   ├── types.ts                 # Shared types: Bindings, Variables, AppType
│   ├── middleware/
│   │   ├── auth.ts              # Bearer/API key authentication
│   │   ├── cors.ts              # CORS configuration
│   │   ├── error-handler.ts     # Global onError handler
│   │   ├── logger.ts            # Structured JSON logging
│   │   ├── rate-limit.ts        # Rate limiting middleware
│   │   └── request-id.ts        # X-Request-Id injection
│   ├── routes/
│   │   ├── index.ts             # Barrel — mounts all route modules
│   │   ├── users.ts             # /api/users routes
│   │   ├── orders.ts            # /api/orders routes
│   │   └── health.ts            # /health & /ready endpoints
│   ├── schemas/                 # Zod schemas (shared between validation & OpenAPI)
│   │   ├── users.ts
│   │   ├── orders.ts
│   │   ├── common.ts            # Pagination, error responses, IDs
│   │   └── index.ts
│   ├── services/                # Business logic (decoupled from HTTP)
│   │   ├── user.service.ts
│   │   └── order.service.ts
│   ├── db/
│   │   ├── schema.ts            # Drizzle ORM schema definitions
│   │   ├── index.ts             # DB client factory
│   │   └── migrations/          # SQL migration files
│   └── lib/
│       ├── errors.ts            # Custom error classes
│       ├── response.ts          # Standardised response helpers
│       └── utils.ts             # Shared utilities
├── tests/
│   ├── env.d.ts                 # Test environment type declarations
│   ├── setup.ts                 # D1 migration setup for tests
│   ├── routes/
│   │   ├── users.test.ts
│   │   └── health.test.ts
│   └── services/
│       └── user.service.test.ts
├── drizzle/
│   └── migrations/              # Generated migration SQL files
├── wrangler.jsonc               # Wrangler configuration (prefer JSON over TOML)
├── drizzle.config.ts            # Drizzle Kit configuration
├── vitest.config.ts             # Vitest with Cloudflare pool
├── tsconfig.json
├── package.json
├── .dev.vars                    # Local development secrets (git-ignored)
└── .github/
    └── workflows/
        └── deploy.yml           # CI/CD pipeline
```

## Key Principles

- Routes are thin — validate, call services, return responses
- Services contain business logic and are framework-agnostic (testable without HTTP)
- Schemas are the single source of truth for validation AND OpenAPI docs
- Types are centralised in `types.ts` to avoid circular imports
