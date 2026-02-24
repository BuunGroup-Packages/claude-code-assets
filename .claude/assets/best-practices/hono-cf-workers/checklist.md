# Production Checklist & Gotchas

## Before First Deploy

- [ ] `wrangler.jsonc` has correct `compatibility_date` (use latest)
- [ ] `nodejs_compat` flag enabled if using any Node.js APIs
- [ ] `observability.enabled = true` with appropriate `head_sampling_rate`
- [ ] All secrets set via `wrangler secret put`
- [ ] D1 database created and ID in config
- [ ] KV namespace created and ID in config (if used)
- [ ] R2 bucket created and name in config (if used)
- [ ] Rate limiter bindings configured
- [ ] `.dev.vars` created for local secrets, added to `.gitignore`
- [ ] Health check endpoint (`/health`, `/ready`) implemented
- [ ] CORS configured with specific origins (not `*` in production)
- [ ] Error handler returns consistent JSON envelope
- [ ] All routes have Zod validation on inputs
- [ ] Types generated with `wrangler types`

## Before Every Deploy

- [ ] `npm run typecheck` passes
- [ ] `npm test` passes
- [ ] D1 migrations applied to target environment
- [ ] No `console.log` of sensitive data

## Environment & Config Gotchas

| Gotcha | Fix |
|--------|-----|
| `process.env` is undefined | Use `c.env.MY_VAR` — Workers don't have `process.env` by default |
| Bindings not in staging env | Bindings are NOT inheritable — redeclare in every `env` section |
| `.dev.vars` not loading | Must be in project root, dotenv syntax, no quotes around values |
| Secrets not in wrangler.jsonc | Use `wrangler secret put NAME` — never in config files |

## Hono Pattern Gotchas

| Gotcha | Fix |
|--------|-----|
| RPC types not inferring | Chain methods: `new Hono().get(...).post(...)` — not separate calls |
| Path params not typed | Write inline handlers, don't extract to "controller" functions |
| CORS not working | Register CORS middleware BEFORE route handlers |
| Header key not found | Hono normalises to lowercase: use `idempotency-key` not `Idempotency-Key` |
| Query params returning string | Use `z.coerce.number()` for numeric query params |

## D1 & Database Gotchas

| Gotcha | Fix |
|--------|-----|
| D1 is SQLite, not Postgres | No `ALTER COLUMN`, limited `JOIN` syntax |
| Migration rollback not supported | Generate a new migration with manual reverse SQL |
| `datetime('now')` is UTC | Convert on the client side |
| D1 size limit: 10GB | Partition large datasets across multiple databases |

## Cloudflare Workers Limits

| Limit | Free | Paid |
|-------|------|------|
| Requests/day | 100,000 | Unlimited |
| CPU time/request | 10ms | 30s |
| Memory | 128MB | 128MB |
| Script size | 3MB | 10MB |
| Subrequests/request | 50 | 1,000 |

## Deployment Gotchas

| Gotcha | Fix |
|--------|-----|
| "cannot find module" on deploy | Ensure deps are in `dependencies`, not just `devDependencies` |
| Wrangler types stale | Run `wrangler types` after changing wrangler.jsonc bindings |
| Safe rollbacks | Use `wrangler deployments` and `wrangler rollback` |
