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
/seo ai llms-txt
/seo ai robots
/seo ai content src/pages/about.astro
```

## AI Crawlers (2026)

| Bot | Company | Purpose |
|-----|---------|---------|
| GPTBot | OpenAI | ChatGPT training |
| OAI-SearchBot | OpenAI | ChatGPT search |
| ChatGPT-User | OpenAI | ChatGPT browsing |
| ClaudeBot | Anthropic | Claude training/search |
| PerplexityBot | Perplexity | AI search engine |
| Google-Extended | Google | Gemini/AI features |
| Googlebot | Google | Google Search + AI |
| Applebot | Apple | Apple Search/Siri |
| Applebot-Extended | Apple | Apple Intelligence |
| Bytespider | ByteDance | TikTok/Doubao AI |
| Meta-ExternalAgent | Meta | Meta AI/Llama |
| FacebookBot | Meta | Facebook AI features |
| Amazonbot | Amazon | Alexa/AI features |
| cohere-ai | Cohere | Cohere models |
| YouBot | You.com | You.com AI search |
| AI2Bot | Allen Institute | AI research |
| Diffbot | Diffbot | Knowledge graph |
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
# =============================================================================
# AI CRAWLERS - Allow with protected routes
# =============================================================================

# OpenAI (ChatGPT)
User-agent: GPTBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

User-agent: OAI-SearchBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

User-agent: ChatGPT-User
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Anthropic (Claude)
User-agent: ClaudeBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Google (Gemini)
User-agent: Google-Extended
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Apple Intelligence
User-agent: Applebot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

User-agent: Applebot-Extended
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Perplexity AI
User-agent: PerplexityBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Meta AI
User-agent: Meta-ExternalAgent
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

User-agent: FacebookBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Amazon (Alexa)
User-agent: Amazonbot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# ByteDance (TikTok)
User-agent: Bytespider
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Cohere
User-agent: cohere-ai
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# You.com
User-agent: YouBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Allen Institute
User-agent: AI2Bot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Diffbot
User-agent: Diffbot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# Common Crawl
User-agent: CCBot
Allow: /
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/

# =============================================================================
# SITEMAP
# =============================================================================
Sitemap: https://yoursite.com/sitemap.xml
```

### Block AI (if needed)

```txt
# Block all AI training/search
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ClaudeBot
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Bytespider
User-agent: Meta-ExternalAgent
User-agent: cohere-ai
User-agent: CCBot
Disallow: /
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
