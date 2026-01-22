# Next.js SEO Implementation

## Overview

Next.js 14+ App Router patterns for SEO meta tags.
Uses built-in Metadata API for static and dynamic meta.

## File Locations

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout with base meta |
| `app/page.tsx` | Home page meta |
| `app/[slug]/page.tsx` | Dynamic page meta |

## Static Metadata Pattern

### 1. Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://yourdomain.com'),
  title: {
    default: 'Your Site',
    template: '%s | Your Site',
  },
  description: 'Default description for your site.',
  openGraph: {
    type: 'website',
    siteName: 'Your Site',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### 2. Page Metadata

```tsx
// app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to our site. We help you achieve amazing results.',
  openGraph: {
    title: 'Home | Your Site',
    description: 'Welcome to our site.',
    images: ['/og-home.png'],
  },
  alternates: {
    canonical: '/',
  },
};

export default function HomePage() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  );
}
```

## Dynamic Metadata Pattern

### generateMetadata Function

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

interface Props {
  params: { slug: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await fetchPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
      images: [post.image],
      publishedTime: post.publishedAt,
      authors: [post.author],
    },
    alternates: {
      canonical: `/blog/${params.slug}`,
    },
  };
}

export default async function BlogPost({ params }: Props) {
  const post = await fetchPost(params.slug);
  
  return (
    <article>
      <h1>{post.title}</h1>
    </article>
  );
}
```

## SEO Helper Function

```tsx
// lib/seo.ts
import type { Metadata } from 'next';

interface SEOConfig {
  title: string;
  description: string;
  image?: string;
  url: string;
  type?: 'website' | 'article';
  noindex?: boolean;
}

export function createMetadata({
  title,
  description,
  image = '/og-default.png',
  url,
  type = 'website',
  noindex = false,
}: SEOConfig): Metadata {
  return {
    title,
    description,
    openGraph: {
      type,
      title,
      description,
      images: [image],
      url,
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [image],
    },
    alternates: {
      canonical: url,
    },
    robots: noindex
      ? { index: false, follow: false }
      : { index: true, follow: true },
  };
}

// Usage in page
export const metadata = createMetadata({
  title: 'About Us',
  description: 'Learn more about our company.',
  url: '/about',
});
```

## JSON-LD in Next.js

```tsx
// app/page.tsx
export default function HomePage() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Your Site',
    url: 'https://yourdomain.com',
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      <main>
        <h1>Welcome</h1>
      </main>
    </>
  );
}
```

### Reusable Schema Component

```tsx
// components/Schema.tsx
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

## Sitemap

```tsx
// app/sitemap.ts
import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://yourdomain.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://yourdomain.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ];
}
```

## Robots.txt

```tsx
// app/robots.ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
    },
    sitemap: 'https://yourdomain.com/sitemap.xml',
  };
}
```

## Checklist

- [ ] metadataBase set in root layout
- [ ] title.template configured
- [ ] Pages export metadata or generateMetadata
- [ ] openGraph images are configured
- [ ] alternates.canonical set per page
- [ ] sitemap.ts created
- [ ] robots.ts created
- [ ] JSON-LD added to key pages
