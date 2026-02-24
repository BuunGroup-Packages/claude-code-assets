# Analyze API Source

Read and deeply analyze API documentation to produce a structured report that
drives SDK generation. This is always the FIRST step before generating any SDK code.

## Workflow

1. Detect source type (OpenAPI spec, route files, markdown docs, URL)
2. Read ALL source files thoroughly
3. Extract resources, endpoints, request/response types, auth patterns
4. Identify pagination strategy
5. Identify error response format
6. Produce structured analysis report

## Source Detection

| Pattern | Source Type | Action |
|---------|------------|--------|
| `*.yaml`, `*.json` with `openapi:` | OpenAPI Spec | Parse spec directly |
| `*.ts` with route handlers | TypeScript Routes | Analyze Hono/Express/Fastify routes |
| `*.py` with route handlers | Python Routes | Analyze FastAPI/Flask/Django routes |
| `*.md` files | Documentation | Extract endpoints from prose |
| Directory path | Mixed | Scan for all above types |
| `http://`, `https://` | URL | Fetch and analyze page content |

## Analysis Process

### For OpenAPI Specs
1. Parse the YAML/JSON spec
2. Group paths by tags -> these become SDK resources
3. Extract `operationId` -> these become method names
4. Map `components/schemas` -> these become TypeScript interfaces / Pydantic models
5. Identify `securitySchemes` -> determines auth pattern
6. Check for pagination patterns (cursor, offset, page)
7. Document error response schemas

### For Route Source Code
1. Read all route handler files
2. Identify the framework (Hono, Express, FastAPI, etc.)
3. Map route paths to resource groups (e.g., `/api/users/*` -> `users` resource)
4. Extract request validation schemas (Zod, Pydantic, Joi)
5. Extract response types from return statements
6. Identify middleware patterns (auth, rate limiting)
7. Identify database models if present

### For Documentation
1. Read all markdown files
2. Identify endpoint tables or lists (method + path + description)
3. Extract request/response examples from code blocks
4. Identify authentication instructions
5. Map endpoints to logical resource groups

## Output Format

Produce this EXACT structure as a markdown report. This report is consumed by
other generation steps.

```markdown
# API Analysis Report

## Meta
- **API Name**: {name}
- **Base URL**: {url}
- **API Version**: {version}
- **Source Type**: OpenAPI | Routes | Documentation | Mixed
- **Source Path**: {path}

## Authentication
- **Strategy**: API Key | Bearer Token | OAuth2 | None
- **Header**: Authorization: Bearer {key} | X-API-Key: {key}
- **Env Variable**: {ENV_VAR_NAME}
- **Notes**: {any special auth details}

## Pagination
- **Strategy**: Cursor | Offset | Page | None
- **Cursor Field**: {field_name} (e.g., `next_cursor`)
- **Limit Field**: {field_name} (e.g., `limit`)
- **Has More Field**: {field_name} (e.g., `has_more`)

## Error Format
- **Structure**: { message, code, status } | { error: { message, type } } | Custom
- **Request ID Header**: {header_name} (e.g., `x-request-id`)
- **Rate Limit Headers**: {headers} (e.g., `x-ratelimit-remaining`)

## Resources

### {ResourceName}
Base path: `/{resource_path}`

| Method | Endpoint | Operation | Description |
|--------|----------|-----------|-------------|
| GET | /{resource} | list | List all {resource} |
| GET | /{resource}/:id | get | Get single {resource} |
| POST | /{resource} | create | Create {resource} |
| PUT | /{resource}/:id | update | Update {resource} |
| DELETE | /{resource}/:id | delete | Delete {resource} |

#### Types

**{ResourceName}** (response model):
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes | Unique identifier |
| name | string | yes | Display name |
| created_at | string (ISO 8601) | yes | Creation timestamp |

**Create{ResourceName}Params** (request):
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| name | string | yes | -- | Display name |
| role | "admin" \| "user" | no | "user" | Access level |

**Update{ResourceName}Params** (request):
All fields from Create optional (Partial<Create{ResourceName}Params>)

### {NextResource}
...repeat for each resource...

## Summary
- **Total Resources**: {count}
- **Total Endpoints**: {count}
- **Total Types**: {count}
- **Auth Required**: Yes | No
- **Pagination**: Yes ({strategy}) | No
- **Streaming**: Yes | No
```

## Key Rules

1. ALWAYS read the ENTIRE source -- do not skip files or sections
2. Group endpoints by URL prefix into logical resources
3. Use `operationId` as method name when available, otherwise derive from HTTP method + path
4. Prefer TypeScript-style type names: `PascalCase` for models, `camelCase` for fields
5. Identify ALL request parameters: path params, query params, body fields, headers
6. Note which fields are read-only (server-assigned) vs writable
7. Document pagination if any endpoint returns lists
8. Flag any streaming/SSE endpoints
9. If the API uses non-standard patterns, note them in the analysis
