# Project Structure

## TypeScript SDK

```
my-sdk/
├── src/
│   ├── index.ts                    # Public API barrel export
│   ├── client.ts                   # Main client class
│   ├── version.ts                  # SDK version constant
│   ├── core/
│   │   ├── http-client.ts          # HTTP transport layer
│   │   ├── auth.ts                 # Authentication handlers
│   │   ├── retry.ts                # Retry logic with backoff
│   │   ├── pagination.ts           # Pagination helpers
│   │   ├── streaming.ts            # SSE / streaming support
│   │   └── errors.ts               # Error class hierarchy
│   ├── resources/
│   │   ├── users.ts                # Users resource
│   │   ├── orders.ts               # Orders resource
│   │   └── webhooks.ts             # Webhook handling
│   ├── types/
│   │   ├── api.ts                  # API request/response types
│   │   ├── models.ts               # Domain model interfaces
│   │   ├── errors.ts               # Error types
│   │   └── shared.ts               # Shared/common types
│   └── utils/
│       ├── headers.ts              # Header construction
│       ├── serialization.ts        # JSON/form-data helpers
│       └── validators.ts           # Input validation (Zod)
├── tests/
│   ├── unit/
│   └── integration/
├── examples/
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

## Python SDK

```
my-sdk/
├── src/
│   └── my_sdk/
│       ├── __init__.py              # Public API exports
│       ├── py.typed                 # PEP 561 marker
│       ├── _client.py               # Main client class
│       ├── _version.py              # Version constant
│       ├── _core/
│       │   ├── _http_client.py      # HTTP transport
│       │   ├── _auth.py             # Authentication
│       │   ├── _retry.py            # Retry with backoff
│       │   ├── _pagination.py       # Pagination iterators
│       │   ├── _streaming.py        # SSE / streaming
│       │   └── _errors.py           # Exception hierarchy
│       ├── resources/
│       ├── types/
│       └── _utils/
├── tests/
├── examples/
├── pyproject.toml
└── README.md
```

**Python conventions:**
- Use `src/` layout to prevent accidental local imports during testing
- Include `py.typed` marker for PEP 561 compliance
- Prefix internal modules with `_` to signal private API
- Use `__init__.py` as public API gateways

## Barrel Exports

**TypeScript — explicit named re-exports:**
```typescript
// src/index.ts
export { MyAPIClient } from './client';
export type { ClientOptions } from './client';
export type { User, Order, CreateUserParams } from './types';
export { APIError, AuthenticationError, RateLimitError } from './core/errors';
```

- Use `export { X }` over `export *` for tree-shaking
- One level of barrel files per logical group
- Avoid deeply nested re-exports (circular dependency risk)

**Python — `__init__.py` as public API:**
```python
from my_sdk._client import MyAPIClient
from my_sdk._core._errors import APIError, AuthenticationError, RateLimitError
from my_sdk.types import User, Order, CreateUserParams
from my_sdk._version import __version__

__all__ = ["MyAPIClient", "APIError", "AuthenticationError", ...]
```
