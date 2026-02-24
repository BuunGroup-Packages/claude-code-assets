---
description: Run SEO implementation and validation
argument-hint: "[command] [framework]"
---

# SEO

Parse the command from `$ARGUMENTS` and execute using the `seo` skill.

## Command Routing

| Pattern | Description |
|---------|-------------|
| `meta [framework]` | Meta tags, Open Graph, Twitter Cards |
| `schema [type]` | JSON-LD structured data |
| `ai [action]` | llms.txt, AI crawler config |
| `perf [target]` | Core Web Vitals optimization |
| `sitemap [framework]` | XML sitemap generation |
| `assets [logo] [color]` | Favicons, OG images, manifests |
| `validate [url]` | Lighthouse audit |
| `all [framework]` | Full SEO setup (all commands) |

## Execution

1. Parse `$ARGUMENTS` to extract the command and its arguments
2. Invoke the `seo` skill with the extracted arguments
3. The skill reads `references/*.md` for generation patterns
4. If no command matches, show the help table
