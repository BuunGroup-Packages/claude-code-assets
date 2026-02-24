# Build Complete SDK

Full end-to-end SDK generation from API documentation. Orchestrates all generation
in the optimal execution order.

## CRITICAL: Read Best Practices First

Before any generation, read:
```
.claude/assets/best-practices/sdk/ (read relevant topic files for the current phase)
.claude/skills/sdk-generator/docs/PATTERNS.md
```

## Workflow

### Phase 1: ANALYZE (Sequential -- Must Complete First)

Read and deeply analyze the API source to produce a structured analysis report.

1. Read ALL files at the SOURCE path
2. Determine source type (OpenAPI spec, route files, docs, mixed)
3. Extract: resources, endpoints, types, auth patterns, pagination, errors
4. Produce the structured analysis report (see references/analyze.md for format)

Store the analysis report -- it feeds into ALL subsequent phases.

### Phase 2: GENERATE (Parallel -- Spawn ALL in Single Message)

After analysis completes, spawn THREE Task tools in a SINGLE message:

1. **Init** (references/init.md) -- Scaffold project directories + config
2. **Core** (references/core.md) -- HTTP client, auth, retry, errors, pagination
3. **Resources** (references/resources.md) -- Resource classes + type definitions

IMPORTANT: Include the FULL analysis context in each Task prompt. Sub-agents
do not share context -- each needs all relevant information from the analysis.

### Phase 3: TESTS (Sequential -- After Phase 2 Completes)

After all Phase 2 agents complete, generate test scaffolding using references/tests.md patterns.

### Phase 4: FINALIZE (Sequential)

After tests complete, do a final pass:

1. Verify `src/index.ts` exports all public types, client, and errors
2. Verify `src/client.ts` wires all resources
3. Verify `package.json` or `pyproject.toml` has correct name and deps
4. Ensure README.md has accurate quick start example
5. Run a quick `tsc --noEmit` or `mypy` check if possible

## Sub-Agent Configuration

| Phase | Model | Purpose |
|-------|-------|---------|
| 1 | opus | API analysis |
| 2 | haiku | Project scaffold |
| 2 | sonnet | Core infrastructure |
| 2 | sonnet | Resources + types |
| 3 | sonnet | Test scaffolding |

## Error Handling

- If analysis finds NO endpoints, stop and report to user
- If source type cannot be determined, ask user to clarify
- If auth pattern is unclear, default to API Key with env var `{SDK_NAME_UPPER}_API_KEY`
- If pagination is unclear, generate Page<T> wrapper but skip auto-pagination

## Output

```
## SDK Build Complete

**Name**: {SDK_NAME}
**Language**: {LANG}
**API Source**: {SOURCE}
**API Name**: {API_NAME}

### Analysis Summary
- Resources: {count}
- Endpoints: {count}
- Types: {count}
- Auth: {strategy}
- Pagination: {strategy}

### Generated Structure
{FULL_DIRECTORY_TREE}

### Resources
| Resource | Methods | Path |
|----------|---------|------|
| {Name} | list, get, create, update, delete | /{path} |

### Quick Start
\`\`\`bash
cd {SDK_NAME}
npm install
export {ENV_VAR}=your_api_key_here
npm test
npm run build
\`\`\`

### Usage
\`\`\`typescript
import { {ClientName} } from '{SDK_NAME}';
const client = new {ClientName}();
const items = await client.{resource}s.list();
\`\`\`
```
