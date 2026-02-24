# Build Complete API

Full end-to-end API generation from requirements or context. Orchestrates all generation
in the optimal phased execution order.

## CRITICAL: Read Best Practices First

Before any generation, read:
```
.claude/assets/best-practices/hono-cf-workers/ (read relevant topic files for the current phase)
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

### Phase 1: PLAN (Sequential — Must Complete First)

Analyze the context and produce a structured API architecture plan.

If CONTEXT is provided:
- Read ALL files at the CONTEXT path
- Analyze requirements, entities, relationships, auth needs
- Produce the structured plan (see references/plan.md for format)

If no CONTEXT:
- Ask the user what the API should do
- Gather: resource names, fields, relationships, auth strategy
- Produce the plan and present for approval

IMPORTANT: Present the plan to the user and wait for approval before proceeding.

### Phase 2: SCAFFOLD (Sequential — Project Must Exist)

After plan approval, scaffold the project using references/init.md patterns:
- Initialize Hono + CF Workers project named {API_NAME}
- Configure bindings from plan

### Phase 3: FOUNDATION (Parallel — Spawn ALL in Single Message)

After scaffold completes, spawn THREE Task tools in a SINGLE message:

1. **Schemas** (references/schemas.md) — Generate Zod schemas for all resources
2. **Middleware** (references/middleware.md) — Generate middleware stack (auth, CORS, rate-limit)
3. **Database** (references/db.md) — Generate Drizzle schema and migrations

### Phase 4: LOGIC (Parallel — Depends on Phase 3)

After all Phase 3 agents complete, spawn TWO Task tools in a SINGLE message:

1. **Services** (references/services.md) — Generate service layer with business logic
2. **Routes** (references/routes.md) — Generate route modules wired to services + schemas

### Phase 5: TESTS (Sequential — Depends on Everything)

After all Phase 4 agents complete, generate test suite using references/tests.md patterns.

### Phase 6: FINALIZE (Sequential)

After tests complete, verify:
1. src/routes/index.ts mounts ALL resource routes
2. src/app.ts has ALL middleware in correct order
3. src/db/schema.ts has ALL tables
4. src/types.ts has ALL bindings from the plan
5. wrangler.jsonc has ALL binding configurations
6. package.json has correct scripts

## Sub-Agent Configuration

| Phase | Model | Purpose |
|-------|-------|---------|
| 1 | opus | Requirements analysis |
| 2 | haiku | Project scaffold |
| 3 | sonnet | Zod schemas, Middleware, Drizzle schema |
| 4 | sonnet | Business logic, Route modules |
| 5 | sonnet | Test suite |

## Error Handling

- If context has no clear resources, ask the user to clarify
- If auth strategy is unclear, default to API Key
- If no database tables needed, skip db generation
- If plan approval is declined, revise the plan based on feedback
- After generation, if `tsc --noEmit` fails, fix type errors

## Output

```
## API Build Complete

**Name**: {API_NAME}
**Stack**: Hono + Cloudflare Workers + D1 + Drizzle ORM
**Auth**: {AUTH_STRATEGY}
**Bindings**: {D1, KV, R2, Rate Limit}

### Architecture Plan
- Resources: {count}
- Endpoints: {count}
- Tables: {count}
- Middleware: {count} layers

### Resources
| Resource | Endpoints | Path |
|----------|-----------|------|
| health | GET /health, GET /ready | /api/ |
| {name} | GET, POST, PUT, DELETE | /api/{name} |

### Generated Structure
{FULL_DIRECTORY_TREE}

### Quick Start
\`\`\`bash
cd {API_NAME}
npm install
npx wrangler d1 create {API_NAME}-db
# Copy database_id to wrangler.jsonc
echo "API_KEY=dev-key-12345" > .dev.vars
npm run db:migrate:local
npm run dev
\`\`\`

### Test
\`\`\`bash
npm test
\`\`\`

### Deploy
\`\`\`bash
npx wrangler secret put API_KEY
npm run db:migrate:prod
npm run deploy
\`\`\`

### RPC Client
\`\`\`typescript
import { hc } from 'hono/client'
import type { AppType } from './{API_NAME}/src/app'

const client = hc<AppType>('http://localhost:8787')
const res = await client.api.{resource}.$get({ query: { page: '1' } })
\`\`\`
```
