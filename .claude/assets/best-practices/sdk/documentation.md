# Documentation Standards

## TSDoc (TypeScript)

```typescript
/**
 * Creates a new user in the system.
 *
 * @remarks
 * Requires the `users:write` scope.
 *
 * @param params - Configuration for the new user
 * @returns The newly created user object
 * @throws {@link AuthenticationError} If the API key lacks `users:write` scope.
 * @throws {@link BadRequestError} If validation fails.
 *
 * @example
 * ```typescript
 * const user = await client.users.create({
 *   name: "Sacha Labourey",
 *   email: "sacha@buungroup.com",
 * });
 * ```
 *
 * @public
 */
async create(params: CreateUserParams): Promise<User> { ... }
```

**Useful tags:** `@param`, `@returns`, `@throws`, `@example`, `@remarks`, `@see`, `@public`, `@internal`, `@deprecated`, `@defaultValue`, `@typeParam`

## Python Docstrings (Google-style)

```python
async def create(self, params: CreateUserParams) -> User:
    """Create a new user in the system.

    Requires the ``users:write`` scope.

    Args:
        params: Configuration for the new user.

    Returns:
        The newly created User object with server-assigned ID.

    Raises:
        AuthenticationError: If the API key lacks ``users:write`` scope.
        BadRequestError: If validation fails.

    Example:
        .. code-block:: python

            user = await client.users.create(
                CreateUserParams(name="Sacha", email="sacha@buungroup.com")
            )
    """
```

## OpenAPI Best Practices

- Always include `operationId` — becomes the method name in generated SDKs
- Use `$ref` via `components/` to reduce duplication
- Include `examples` on request/response schemas
- Mark fields with `readOnly` / `writeOnly`
- Use `tags` to organize into SDK resource groups
- Include `description` on every schema property
- Use `format` hints (`email`, `uri`, `date-time`, `uuid`)
