# CI/CD & Deployment

## GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy API

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run typecheck
      - run: npm run lint
      - run: npm test

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - name: Migrate D1 (staging)
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: d1 migrations apply my-api-db-staging --env staging --remote
      - name: Deploy (staging)
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env staging

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - name: Migrate D1 (production)
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: d1 migrations apply my-api-db --remote
      - name: Deploy (production)
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy
```

## Package Scripts

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "dev:remote": "wrangler dev --remote",
    "deploy": "wrangler deploy",
    "deploy:staging": "wrangler deploy --env staging",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src/",
    "test": "vitest run",
    "test:watch": "vitest",
    "db:generate": "drizzle-kit generate",
    "db:migrate:local": "wrangler d1 migrations apply my-api-db --local",
    "db:migrate:prod": "wrangler d1 migrations apply my-api-db --remote",
    "db:studio": "drizzle-kit studio",
    "cf-typegen": "wrangler types"
  }
}
```

## Quick-Start

```bash
npm create hono@latest my-api -- --template cloudflare-workers
cd my-api
npm install zod @hono/zod-validator drizzle-orm
npm install -D drizzle-kit @cloudflare/vitest-pool-workers vitest
npx wrangler d1 create my-api-db       # Copy database_id to wrangler.jsonc
npx wrangler kv namespace create KV     # Copy id to wrangler.jsonc
npx wrangler secret put API_KEY
npx wrangler secret put JWT_SECRET
npx wrangler types
echo "API_KEY=dev-key-12345" > .dev.vars
npm run dev
```

## Dependencies

```json
{
  "dependencies": {
    "hono": "^4.7.0",
    "@hono/zod-validator": "^0.5.0",
    "zod": "^3.24.0",
    "drizzle-orm": "^0.38.0"
  },
  "devDependencies": {
    "@cloudflare/vitest-pool-workers": "^0.9.0",
    "@cloudflare/workers-types": "^4.20250401.0",
    "drizzle-kit": "^0.30.0",
    "vitest": "^3.0.0",
    "wrangler": "^4.0.0",
    "typescript": "^5.7.0"
  }
}
```
