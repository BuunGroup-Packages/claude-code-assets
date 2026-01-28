# Astro 6 Reference

## Breaking Changes from v5

### 1. Node.js Requirement
- **Astro 6 requires Node.js 22+** (drops 18 & 20 support)

### 2. Removed APIs
- `Astro.glob()` - use `import.meta.glob()` instead
- `emitESMImage()` - removed
- `<ViewTransitions />` (deprecated) - use `<ClientRouter />`
- Legacy content collections - use new content layer

### 3. Cloudflare Adapter Changes

**Removed `Astro.locals.runtime`:**
```typescript
// OLD (v5) - REMOVED
const { env } = Astro.locals.runtime;

// NEW (v6) - Direct import
import { env } from "cloudflare:workers";
```

**Access patterns:**
```typescript
// Environment variables
import { env } from "cloudflare:workers";
const db = env.DB;

// CF object (geolocation, IP, etc.)
const cf = Astro.request.cf;
const country = cf?.country;

// Caches API
caches.default.put(request, response);

// Execution context
const ctx = Astro.locals.cfContext;
ctx.waitUntil(asyncOperation());
```

### 4. wrangler.jsonc Changes

**Unified entrypoint:**
```jsonc
{
  "main": "@astrojs/cloudflare/entrypoints/server"
}
```

### 5. Development Runtime
- `astro dev` now uses Cloudflare's `workerd` instead of Node.js
- Provides production-equivalent behavior during development

### 6. Zod 4 Required
- Astro 6 uses Zod 4 for validation
- Import from `astro/zod` for compatibility

## Astro Actions

### Definition

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from "astro:actions";
import { z } from "astro/zod";

export const server = {
  myAction: defineAction({
    input: z.object({
      name: z.string(),
    }),
    handler: async (input, context) => {
      return { greeting: `Hello, ${input.name}!` };
    },
  }),
};
```

### Form Actions

```typescript
export const server = {
  submitForm: defineAction({
    accept: "form",
    input: z.object({
      email: z.string().email(),
      subscribe: z.coerce.boolean().default(false),
      file: z.instanceof(File).optional(),
    }),
    handler: async (input) => {
      // Process form data
      return { success: true };
    },
  }),
};
```

### Error Handling

```typescript
import { ActionError } from "astro:actions";

throw new ActionError({
  code: "UNAUTHORIZED",
  message: "You must be logged in",
});

// Available codes:
// BAD_REQUEST, UNAUTHORIZED, FORBIDDEN, NOT_FOUND,
// TIMEOUT, CONFLICT, PRECONDITION_FAILED, PAYLOAD_TOO_LARGE,
// UNSUPPORTED_MEDIA_TYPE, UNPROCESSABLE_CONTENT, TOO_MANY_REQUESTS,
// CLIENT_CLOSED_REQUEST, INTERNAL_SERVER_ERROR
```

### Client Usage

```typescript
import { actions } from "astro:actions";

// Direct call
const { data, error } = await actions.myAction({ name: "World" });

// With throw
const data = await actions.myAction.orThrow({ name: "World" });
```

### React Integration

```tsx
import { actions } from "astro:actions";
import { useActionState } from "react";
import { withState } from "@astrojs/react/actions";

export function MyForm() {
  const [state, action, pending] = useActionState(
    withState(actions.submitForm),
    { data: undefined, error: undefined }
  );

  return (
    <form action={action}>
      <input name="email" type="email" required />
      <button disabled={pending}>Submit</button>
      {state.error && <p>{state.error.message}</p>}
    </form>
  );
}
```

### Server-side Calling

```astro
---
import { actions } from "astro:actions";

const result = await Astro.callAction(actions.myAction, { name: "World" });
---
```

## API Endpoints

```typescript
// src/pages/api/users.ts
import type { APIRoute } from "astro";

export const prerender = false;

export const GET: APIRoute = async ({ params, request }) => {
  return new Response(JSON.stringify({ users: [] }), {
    headers: { "Content-Type": "application/json" },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  return new Response(JSON.stringify(body), { status: 201 });
};
```

## File-Based Routing

| File | URL |
|------|-----|
| `src/pages/index.astro` | `/` |
| `src/pages/about.astro` | `/about` |
| `src/pages/blog/[slug].astro` | `/blog/:slug` |
| `src/pages/docs/[...path].astro` | `/docs/*` |

### Underscore Exclusion
Files/folders prefixed with `_` are NOT routed:
```
src/pages/dashboard/
├── index.astro          # /dashboard
├── _components/         # NOT routed
└── _hooks/              # NOT routed
```

## React Integration

### Installation
```bash
npx astro add react
```

### Configuration
```typescript
// astro.config.ts
import react from "@astrojs/react";

export default defineConfig({
  integrations: [react()],
});
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react"
  }
}
```

### Hydration Directives
- `client:load` - Hydrate immediately
- `client:idle` - Hydrate when browser is idle
- `client:visible` - Hydrate when visible in viewport
- `client:media="(max-width: 768px)"` - Hydrate on media query match
- `client:only="react"` - Skip SSR, only render on client

## Sessions (Cloudflare KV)

```astro
---
export const prerender = false;

// Get session value
const cart = await Astro.session?.get('cart');

// Set session value
await Astro.session?.set('cart', ['item1', 'item2']);
---
```

Sessions automatically use Workers KV when deployed to Cloudflare.

## Image Optimization

```typescript
// astro.config.ts
export default defineConfig({
  adapter: cloudflare({
    imageService: "cloudflare", // or "compile", "passthrough"
  }),
});
```

## References

- [Astro 6 Docs](https://v6.docs.astro.build/)
- [Cloudflare Adapter](https://v6.docs.astro.build/en/guides/integrations-guide/cloudflare/)
- [Astro Actions](https://v6.docs.astro.build/en/guides/actions/)
- [React Integration](https://v6.docs.astro.build/en/guides/integrations-guide/react/)
