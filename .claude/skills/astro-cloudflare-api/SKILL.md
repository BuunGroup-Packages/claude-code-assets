---
name: astro-cloudflare:api
model: haiku
description: |
  Add Hono API route to Cloudflare Workers functions/ folder.
  Type-safe bindings, RPC support, middleware patterns.
argument-hint: "<action-name> [--endpoint]"
---

# Add Astro Action or API Endpoint

Astro 6 uses **Actions** for type-safe backend calls. Use `--endpoint` for raw API endpoints (webhooks, external APIs).

## Variables

NAME: $1 (required, e.g., createUser, getProducts)
ENDPOINT: --endpoint flag creates raw API endpoint instead of Action

## Workflow

1. Parse NAME and flags
2. Create Action in src/actions/index.ts OR endpoint in src/pages/api/
3. Add TypeScript types
4. Output usage example

## Astro 6 Environment Access

```typescript
// NEW in Astro 6 - import from cloudflare:workers
import { env } from "cloudflare:workers";

const db = env.DB;        // D1Database
const bucket = env.BUCKET; // R2Bucket
const cache = env.CACHE;   // KVNamespace
```

## Astro Actions (Default)

### Simple Action

```typescript
// Add to src/actions/index.ts
import { defineAction } from "astro:actions";
import { z } from "astro/zod";

export const server = {
  ${NAME}: defineAction({
    input: z.object({
      // Define input schema
    }),
    handler: async (input, context) => {
      // Your logic here
      return { success: true };
    },
  }),
};
```

### Action with D1 Database

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from "astro:actions";
import { z } from "astro/zod";
import { env } from "cloudflare:workers";

export const server = {
  get${pascal(NAME)}s: defineAction({
    handler: async () => {
      const { results } = await env.DB.prepare(
        "SELECT * FROM ${plural(NAME)}"
      ).all();
      return results;
    },
  }),

  get${pascal(NAME)}ById: defineAction({
    input: z.object({
      id: z.string(),
    }),
    handler: async (input) => {
      const result = await env.DB.prepare(
        "SELECT * FROM ${plural(NAME)} WHERE id = ?"
      ).bind(input.id).first();

      if (!result) {
        throw new ActionError({
          code: "NOT_FOUND",
          message: "${pascal(NAME)} not found",
        });
      }

      return result;
    },
  }),

  create${pascal(NAME)}: defineAction({
    accept: "form",
    input: z.object({
      name: z.string().min(1),
      email: z.string().email(),
    }),
    handler: async (input) => {
      const result = await env.DB.prepare(
        "INSERT INTO ${plural(NAME)} (name, email) VALUES (?, ?) RETURNING *"
      ).bind(input.name, input.email).first();
      return result;
    },
  }),

  delete${pascal(NAME)}: defineAction({
    input: z.object({
      id: z.string(),
    }),
    handler: async (input) => {
      await env.DB.prepare(
        "DELETE FROM ${plural(NAME)} WHERE id = ?"
      ).bind(input.id).run();
      return { deleted: true };
    },
  }),
};
```

### Action with Auth Check

```typescript
import { defineAction, ActionError } from "astro:actions";

export const server = {
  ${NAME}: defineAction({
    handler: async (_input, context) => {
      // Check authentication
      if (!context.locals.user) {
        throw new ActionError({
          code: "UNAUTHORIZED",
          message: "You must be logged in",
        });
      }

      // Proceed with authenticated logic
      return { userId: context.locals.user.id };
    },
  }),
};
```

### Action with R2 Storage

```typescript
import { defineAction } from "astro:actions";
import { z } from "astro/zod";
import { env } from "cloudflare:workers";

export const server = {
  upload${pascal(NAME)}: defineAction({
    accept: "form",
    input: z.object({
      file: z.instanceof(File),
    }),
    handler: async (input) => {
      const key = `${NAME}/${Date.now()}-${input.file.name}`;
      const buffer = await input.file.arrayBuffer();

      await env.BUCKET.put(key, buffer, {
        httpMetadata: { contentType: input.file.type },
      });

      return { key, url: `/api/files/${key}` };
    },
  }),
};
```

### Action with KV Cache

```typescript
import { defineAction } from "astro:actions";
import { z } from "astro/zod";
import { env } from "cloudflare:workers";

export const server = {
  getCached${pascal(NAME)}: defineAction({
    input: z.object({
      key: z.string(),
    }),
    handler: async (input) => {
      // Try cache first
      const cached = await env.CACHE.get(input.key);
      if (cached) {
        return JSON.parse(cached);
      }

      // Fetch fresh data
      const data = await fetchFreshData();

      // Cache for 1 hour
      await env.CACHE.put(input.key, JSON.stringify(data), {
        expirationTtl: 3600,
      });

      return data;
    },
  }),
};
```

## Client Usage

### In React Component with useActionState (v6)

```tsx
import { actions } from "astro:actions";
import { useActionState } from "react";
import { withState } from "@astrojs/react/actions";

export function ${pascal(NAME)}Form() {
  const [state, action, pending] = useActionState(
    withState(actions.create${pascal(NAME)}),
    { data: undefined, error: undefined }
  );

  return (
    <form action={action}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button disabled={pending}>
        {pending ? "Saving..." : "Save"}
      </button>
      {state.error && <p className="error">{state.error.message}</p>}
    </form>
  );
}
```

### Direct Call (onClick)

```tsx
import { actions } from "astro:actions";

export function DeleteButton({ id }: { id: string }) {
  const handleDelete = async () => {
    const { error } = await actions.delete${pascal(NAME)}({ id });
    if (error) {
      alert(error.message);
    }
  };

  return <button onClick={handleDelete}>Delete</button>;
}
```

### In Astro Component (Server-side)

```astro
---
import { actions } from "astro:actions";

const result = await Astro.callAction(actions.get${pascal(NAME)}s, {});
---

{result.data && (
  <ul>
    {result.data.map((item) => <li>{item.name}</li>)}
  </ul>
)}
```

## Raw API Endpoints (--endpoint flag)

For webhooks, external APIs, or non-Action use cases.

### Basic Endpoint

```typescript
// src/pages/api/${NAME}.ts
import type { APIRoute } from "astro";

export const prerender = false;

export const GET: APIRoute = async () => {
  return new Response(
    JSON.stringify({ message: "Hello from ${NAME}" }),
    {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }
  );
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();

  return new Response(
    JSON.stringify({ received: body }),
    {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }
  );
};
```

### Webhook Endpoint

```typescript
// src/pages/api/webhooks/${NAME}.ts
import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

export const POST: APIRoute = async ({ request, locals }) => {
  // Verify webhook signature
  const signature = request.headers.get("X-Webhook-Signature");
  const body = await request.text();

  if (!verifySignature(signature, body)) {
    return new Response("Invalid signature", { status: 401 });
  }

  const payload = JSON.parse(body);

  // Process webhook async using cfContext
  locals.cfContext.waitUntil(
    processWebhook(payload)
  );

  return new Response("OK", { status: 200 });
};
```

### Dynamic Route Endpoint

```typescript
// src/pages/api/${NAME}/[id].ts
import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

export const GET: APIRoute = async ({ params }) => {
  const item = await env.DB.prepare(
    "SELECT * FROM ${plural(NAME)} WHERE id = ?"
  ).bind(params.id).first();

  if (!item) {
    return new Response(
      JSON.stringify({ error: "Not found" }),
      { status: 404, headers: { "Content-Type": "application/json" } }
    );
  }

  return new Response(JSON.stringify(item), {
    headers: { "Content-Type": "application/json" },
  });
};

export const DELETE: APIRoute = async ({ params }) => {
  await env.DB.prepare(
    "DELETE FROM ${plural(NAME)} WHERE id = ?"
  ).bind(params.id).run();

  return new Response(null, { status: 204 });
};
```

### File Serve Endpoint

```typescript
// src/pages/api/files/[...path].ts
import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

export const GET: APIRoute = async ({ params }) => {
  const object = await env.BUCKET.get(params.path);

  if (!object) {
    return new Response("Not found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("Cache-Control", "public, max-age=31536000");

  return new Response(object.body, { headers });
};
```

## Output

```
## Action/Endpoint Created

**Name**: ${NAME}
**Type**: ${ENDPOINT ? 'API Endpoint' : 'Astro Action'}
**Path**: ${ENDPOINT ? `src/pages/api/${NAME}.ts` : 'src/actions/index.ts'}

### Usage

${ENDPOINT ? `
\`\`\`typescript
// Fetch from client
const res = await fetch('/api/${NAME}');
const data = await res.json();
\`\`\`
` : `
\`\`\`typescript
// Import and call
import { actions } from 'astro:actions';
const { data, error } = await actions.${NAME}({ ... });
\`\`\`
`}

### Next Steps
- Add input validation with Zod
- Add error handling
- Add to component: \`/astro-cloudflare component ${NAME}Form\`
```
