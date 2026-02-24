# Extraction Workflow — Full Pipeline

Complete step-by-step for the `clone` command. Uses Puppeteer to visit a website, extract its visual design system, capture screenshots, and produce a ui-styles preset.

## Step 1: Parse URL and Create Directories

```javascript
// Derive slug
const url = new URL(inputUrl);
const slug = url.hostname.replace(/^www\./, '').replace(/\./g, '-');

// Create output directories
const stylesDir = `.claude/skills/ui-styles/${slug}`;
const refsDir = `${stylesDir}/references`;
const examplesDir = `${stylesDir}/examples`;  // screenshots live with the preset
const cloneDir = `${process.env.CLAUDE_PROJECT_DIR}/ui-clones/${slug}`;
```

Create all directories with `mkdir -p`.

## Step 2: Launch Puppeteer

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setViewport({
  width: 1440,
  height: 900,
  deviceScaleFactor: 2,
});
```

## Step 3: Navigate to Homepage

```javascript
await page.goto(url.href, {
  waitUntil: 'networkidle2',
  timeout: 30000,
});
```

On timeout, retry with `waitUntil: 'domcontentloaded'`.

## Step 4: Dismiss Cookie Banners

Try selectors in order, click first match with a short timeout:

```javascript
const cookieSelectors = [
  '[class*="cookie"] button[class*="accept"]',
  '[id*="cookie"] button[class*="accept"]',
  'button[id*="accept-cookies"]',
  '[class*="consent"] button:first-of-type',
  '[class*="banner"] button[class*="close"]',
  'button[class*="agree"]',
  '[class*="cookie"] button:not([class*="reject"])',
];

for (const sel of cookieSelectors) {
  try {
    const btn = await page.$(sel);
    if (btn) {
      await btn.click();
      await page.waitForTimeout(500);
      break;
    }
  } catch (e) { /* ignore */ }
}
```

## Step 5: Run Extraction Scripts

Run all extraction functions from `page-evaluate.md` in a single `page.evaluate()` call:

```javascript
const data = await page.evaluate(async () => {
  // All extraction functions defined here...
  return {
    colors: await extractColors(),
    typography: await extractTypography(),
    spacing: await extractSpacing(),
    layout: await extractLayout(),
    components: await detectComponents(),
    animations: await extractAnimations(),
    icons: await detectIcons(),
    meta: {
      title: document.title,
      description: document.querySelector('meta[name="description"]')?.content || '',
      url: window.location.href,
    },
  };
});
```

## Step 6: Capture Screenshots

### Full Page

```javascript
await page.screenshot({
  path: `${examplesDir}/full-page.png`,
  fullPage: true,
});
```

### Element Screenshots

For each component, find the element and use `element.screenshot()`:

```javascript
async function captureElement(page, selectors, filename, examplesDir) {
  for (const sel of selectors) {
    try {
      const el = await page.$(sel);
      if (el) {
        const box = await el.boundingBox();
        if (box && box.height > 10) {
          await el.screenshot({ path: `${examplesDir}/${filename}` });
          return true;
        }
      }
    } catch (e) { /* skip */ }
  }
  return false;
}

// Header
await captureElement(page, ['header', 'nav', '[role="banner"]'], 'header.png', examplesDir);

// Hero
await captureElement(page, [
  '[class*="hero"]', '[id*="hero"]',
  'main > section:first-child', 'main > div:first-child',
], 'hero.png', examplesDir);

// Footer
await captureElement(page, ['footer', '[role="contentinfo"]'], 'footer.png', examplesDir);

// Cards (if detected)
if (data.components.cards.length > 0) {
  const cardSel = data.components.cards[0].selector;
  await captureElement(page, [cardSel], 'cards.png', examplesDir);
}

// Buttons — screenshot first unique button
if (data.components.buttons.length > 0) {
  const btnClass = data.components.buttons[0].class;
  if (btnClass) {
    await captureElement(page, [`.${btnClass.split(' ')[0]}`], 'buttons.png', examplesDir);
  }
}
```

## Step 7: Additional Pages (clone only)

### Auto-detect key pages

```javascript
const navLinks = await page.$$eval('header a, nav a', links =>
  links.map(a => ({ href: a.href, text: a.textContent?.trim() }))
    .filter(l => l.href && !l.href.includes('#') && l.text)
    .slice(0, 10)
);

// Filter to same-origin, unique paths
const baseUrl = new URL(url.href);
const additionalPages = navLinks
  .filter(l => {
    try { return new URL(l.href).origin === baseUrl.origin; } catch { return false; }
  })
  .map(l => new URL(l.href).pathname)
  .filter((p, i, arr) => p !== '/' && arr.indexOf(p) === i)
  .slice(0, 3);
```

### Or use `--pages` argument

If the user provided `--pages="/about,/pricing"`, parse and use those instead.

### Visit each page

```javascript
for (const path of additionalPages) {
  const pageUrl = new URL(path, baseUrl.origin).href;
  await page.goto(pageUrl, { waitUntil: 'networkidle2', timeout: 20000 });

  // Run extraction again
  const pageData = await page.evaluate(/* same extraction function */);

  // Merge new tokens into main data
  mergeExtractionData(data, pageData);

  // Screenshot
  const pageName = path.replace(/\//g, '-').replace(/^-/, '') || 'page';
  await page.screenshot({
    path: `${examplesDir}/${pageName}.png`,
    fullPage: true,
  });
}
```

### Merge strategy

```javascript
function mergeExtractionData(main, pageData) {
  // Colors: add new colors not already seen
  for (const bg of pageData.colors.backgrounds) {
    const existing = main.colors.backgrounds.find(b => b.color === bg.color);
    if (existing) existing.count += bg.count;
    else main.colors.backgrounds.push(bg);
  }
  // Same for textColors, borderColors, fontSizes, etc.
  // Merge cssVariables (pageData takes precedence for same keys)
  Object.assign(main.colors.cssVariables, pageData.colors.cssVariables);
  // Merge components: keep richer version
  if (!main.components.footer && pageData.components.footer) {
    main.components.footer = pageData.components.footer;
  }
}
```

## Step 8: Color Grouping (HSL Analysis)

Group extracted colors into semantic roles:

```javascript
function groupColors(rawColors) {
  // Parse all colors to HSL
  const parsed = rawColors.map(c => ({ ...c, hsl: parseToHSL(c.color) })).filter(c => c.hsl);

  // Group by role:
  // - Primary: most-used non-neutral background color with saturation > 10%
  // - Accent: high-saturation color used on interactive elements
  // - Neutral: low saturation (< 10%), grouped by lightness
  // - Semantic: reds (error), greens (success), yellows (warning)

  const neutrals = parsed.filter(c => c.hsl.s < 10);
  const chromatic = parsed.filter(c => c.hsl.s >= 10);

  // Sort chromatic by usage count
  chromatic.sort((a, b) => b.count - a.count);

  return {
    primary: chromatic[0] || null,
    accent: chromatic[1] || chromatic[0] || null,
    neutrals: neutrals.sort((a, b) => a.hsl.l - b.hsl.l),
    semantic: {
      success: chromatic.find(c => c.hsl.h >= 90 && c.hsl.h <= 150),
      error: chromatic.find(c => c.hsl.h >= 340 || c.hsl.h <= 20),
      warning: chromatic.find(c => c.hsl.h >= 30 && c.hsl.h <= 60),
    },
    all: chromatic,
  };
}
```

## Step 9: Token Mapping

Map raw sizes to a token scale:

```javascript
function mapToScale(sizes, scaleTokens) {
  // scaleTokens = ['--text-xs', '--text-sm', '--text-base', ...]
  // sizes = sorted array of { value: '16px', count: 42 }

  // Sort by parsed px value
  const sorted = sizes
    .map(s => ({ ...s, px: parseFloat(s.value) }))
    .filter(s => !isNaN(s.px))
    .sort((a, b) => a.px - b.px);

  // Map to scale: smallest -> first token, largest -> last token
  // Use frequency-weighted assignment for middle values
  const mapped = {};
  const step = sorted.length / scaleTokens.length;
  scaleTokens.forEach((token, i) => {
    const idx = Math.min(Math.round(i * step), sorted.length - 1);
    if (sorted[idx]) mapped[token] = sorted[idx].value;
  });

  return mapped;
}
```

## Step 10: Write Output Files

Use the templates from `output-templates.md` to generate each file:

1. **STYLE.md** — Fill in vibe description, palette preview table, font info, key patterns
2. **references/colors.md** — CSS `:root {}` with mapped color tokens + usage table
3. **references/typography.md** — Font stack, scale, weights, heading styles
4. **references/spacing.md** — Scale, radii, layout, breakpoints, component spacing
5. **references/components.md** — CSS for each detected component (buttons, cards, header, sections, footer)
6. **references/animations.md** — Timing tokens, keyframes, hover states, reduced motion
7. **examples/*.png** — Screenshots are already saved to `examplesDir` (inside the style preset)
8. **clone-report.json** — Full raw extraction data (saved to `$CLAUDE_PROJECT_DIR/ui-clones/<slug>/`)

## Step 11: Update ui-styles Table

Read `.claude/skills/ui-styles/SKILL.md` and add a new row to the Available Styles table:

```markdown
| `<slug>` | <theme> | <vibe description> | <primary font> |
```

## Step 12: Close Browser

```javascript
await browser.close();
```

## Error Recovery

- **Puppeteer launch fails**: Check installation, suggest `npm i puppeteer`
- **Navigation timeout**: Retry with `domcontentloaded`, then try without images
- **Empty extraction**: Fall back to parsing external CSS files via fetch
- **Element screenshot fails**: Skip that screenshot, note in report
- **Cross-origin stylesheets**: Note in report, rely on computed styles instead

Always produce output with whatever data was collected. Partial output is better than none.
