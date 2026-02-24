# SDK Generation Tools

| Tool | Languages | Approach | Used By |
|---|---|---|---|
| **Stainless** | TS, Python, Go, Java, Kotlin | OpenAPI + custom config | OpenAI, Anthropic, Cloudflare |
| **Speakeasy** | TS, Python, Go, Java, C#, + more | OpenAPI-native, Zod validation | Vercel, various |
| **Fern** | TS, Python, Go, Java, C#, PHP, Ruby, Swift, Rust | OpenAPI or Fern definition | Various |
| **OpenAPI Generator** | 50+ languages | Open-source, template-based | Community |

## Decision Factors

- **Stainless** produces the most polished, "hand-crafted" feeling SDKs (industry leaders)
- **Speakeasy** offers broadest feature set with runtime validation (Zod schemas)
- **OpenAPI Generator** is free but typically requires manual refinement
- All require a well-written OpenAPI spec as the foundation
