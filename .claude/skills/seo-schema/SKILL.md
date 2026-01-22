---
name: seo-schema
description: |
  Implement JSON-LD structured data for SEO rich snippets. Handles Organization,
  Article, LocalBusiness, Product, FAQ, BreadcrumbList, and more. Auto-validates
  via PostToolUse hook. Use when adding structured data or implementing rich results.
argument-hint: "[schema_type] [file]"
hooks:
  PostToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_schema_validate.py"
---

# JSON-LD Structured Data

## Overview

Implements Schema.org JSON-LD for Google rich snippets.
PostToolUse hook validates every edit automatically.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | schema_type | Organization, Article, Product, LocalBusiness, FAQ, etc. | Required |
| $2 | file | Target file path | Layout/page file |

## Usage

```bash
/seo-schema Organization
/seo-schema Article src/layouts/BlogPost.astro
/seo-schema LocalBusiness
```

## Supported Schema Types

| Type | Required Properties | Error Code |
|------|---------------------|------------|
| Organization | name, url | SCHEMA005 |
| LocalBusiness | name, address | SCHEMA005 |
| Article | headline, author, datePublished | SCHEMA005 |
| BlogPosting | headline, author, datePublished | SCHEMA005 |
| Product | name, description | SCHEMA005 |
| WebSite | name, url | SCHEMA005 |
| BreadcrumbList | itemListElement | SCHEMA005 |
| FAQPage | mainEntity | SCHEMA005 |
| Event | name, startDate, location | SCHEMA005 |
| Recipe | name, recipeIngredient, recipeInstructions | SCHEMA005 |

## Implementation

### Basic Structure

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company",
  "url": "https://yoursite.com",
  "logo": "https://yoursite.com/logo.png"
}
```

### Framework Patterns

**Astro**:
```astro
<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

**React/Next.js**:
```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
/>
```

**TanStack Start**:
```tsx
<script type="application/ld+json">{JSON.stringify(schema)}</script>
```

## Templates

Use templates from [assets/templates/](assets/templates/):

- `organization.json` - Company/brand
- `article.json` - Blog posts/news
- `local-business.json` - Physical locations
- `product.json` - E-commerce products
- `faq.json` - FAQ pages
- `breadcrumb.json` - Navigation breadcrumbs

## Validation

PostToolUse hook runs `post_schema_validate.py` after every edit.

**On failure**, returns:
```
✗ SCHEMA VALIDATION FAILED
File: src/components/Schema.astro
Errors: 2 | Warnings: 0

============================================================
FIX INSTRUCTIONS (execute in order):
============================================================

1. [SCHEMA002] @context at line 5
   Rule: JSON-LD must have @context
   Expected: "@context": "https://schema.org"
   Fix: Add "@context": "https://schema.org" as first property.

2. [SCHEMA005] @type=Organization at line 5
   Rule: Organization requires 'url' property
   Current: Missing: url
   Expected: "url": "..."
   Fix: Add "url" property. See schema.org/Organization.

============================================================
After fixing, save file. Validation re-runs automatically.
```

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| SCHEMA001 | error | Invalid JSON syntax |
| SCHEMA002 | error | Missing @context |
| SCHEMA003 | error | Invalid @context (not schema.org) |
| SCHEMA004 | error | Missing @type |
| SCHEMA005 | error | Missing required property |
| SCHEMA006 | error | URL property not absolute |
| SCHEMA007 | error | No JSON-LD script tag found |
