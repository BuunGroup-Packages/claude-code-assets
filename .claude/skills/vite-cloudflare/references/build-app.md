# Build Full-Stack App

Orchestrate parallel sub-agents to scaffold a complete Vite + React + Cloudflare Workers app.

## CRITICAL: Parallel Execution Required

This command MUST spawn multiple sub-agents in PARALLEL using a single message with multiple Task tool calls.

## Workflow

Parse `$ARGUMENTS` to get APP_NAME, then spawn ALL of these Task tools in a SINGLE message:

1. **vite-cloudflare init** (haiku) -- Initialize project named {APP_NAME}
2. **vite-cloudflare binding** (haiku) -- Add D1 database binding named DB
3. **api-generator init** (haiku) -- Initialize the Hono API worker structure following best practices
4. **vite-cloudflare page** (haiku) -- Create home page with components

## API Delegation

API generation is handled by the `api-generator` skill, NOT by vite-cloudflare. This ensures:
- Proper service layer (routes are thin, services contain business logic)
- Drizzle ORM for database access (not raw D1 prepare/bind)
- Structured error handling with custom error classes
- Middleware stack (request-id, logger, CORS, rate-limit, auth)
- Production patterns from `.claude/assets/best-practices/hono-cf-workers/`

## Example Execution

For `/vite-cloudflare build-app my-saas`:

```
// Spawn ALL in a SINGLE message:

Task(model: "haiku", prompt: "Read .claude/skills/vite-cloudflare/references/init.md. Initialize Vite + React + Cloudflare project named my-saas.")

Task(model: "haiku", prompt: "Read .claude/skills/vite-cloudflare/references/binding.md. Add D1 database binding named DB for project my-saas.")

Task(model: "haiku", prompt: "Read .claude/skills/api-generator/references/init.md and .claude/assets/best-practices/hono-cf-workers/project-structure.md. Initialize Hono API for project my-saas with health route.")

Task(model: "haiku", prompt: "Read .claude/skills/vite-cloudflare/references/page.md. Create home page with --with-components for project my-saas.")
```

## Output

After all agents complete, summarize:

```
## Full-Stack App Created

**Name**: {APP_NAME}
**Stack**: Vite 6 + React 19 + Cloudflare Workers + Hono

### Sub-Agents Spawned (Parallel)
1. vite-cloudflare init - Project scaffold
2. vite-cloudflare binding - D1 database
3. api-generator init - API with best practices
4. vite-cloudflare page - Home page

### Next Steps
\`\`\`bash
cd {APP_NAME}
npm install
wrangler d1 create {APP_NAME}-db  # Get ID
# Update wrangler.jsonc with database_id
npm run dev
\`\`\`

### Add Features
\`\`\`bash
/vite-cloudflare add-feature users
/vite-cloudflare add-feature products
\`\`\`
```
