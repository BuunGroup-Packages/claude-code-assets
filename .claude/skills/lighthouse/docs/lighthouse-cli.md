# Lighthouse CLI Reference

> Sources: [GitHub](https://github.com/GoogleChrome/lighthouse) | [Chrome DevTools Docs](https://developer.chrome.com/docs/lighthouse/overview) | [CLI Flags](https://github.com/GoogleChrome/lighthouse#cli-options) | [Node API](https://github.com/GoogleChrome/lighthouse/blob/main/docs/readme.md#using-programmatically) | [User Flows](https://github.com/GoogleChrome/lighthouse/blob/main/docs/user-flows.md) | [Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring) | [Budgets](https://developer.chrome.com/docs/lighthouse/performance/performance-budgets) | [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)

## Install

```bash
npm install -g lighthouse   # global
npx lighthouse <url>        # one-off
```

Requires Node 22+ and Google Chrome.

## Syntax

```
lighthouse <url> [flags]
```

## All Flags

### Output
| Flag | Description |
|------|-------------|
| `--output [html\|json\|csv]` | Report format(s), combine multiple |
| `--output-path <path>` | Output destination (extensions auto-appended) |
| `--view` | Open HTML report in browser |
| `--save-assets` | Save trace + devtools logs to disk |
| `--list-all-audits` | Print all available audit IDs |
| `--list-trace-categories` | Print trace categories |

### Logging
| Flag | Description |
|------|-------------|
| `--verbose` | Detailed logging |
| `--quiet` | Suppress all output |

### Category & Audit Selection
| Flag | Description |
|------|-------------|
| `--only-categories [cat,...]` | Run specific categories only |
| `--only-audits [id ...]` | Run specific audits only |
| `--skip-audits [id ...]` | Exclude specific audits |
| `--budget-path <path>` | Performance budget JSON |

### Device & Emulation
| Flag | Description |
|------|-------------|
| `--preset=desktop` | Desktop scoring + emulation + throttling |
| `--form-factor [mobile\|desktop]` | Scoring profile (doesn't change emulation) |
| `--screenEmulation.width=N` | Screen width (default 360 mobile) |
| `--screenEmulation.height=N` | Screen height (default 640 mobile) |
| `--screenEmulation.deviceScaleFactor=N` | Device pixel ratio |
| `--screenEmulation.mobile=BOOL` | Mobile overlay scrollbars |
| `--screenEmulation.disabled` | Disable screen emulation |
| `--emulatedUserAgent <string>` | Custom user agent |
| `--no-emulatedUserAgent` | Disable UA spoofing |

### Throttling
| Flag | Description |
|------|-------------|
| `--throttling-method [simulate\|devtools\|provided]` | Throttling approach |
| `--throttling.rttMs=N` | Simulated RTT (default 150) |
| `--throttling.throughputKbps=N` | Download throughput (default 1638) |
| `--throttling.uploadThroughputKbps=N` | Upload throughput (default 750) |
| `--throttling.cpuSlowdownMultiplier=N` | CPU slowdown (default 4) |

Throttling methods:
- `simulate` (default) — fast, deterministic, based on unthrottled data
- `devtools` — request-level throttling via DevTools protocol
- `provided` — no throttling (use with external throttling)

### Chrome & Connection
| Flag | Description |
|------|-------------|
| `--chrome-flags="<flags>"` | Custom Chrome arguments (quoted) |
| `--chrome-ignore-default-flags` | Disable Lighthouse's default Chrome flags |
| `--port <N>` | Chrome debugging protocol port (0=random) |
| `--hostname <string>` | Debugging protocol host (default localhost) |
| `--disable-storage-reset` | Keep cache/storage between runs |
| `--disable-full-page-screenshot` | Skip full-page screenshot |

### Configuration
| Flag | Description |
|------|-------------|
| `--config-path <path>` | Custom config JS file |
| `--preset [perf\|experimental\|desktop]` | Built-in preset |
| `--plugins [plugin1 plugin2]` | Run plugins |
| `--locale <lang>` | Report language |
| `--extra-headers <json\|path>` | Custom HTTP headers |
| `--blocked-url-patterns [patterns]` | Block matching requests |
| `--max-wait-for-load <ms>` | Page load timeout |

### Artifact Lifecycle
| Flag | Description |
|------|-------------|
| `-G` | Gather artifacts only (no audit) |
| `-A` | Audit saved artifacts (no browser) |
| `-GA` | Full run + save artifacts |
| `-GA=./folder` | Custom artifact folder |

## Node API

> [Programmatic usage](https://github.com/GoogleChrome/lighthouse/blob/main/docs/readme.md#using-programmatically) | [chrome-launcher](https://github.com/GoogleChrome/chrome-launcher)

```javascript
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
const result = await lighthouse('https://example.com', {
  logLevel: 'info',
  output: 'html',
  onlyCategories: ['performance'],
  port: chrome.port
});

// result.report — HTML string
// result.lhr — Lighthouse Result object
console.log('Performance:', result.lhr.categories.performance.score * 100);
chrome.kill();
```

## User Flows (Multi-step)

> [User Flows guide](https://github.com/GoogleChrome/lighthouse/blob/main/docs/user-flows.md)

```javascript
import {startFlow} from 'lighthouse';
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({headless: true});
const page = await browser.newPage();
const flow = await startFlow(page);

// Navigation — full performance score
await flow.navigate('https://example.com');

// Timespan — measures during interactions (CLS, TBT)
await flow.startTimespan();
await page.click('#button');
await flow.endTimespan();

// Snapshot — current page state (accessibility, best-practices)
await flow.snapshot();

const report = await flow.generateReport(); // HTML
await browser.close();
```

Desktop flows: `import {desktopConfig} from 'lighthouse'` then pass `{config: desktopConfig}`.

## Custom Config

> [Configuration](https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md)

```javascript
// custom-config.js
export default {
  extends: 'lighthouse:default',
  settings: {
    onlyCategories: ['performance', 'accessibility'],
    formFactor: 'desktop',
    throttling: { rttMs: 40, throughputKbps: 10240, cpuSlowdownMultiplier: 1 },
  },
};
```

```bash
lighthouse https://example.com --config-path=./custom-config.js
```

## Lighthouse CI

> [Lighthouse CI repo](https://github.com/GoogleChrome/lighthouse-ci) | [Configuration](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md) | [Assertions](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#assert)

```json
{
  "ci": {
    "collect": {
      "url": ["https://example.com"],
      "numberOfRuns": 3,
      "settings": { "preset": "desktop" }
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "categories:accessibility": ["warn", {"minScore": 0.95}]
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

Config filenames (searched in order): `.lighthouserc.{js,cjs,json,yml,yaml}`, `lighthouserc.{js,cjs,json,yml,yaml}`

## Authenticated Pages

> [Auth guide](https://github.com/GoogleChrome/lighthouse/blob/main/docs/authenticated-pages.md)

```bash
# Header auth
lighthouse https://example.com --extra-headers='{"Authorization":"Bearer TOKEN"}'

# Cookie auth
lighthouse https://example.com --extra-headers='{"Cookie":"session=abc123"}'

# Existing Chrome session (manual login first)
chrome-debug                               # Terminal 1: launch + login
lighthouse https://example.com --port=9222 --disable-storage-reset  # Terminal 2
```

## Performance Budget

> [Performance budgets](https://developer.chrome.com/docs/lighthouse/performance/performance-budgets) | [Budget format](https://github.com/GoogleChrome/budget.json)

```json
[{
  "path": "/*",
  "resourceSizes": [
    {"resourceType": "script", "budget": 125},
    {"resourceType": "image", "budget": 100},
    {"resourceType": "total", "budget": 300}
  ],
  "resourceCounts": [
    {"resourceType": "third-party", "budget": 10}
  ],
  "timings": [
    {"metric": "interactive", "budget": 3000},
    {"metric": "first-meaningful-paint", "budget": 1000}
  ]
}]
```

Resource types: `document`, `font`, `image`, `media`, `other`, `script`, `stylesheet`, `third-party`, `total`

## LHR Object Structure

> [LHR typedefs](https://github.com/GoogleChrome/lighthouse/blob/main/types/lhr/lhr.d.ts) | [Report viewer](https://googlechrome.github.io/lighthouse/viewer/)

```
lhr.lighthouseVersion        — version string
lhr.fetchTime                — ISO-8601 timestamp
lhr.requestedUrl             — initial URL
lhr.finalDisplayedUrl        — URL after redirects + history API
lhr.categories[id].score     — 0-1 weighted average
lhr.audits[id].score         — 0-1 or null
lhr.audits[id].numericValue  — raw metric value
lhr.audits[id].displayValue  — formatted string
lhr.audits[id].details       — detailed findings object
lhr.audits[id].scoreDisplayMode — binary|numeric|error|manual|notApplicable|informative
lhr.configSettings           — config used for this run
lhr.timing.total             — total audit time (ms)
lhr.runtimeError             — critical error if any
lhr.runWarnings              — array of warnings
```

## Default Throttling (Mobile)

- Network: RTT 150ms, Download 1.6 Mbps, Upload 750 Kbps
- CPU: 4x slowdown
- Represents bottom 25% of 4G connections

## Batch Auditing

```bash
for url in https://example.com https://example.com/about; do
  slug=$(echo "$url" | sed 's/[^a-zA-Z0-9]/_/g')
  npx lighthouse "$url" --output json --output-path="./reports/${slug}.json" \
    --chrome-flags="--headless" --quiet
done
```

## References

| Topic | URL |
|-------|-----|
| GitHub repo | https://github.com/GoogleChrome/lighthouse |
| npm package | https://www.npmjs.com/package/lighthouse |
| Chrome DevTools overview | https://developer.chrome.com/docs/lighthouse/overview |
| Performance scoring | https://developer.chrome.com/docs/lighthouse/performance/performance-scoring |
| Performance budgets | https://developer.chrome.com/docs/lighthouse/performance/performance-budgets |
| Accessibility scoring | https://developer.chrome.com/docs/lighthouse/accessibility/scoring |
| SEO audits | https://developer.chrome.com/docs/lighthouse/seo |
| Best practices audits | https://developer.chrome.com/docs/lighthouse/best-practices |
| Node API docs | https://github.com/GoogleChrome/lighthouse/blob/main/docs/readme.md#using-programmatically |
| User flows guide | https://github.com/GoogleChrome/lighthouse/blob/main/docs/user-flows.md |
| Configuration | https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md |
| Authenticated pages | https://github.com/GoogleChrome/lighthouse/blob/main/docs/authenticated-pages.md |
| Throttling | https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md |
| Plugins | https://github.com/GoogleChrome/lighthouse/blob/main/docs/plugins.md |
| LHR typedefs | https://github.com/GoogleChrome/lighthouse/blob/main/types/lhr/lhr.d.ts |
| Report viewer | https://googlechrome.github.io/lighthouse/viewer/ |
| Lighthouse CI | https://github.com/GoogleChrome/lighthouse-ci |
| LHCI configuration | https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md |
| chrome-launcher | https://github.com/GoogleChrome/chrome-launcher |
| Budget.json spec | https://github.com/GoogleChrome/budget.json |
| PageSpeed Insights API | https://developers.google.com/speed/docs/insights/v5/get-started |
