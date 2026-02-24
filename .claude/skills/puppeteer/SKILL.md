---
name: puppeteer
description: Browser automation with Puppeteer. Launch headless Chrome, navigate pages, interact with elements, take screenshots, generate PDFs, intercept network, evaluate JS. Keywords - puppeteer, browser, headless, scrape, screenshot, pdf, automation.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Puppeteer

## Purpose

Automate Chrome programmatically via Puppeteer. Launch headless browsers, navigate pages, interact with DOM, take screenshots, generate PDFs, intercept network requests, and evaluate JavaScript in page context.

## Key Details

- **Headless by default** — pass `headless: false` for visible browser
- **Auto-downloads Chrome** — `puppeteer` package includes browser; `puppeteer-core` does not
- **Locator API** (recommended) — auto-waits for visibility, stability, enabled state
- **Shadow DOM** — `>>>` (deep descendant) and `>>>>` (deep child) combinators
- **Network interception** — block, modify, or mock any request
- **Integrates with Lighthouse** — pass page to `lighthouse()` for authenticated audits

## Quick Reference

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://example.com', { waitUntil: 'networkidle2' });

// Interact
await page.locator('button').click();
await page.locator('input').fill('text');
await page.locator('::-p-text(Submit)').click();

// Extract
const title = await page.title();
const text = await page.$eval('.el', el => el.textContent);
const items = await page.$$eval('.item', els => els.map(e => e.textContent));

// Screenshot / PDF
await page.screenshot({ path: 'shot.png', fullPage: true });
await page.pdf({ path: 'page.pdf', format: 'A4' });

await browser.close();
```

## Selectors

```
CSS:      page.locator('div.class')
Text:     page.locator('::-p-text(Click me)')
ARIA:     page.locator('::-p-aria(Submit)')
XPath:    page.locator('::-p-xpath(//h2)')
Shadow:   page.locator('my-el >>> button')       # deep descendant
Pierce:   page.locator('my-el >>>> button')      # immediate shadow root
```

## Launch Options

```javascript
const browser = await puppeteer.launch({
  headless: true,           // true | false | 'shell' (fastest, fewer features)
  args: ['--no-sandbox'],   // Chrome flags
  executablePath: '/path',  // custom Chrome binary
  userDataDir: './profile', // persist cookies/storage
  devtools: false,          // auto-open DevTools (forces headed)
  timeout: 30000,           // startup timeout (0 = none)
  channel: 'chrome',        // use installed Chrome instead of bundled
});
```

## Navigation

```javascript
await page.goto(url, { waitUntil, timeout });
// waitUntil: 'load' | 'domcontentloaded' | 'networkidle0' | 'networkidle2'

await page.goBack();
await page.goForward();
await page.reload();

// Wait for navigation after click
await Promise.all([
  page.waitForNavigation({ waitUntil: 'networkidle0' }),
  page.click('a.link'),
]);
```

## Waiting

```javascript
await page.waitForSelector('.el', { visible: true, timeout: 30000 });
await page.waitForFunction(() => document.querySelectorAll('.item').length > 0);
await page.waitForNetworkIdle({ idleTime: 500 });
await page.waitForResponse(url => url.includes('/api/'));
```

## Evaluate JavaScript

```javascript
// Return values (serialized)
const title = await page.evaluate(() => document.title);
const sum = await page.evaluate((a, b) => a + b, 1, 2);

// Query helpers
const text = await page.$eval('.el', el => el.textContent);
const texts = await page.$$eval('p', els => els.map(e => e.textContent));

// Expose Node function to page
await page.exposeFunction('md5', text => crypto.createHash('md5').update(text).digest('hex'));
```

## Network Interception

```javascript
await page.setRequestInterception(true);
page.on('request', req => {
  if (req.resourceType() === 'image') req.abort();
  else req.continue();
});

// Custom response
page.on('request', req => {
  if (req.url().includes('/api/data'))
    req.respond({ status: 200, contentType: 'application/json', body: '{"mock":true}' });
  else req.continue();
});
```

## Emulation

```javascript
import { KnownDevices } from 'puppeteer';
await page.emulate(KnownDevices['iPhone 15 Pro']);

await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
await page.setUserAgent('custom-agent');
await page.emulateMediaType('print');
await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }]);
await page.emulateCPUThrottling(4);
await page.emulateNetworkConditions({ download: 1.5*1024*1024/8, upload: 750*1024/8, latency: 40 });
```

## Cookies & Auth

```javascript
await browser.setCookie({ name: 'session', value: 'abc', domain: 'example.com' });
const cookies = await browser.cookies();
await browser.deleteCookie({ name: 'session', domain: 'example.com' });

await page.authenticate({ username: 'user', password: 'pass' });  // HTTP auth
await page.setExtraHTTPHeaders({ 'Authorization': 'Bearer TOKEN' });
```

## Lighthouse Integration

```javascript
import lighthouse from 'lighthouse';
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

// Authenticate first
await page.goto('https://example.com/login');
await page.locator('#email').fill('user@example.com');
await page.locator('#password').fill('password');
await page.locator('button[type=submit]').click();
await page.waitForNavigation();

// Pass page to Lighthouse
const result = await lighthouse('https://example.com/dashboard', undefined, undefined, page);
console.log('Performance:', result.lhr.categories.performance.score * 100);
await browser.close();
```

## Docker / CI

```javascript
const browser = await puppeteer.launch({
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});
```

## Full Reference

See [docs/puppeteer-api.md](docs/puppeteer-api.md) for complete API, all options, frames, file uploads, and troubleshooting.
