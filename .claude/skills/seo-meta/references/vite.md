# Vite + React SEO Implementation

## Overview

Vite/React patterns for SEO meta tags.
Requires react-helmet-async or similar for SSR support.

## File Locations

| File | Purpose |
|------|---------|
| `src/components/SEO.tsx` | Reusable SEO component |
| `src/App.tsx` | Provider setup |
| `index.html` | Fallback meta |

## Dependencies

```bash
npm install react-helmet-async
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

## Fallback Meta (index.html)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- Fallback meta (overridden by Helmet) -->
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

// Usage
<Schema
  schema={{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Your Company",
    "url": "https://yourdomain.com",
  }}
/>
```

## SSR Considerations

For SSR with Vite (vite-plugin-ssr, etc.):

```tsx
// server.ts
import { renderToString } from 'react-dom/server';
import { HelmetProvider } from 'react-helmet-async';

const helmetContext = {};

const html = renderToString(
  <HelmetProvider context={helmetContext}>
    <App />
  </HelmetProvider>
);

const { helmet } = helmetContext;

// Insert into HTML
const finalHtml = `
  <!DOCTYPE html>
  <html ${helmet.htmlAttributes.toString()}>
    <head>
      ${helmet.title.toString()}
      ${helmet.meta.toString()}
      ${helmet.link.toString()}
    </head>
    <body>
      <div id="root">${html}</div>
    </body>
  </html>
`;
```

## Checklist

- [ ] react-helmet-async installed
- [ ] HelmetProvider wraps app
- [ ] SEO component with all meta
- [ ] Pages use SEO component
- [ ] Environment variables configured
- [ ] Fallback meta in index.html
- [ ] OG images are absolute URLs
