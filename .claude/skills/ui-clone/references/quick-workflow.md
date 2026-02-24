# Quick Workflow — Homepage Only

Streamlined single-page extraction for the `quick` command. Produces the same output format as the full pipeline but skips additional pages and deep component detection.

## What's Different from Full Clone

| Aspect | Full Clone | Quick |
|--------|-----------|-------|
| Pages visited | Homepage + 3 auto-detected | Homepage only |
| Component detection | Deep (cards, forms, inputs) | Basic (header, hero, footer) |
| Screenshots | Full page + all element types | Full page + header, hero, footer |
| Processing time | ~60-90s | ~20-30s |
| Output quality | Comprehensive | Good enough for most uses |

## Steps

### 1. Parse URL, Create Dirs

Same as full pipeline. Derive slug, create:
- `.claude/skills/ui-styles/<slug>/references/`
- `.claude/skills/ui-styles/<slug>/examples/`
- `$CLAUDE_PROJECT_DIR/ui-clones/<slug>/`

### 2. Launch Puppeteer + Navigate

```javascript
const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
```

### 3. Dismiss Cookie Banners

Same cookie dismissal logic as full pipeline.

### 4. Run All Extraction Scripts

Run the full set of extraction functions from `page-evaluate.md` — same as full clone but only on homepage:

```javascript
const data = await page.evaluate(async () => {
  return {
    colors: await extractColors(),
    typography: await extractTypography(),
    spacing: await extractSpacing(),
    layout: await extractLayout(),
    components: await detectComponents(),
    animations: await extractAnimations(),
    icons: await detectIcons(),
    meta: { title: document.title, url: window.location.href },
  };
});
```

### 5. Capture Screenshots (Limited Set)

Only four screenshots:

```javascript
// Full page
await page.screenshot({ path: `${examplesDir}/full-page.png`, fullPage: true });

// Header
const header = await page.$('header') || await page.$('nav') || await page.$('[role="banner"]');
if (header) await header.screenshot({ path: `${examplesDir}/header.png` });

// Hero
const heroSelectors = ['[class*="hero"]', '[id*="hero"]', 'main > section:first-child'];
for (const sel of heroSelectors) {
  const el = await page.$(sel);
  if (el) {
    const box = await el.boundingBox();
    if (box && box.height > 200) {
      await el.screenshot({ path: `${examplesDir}/hero.png` });
      break;
    }
  }
}

// Footer
const footer = await page.$('footer') || await page.$('[role="contentinfo"]');
if (footer) await footer.screenshot({ path: `${examplesDir}/footer.png` });
```

### 6. Post-Process + Write Output

Same post-processing as full pipeline:
- Group colors into palette via HSL analysis
- Map sizes to token scale
- Write all 6 output files using templates from `output-templates.md`
- Write `clone-report.json`
- Update ui-styles table

### 7. Close Browser

```javascript
await browser.close();
```

## When to Use Quick vs Full

- **Quick**: Rapid prototyping, exploring a site's style, first pass before deciding
- **Full Clone**: Production style preset, when you need complete component coverage, multi-page consistency
