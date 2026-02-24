---
name: research
description: Web research using Brave Search and WebFetch. Use when you need to search for information, gather data from multiple sources, and compile findings. Keywords - research, search, brave, web, data, facts, investigate.
---

# Research

## Purpose

Search the web, fetch pages, and compile structured findings on any topic. Uses Brave Search (`mcp__brave-search__brave_web_search`) for discovery and `WebFetch` for deep reading.

## Workflow

1. **Search** — run 2-4 Brave searches with varied query angles on the topic
2. **Fetch** — open the top 3-5 results per search and extract relevant data
3. **Compile** — merge findings into a deduplicated, structured list
4. **Cite** — every fact includes its source URL

## Rate Limit Fallback

If Brave Search returns a 429 or any rate limit error, immediately fall back to `WebSearch` for the remaining queries. Do not retry Brave — switch and continue.

## Output Format

Return results as a JSON array written to `./research/<topic-kebab>_<8-char-uuid>.json`:

```json
{
  "topic": "the research topic",
  "date": "YYYY-MM-DD",
  "query_count": 4,
  "source_count": 12,
  "items": [
    {
      "rank": 1,
      "name": "Item name",
      "details": { "key": "value" },
      "sources": ["https://...", "https://..."],
      "confidence": "high|medium|low"
    }
  ],
  "methodology": "Brief description of search queries used",
  "sources": ["https://...", "https://..."]
}
```

Confidence levels:
- **high** — confirmed by 3+ independent sources
- **medium** — confirmed by 2 sources
- **low** — single source only
