---
description: Run SEO implementation and validation
argument-hint: "[command] [framework]"
---

# SEO Command

Run `/seo $ARGUMENTS` to implement SEO for the current project.

## Commands

| Command | Description |
|---------|-------------|
| all | Full SEO setup (meta + schema + ai + perf + validate) |
| meta | Meta tags, Open Graph, Twitter Cards |
| schema | JSON-LD structured data |
| ai | llms.txt, AI crawler config |
| perf | Core Web Vitals optimization |
| validate | Run Lighthouse audit |

## Examples

```
/seo all astro
/seo meta
/seo validate
```
