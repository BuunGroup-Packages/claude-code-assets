# Plan API Architecture

Read and deeply analyze project context — requirements docs, existing APIs, database schemas,
or verbal descriptions — then produce a structured architecture plan that drives all
subsequent generation.

This is always the FIRST step before generating any API code.

## Best Practices Reference

ALWAYS read before planning:
```
.claude/assets/best-practices/hono-cf-workers/ (read relevant topic files)
.claude/skills/api-generator/docs/PATTERNS.md
```

## Workflow

1. Read ALL context sources thoroughly
2. Identify the API's domain and purpose
3. Extract resources and their relationships
4. Map out endpoints for each resource
5. Determine authentication strategy
6. Determine rate limiting tiers
7. Identify Cloudflare bindings needed (D1, KV, R2)
8. Design database schema
9. Identify middleware requirements
10. Produce the structured plan

## Context Analysis Process

### For Requirements Documents
1. Read all markdown/text files
2. Extract feature descriptions -> map to API resources
3. Identify user roles -> map to auth strategy
4. Identify data entities -> map to database tables
5. Extract business rules -> map to service layer logic

### For Existing API Code
1. Read all route handler files
2. Map routes to resource groups
3. Extract validation schemas
4. Identify missing patterns (error handling, pagination, etc.)
5. Propose improvements based on best practices

### For Database Schemas
1. Read table definitions
2. Map tables to API resources
3. Identify relationships (foreign keys)
4. Design CRUD endpoints for each resource
5. Add pagination for list endpoints

### For Verbal Descriptions
1. Parse the description for entities and actions
2. Ask clarifying questions if critical details are missing
3. Propose a resource structure
4. Present the plan for approval before proceeding

## Output Format

Produce this EXACT structure as a markdown plan. This plan is consumed by
all other generation steps.

```markdown
# API Architecture Plan

## Overview
- **API Name**: {name}
- **Purpose**: {one-sentence description}
- **Base Path**: /api
- **Version**: v1

## Authentication
- **Strategy**: API Key | JWT | Both
- **Header**: X-API-Key | Authorization: Bearer {token}
- **Public endpoints**: /health, /ready, {others}
- **Protected endpoints**: /api/*
- **Roles**: {admin, member, viewer} | None

## Cloudflare Bindings
| Binding | Type | Name | Purpose |
|---------|------|------|---------|
| DB | D1 | {api-name}-db | Primary database |
| KV | KV | {api-name}-kv | Cache / sessions |
| BUCKET | R2 | {api-name}-uploads | File storage |
| RATE_LIMITER | Rate Limit | Standard (100/60s) | General API |
| RATE_LIMITER_STRICT | Rate Limit | Strict (10/60s) | Auth endpoints |

## Resources

### {ResourceName}
**Table**: {table_name}
**Base path**: /api/{resource}

#### Database Schema
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK, UUID | Unique identifier |
| name | TEXT | NOT NULL | Display name |
| created_at | TEXT | NOT NULL, DEFAULT now | Creation timestamp |
| updated_at | TEXT | NOT NULL, DEFAULT now | Last update |

#### Relationships
- belongs_to: {other_resource} (via {foreign_key})
- has_many: {other_resource}

#### Endpoints
| Method | Path | Operation | Auth | Rate Limit | Description |
|--------|------|-----------|------|------------|-------------|
| GET | /api/{resource} | list | Required | Standard | List with pagination |
| GET | /api/{resource}/:id | get | Required | Standard | Get by ID |
| POST | /api/{resource} | create | Required | Standard | Create new |
| PUT | /api/{resource}/:id | update | Required | Standard | Update existing |
| DELETE | /api/{resource}/:id | delete | Required | Standard | Delete |

#### Schemas
**Create{Resource}**:
| Field | Type | Required | Validation | Default |
|-------|------|----------|------------|---------|
| name | string | yes | min:1, max:255 | -- |
| email | string | yes | email format | -- |

**Update{Resource}**: All Create fields, all optional (Partial)

**List{Resource}Query**: paginationQuery + filters:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| search | string | no | Name search |
| role | enum | no | Filter by role |

### {NextResource}
... repeat for each resource ...

## Middleware Stack
| Order | Middleware | Scope | Configuration |
|-------|-----------|-------|---------------|
| 1 | request-id | * | UUID or forwarded X-Request-Id |
| 2 | structured-logger | * | JSON, includes request_id |
| 3 | secure-headers | * | nosniff, DENY, strict-origin |
| 4 | cors | /api/* | {allowed origins} |
| 5 | rate-limit | /api/* | 100 req/60s per API key |
| 6 | auth | /api/* | API Key (constant-time compare) |

## Environment Variables
| Name | Source | Description |
|------|--------|-------------|
| ENVIRONMENT | vars | production/staging |
| API_VERSION | vars | v1 |
| LOG_LEVEL | vars | info/debug |
| API_KEY | secret | API authentication key |
| JWT_SECRET | secret | JWT signing secret |

## Summary
- **Total Resources**: {count}
- **Total Endpoints**: {count}
- **Total Tables**: {count}
- **Auth**: {strategy}
- **Bindings**: D1{, KV}{, R2}
- **Estimated files**: {count}
```

## Key Rules

1. ALWAYS read the ENTIRE context — do not skip files
2. Every resource MUST have a database schema section
3. Every endpoint MUST specify auth and rate limit requirements
4. Identify ALL relationships between resources
5. Include pagination on ALL list endpoints
6. Include health check (/health + /ready) in every API
7. Use UUID primary keys (TEXT type in SQLite/D1)
8. Use `created_at` and `updated_at` timestamps on every table
9. If the context is ambiguous, note assumptions clearly
10. Present the plan to the user for review before proceeding to generation
