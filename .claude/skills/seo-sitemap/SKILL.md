---
name: seo-sitemap
description: |
  Generate XML sitemap and configure sitemap generation for frameworks.
  Handles static sitemaps, dynamic generation, and robots.txt integration.
argument-hint: "[framework] [base_url]"
hooks:
  PostToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_sitemap_validate.py"
---

# Sitemap Generation

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | framework | astro, nextjs, vite, tanstack | Auto-detect |
| $2 | base_url | Site URL | https://example.com |

## Usage

```bash
/seo-sitemap astro https://mysite.com
/seo-sitemap nextjs
```

## Framework Implementations

### Astro

Install integration:
```bash
npx astro add sitemap
```

Configure `astro.config.mjs`:
```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://mysite.com',
  integrations: [sitemap()],
});
```

### Next.js (App Router)

Create `app/sitemap.ts`:
```ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://mysite.com'

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ]
}
```

### Vite / Static

Create `public/sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://mysite.com/</loc>
    <lastmod>2026-01-22</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://mysite.com/about</loc>
    <lastmod>2026-01-22</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### TanStack Start

Create `public/sitemap.xml` or use build script:
```ts
// scripts/generate-sitemap.ts
import { writeFileSync } from 'fs'

const baseUrl = 'https://mysite.com'
const pages = ['/', '/about', '/contact']

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(page => `  <url>
    <loc>${baseUrl}${page}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </url>`).join('\n')}
</urlset>`

writeFileSync('public/sitemap.xml', sitemap)
```

## robots.txt Integration

Add sitemap reference:
```txt
Sitemap: https://mysite.com/sitemap.xml
```

## Validation

Sitemap must:
- Be valid XML
- Have `<urlset>` root with proper namespace
- Include `<loc>` for each URL
- Use absolute URLs
- Be referenced in robots.txt

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| SITEMAP001 | error | Invalid XML syntax |
| SITEMAP002 | error | Missing urlset namespace |
| SITEMAP003 | error | URL not absolute |
| SITEMAP004 | warning | Missing lastmod |
| SITEMAP005 | warning | Not in robots.txt |
