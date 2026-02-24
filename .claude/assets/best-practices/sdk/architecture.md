# Architecture & Design Philosophy

## Specification-First Approach

Your OpenAPI spec should be the **single source of truth** from which SDKs, documentation, and tests are all derived.

```
OpenAPI Spec (YAML/JSON)
    ├── SDK Generation (TypeScript, Python, Go, etc.)
    ├── API Reference Docs (auto-generated)
    ├── Server Stubs / Validation
    └── Integration Tests
```

Commit your OpenAPI description to source control as a first-class source file, not a documentation afterthought.

## Idiomatic Language Conventions

Every SDK must feel native to its target language.

| Convention | TypeScript | Python | Go |
|---|---|---|---|
| Method names | `camelCase` | `snake_case` | `PascalCase` (exported) |
| Class names | `PascalCase` | `PascalCase` | `PascalCase` |
| Constants | `UPPER_CASE` | `UPPER_CASE` | `PascalCase` or `UPPER_CASE` |
| Async pattern | `Promise<T>` / `async/await` | `async/await` with `asyncio` | Goroutines / channels |
| Error handling | Exceptions or `Result<T>` | Exceptions | `(value, error)` tuple |
| HTTP client | `fetch` (native) | `httpx` or `requests` | `net/http` |
| Package manager | npm / yarn | pip / poetry / uv | `go mod` |

## Resource-Oriented Client Design

Model your SDK after your API's resource hierarchy (Stripe, OpenAI, Anthropic pattern).

**TypeScript:**
```typescript
const client = new MyAPI({ apiKey: process.env.MY_API_KEY });
const user = await client.users.create({ name: "Sacha" });
const order = await client.users.orders.list("user_123");
```

**Python:**
```python
client = MyAPI(api_key=os.environ["MY_API_KEY"])
user = client.users.create(name="Sacha")
order = client.users.orders.list("user_123")
```
