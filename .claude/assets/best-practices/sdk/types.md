# Type Safety & Models

## TypeScript

```typescript
// types/models.ts — Domain models mirror API schemas
export interface User {
  readonly id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
  readonly created_at: string;
}

// types/api.ts — Request/response parameter types
export interface CreateUserParams {
  name: string;
  email: string;
  role?: 'admin' | 'user' | 'viewer';
}

export interface ListUsersParams {
  limit?: number;
  after?: string;
  role?: 'admin' | 'user' | 'viewer';
}

export interface Page<T> {
  data: T[];
  has_more: boolean;
  next_cursor: string | null;
}
```

## Python

```python
from pydantic import BaseModel, Field
from typing import Literal, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")

class User(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=255)
    email: str
    role: Literal["admin", "user", "viewer"] = "user"
    created_at: datetime
    model_config = {"frozen": True}  # Immutable response objects

class CreateUserParams(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str
    role: Literal["admin", "user", "viewer"] = "user"

class ListUsersParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    after: str | None = None
    role: Literal["admin", "user", "viewer"] | None = None

class Page(BaseModel, Generic[T]):
    data: list[T]
    has_more: bool
    next_cursor: str | None = None
```
