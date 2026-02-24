---
description: Run Puppeteer browser automation tasks
argument-hint: "<action> [url] [options]"
---

# Puppeteer

Run browser automation using the `puppeteer` skill. Writes and executes Puppeteer scripts for headless Chrome tasks.

## Command Routing

Parse `$ARGUMENTS` to determine the action:

| Pattern | Description |
|---------|-------------|
| `screenshot <url> [path]` | Take a full-page screenshot |
| `pdf <url> [path]` | Generate a PDF of the page |
| `scrape <url> [selector]` | Extract text/data from elements |
| `intercept <url> [pattern]` | Navigate with network interception, log requests |
| `prerender <dist> [routes...]` | Prerender Vite SPA routes for SEO |
| `audit <url>` | Puppeteer + Lighthouse authenticated audit |
| `<prompt>` | Freeform — write a Puppeteer script for the described task |

## Execution

1. Parse `$ARGUMENTS` to extract the action, URL, and options
2. Read `.claude/skills/puppeteer/SKILL.md` for API patterns
3. Write a Puppeteer script (`.mjs`) tailored to the action
4. Execute: `node script.mjs`
5. Report results and clean up temp files

## Examples

```
/puppeteer screenshot https://example.com shot.png
/puppeteer pdf https://example.com --format=A4
/puppeteer scrape https://example.com ".product-card h2"
/puppeteer prerender dist / /about /pricing /contact
/puppeteer intercept https://example.com "/api/*"
/puppeteer audit http://localhost:3000
/puppeteer login to example.com, navigate to dashboard, take screenshot
```

## Default Behavior

If no recognized action keyword is found, treat the entire argument as a freeform prompt and write a Puppeteer script that accomplishes the described task.
