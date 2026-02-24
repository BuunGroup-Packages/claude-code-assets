# Wrangler Configuration

Use `wrangler.jsonc` (JSON with comments) as the source of truth. Prefer JSON over TOML for better tooling support.

```jsonc
// wrangler.jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-api",
  "main": "src/index.ts",
  "compatibility_date": "2025-04-01",
  "compatibility_flags": ["nodejs_compat"],

  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  },

  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-api-db",
      "database_id": "YOUR_DATABASE_ID",
      "migrations_dir": "drizzle/migrations"
    }
  ],

  "kv_namespaces": [
    { "binding": "KV", "id": "YOUR_KV_NAMESPACE_ID" }
  ],

  "r2_buckets": [
    { "binding": "BUCKET", "bucket_name": "my-api-uploads" }
  ],

  "rate_limits": [
    {
      "binding": "RATE_LIMITER",
      "namespace_id": "1001",
      "simple": { "limit": 100, "period": 60 }
    },
    {
      "binding": "RATE_LIMITER_STRICT",
      "namespace_id": "1002",
      "simple": { "limit": 10, "period": 60 }
    }
  ],

  "vars": {
    "ENVIRONMENT": "production",
    "API_VERSION": "v1",
    "LOG_LEVEL": "info"
  },

  "env": {
    "staging": {
      "name": "my-api-staging",
      "vars": {
        "ENVIRONMENT": "staging",
        "LOG_LEVEL": "debug"
      },
      "d1_databases": [
        {
          "binding": "DB",
          "database_name": "my-api-db-staging",
          "database_id": "YOUR_STAGING_DB_ID",
          "migrations_dir": "drizzle/migrations"
        }
      ],
      "kv_namespaces": [
        { "binding": "KV", "id": "YOUR_STAGING_KV_ID" }
      ]
    }
  }
}
```

## Critical Notes

- `compatibility_date` determines which Workers runtime features are available — always use a recent date
- `nodejs_compat` enables Node.js APIs (Buffer, crypto, etc.) — required for most ORMs
- Bindings are **not inheritable** across environments — you MUST redeclare them in each `env`
- Secrets (`wrangler secret put API_KEY`) are separate from `vars` and never appear in the config file
- For local dev, use `.dev.vars` file for secrets (never committed to git)
