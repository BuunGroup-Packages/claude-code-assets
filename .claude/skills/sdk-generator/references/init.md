# Initialize SDK Project

Scaffold a clean SDK project following best practices from:
```
.claude/assets/best-practices/sdk/project-structure.md
```

## Workflow

1. Create project root directory
2. Create directory structure
3. Generate package configuration
4. Generate build/tooling configuration
5. Generate placeholder entry point
6. Generate README skeleton

---

## TypeScript Project (`--lang ts`)

### Directory Structure

```
{SDK_NAME}/
├── src/
│   ├── index.ts
│   ├── client.ts
│   ├── version.ts
│   ├── core/
│   │   └── index.ts
│   ├── resources/
│   │   └── index.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── index.ts
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   └── resources/
│   └── integration/
├── examples/
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── vitest.config.ts
├── .eslintrc.json
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

### package.json

```json
{
  "name": "${SDK_NAME}",
  "version": "0.1.0",
  "description": "SDK for ${API_NAME}",
  "type": "module",
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/esm/index.d.ts",
        "default": "./dist/esm/index.js"
      },
      "require": {
        "types": "./dist/cjs/index.d.ts",
        "default": "./dist/cjs/index.js"
      }
    }
  },
  "files": [
    "dist",
    "LICENSE",
    "README.md"
  ],
  "engines": {
    "node": ">=18"
  },
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "eslint": "^9.0.0",
    "tsup": "^8.0.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  },
  "keywords": ["sdk", "api", "typescript"],
  "license": "MIT"
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### tsconfig.build.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "declaration": true,
    "declarationDir": "./dist"
  },
  "exclude": ["tests", "examples", "**/*.test.ts"]
}
```

### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/**/index.ts'],
    },
  },
});
```

### src/version.ts

```typescript
export const VERSION = '0.1.0';
```

### src/index.ts (placeholder)

```typescript
export { VERSION } from './version';
// Client, types, and errors will be added by other generation steps
```

### .gitignore

```
node_modules/
dist/
*.tsbuildinfo
.env
.env.*
coverage/
```

---

## Python Project (`--lang py`)

### Directory Structure

```
{SDK_NAME}/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       ├── py.typed
│       ├── _client.py
│       ├── _version.py
│       ├── _core/
│       │   └── __init__.py
│       ├── resources/
│       │   └── __init__.py
│       ├── types/
│       │   └── __init__.py
│       └── _utils/
│           └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   └── resources/
│   └── integration/
├── examples/
├── pyproject.toml
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

Where `{package_name}` is `SDK_NAME` converted to `snake_case` with hyphens replaced by underscores.

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "${SDK_NAME}"
version = "0.1.0"
description = "SDK for ${API_NAME}"
readme = "README.md"
license = "MIT"
requires-python = ">=3.9"
dependencies = [
    "httpx>=0.27.0,<1.0",
    "pydantic>=2.0,<3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-httpx>=0.30",
    "ruff>=0.8",
    "mypy>=1.13",
]

[tool.ruff]
target-version = "py39"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.9"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### src/{package_name}/_version.py

```python
__version__ = "0.1.0"
```

### src/{package_name}/__init__.py (placeholder)

```python
from {package_name}._version import __version__

__all__ = ["__version__"]
```

### src/{package_name}/py.typed

Empty file (PEP 561 marker).

### .gitignore

```
__pycache__/
*.py[cod]
*$py.class
dist/
*.egg-info/
.env
.env.*
.venv/
.mypy_cache/
.pytest_cache/
.ruff_cache/
coverage/
htmlcov/
```

---

## README.md Skeleton

```markdown
# {SDK_NAME}

Official SDK for {API_NAME}.

## Installation

\`\`\`bash
npm install {SDK_NAME}
\`\`\`

## Quick Start

\`\`\`typescript
import { {ClientName} } from '{SDK_NAME}';

const client = new {ClientName}();
\`\`\`

## Documentation

See [API Reference]({API_DOCS_URL}) for full documentation.

## License

MIT
```

---

## Output

```
## SDK Project Initialized

**Name**: {SDK_NAME}
**Language**: {LANG}
**Package Manager**: npm | uv

### Structure
{DIRECTORY_TREE}

### Next Steps
\`\`\`bash
cd {SDK_NAME}
npm install  # or: uv sync
\`\`\`
```
