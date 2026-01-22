---
name: seo-ai
description: |
  Implement AI SEO: llms.txt for AI assistants, robots.txt AI crawler config,
  and content optimization for LLM extraction. Auto-validates via PostToolUse
  hook. Use when optimizing for ChatGPT, Perplexity, Claude, or Google AI.
argument-hint: "[action] [file]"
hooks:
  PostToolUse:
    - matcher: "Edit|Write|MultiEdit"
      hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_ai_validate.py"
---

# AI SEO Implementation

## Overview

Optimizes site for AI search engines and assistants.
PostToolUse hook validates every edit automatically.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | action | llms-txt, robots, content | llms-txt |
| $2 | file | Target file path | Auto-select |

## Usage

```bash
/seo-ai llms-txt
/seo-ai robots
/seo-ai content src/pages/about.astro
```

## AI Crawlers

| Bot | Company | Purpose |
|-----|---------|---------|
| GPTBot | OpenAI | ChatGPT training/search |
| ClaudeBot | Anthropic | Claude training/search |
| PerplexityBot | Perplexity | AI search engine |
| Google-Extended | Google | Gemini/AI features |
| Amazonbot | Amazon | Alexa/AI features |
| CCBot | Common Crawl | Open dataset |

## llms.txt Specification

Create `public/llms.txt`:

```txt
# Site Name
> One-line description of your site

## About
2-3 sentences about what your site does and who it's for.
Include key information AI assistants should know.

## Key Pages
- /about: About us and our mission
- /products: Our product catalog
- /docs: Documentation and guides
- /contact: How to reach us

## Contact
- Email: hello@yoursite.com
- Support: support@yoursite.com
```

### Required Sections

| Section | Error Code | Description |
|---------|------------|-------------|
| Title (# Name) | AI003 | First line, site name |
| Description (> ...) | AI004 | One-line summary |
| ## About | AI002 | Detailed description |

### Recommended Sections

| Section | Error Code | Description |
|---------|------------|-------------|
| ## Key Pages | AI002 | Important page list |
| ## Contact | AI002 | Contact information |

## robots.txt for AI

Add to `public/robots.txt`:

```txt
# AI Crawlers - Allow access
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Sitemap
Sitemap: https://yoursite.com/sitemap.xml
```

### Block AI (if needed)

```txt
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /
```

## Validation

PostToolUse hook runs `post_ai_validate.py` after every edit.

**On failure**, returns:
```
✗ AI-SEO VALIDATION FAILED
File: public/llms.txt
Errors: 1 | Warnings: 2

============================================================
FIX INSTRUCTIONS (execute in order):
============================================================

1. [AI003] llms.txt at line 1
   Rule: llms.txt must have site title on first line
   Expected: # Site Name
   Fix: Add '# Site Name' as first line of llms.txt.

------------------------------------------------------------
WARNINGS (recommended fixes):
------------------------------------------------------------

1. [AI002] llms.txt
   Rule: llms.txt should have 'Key Pages' section
   Expected: ## Key Pages
   Fix: Add '## Key Pages' section with important URLs.

============================================================
After fixing, save file. Validation re-runs automatically.
```

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| AI001 | error | Missing llms.txt file |
| AI002 | warning | Missing recommended section |
| AI003 | error | Missing title in llms.txt |
| AI004 | error | Missing description in llms.txt |
| AI005 | warning | robots.txt blocks AI crawler |
| AI006 | warning | Missing robots.txt |
| AI007 | warning | llms.txt too short (<100 chars) |
| AI008 | warning | Wildcard may block AI bots |
| AI009 | warning | Missing sitemap in robots.txt |
