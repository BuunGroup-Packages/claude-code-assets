---
name: astro-cloudflare
model: sonnet
description: |
  Build Astro 6 + Cloudflare Workers websites with Hono API, D1, R2, KV.
  TypeScript-first, React default, CSS animations. Co-located components.
  Orchestrates init, component, api, binding sub-skills.
argument-hint: "[command] [args]"
---

# Astro 6 + Cloudflare Workers Stack

## Stack Overview

| Layer | Technology |
|-------|------------|
| Framework | Astro 6 (Node 22+) |
| UI | React 19 Islands |
| API | Astro Actions |
| Database | Cloudflare D1 |
| Storage | Cloudflare R2 |
| Cache | Cloudflare KV |
| Animations | CSS only |

## Commands

| Command | Sub-skill | What it does |
|---------|-----------|--------------|
| init | /astro-cloudflare:init | Scaffold new project |
| component | /astro-cloudflare:component | Add React island |
| api | /astro-cloudflare:api | Add Astro Action |
| binding | /astro-cloudflare:binding | Configure D1/R2/KV |
| page | /astro-cloudflare:page | Add page with co-location |

---

## Island Architecture

Astro renders pages as **static HTML** with interactive **React islands**.

```
┌─────────────────────────────────────────────────────┐
│  Static HTML (Astro)                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ React Island│  │ React Island│  │ React Island│ │
│  │ client:load │  │client:visible│  │ client:idle │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│  Static HTML continues...                          │
└─────────────────────────────────────────────────────┘
```

### Hydration Strategies

| Directive | When | Use For |
|-----------|------|---------|
| `client:load` | Immediately | Critical interactive UI |
| `client:idle` | Browser idle | Non-critical forms |
| `client:visible` | In viewport | Below-fold content |
| `client:only="react"` | Never SSR | Client-only features |
| *(none)* | Never | Static display |

### Island Example

```astro
---
// Static: runs at build/request time
import Layout from "@/layouts/Layout.astro";
import { SearchBar } from "./_components/SearchBar";
import { ResultsList } from "./_components/ResultsList";
import { Newsletter } from "./_components/Newsletter";

const staticData = await getStaticData();
---

<Layout title="Search">
  <!-- Static HTML -->
  <header>
    <h1>Search</h1>
  </header>

  <!-- Island: interactive search (load immediately) -->
  <SearchBar client:load />

  <!-- Island: results (hydrate when visible) -->
  <ResultsList client:visible initialData={staticData} />

  <!-- Static HTML -->
  <footer>
    <p>Static footer content</p>
    <!-- Island: newsletter form (hydrate when idle) -->
    <Newsletter client:idle />
  </footer>
</Layout>
```

---

## Co-located Design

Each page/feature is **self-contained** with its own components, hooks, types, and utils.

### Project Structure

```
src/
├── pages/
│   ├── index.astro
│   │
│   ├── dashboard/                    # Feature: Dashboard
│   │   ├── index.astro               # Page entry
│   │   ├── _components/              # React islands
│   │   │   ├── StatsCard.tsx
│   │   │   ├── StatsCard.css
│   │   │   ├── ActivityFeed.tsx
│   │   │   ├── ActivityFeed.css
│   │   │   └── index.ts              # Barrel export
│   │   ├── _hooks/                   # React hooks
│   │   │   ├── useStats.ts
│   │   │   ├── useActivity.ts
│   │   │   └── index.ts
│   │   ├── _types/                   # TypeScript types
│   │   │   ├── stats.ts
│   │   │   ├── activity.ts
│   │   │   └── index.ts
│   │   └── _utils/                   # Utilities
│   │       ├── formatters.ts
│   │       └── index.ts
│   │
│   ├── secrets/                      # Feature: Secrets
│   │   ├── index.astro
│   │   ├── [id].astro                # Dynamic route
│   │   ├── _components/
│   │   │   ├── CreateForm.tsx
│   │   │   ├── SecretView.tsx
│   │   │   └── index.ts
│   │   ├── _hooks/
│   │   │   └── useSecret.ts
│   │   └── _types/
│   │       └── secret.ts
│   │
│   └── api/                          # API endpoints
│       └── health.ts
│
├── components/                       # SHARED components only
│   ├── Button.tsx
│   ├── Button.css
│   └── index.ts
│
├── hooks/                            # SHARED hooks only
│   └── useMediaQuery.ts
│
├── types/                            # SHARED types only
│   └── common.ts
│
├── actions/                          # Astro Actions
│   └── index.ts
│
├── layouts/
│   └── Layout.astro
│
└── styles/
    ├── global.css
    └── animations.css
```

### Co-location Rules

1. **Page-specific code** → `src/pages/[feature]/_*` folders
2. **Shared across pages** → `src/components/`, `src/hooks/`, `src/types/`
3. **Underscore prefix** → Excluded from routing
4. **Barrel exports** → Each `_*/index.ts` exports all

---

## Co-located Patterns

### _components/index.ts (Barrel Export)

```typescript
// src/pages/dashboard/_components/index.ts
export { StatsCard } from "./StatsCard";
export { ActivityFeed } from "./ActivityFeed";
export { QuickActions } from "./QuickActions";
```

### _types/index.ts

```typescript
// src/pages/dashboard/_types/index.ts
export type { Stat, StatPeriod } from "./stats";
export type { Activity, ActivityType } from "./activity";
```

### _hooks/index.ts

```typescript
// src/pages/dashboard/_hooks/index.ts
export { useStats } from "./useStats";
export { useActivity } from "./useActivity";
```

### Page Using Co-located Code

```astro
---
// src/pages/dashboard/index.astro
import Layout from "@/layouts/Layout.astro";
import { StatsCard, ActivityFeed, QuickActions } from "./_components";
import type { Stat } from "./_types";

export const prerender = false;

// Server-side data fetch
const initialStats: Stat[] = await fetchStats();
---

<Layout title="Dashboard">
  <main class="dashboard fade-in">
    <h1>Dashboard</h1>

    <!-- Island: Stats (immediate) -->
    <section class="stats-grid">
      <StatsCard client:load stats={initialStats} />
    </section>

    <!-- Island: Activity (when visible) -->
    <section class="activity">
      <h2>Recent Activity</h2>
      <ActivityFeed client:visible />
    </section>

    <!-- Island: Actions (when idle) -->
    <aside class="actions">
      <QuickActions client:idle />
    </aside>
  </main>
</Layout>

<style>
  .dashboard {
    display: grid;
    gap: 2rem;
  }
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
</style>
```

---

## Island Component Pattern

### Component with Co-located Hook

```tsx
// src/pages/dashboard/_components/StatsCard.tsx
import type { FC } from "react";
import { useStats } from "../_hooks";
import type { Stat } from "../_types";
import "./StatsCard.css";

interface StatsCardProps {
  stats?: Stat[];
}

export const StatsCard: FC<StatsCardProps> = ({ stats: initialStats }) => {
  const { stats, loading, refetch } = useStats(initialStats);

  if (loading) {
    return <div className="stats-card stats-card--loading">Loading...</div>;
  }

  return (
    <div className="stats-card fade-in">
      {stats.map((stat) => (
        <div key={stat.id} className="stat">
          <span className="stat__label">{stat.label}</span>
          <span className="stat__value">{stat.value}</span>
        </div>
      ))}
      <button onClick={refetch} className="stats-card__refresh">
        Refresh
      </button>
    </div>
  );
};
```

### Co-located Hook

```typescript
// src/pages/dashboard/_hooks/useStats.ts
import { useState, useEffect, useCallback } from "react";
import { actions } from "astro:actions";
import type { Stat } from "../_types";

export function useStats(initialStats?: Stat[]) {
  const [stats, setStats] = useState<Stat[]>(initialStats ?? []);
  const [loading, setLoading] = useState(!initialStats);
  const [error, setError] = useState<Error | null>(null);

  const fetchStats = useCallback(async () => {
    setLoading(true);
    try {
      const { data, error } = await actions.dashboard.getStats();
      if (error) throw new Error(error.message);
      setStats(data ?? []);
    } catch (e) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!initialStats) {
      fetchStats();
    }
  }, [initialStats, fetchStats]);

  return { stats, loading, error, refetch: fetchStats };
}
```

### Co-located Types

```typescript
// src/pages/dashboard/_types/stats.ts
export interface Stat {
  id: string;
  label: string;
  value: number;
  change?: number;
  period: StatPeriod;
}

export type StatPeriod = "day" | "week" | "month" | "year";
```

### Co-located CSS

```css
/* src/pages/dashboard/_components/StatsCard.css */
.stats-card {
  padding: 1.5rem;
  background: var(--color-surface);
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stats-card--loading {
  opacity: 0.7;
  pointer-events: none;
}

.stat {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
}

.stat:last-of-type {
  border-bottom: none;
}

.stat__label {
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.stat__value {
  font-weight: 600;
  font-size: 1.25rem;
}

.stats-card__refresh {
  margin-top: 1rem;
  width: 100%;
}
```

---

## Astro Actions (Organized)

```typescript
// src/actions/index.ts
import { defineAction } from "astro:actions";
import { z } from "astro/zod";
import { env } from "cloudflare:workers";

export const server = {
  // Grouped by feature
  dashboard: {
    getStats: defineAction({
      handler: async () => {
        const { results } = await env.DB.prepare(
          "SELECT * FROM stats ORDER BY created_at DESC LIMIT 10"
        ).all();
        return results;
      },
    }),

    getActivity: defineAction({
      input: z.object({ limit: z.number().default(20) }),
      handler: async ({ limit }) => {
        const { results } = await env.DB.prepare(
          "SELECT * FROM activity ORDER BY created_at DESC LIMIT ?"
        ).bind(limit).all();
        return results;
      },
    }),
  },

  secrets: {
    create: defineAction({
      accept: "form",
      input: z.object({
        content: z.string().min(1).max(10000),
        expiresIn: z.enum(["1h", "24h", "7d", "30d"]).default("24h"),
      }),
      handler: async (input) => {
        const id = crypto.randomUUID();
        const expiresAt = calculateExpiry(input.expiresIn);

        await env.CACHE.put(
          `secret:${id}`,
          JSON.stringify({ content: input.content, views: 0 }),
          { expiration: Math.floor(expiresAt.getTime() / 1000) }
        );

        return { id, expiresAt: expiresAt.toISOString() };
      },
    }),

    view: defineAction({
      input: z.object({ id: z.string().uuid() }),
      handler: async ({ id }) => {
        const raw = await env.CACHE.get(`secret:${id}`);
        if (!raw) return null;

        // Delete after viewing (one-time secret)
        await env.CACHE.delete(`secret:${id}`);

        return JSON.parse(raw);
      },
    }),
  },
};
```

---

## Usage Examples

```bash
# Create project
/astro-cloudflare init destroy-network

# Add page with full co-location
/astro-cloudflare page secrets --with-components

# Add island to existing page
/astro-cloudflare component SecretForm src/pages/secrets/_components

# Add action
/astro-cloudflare api secrets.create

# Add binding
/astro-cloudflare binding kv SECRETS
```

---

## Development

```bash
wrangler types              # Generate binding types
npm run dev                 # Dev with workerd runtime
npm run build && npm run preview  # Preview production
npm run deploy              # Deploy to Cloudflare
```

---

## Output

After executing command:

```
## Astro 6 + Cloudflare

**Command**: [COMMAND]
**Result**: [description]

### Files
- [list]

### Next Steps
- [actions]
```
