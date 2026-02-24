# Vite + React SEO Implementation

## Overview

Vite/React patterns for SEO meta tags.
Uses react-helmet-async for client-side head management, plus **post-build prerendering** via the `puppeteer` skill to ensure crawlers see fully rendered HTML.

## CRITICAL: Vite SPA Crawler Problem

Vite SPAs serve an empty `<div id="root"></div>` to crawlers. Google, social platforms, and AI bots see **no content, no meta tags, no JSON-LD** — only the shell HTML. Helmet runs client-side only.

**Solution**: Post-build prerendering using the `puppeteer` skill. After `vite build`, a script launches headless Chrome, visits each route, captures the fully-rendered HTML (including Helmet `<head>` tags), and writes it to `dist/`. React hydrates on top at runtime.

This is **required** for any Vite SPA that needs SEO. Without it, all other SEO work is invisible to crawlers.

## File Locations

| File | Purpose |
|------|---------|
| `src/components/SEO.tsx` | Reusable SEO component |
| `src/App.tsx` | Provider setup |
| `index.html` | Fallback meta |
| `scripts/prerender-pages.mjs` | Post-build prerender (uses `puppeteer` skill patterns) |

## Dependencies

```bash
npm install react-helmet-async
npm install -D puppeteer
```

## SEO Component Pattern

### 1. Create SEO Component

```tsx
// src/components/SEO.tsx
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url?: string;
  type?: 'website' | 'article';
  noindex?: boolean;
}

const SITE_NAME = import.meta.env.VITE_SITE_NAME || 'Your Site';
const SITE_URL = import.meta.env.VITE_SITE_URL || '';

export function SEO({
  title,
  description,
  image = '/og-default.png',
  url,
  type = 'website',
  noindex = false,
}: SEOProps) {
  const fullTitle = `${title} | ${SITE_NAME}`;
  const absoluteImage = image.startsWith('http') ? image : `${SITE_URL}${image}`;
  const canonicalUrl = url || (typeof window !== 'undefined' ? window.location.href : '');

  return (
    <Helmet>
      {/* Primary Meta */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={canonicalUrl} />
      <meta name="robots" content={noindex ? 'noindex, nofollow' : 'index, follow'} />

      {/* Open Graph */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={absoluteImage} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:site_name" content={SITE_NAME} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={absoluteImage} />
    </Helmet>
  );
}
```

### 2. Setup Provider

```tsx
// src/App.tsx
import { HelmetProvider } from 'react-helmet-async';
import { BrowserRouter } from 'react-router-dom';

export function App() {
  return (
    <HelmetProvider>
      <BrowserRouter>
        {/* Your routes */}
      </BrowserRouter>
    </HelmetProvider>
  );
}
```

### 3. Use in Pages

```tsx
// src/pages/Home.tsx
import { SEO } from '../components/SEO';

export function Home() {
  return (
    <>
      <SEO
        title="Home"
        description="Welcome to our site. We help you achieve amazing results with our products."
      />
      <main>
        <h1>Welcome</h1>
      </main>
    </>
  );
}
```

## Post-Build Prerendering

Uses the `puppeteer` skill for all browser automation patterns.
See `.claude/skills/puppeteer/SKILL.md` for launch options, selectors, network interception, waiting, and CI/Docker args.

### Why This Is Required

| Without prerender | With prerender |
|-------------------|----------------|
| Crawlers see `<div id="root"></div>` | Crawlers see full HTML with content |
| No meta tags in source | Helmet meta tags baked into HTML |
| No JSON-LD visible | JSON-LD in rendered output |
| Social shares show blank | OG images and descriptions work |
| AI bots extract nothing | AI bots see structured content |

### Prerender Script

Create `scripts/prerender-pages.mjs`:

```js
#!/usr/bin/env node
/**
 * Post-build prerendering for Vite SPAs.
 *
 * Uses Puppeteer (see `puppeteer` skill) to:
 * 1. Serve built dist/ via local static server
 * 2. Visit each route with headless Chrome
 * 3. Capture fully-rendered HTML (including Helmet <head>)
 * 4. Write to dist/{route}/index.html
 *
 * Key Puppeteer patterns used:
 * - Launch: headless + CI args (--no-sandbox, --disable-dev-shm-usage)
 * - Navigation: page.goto() with waitUntil: 'networkidle0'
 * - Network interception: block analytics, mock API responses
 * - Content extraction: page.content() for full rendered HTML
 * - Viewport: page.setViewport() for consistent rendering
 */
import { createServer } from 'node:http'
import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs'
import { resolve, dirname, extname } from 'node:path'
import { fileURLToPath } from 'node:url'
import puppeteer from 'puppeteer'

const __dirname = dirname(fileURLToPath(import.meta.url))
const DIST_DIR = resolve(__dirname, '..', 'dist')
const CONCURRENCY = 4
const POST_RENDER_DELAY_MS = 1500

// Routes to prerender — add all public, static pages
const ROUTES = [
  '/',
  '/about',
  '/pricing',
  '/contact',
  // Add your routes here
]

// --- Static file server with SPA fallback ---

const MIME = {
  '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ico': 'image/x-icon',
  '.webp': 'image/webp',
}

function createStaticServer() {
  const fallback = readFileSync(resolve(DIST_DIR, 'index.html'))
  const server = createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`)
    const fp = resolve(DIST_DIR, '.' + url.pathname)
    try {
      const s = existsSync(fp) && statSync(fp)
      if (s && s.isFile()) {
        res.writeHead(200, { 'Content-Type': MIME[extname(fp)] || 'application/octet-stream' })
        return res.end(readFileSync(fp))
      }
    } catch {}
    try {
      const ip = resolve(fp, 'index.html')
      if (existsSync(ip)) { res.writeHead(200, { 'Content-Type': 'text/html' }); return res.end(readFileSync(ip)) }
    } catch {}
    res.writeHead(200, { 'Content-Type': 'text/html' })
    res.end(fallback)
  })
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r({ server, port: server.address().port })))
}

// --- Network interception (puppeteer skill pattern) ---

async function setupInterception(page) {
  await page.setRequestInterception(true)
  page.on('request', async (req) => {
    if (req.isInterceptResolutionHandled()) return
    const url = req.url()
    try {
      // Block analytics
      if (url.includes('googletagmanager.com') || url.includes('google-analytics.com')) {
        return await req.abort()
      }
      // Mock API responses (no backend during prerender)
      if (url.includes('/api/')) {
        return await req.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ data: [] }),
        })
      }
      await req.continue()
    } catch {}
  })
}

// --- Render a single route ---

async function renderRoute(browser, baseUrl, route) {
  const outPath = route === '/'
    ? resolve(DIST_DIR, 'index.html')
    : resolve(DIST_DIR, route.slice(1), 'index.html')

  if (existsSync(outPath)) {
    const existing = readFileSync(outPath, 'utf-8')
    if (existing.includes('data-prerendered')) {
      console.log(`  skip  ${route}`)
      return 'skipped'
    }
  }

  const page = await browser.newPage()
  try {
    await setupInterception(page)
    await page.setViewport({ width: 1280, height: 800 })
    await page.goto(`${baseUrl}${route}`, { waitUntil: 'networkidle0', timeout: 30000 })
    await new Promise((r) => setTimeout(r, POST_RENDER_DELAY_MS))

    let html = await page.content()
    html = html.replace('<div id="root"', '<div data-prerendered="true" id="root"')

    mkdirSync(dirname(outPath), { recursive: true })
    writeFileSync(outPath, html)
    console.log(`  done  ${route}`)
    return 'done'
  } catch (err) {
    console.error(`  FAIL  ${route}: ${err.message}`)
    return 'error'
  } finally {
    await page.close()
  }
}

// --- Main ---

async function main() {
  console.log('Prerendering static pages...\n')
  const { server, port } = await createStaticServer()

  // Launch with CI-safe args (see puppeteer skill: Docker / CI section)
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  })

  const results = { done: 0, skipped: 0, error: 0 }
  const queue = [...ROUTES]
  await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
    while (queue.length) {
      const route = queue.shift()
      if (route) results[await renderRoute(browser, `http://127.0.0.1:${port}`, route)]++
    }
  }))

  await browser.close()
  server.close()
  console.log(`\nPrerendered ${results.done}, skipped ${results.skipped}, errors ${results.error}`)
}

main().catch((err) => { console.error('Prerender failed:', err); process.exit(1) })
```

### Wire Into Build

```json
{
  "scripts": {
    "build": "vite build && node scripts/prerender-pages.mjs"
  }
}
```

### How It Works

1. `vite build` outputs the SPA to `dist/`
2. Script starts a local static file server with SPA fallback
3. Puppeteer visits each route with concurrency (4 pages at once)
4. Uses `waitUntil: 'networkidle0'` + delay for React/Helmet to render
5. `page.content()` captures full HTML including Helmet `<head>` tags
6. Writes to `dist/{route}/index.html`
7. Marks with `data-prerendered="true"` for hydration debugging
8. Network interception blocks analytics, mocks API calls

### Customization

| Config | Default | Purpose |
|--------|---------|---------|
| `DIST_DIR` | `dist` | Vite output directory |
| `CONCURRENCY` | `4` | Parallel browser pages |
| `POST_RENDER_DELAY_MS` | `1500` | Wait after networkidle for React/Helmet |
| `ROUTES` | `[]` | List of routes to prerender |

### Extending Network Interception

Uses the `puppeteer` skill's network interception pattern. Add mocks for your specific API endpoints:

```js
// Mock authenticated endpoints
if (url.includes('/user/me') || url.includes('/billing/')) {
  return await req.respond({ status: 401, contentType: 'application/json', body: '{"error":"Unauthorized"}' })
}

// Mock list endpoints with specific shape
if (url.includes('/v1/items')) {
  return await req.respond({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ data: [], meta: { total: 0, page: 1, limit: 20 } }),
  })
}

// Block heavy assets (3D models, videos)
if (url.endsWith('.glb') || url.endsWith('.mp4')) {
  return await req.abort()
}
```

See `.claude/skills/puppeteer/SKILL.md` for full network interception patterns.

## Fallback Meta (index.html)

Keep fallback meta in `index.html` for unprerendered routes:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Fallback meta (overridden by Helmet, baked in by prerender) -->
    <title>Your Site</title>
    <meta name="description" content="Default description for your site." />

    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## Environment Variables

```env
# .env
VITE_SITE_NAME=Your Site Name
VITE_SITE_URL=https://yourdomain.com
```

## JSON-LD in React

```tsx
// src/components/Schema.tsx
interface SchemaProps {
  schema: Record<string, unknown>;
}

export function Schema({ schema }: SchemaProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

## Checklist

- [ ] react-helmet-async installed
- [ ] HelmetProvider wraps app
- [ ] SEO component with all meta tags
- [ ] Pages use SEO component with title + description
- [ ] Fallback meta in index.html
- [ ] Environment variables configured
- [ ] OG images are absolute URLs
- [ ] **puppeteer installed as dev dependency**
- [ ] **`scripts/prerender-pages.mjs` created with all public routes listed in ROUTES**
- [ ] **API mocks added for endpoints that need a running backend**
- [ ] **build script chains: `vite build && node scripts/prerender-pages.mjs`**
- [ ] **Verified: `dist/{route}/index.html` contains prerendered HTML (not just SPA shell)**
