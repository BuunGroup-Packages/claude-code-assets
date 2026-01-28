---
description: Build Astro 6 + Cloudflare Workers websites
argument-hint: "<command> [args]"
---

# Astro 6 + Cloudflare Stack

Run `/astro-cloudflare $ARGUMENTS` to use this stack.

## Commands

| Command | Description |
|---------|-------------|
| init NAME | Create new project with full stack |
| component NAME [path] | Add React component |
| api NAME [--endpoint] | Add Astro Action (or API endpoint) |
| binding TYPE NAME | Add D1/R2/KV binding |
| page NAME [--with-components] | Add Astro page |

## Examples

```bash
# Initialize project
/astro-cloudflare init my-app

# Add component
/astro-cloudflare component Button
/astro-cloudflare component StatCard src/pages/dashboard/_components

# Add Action
/astro-cloudflare api createUser
/astro-cloudflare api webhook --endpoint

# Add binding
/astro-cloudflare binding d1 DB
/astro-cloudflare binding r2 BUCKET
/astro-cloudflare binding kv CACHE

# Add page
/astro-cloudflare page about
/astro-cloudflare page dashboard --with-components
```

## Stack

| Layer | Technology |
|-------|------------|
| Framework | Astro 6 (Node 22+) |
| UI | React 19 |
| API | Astro Actions |
| Database | Cloudflare D1 |
| Storage | Cloudflare R2 |
| Cache | Cloudflare KV |
| Animations | CSS (no Framer Motion) |

## Key v6 Patterns

```typescript
// Environment access (v6)
import { env } from "cloudflare:workers";
const db = env.DB;

// Astro Actions
import { actions } from "astro:actions";
const { data, error } = await actions.myAction({ ... });

// React with Actions
import { useActionState } from "react";
import { withState } from "@astrojs/react/actions";
```
