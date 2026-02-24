# Security

## API Key & Secrets Handling

```typescript
// Good — environment variable
const client = new MyAPI({ apiKey: process.env.MY_API_KEY });

// Good — auto-detect from environment
const client = new MyAPI();  // Reads MY_API_KEY from env

// Bad — hardcoded key
const client = new MyAPI({ apiKey: "sk-live-abc123..." });
```

**Requirements:**
- Auto-detect API keys from well-known env vars
- Never log credentials in debug logs, error messages, or stack traces
- Default to HTTPS; reject HTTP unless explicitly overridden for local dev
- Validate key format client-side before making network requests
- Always use headers (Authorization / X-API-Key), never query parameters
- Support OAuth 2.0 / JWT refresh flows where applicable

## Authentication Patterns

```typescript
const client = new MyAPI({
  apiKey: process.env.MY_API_KEY,       // API Key
  bearerToken: accessToken,              // Bearer token
  oauth: {                               // OAuth2
    clientId: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRET,
    tokenUrl: "https://auth.example.com/token",
  },
});
```

**OpenAPI Security Scheme:**
```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## Input Validation

**TypeScript (Zod):**
```typescript
const CreateUserSchema = z.object({
  name: z.string().min(1).max(255),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'viewer']).default('user'),
});
```

**Python (Pydantic):**
```python
class CreateUserParams(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: Literal["admin", "user", "viewer"] = "user"
```

## Dependency Security

- Pin dependencies to exact versions or narrow ranges
- Use `npm audit` / `pip-audit` in CI
- Minimize third-party dependencies
- Monitor CVEs with Dependabot / Renovate
