# SEO Module

Self-validating SEO implementation for Claude Code.

## Quick Start

```bash
# 1. Install dependencies
cd .claude/setup && make

# 2. Build and start your dev server
npm run build && npm run dev

# 3. Run full SEO implementation
/seo all astro
```

## Dependencies

Installed via `make deps` or `make deps-wsl`:

| Package | Purpose |
|---------|---------|
| uv | Python package runner |
| playwright | Browser automation |
| lighthouse | SEO/performance audits |
| terser | JS minifier (Vite builds) |
| imagemagick | Image processing (WSL) |

## Commands

### Full Implementation

```bash
# Implement everything (meta + schema + ai + perf) then validate
/seo all astro
/seo all nextjs
/seo all vite
```

### Audit First (Read-Only)

```bash
# See what's missing before making changes
@seo-auditor Audit this project for SEO issues
```

### Research Best Practices

```bash
# Get latest SEO recommendations via web search
@seo-research What are the latest SEO best practices for Astro in 2026?
@seo-research Are there any new AI crawlers I should add to robots.txt?
@seo-research What Core Web Vitals thresholds changed in 2026?
```

### Individual Skills

```bash
# Meta tags (title, description, Open Graph, Twitter Cards)
/seo meta astro
/seo meta nextjs src/app/layout.tsx

# JSON-LD structured data
/seo schema Organization
/seo schema Article src/layouts/BlogPost.astro
/seo schema LocalBusiness

# AI SEO (llms.txt, robots.txt for AI crawlers)
/seo ai llms-txt
/seo ai robots

# Performance (images, fonts, Core Web Vitals)
/seo perf all
/seo perf images
/seo perf fonts

# Sitemap
/seo sitemap astro https://mysite.com
/seo sitemap nextjs

# Assets (favicons, OG images, manifests)
/seo assets
/seo assets public/logo.svg #3B82F6

# Lighthouse validation
/seo validate http://localhost:4321
/seo validate http://localhost:3000 95
```

## Example Workflow

### New Astro Project

```bash
# Start dev server in terminal
npm run dev

# In Claude Code:
/seo all astro

# Claude will:
# 1. Add meta tags to src/layouts/Layout.astro
# 2. Add Organization JSON-LD schema
# 3. Create public/llms.txt
# 4. Configure public/robots.txt for AI crawlers
# 5. Optimize images with width/height/lazy
# 6. Generate/configure sitemap.xml
# 7. Generate all favicons, OG images, manifests
# 8. Run Lighthouse to verify 100 scores
```

### Existing Next.js App

```bash
# Audit first to see current state
@seo-auditor Check SEO status

# Fix specific issues
/seo meta nextjs
/seo schema Organization

# Validate
/seo validate http://localhost:3000
```

### Fix Specific Issues

```bash
# Only missing meta tags
/seo meta

# Only JSON-LD
/seo schema Product

# Only performance
/seo perf images
```

## Supported Frameworks

| Framework | Layout File |
|-----------|-------------|
| Astro | `src/layouts/Layout.astro` |
| Next.js | `src/app/layout.tsx` |
| Vite + React | `index.html` or `src/App.tsx` |
| TanStack Start | `src/routes/__root.tsx` |

## Validation

Each skill auto-validates via PostToolUse hooks. Errors include:

```
✗ META VALIDATION FAILED
File: src/layouts/Layout.astro
Errors: 2

1. [META004] Missing meta description
   Fix: Add <meta name="description" content="...">

2. [META011] Missing og:image
   Fix: Add <meta property="og:image" content="https://...">
```

## Error Codes

| Prefix | Category |
|--------|----------|
| META0xx | Meta tags |
| SCHEMA0xx | JSON-LD |
| AI0xx | AI SEO |
| PERF0xx | Performance |
| SITEMAP0xx | Sitemap |
| ASSET0xx | Image assets |
| LH_xxx | Lighthouse |

## Troubleshooting

### WSL Lighthouse Issues

Headless Chrome can fail in WSL. Use chromium-browser with sandbox disabled:

```bash
# Install chromium
sudo apt install chromium-browser

# Set Chrome path
export CHROME_PATH=$(which chromium-browser)

# Run Lighthouse with WSL flags
lighthouse http://localhost:3000 --chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"
```

Add to `.bashrc` for persistence:
```bash
echo 'export CHROME_PATH=$(which chromium-browser)' >> ~/.bashrc
```

### Alternative: Chrome DevTools

For WSL, Chrome DevTools method is most reliable:

1. Open Chrome on Windows
2. Go to `chrome://inspect`
3. Click "Configure" and add `localhost:9222`
4. Run your dev server
5. Use Chrome DevTools Lighthouse tab directly

### Playwright Issues

```bash
# Reinstall browsers
playwright install --force chromium

# Check installation
playwright --version
```

### Hooks Not Running

1. Verify uv installed: `uv --version`
2. Check Claude Code version: `claude --version` (need 2.1.0+)
3. Verify hook paths match actual file locations

## CLI Scripts

Run these directly for automation or debugging:

### Lighthouse Audit

**IMPORTANT**: Lighthouse must run against localhost, not remote URLs.

```bash
# Start your dev server first!
npm run dev

# Run audit against local dev server
uv run .claude/hooks/seo/lib/lighthouse.py --url http://localhost:3000

# With target score
uv run .claude/hooks/seo/lib/lighthouse.py --url http://localhost:3000 --target 90

# JSON output for CI/CD
uv run .claude/hooks/seo/lib/lighthouse.py --url http://localhost:3000 --json

# Don't save report (temp only)
uv run .claude/hooks/seo/lib/lighthouse.py --url http://localhost:3000 --no-save

# Common ports:
# - http://localhost:3000  (Next.js, Create React App)
# - http://localhost:4321  (Astro)
# - http://localhost:5173  (Vite)
```

**Reports**: Saved to `reports/seo/lighthouse-{timestamp}.json`

**Cleanup**: Automatically removes lighthouse temp directories:
- Windows: `AppData\Local\lighthouse.*`
- Linux/WSL: `/tmp/lighthouse.*`

### Asset Generation

**IMPORTANT**: Assets must be in `public/` root, not subdirectories.

```bash
# Auto-detect logo, generate all assets to public/ root
uv run .claude/hooks/seo/lib/generate_assets.py --output public

# Specify logo, color, site name
uv run .claude/hooks/seo/lib/generate_assets.py \
  --logo public/logo.svg \
  --color "#3B82F6" \
  --name "My Site" \
  --output public

# JSON output
uv run .claude/hooks/seo/lib/generate_assets.py --output public --json
```

Files are created at:
```
public/favicon.ico          → /favicon.ico
public/apple-touch-icon.png → /apple-touch-icon.png
public/og-image.png         → /og-image.png
```

NOT in subdirectories like `public/images/logo/` - browsers won't find them there!

### Generated Assets

The asset generator creates:
- Favicons: 16x16, 32x32, 96x96, .ico
- Apple: 180x180, 152x152, 120x120
- Android: 192x192, 512x512, maskable
- MS Tiles: 70x70, 150x150, 310x310, 310x150
- OG/Twitter: 1200x630, 1200x600
- Config: site.webmanifest, browserconfig.xml
