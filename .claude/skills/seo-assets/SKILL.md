---
name: seo-assets
description: |
  Generate all SEO image assets: favicons, OG images, Apple touch icons,
  MS tiles, and manifest files. Scans for logo and generates all sizes.
argument-hint: "[logo_path] [brand_color]"
allowed-tools: Bash, Read, Write, Glob, Grep
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/seo/post_assets_validate.py"
---

# SEO Assets Generator

## Purpose

Generate all required image assets for complete SEO/PWA compliance.
Scans codebase for logo, generates all sizes, creates manifest files.

## Arguments

| Position | Name | Values | Default |
|----------|------|--------|---------|
| $1 | logo_path | Path to source logo | Auto-detect in public/ |
| $2 | brand_color | Hex color for theme | #000000 |

## Usage

```bash
/seo-assets
/seo-assets public/logo.svg #3B82F6
/seo-assets src/assets/brand.png
```

## Quick Generate (Script)

Run the generator script directly:

```bash
# Auto-detect logo, generate all assets
uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/generate_assets.py

# Specify logo and color
uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/generate_assets.py \
  --logo public/logo.svg \
  --color "#3B82F6" \
  --name "My Site"

# Output JSON for automation
uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/lib/generate_assets.py --json
```

## Generated Assets

### Favicons (public/)

| File | Size | Purpose |
|------|------|---------|
| favicon.ico | 16x16, 32x32, 48x48 | Browser tab (legacy) |
| favicon.svg | vector | Modern browsers |
| favicon-16x16.png | 16x16 | Small favicon |
| favicon-32x32.png | 32x32 | Standard favicon |
| favicon-96x96.png | 96x96 | Large favicon |

### Apple Touch Icons (public/)

| File | Size | Purpose |
|------|------|---------|
| apple-touch-icon.png | 180x180 | iOS home screen |
| apple-touch-icon-152x152.png | 152x152 | iPad |
| apple-touch-icon-120x120.png | 120x120 | iPhone |

### Android/PWA (public/)

| File | Size | Purpose |
|------|------|---------|
| android-chrome-192x192.png | 192x192 | Android home screen |
| android-chrome-512x512.png | 512x512 | Android splash |
| maskable-icon-512x512.png | 512x512 | Maskable icon |

### MS Tiles (public/)

| File | Size | Purpose |
|------|------|---------|
| mstile-70x70.png | 70x70 | Small tile |
| mstile-150x150.png | 150x150 | Medium tile |
| mstile-310x310.png | 310x310 | Large tile |
| mstile-310x150.png | 310x150 | Wide tile |

### Open Graph (public/)

| File | Size | Purpose |
|------|------|---------|
| og-image.png | 1200x630 | Social sharing |
| twitter-image.png | 1200x600 | Twitter cards |

### Config Files (public/)

| File | Purpose |
|------|---------|
| site.webmanifest | PWA manifest |
| browserconfig.xml | MS tile config |

## Workflow

1. **Detect Logo**
   ```bash
   # Search order:
   public/logo.svg
   public/logo.png
   src/assets/logo.*
   public/brand.*
   public/icon.*
   ```

2. **Generate Assets**
   ```bash
   # Using ImageMagick or Sharp
   # SVG source preferred for quality
   convert logo.svg -resize 32x32 favicon-32x32.png
   convert logo.svg -resize 180x180 apple-touch-icon.png
   convert logo.svg -resize 1200x630 -background white -gravity center -extent 1200x630 og-image.png
   ```

3. **Create Manifest**
   ```json
   {
     "name": "Site Name",
     "short_name": "Site",
     "description": "Brief description of your site or app",
     "start_url": "/",
     "scope": "/",
     "display": "standalone",
     "orientation": "portrait-primary",
     "lang": "en",
     "theme_color": "#3B82F6",
     "background_color": "#ffffff",
     "categories": ["business", "productivity"],
     "icons": [
       {
         "src": "/android-chrome-192x192.png",
         "sizes": "192x192",
         "type": "image/png",
         "purpose": "any"
       },
       {
         "src": "/android-chrome-512x512.png",
         "sizes": "512x512",
         "type": "image/png",
         "purpose": "any"
       },
       {
         "src": "/maskable-icon-512x512.png",
         "sizes": "512x512",
         "type": "image/png",
         "purpose": "maskable"
       }
     ],
     "shortcuts": [
       {
         "name": "Main Feature",
         "short_name": "Feature",
         "description": "Quick access to main feature",
         "url": "/feature",
         "icons": [{ "src": "/android-chrome-192x192.png", "sizes": "192x192" }]
       }
     ]
   }
   ```

   **Manifest Fields:**

   | Field | Required | Description |
   |-------|----------|-------------|
   | name | Yes | Full app name |
   | short_name | Yes | Short name for home screen |
   | description | Yes | App description |
   | start_url | Yes | Entry point URL |
   | scope | Recommended | Navigation scope |
   | display | Yes | standalone, fullscreen, minimal-ui, browser |
   | orientation | Recommended | portrait-primary, landscape-primary, any |
   | lang | Recommended | Language code (en, es, etc.) |
   | theme_color | Yes | Browser chrome color |
   | background_color | Yes | Splash screen background |
   | categories | Recommended | App store categories |
   | icons | Yes | App icons with purpose |
   | shortcuts | Recommended | Quick action links |

4. **Create browserconfig.xml**
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <browserconfig>
     <msapplication>
       <tile>
         <square70x70logo src="/mstile-70x70.png"/>
         <square150x150logo src="/mstile-150x150.png"/>
         <square310x310logo src="/mstile-310x310.png"/>
         <wide310x150logo src="/mstile-310x150.png"/>
         <TileColor>#3B82F6</TileColor>
       </tile>
     </msapplication>
   </browserconfig>
   ```

5. **Validate**
   - Hook checks all required files exist
   - Validates image dimensions
   - Checks manifest JSON syntax

## HTML Integration

Add to `<head>`:

```html
<!-- Favicon -->
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">

<!-- Apple -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Manifest -->
<link rel="manifest" href="/site.webmanifest">

<!-- MS -->
<meta name="msapplication-TileColor" content="#3B82F6">
<meta name="msapplication-config" content="/browserconfig.xml">

<!-- Theme -->
<meta name="theme-color" content="#3B82F6">

<!-- OG Image -->
<meta property="og:image" content="https://yoursite.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

## Dependencies

Requires one of:
- ImageMagick: `sudo apt install imagemagick`
- Sharp (Node): `npm install sharp`
- Pillow (Python): `pip install pillow`

## Error Codes

| Code | Severity | Issue |
|------|----------|-------|
| ASSET001 | error | No source logo found |
| ASSET002 | error | Missing required favicon |
| ASSET003 | error | Missing apple-touch-icon |
| ASSET004 | error | Missing android icons |
| ASSET005 | error | Missing og-image |
| ASSET006 | error | Invalid manifest JSON or missing required field |
| ASSET007 | warning | Missing maskable icon |
| ASSET008 | warning | Image wrong dimensions |
| ASSET009 | warning | Missing browserconfig.xml |
| ASSET010 | warning | Missing recommended manifest field |
| ASSET011 | warning | No icon with purpose 'any' |
