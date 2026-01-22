# Astro SEO Implementation

## Overview

Astro-specific patterns for SEO meta tags.
Zero-JS by default = excellent baseline performance.

## File Locations

| File | Purpose |
|------|---------|
| `src/layouts/Layout.astro` | Base layout with SEO |
| `src/components/SEO.astro` | Reusable SEO component |
| `src/components/BaseHead.astro` | Head-only component |

## SEO Component Pattern

### 1. Create SEO Component

```astro
---
// src/components/SEO.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  canonicalUrl?: string;
  type?: 'website' | 'article';
  noindex?: boolean;
}

const {
  title,
  description,
  image = '/og-default.png',
  canonicalUrl = Astro.url.href,
  type = 'website',
  noindex = false,
} = Astro.props;

const siteName = import.meta.env.SITE_NAME || 'Your Site';
const siteUrl = Astro.site?.toString() || '';
const fullTitle = `${title} | ${siteName}`;
const absoluteImage = new URL(image, siteUrl).toString();
---

<!-- Primary Meta -->
<title>{fullTitle}</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonicalUrl} />
<meta name="robots" content={noindex ? 'noindex, nofollow' : 'index, follow'} />

<!-- Open Graph -->
<meta property="og:type" content={type} />
<meta property="og:title" content={fullTitle} />
<meta property="og:description" content={description} />
<meta property="og:image" content={absoluteImage} />
<meta property="og:url" content={canonicalUrl} />
<meta property="og:site_name" content={siteName} />

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={fullTitle} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={absoluteImage} />
```

### 2. Use in Layout

```astro
---
// src/layouts/Layout.astro
import SEO from '../components/SEO.astro';

interface Props {
  title: string;
  description: string;
  image?: string;
}

const { title, description, image } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <SEO title={title} description={description} image={image} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body>
    <slot />
  </body>
</html>
```

### 3. Use in Pages

```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
---

<Layout 
  title="Home" 
  description="Welcome to our site. We help you achieve amazing results."
>
  <main>
    <h1>Welcome</h1>
  </main>
</Layout>
```

## Configuration

### astro.config.mjs

```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yourdomain.com', // REQUIRED for canonical URLs
  integrations: [sitemap()],
});
```

### Install Sitemap

```bash
npx astro add sitemap
```

## JSON-LD in Astro

```astro
---
const schema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company",
  "url": Astro.site?.toString(),
};
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

## Content Collections SEO

```astro
---
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string().max(60),
    description: z.string().min(120).max(160),
    image: z.string().optional(),
    pubDate: z.date(),
  }),
});

export const collections = { blog };
---
```

## View Transitions

Preserve SEO during transitions:

```astro
---
import { ViewTransitions } from 'astro:transitions';
---

<head>
  <ViewTransitions />
  <!-- Meta tags update automatically -->
</head>
```

## Checklist

- [ ] `site` configured in astro.config.mjs
- [ ] SEO component with all required meta
- [ ] Layout uses SEO component
- [ ] Pages pass title + description
- [ ] Sitemap integration added
- [ ] OG images are absolute URLs
- [ ] Canonical URLs are absolute
