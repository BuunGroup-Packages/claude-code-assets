# TanStack Start SEO Implementation

## Overview

TanStack Start patterns for SEO meta tags.
Uses built-in head management via route definitions.

## File Locations

| File | Purpose |
|------|---------|
| `app/routes/__root.tsx` | Root layout with base meta |
| `app/routes/index.tsx` | Home page meta |
| `app/components/SEO.tsx` | Reusable SEO component |

## Route-Based Meta Pattern

### 1. Root Layout

```tsx
// app/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router';

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    ],
    links: [
      { rel: 'icon', href: '/favicon.svg' },
    ],
  }),
  component: RootComponent,
});

function RootComponent() {
  return (
    <html lang="en">
      <head>
        <Meta />
      </head>
      <body>
        <Outlet />
      </body>
    </html>
  );
}
```

### 2. Page-Specific Meta

```tsx
// app/routes/index.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  head: () => ({
    meta: [
      { title: 'Home | Your Site' },
      { name: 'description', content: 'Welcome to our site. We help you achieve amazing results.' },
      { name: 'robots', content: 'index, follow' },
      // Open Graph
      { property: 'og:type', content: 'website' },
      { property: 'og:title', content: 'Home | Your Site' },
      { property: 'og:description', content: 'Welcome to our site.' },
      { property: 'og:image', content: 'https://yourdomain.com/og-default.png' },
      { property: 'og:url', content: 'https://yourdomain.com/' },
      // Twitter
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: 'Home | Your Site' },
      { name: 'twitter:description', content: 'Welcome to our site.' },
      { name: 'twitter:image', content: 'https://yourdomain.com/og-default.png' },
    ],
    links: [
      { rel: 'canonical', href: 'https://yourdomain.com/' },
    ],
  }),
  component: HomePage,
});

function HomePage() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  );
}
```

## SEO Helper Function

### 1. Create Helper

```tsx
// app/lib/seo.ts
interface SEOConfig {
  title: string;
  description: string;
  image?: string;
  url: string;
  type?: 'website' | 'article';
  noindex?: boolean;
}

const SITE_NAME = 'Your Site';
const SITE_URL = 'https://yourdomain.com';

export function createSEOMeta({
  title,
  description,
  image = '/og-default.png',
  url,
  type = 'website',
  noindex = false,
}: SEOConfig) {
  const fullTitle = `${title} | ${SITE_NAME}`;
  const absoluteImage = image.startsWith('http') ? image : `${SITE_URL}${image}`;
  const canonicalUrl = url.startsWith('http') ? url : `${SITE_URL}${url}`;

  return {
    meta: [
      { title: fullTitle },
      { name: 'description', content: description },
      { name: 'robots', content: noindex ? 'noindex, nofollow' : 'index, follow' },
      // Open Graph
      { property: 'og:type', content: type },
      { property: 'og:title', content: fullTitle },
      { property: 'og:description', content: description },
      { property: 'og:image', content: absoluteImage },
      { property: 'og:url', content: canonicalUrl },
      { property: 'og:site_name', content: SITE_NAME },
      // Twitter
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: fullTitle },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: absoluteImage },
    ],
    links: [
      { rel: 'canonical', href: canonicalUrl },
    ],
  };
}
```

### 2. Use in Routes

```tsx
// app/routes/about.tsx
import { createFileRoute } from '@tanstack/react-router';
import { createSEOMeta } from '../lib/seo';

export const Route = createFileRoute('/about')({
  head: () => createSEOMeta({
    title: 'About Us',
    description: 'Learn more about our company and mission.',
    url: '/about',
  }),
  component: AboutPage,
});

function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
    </main>
  );
}
```

## Dynamic Meta with Loaders

```tsx
// app/routes/blog/$slug.tsx
import { createFileRoute } from '@tanstack/react-router';
import { createSEOMeta } from '../../lib/seo';

export const Route = createFileRoute('/blog/$slug')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.slug);
    return { post };
  },
  head: ({ loaderData }) => createSEOMeta({
    title: loaderData.post.title,
    description: loaderData.post.excerpt,
    image: loaderData.post.image,
    url: `/blog/${loaderData.post.slug}`,
    type: 'article',
  }),
  component: BlogPost,
});
```

## JSON-LD in TanStack

```tsx
// app/components/Schema.tsx
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

Add to route component:

```tsx
function HomePage() {
  return (
    <>
      <Schema
        schema={{
          "@context": "https://schema.org",
          "@type": "WebSite",
          "name": "Your Site",
          "url": "https://yourdomain.com",
        }}
      />
      <main>
        <h1>Welcome</h1>
      </main>
    </>
  );
}
```

## Checklist

- [ ] Root route has base meta (charset, viewport)
- [ ] createSEOMeta helper created
- [ ] All routes use head function
- [ ] Dynamic routes use loader data
- [ ] OG images are absolute URLs
- [ ] Canonical URLs are absolute
- [ ] JSON-LD added to key pages
