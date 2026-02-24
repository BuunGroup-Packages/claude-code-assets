# Puppeteer API Reference

> Sources: [pptr.dev](https://pptr.dev/) | [GitHub](https://github.com/puppeteer/puppeteer) | [API docs](https://pptr.dev/api) | [Guides](https://pptr.dev/guides/getting-started) | [Configuration](https://pptr.dev/guides/configuration)

## Install

```bash
npm install puppeteer          # downloads Chrome
npm install puppeteer-core     # library only, no browser
```

## Launch Options

> [LaunchOptions API](https://pptr.dev/api/puppeteer.launchoptions)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `headless` | `boolean \| 'shell'` | `true` | `true` = new headless, `'shell'` = faster/fewer features, `false` = headed |
| `channel` | `string` | -- | Use installed Chrome: `'chrome'`, `'chrome-beta'`, etc. |
| `executablePath` | `string` | -- | Custom browser binary |
| `args` | `string[]` | -- | Extra Chrome CLI flags |
| `userDataDir` | `string` | -- | Persist cookies/storage across sessions |
| `devtools` | `boolean` | `false` | Auto-open DevTools (forces headed) |
| `timeout` | `number` | `30000` | Startup timeout ms (0 = none) |
| `dumpio` | `boolean` | `false` | Pipe browser stdout/stderr |
| `pipe` | `boolean` | `false` | Connect via pipe (not WebSocket) |
| `ignoreDefaultArgs` | `boolean \| string[]` | -- | Skip specific default args |
| `enableExtensions` | `boolean \| string[]` | -- | Load extensions |
| `env` | `Record<string, string>` | `process.env` | Browser env vars |
| `signal` | `AbortSignal` | -- | Close on abort |

## Connect to Existing Browser

> [ConnectOptions API](https://pptr.dev/api/puppeteer.connectoptions)

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://127.0.0.1:9222/...',
  // or: browserURL: 'http://127.0.0.1:9222',
  defaultViewport: { width: 1280, height: 720 },
  acceptInsecureCerts: false,
  slowMo: 0,
  protocolTimeout: 180000,
});
```

## Navigation

> [page.goto](https://pptr.dev/api/puppeteer.page.goto)

```javascript
const response = await page.goto(url, options);
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `waitUntil` | `string \| string[]` | `'load'` | `'load'`, `'domcontentloaded'`, `'networkidle0'`, `'networkidle2'` |
| `timeout` | `number` | `30000` | Navigation timeout (0 = none) |
| `referer` | `string` | -- | Referer header |
| `signal` | `AbortSignal` | -- | Cancel navigation |

```javascript
await page.goBack(options);
await page.goForward(options);
await page.reload(options);

// Click + wait for navigation
await Promise.all([
  page.waitForNavigation({ waitUntil: 'networkidle0' }),
  page.click('a'),
]);
```

## Selectors

> [Selectors guide](https://pptr.dev/guides/page-interactions#selectors)

| Type | Syntax | Description |
|------|--------|-------------|
| CSS | `'div.class'` | Standard CSS selector |
| Text | `'::-p-text(Click me)'` | Minimal element containing text |
| ARIA | `'::-p-aria(Submit)'` | By accessible name/role |
| XPath | `'::-p-xpath(//h2)'` | XPath expression |
| Shadow deep | `'host >>> .child'` | Descendant through shadow roots |
| Shadow child | `'host >>>> .child'` | Immediate shadow root only |
| Pierce | `'pierce/div'` | Legacy shadow DOM syntax |

Escape special chars in text: `'::-p-text(Price \\(USD\\))'`

## Locators (Recommended)

> [Locators guide](https://pptr.dev/guides/page-interactions#locators)

Auto-waits for: in viewport, visible, enabled, stable bounding box.

```javascript
await page.locator('button').click();
await page.locator('input').fill('value');
await page.locator('div').hover();
await page.locator('div').scroll({ scrollTop: 100 });
await page.locator('.el').wait();                          // wait for visible

// Filter
await page.locator('button').filter(b => b.textContent === 'OK').click();

// Map + wait
const text = await page.locator('h1').map(el => el.textContent).wait();

// Disable preconditions
await page.locator('button')
  .setEnsureElementIsInTheViewport(false)
  .setVisibility(null)
  .setTimeout(5000)
  .click();
```

## Waiting

> [waitForSelector](https://pptr.dev/api/puppeteer.page.waitforselector) | [waitForFunction](https://pptr.dev/api/puppeteer.page.waitforfunction)

```javascript
const el = await page.waitForSelector('.el', { visible: true, timeout: 30000 });
await page.waitForFunction(() => document.querySelectorAll('.item').length > 0, { polling: 'raf' });
await page.waitForNetworkIdle({ idleTime: 500, concurrency: 0 });
await page.waitForRequest(url => url.includes('/api/'));
await page.waitForResponse('https://example.com/api/data');
await page.waitForFrame(f => f.url().includes('iframe'));
```

`polling`: `'raf'` (requestAnimationFrame), `'mutation'` (DOM changes), or `number` (ms interval).

## Evaluate JavaScript

> [Evaluate guide](https://pptr.dev/guides/evaluate-javascript)

```javascript
const result = await page.evaluate(() => document.title);
const sum = await page.evaluate((a, b) => a + b, 1, 2);

// Query helpers
const text = await page.$eval('.el', el => el.textContent);
const texts = await page.$$eval('p', els => els.map(e => e.textContent));

// Return handle (not serialized)
const handle = await page.evaluateHandle(() => document.body);

// Expose Node function to browser
await page.exposeFunction('hash', text => crypto.createHash('md5').update(text).digest('hex'));

// Run before every navigation
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
});

// Inject script/style
await page.addScriptTag({ url: 'https://cdn.example.com/lib.js' });
await page.addStyleTag({ content: 'body { background: red; }' });
```

## Screenshots

> [Screenshots guide](https://pptr.dev/guides/screenshots-and-pdfs)

```javascript
await page.screenshot({ path: 'shot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
await page.screenshot({ path: 'region.png', clip: { x: 0, y: 0, width: 800, height: 600 } });
const base64 = await page.screenshot({ encoding: 'base64' });
const buffer = await page.screenshot();  // Uint8Array

// Element screenshot
const el = await page.$('.element');
await el.screenshot({ path: 'element.png' });
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `path` | `string` | -- | File path (type inferred from extension) |
| `type` | `'png' \| 'jpeg' \| 'webp'` | `'png'` | Image format |
| `quality` | `number` | -- | 0-100, jpeg/webp only |
| `fullPage` | `boolean` | `false` | Full scrollable page |
| `clip` | `{x, y, width, height}` | -- | Region to capture |
| `omitBackground` | `boolean` | `false` | Transparent background |
| `encoding` | `'base64' \| 'binary'` | `'binary'` | Return format |
| `optimizeForSpeed` | `boolean` | `false` | Faster capture |

## PDF Generation

> [page.pdf](https://pptr.dev/api/puppeteer.page.pdf)

Headless Chrome only. Waits for fonts by default.

```javascript
await page.pdf({ path: 'page.pdf', format: 'A4', printBackground: true });
await page.emulateMediaType('screen');  // use screen CSS for PDF
await page.pdf({ path: 'screen.pdf' });
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `path` | `string` | -- | File path |
| `format` | `PaperFormat` | `'letter'` | `'letter'`, `'legal'`, `'a0'`-`'a6'`, `'tabloid'`, `'ledger'` |
| `landscape` | `boolean` | `false` | Landscape orientation |
| `printBackground` | `boolean` | `false` | Include background graphics |
| `scale` | `number` | `1` | 0.1-2.0 |
| `margin` | `{top,right,bottom,left}` | -- | CSS units |
| `pageRanges` | `string` | `''` (all) | e.g. `'1-5, 8'` |
| `displayHeaderFooter` | `boolean` | `false` | Show header/footer |
| `headerTemplate` | `string` | -- | HTML with `.date`, `.title`, `.url`, `.pageNumber`, `.totalPages` |
| `preferCSSPageSize` | `boolean` | `false` | Use CSS `@page` size |

## Network Interception

> [Network guide](https://pptr.dev/guides/network-logging)

```javascript
// Logging
page.on('request', req => console.log(req.method(), req.url()));
page.on('response', res => console.log(res.status(), res.url()));

// Interception
await page.setRequestInterception(true);
page.on('request', req => {
  if (req.isInterceptResolutionHandled()) return;
  if (req.resourceType() === 'image') req.abort();
  else req.continue();
});

// Modify request
page.on('request', req => {
  req.continue({ headers: { ...req.headers(), 'X-Custom': 'value' } });
});

// Mock response
page.on('request', req => {
  if (req.url().includes('/api/'))
    req.respond({ status: 200, contentType: 'application/json', body: '{}' });
  else req.continue();
});
```

HTTPRequest methods: `url()`, `method()`, `headers()`, `resourceType()`, `isNavigationRequest()`, `redirectChain()`, `abort()`, `continue()`, `respond()`

HTTPResponse methods: `url()`, `status()`, `headers()`, `ok()`, `text()`, `json()`, `buffer()`, `timing()`, `fromCache()`, `remoteAddress()`

## Emulation

> [KnownDevices](https://pptr.dev/api/puppeteer.knowndevices)

```javascript
import { KnownDevices } from 'puppeteer';
await page.emulate(KnownDevices['iPhone 15 Pro']);  // call BEFORE goto

await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2, isMobile: false });
await page.setUserAgent('custom-agent');
await page.emulateMediaType('screen');    // or 'print', null
await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }]);
await page.emulateTimezone('America/New_York');
await page.emulateCPUThrottling(4);
await page.emulateNetworkConditions({ download: 1.5*1024*1024/8, upload: 750*1024/8, latency: 40 });
await page.emulateVisionDeficiency('deuteranopia');
await page.setGeolocation({ latitude: 51.5, longitude: -0.1 });
```

Devices: iPhone 4–15 Pro Max, iPad, iPad Pro, Galaxy S5/S8/S9+, Pixel 2–5, Nexus, Kindle (+ landscape variants).

## Cookies & Auth

```javascript
// Cookies (use browser/context, not page — page methods are deprecated)
await browser.setCookie({ name: 'session', value: 'abc', domain: 'example.com', httpOnly: true });
const cookies = await browser.cookies();
await browser.deleteCookie({ name: 'session', domain: 'example.com' });

// HTTP basic auth
await page.authenticate({ username: 'user', password: 'pass' });

// Custom headers (sent with every request)
await page.setExtraHTTPHeaders({ 'Authorization': 'Bearer TOKEN' });
```

## Frames & iframes

```javascript
const frames = page.frames();
const frame = await page.waitForFrame(f => f.url().includes('iframe'));
const handle = await page.$('iframe');
const frame2 = await handle.contentFrame();

// Frames have same API as Page: goto, $, $$, evaluate, locator, click, type, etc.
await frame.locator('button').click();
```

## File Uploads

```javascript
const input = await page.$('input[type=file]');
await input.uploadFile('/path/to/file.pdf');

// FileChooser pattern
const [chooser] = await Promise.all([
  page.waitForFileChooser(),
  page.click('#upload-btn'),
]);
await chooser.accept(['/tmp/file.pdf']);
```

## Page Content & Misc

```javascript
const html = await page.content();
await page.setContent('<h1>Hello</h1>');
const url = page.url();
const title = await page.title();
await page.setCacheEnabled(false);
await page.setBypassCSP(true);
await page.setJavaScriptEnabled(false);
await page.setOfflineMode(true);
page.setDefaultTimeout(60000);
page.setDefaultNavigationTimeout(60000);
const metrics = await page.metrics();
```

## Browser Contexts (Incognito)

```javascript
const context = await browser.createBrowserContext();
const page = await context.newPage();
// Isolated cookies, storage, cache
await context.close();
```

## Docker / CI

```javascript
const browser = await puppeteer.launch({
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});
```

```bash
docker run -i --init --cap-add=SYS_ADMIN --rm ghcr.io/puppeteer/puppeteer:latest node -e "$(cat script.js)"
```

## Configuration Files

Searched in order: `.puppeteerrc.cjs`, `.puppeteerrc.js`, `.puppeteerrc` (YAML/JSON), `puppeteer.config.js`

```javascript
// .puppeteerrc.cjs
module.exports = {
  cacheDirectory: './node_modules/.puppeteer_cache',
  defaultBrowser: 'chrome',
};
```

Env vars: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `PUPPETEER_CACHE_DIR`

After config changes: `npx puppeteer browsers install`

## Lighthouse Integration

```javascript
import lighthouse from 'lighthouse';
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

// Login first
await page.goto('https://example.com/login');
await page.locator('#email').fill('user@test.com');
await page.locator('#password').fill('pass');
await page.locator('button[type=submit]').click();
await page.waitForNavigation();

// Pass page as 4th arg
const result = await lighthouse('https://example.com/dashboard', undefined, undefined, page);
console.log('Score:', result.lhr.categories.performance.score * 100);
await browser.close();
```

## References

| Topic | URL |
|-------|-----|
| Main docs | https://pptr.dev/ |
| GitHub | https://github.com/puppeteer/puppeteer |
| API reference | https://pptr.dev/api |
| npm | https://www.npmjs.com/package/puppeteer |
| Getting started | https://pptr.dev/guides/getting-started |
| Configuration | https://pptr.dev/guides/configuration |
| Page interactions | https://pptr.dev/guides/page-interactions |
| Evaluate JS | https://pptr.dev/guides/evaluate-javascript |
| Screenshots & PDFs | https://pptr.dev/guides/screenshots-and-pdfs |
| Network logging | https://pptr.dev/guides/network-logging |
| Docker guide | https://pptr.dev/guides/docker |
| Troubleshooting | https://pptr.dev/troubleshooting |
| KnownDevices list | https://pptr.dev/api/puppeteer.knowndevices |
| chrome-launcher | https://github.com/GoogleChrome/chrome-launcher |
| Lighthouse integration | https://github.com/GoogleChrome/lighthouse/blob/main/docs/puppeteer.md |
