# Versioning & Distribution

## Semantic Versioning

- **MAJOR:** Breaking changes to public API
- **MINOR:** New features, backward-compatible
- **PATCH:** Bug fixes, security patches

## TypeScript `package.json`

```json
{
  "name": "@myorg/sdk",
  "version": "1.2.3",
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist", "LICENSE", "README.md"],
  "engines": { "node": ">=18" }
}
```

## Python `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-sdk"
version = "1.2.3"
requires-python = ">=3.9"
dependencies = [
    "httpx>=0.25.0,<1.0",
    "pydantic>=2.0,<3.0",
]

[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio", "ruff", "mypy"]
```

## Publishing Checklist

- [ ] Publish to npm (TypeScript) and PyPI (Python)
- [ ] Include `CHANGELOG.md` with every release
- [ ] Tag releases in git
- [ ] Automate publishing via CI/CD
- [ ] Include `LICENSE` and `README.md` in package
- [ ] Run `npm audit` / `pip-audit` before release
- [ ] Validate package contents (`npm pack --dry-run`)
