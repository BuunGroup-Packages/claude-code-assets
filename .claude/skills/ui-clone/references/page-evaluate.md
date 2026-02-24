# Page Evaluate Scripts

Self-contained JavaScript functions that run inside `page.evaluate()`. Each returns a serializable object.

## extractColors

Scans all visible elements for color properties and parses accessible stylesheets for CSS custom properties.

```javascript
async function extractColors() {
  const colors = {
    backgrounds: new Map(),
    textColors: new Map(),
    borderColors: new Map(),
    shadowColors: [],
    cssVariables: {},
  };

  // 1. Extract CSS custom properties from :root
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root' || rule.selectorText === ':root, :host') {
          for (const prop of rule.style) {
            if (prop.startsWith('--')) {
              const val = rule.style.getPropertyValue(prop).trim();
              if (/^(#|rgb|hsl|oklch|color\()/.test(val) || /^(transparent|inherit|currentColor)$/i.test(val)) {
                colors.cssVariables[prop] = val;
              }
            }
          }
        }
      }
    } catch (e) { /* cross-origin stylesheet — skip */ }
  }

  // 2. Scan computed styles from visible elements
  const elements = document.querySelectorAll('body *');
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'META', 'LINK', 'BR', 'HR']);

  for (const el of elements) {
    if (skip.has(el.tagName)) continue;
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;

    const cs = getComputedStyle(el);

    // Background color
    const bg = cs.backgroundColor;
    if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
      colors.backgrounds.set(bg, (colors.backgrounds.get(bg) || 0) + 1);
    }

    // Background image (gradients)
    const bgImg = cs.backgroundImage;
    if (bgImg && bgImg !== 'none' && bgImg.includes('gradient')) {
      colors.backgrounds.set(bgImg, (colors.backgrounds.get(bgImg) || 0) + 1);
    }

    // Text color
    const color = cs.color;
    if (color) {
      colors.textColors.set(color, (colors.textColors.get(color) || 0) + 1);
    }

    // Border color
    const bc = cs.borderColor;
    if (bc && bc !== cs.color && cs.borderWidth !== '0px') {
      colors.borderColors.set(bc, (colors.borderColors.get(bc) || 0) + 1);
    }

    // Box shadow
    const shadow = cs.boxShadow;
    if (shadow && shadow !== 'none') {
      colors.shadowColors.push(shadow);
    }
  }

  // Convert Maps to sorted arrays (most used first)
  const sortMap = (m) => [...m.entries()].sort((a, b) => b[1] - a[1]).map(([color, count]) => ({ color, count }));

  return {
    backgrounds: sortMap(colors.backgrounds),
    textColors: sortMap(colors.textColors),
    borderColors: sortMap(colors.borderColors),
    shadows: [...new Set(colors.shadowColors)].slice(0, 10),
    cssVariables: colors.cssVariables,
  };
}
```

## extractTypography

Extracts font families, sizes, weights, line-heights, letter-spacings from computed styles, `document.fonts`, and `@font-face` rules.

```javascript
async function extractTypography() {
  const typo = {
    fontFamilies: new Map(),
    fontSizes: new Map(),
    fontWeights: new Map(),
    lineHeights: new Map(),
    letterSpacings: new Map(),
    fontFaceRules: [],
    headingStyles: [],
    bodyStyle: null,
  };

  // 1. @font-face rules from stylesheets
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSFontFaceRule) {
          typo.fontFaceRules.push({
            family: rule.style.getPropertyValue('font-family').replace(/['"]/g, ''),
            weight: rule.style.getPropertyValue('font-weight') || '400',
            style: rule.style.getPropertyValue('font-style') || 'normal',
            src: rule.style.getPropertyValue('src')?.slice(0, 200),
          });
        }
      }
    } catch (e) { /* cross-origin */ }
  }

  // 2. Loaded fonts from document.fonts API
  const loadedFonts = [];
  if (document.fonts) {
    document.fonts.forEach(f => {
      loadedFonts.push({ family: f.family.replace(/['"]/g, ''), weight: f.weight, style: f.style });
    });
  }

  // 3. Scan computed styles
  const elements = document.querySelectorAll('body *');
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'META', 'LINK']);

  for (const el of elements) {
    if (skip.has(el.tagName)) continue;
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;
    if (!el.textContent?.trim()) continue;

    const cs = getComputedStyle(el);
    const family = cs.fontFamily;
    const size = cs.fontSize;
    const weight = cs.fontWeight;
    const lh = cs.lineHeight;
    const ls = cs.letterSpacing;

    if (family) typo.fontFamilies.set(family, (typo.fontFamilies.get(family) || 0) + 1);
    if (size) typo.fontSizes.set(size, (typo.fontSizes.get(size) || 0) + 1);
    if (weight) typo.fontWeights.set(weight, (typo.fontWeights.get(weight) || 0) + 1);
    if (lh && lh !== 'normal') typo.lineHeights.set(lh, (typo.lineHeights.get(lh) || 0) + 1);
    if (ls && ls !== 'normal' && ls !== '0px') typo.letterSpacings.set(ls, (typo.letterSpacings.get(ls) || 0) + 1);
  }

  // 4. Heading styles (h1-h6)
  for (let i = 1; i <= 6; i++) {
    const h = document.querySelector(`h${i}`);
    if (h) {
      const cs = getComputedStyle(h);
      typo.headingStyles.push({
        tag: `h${i}`,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        fontFamily: cs.fontFamily,
        color: cs.color,
        textTransform: cs.textTransform,
      });
    }
  }

  // 5. Body style
  const body = document.body;
  if (body) {
    const cs = getComputedStyle(body);
    typo.bodyStyle = {
      fontSize: cs.fontSize,
      fontWeight: cs.fontWeight,
      lineHeight: cs.lineHeight,
      fontFamily: cs.fontFamily,
      color: cs.color,
    };
  }

  const sortMap = (m) => [...m.entries()].sort((a, b) => b[1] - a[1]).map(([value, count]) => ({ value, count }));

  return {
    fontFamilies: sortMap(typo.fontFamilies),
    fontSizes: sortMap(typo.fontSizes),
    fontWeights: sortMap(typo.fontWeights),
    lineHeights: sortMap(typo.lineHeights),
    letterSpacings: sortMap(typo.letterSpacings),
    fontFaceRules: typo.fontFaceRules,
    loadedFonts,
    headingStyles: typo.headingStyles,
    bodyStyle: typo.bodyStyle,
  };
}
```

## extractSpacing

Extracts margins, paddings, gaps, border-radii, and max-widths to identify the spacing system.

```javascript
async function extractSpacing() {
  const spacing = {
    paddings: new Map(),
    margins: new Map(),
    gaps: new Map(),
    borderRadii: new Map(),
    maxWidths: new Map(),
  };

  const elements = document.querySelectorAll('body *');
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'META', 'LINK', 'BR', 'HR']);

  for (const el of elements) {
    if (skip.has(el.tagName)) continue;
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;

    const cs = getComputedStyle(el);

    // Padding (collect non-zero individual sides)
    ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].forEach(prop => {
      const val = cs[prop];
      if (val && val !== '0px') {
        spacing.paddings.set(val, (spacing.paddings.get(val) || 0) + 1);
      }
    });

    // Margin (collect non-zero, non-auto)
    ['marginTop', 'marginRight', 'marginBottom', 'marginLeft'].forEach(prop => {
      const val = cs[prop];
      if (val && val !== '0px' && val !== 'auto') {
        spacing.margins.set(val, (spacing.margins.get(val) || 0) + 1);
      }
    });

    // Gap (flex/grid)
    const gap = cs.gap;
    if (gap && gap !== 'normal' && gap !== '0px') {
      spacing.gaps.set(gap, (spacing.gaps.get(gap) || 0) + 1);
    }

    // Border radius
    const br = cs.borderRadius;
    if (br && br !== '0px') {
      spacing.borderRadii.set(br, (spacing.borderRadii.get(br) || 0) + 1);
    }

    // Max width
    const mw = cs.maxWidth;
    if (mw && mw !== 'none' && mw !== '0px') {
      spacing.maxWidths.set(mw, (spacing.maxWidths.get(mw) || 0) + 1);
    }
  }

  const sortMap = (m) => [...m.entries()].sort((a, b) => b[1] - a[1]).map(([value, count]) => ({ value, count }));

  return {
    paddings: sortMap(spacing.paddings).slice(0, 20),
    margins: sortMap(spacing.margins).slice(0, 20),
    gaps: sortMap(spacing.gaps).slice(0, 15),
    borderRadii: sortMap(spacing.borderRadii).slice(0, 10),
    maxWidths: sortMap(spacing.maxWidths).slice(0, 10),
  };
}
```

## extractLayout

Identifies flex/grid containers and extracts media query breakpoints from stylesheets.

```javascript
async function extractLayout() {
  const layout = {
    flexContainers: [],
    gridContainers: [],
    breakpoints: new Set(),
  };

  // 1. Find flex and grid containers
  const elements = document.querySelectorAll('body *');
  let flexCount = 0, gridCount = 0;

  for (const el of elements) {
    const cs = getComputedStyle(el);
    const display = cs.display;

    if (display === 'flex' || display === 'inline-flex') {
      flexCount++;
      if (flexCount <= 10) {
        layout.flexContainers.push({
          tag: el.tagName.toLowerCase(),
          class: el.className?.toString().slice(0, 100) || '',
          direction: cs.flexDirection,
          wrap: cs.flexWrap,
          justify: cs.justifyContent,
          align: cs.alignItems,
          gap: cs.gap,
        });
      }
    }

    if (display === 'grid' || display === 'inline-grid') {
      gridCount++;
      if (gridCount <= 10) {
        layout.gridContainers.push({
          tag: el.tagName.toLowerCase(),
          class: el.className?.toString().slice(0, 100) || '',
          columns: cs.gridTemplateColumns,
          rows: cs.gridTemplateRows,
          gap: cs.gap,
        });
      }
    }
  }

  // 2. Extract breakpoints from @media rules
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSMediaRule) {
          const text = rule.conditionText || rule.media?.mediaText || '';
          const matches = text.match(/(\d+)px/g);
          if (matches) {
            matches.forEach(m => layout.breakpoints.add(m));
          }
        }
      }
    } catch (e) { /* cross-origin */ }
  }

  return {
    flexContainers: layout.flexContainers,
    gridContainers: layout.gridContainers,
    totalFlex: flexCount,
    totalGrid: gridCount,
    breakpoints: [...layout.breakpoints].sort((a, b) => parseInt(a) - parseInt(b)),
  };
}
```

## detectComponents

Finds key page components: header/nav, hero, buttons, cards, forms, footer. Returns selector, dimensions, and key computed styles.

```javascript
async function detectComponents() {
  const components = {
    header: null,
    hero: null,
    buttons: [],
    cards: [],
    forms: [],
    footer: null,
    sections: [],
  };

  function getStyles(el) {
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return {
      width: rect.width,
      height: rect.height,
      top: rect.top,
      background: cs.backgroundColor,
      backgroundImage: cs.backgroundImage !== 'none' ? cs.backgroundImage.slice(0, 200) : null,
      color: cs.color,
      fontSize: cs.fontSize,
      fontWeight: cs.fontWeight,
      padding: cs.padding,
      borderRadius: cs.borderRadius,
      border: cs.border,
      boxShadow: cs.boxShadow !== 'none' ? cs.boxShadow : null,
      display: cs.display,
    };
  }

  // Header / Nav
  const headerEl = document.querySelector('header') || document.querySelector('nav') || document.querySelector('[role="banner"]');
  if (headerEl) {
    components.header = {
      tag: headerEl.tagName.toLowerCase(),
      selector: headerEl.tagName.toLowerCase(),
      ...getStyles(headerEl),
      links: headerEl.querySelectorAll('a').length,
    };
  }

  // Hero — first large section or element with hero-like class
  const heroSelectors = [
    '[class*="hero"]', '[id*="hero"]',
    'main > section:first-child', 'main > div:first-child',
    '.banner', '[class*="banner"]',
  ];
  for (const sel of heroSelectors) {
    const el = document.querySelector(sel);
    if (el) {
      const rect = el.getBoundingClientRect();
      if (rect.height > 200) {
        components.hero = { selector: sel, ...getStyles(el) };
        break;
      }
    }
  }
  // Fallback: first section with height > 400px
  if (!components.hero) {
    for (const section of document.querySelectorAll('section, [class*="section"]')) {
      const rect = section.getBoundingClientRect();
      if (rect.height > 400 && rect.top < 800) {
        components.hero = { selector: 'section (first large)', ...getStyles(section) };
        break;
      }
    }
  }

  // Buttons — find unique visual variants
  const buttonEls = document.querySelectorAll('button, a[class*="btn"], a[class*="button"], [role="button"]');
  const seenButtonStyles = new Set();
  for (const btn of buttonEls) {
    const cs = getComputedStyle(btn);
    const key = `${cs.backgroundColor}|${cs.color}|${cs.borderRadius}|${cs.border}`;
    if (!seenButtonStyles.has(key) && btn.textContent?.trim()) {
      seenButtonStyles.add(key);
      components.buttons.push({
        text: btn.textContent.trim().slice(0, 50),
        tag: btn.tagName.toLowerCase(),
        class: btn.className?.toString().slice(0, 100) || '',
        ...getStyles(btn),
      });
    }
    if (components.buttons.length >= 6) break;
  }

  // Cards — elements with card-like class or repeated similar structures
  const cardSelectors = ['[class*="card"]', '[class*="Card"]', 'article', '[class*="tile"]', '[class*="item"]'];
  for (const sel of cardSelectors) {
    const els = document.querySelectorAll(sel);
    if (els.length >= 2) {
      for (let i = 0; i < Math.min(3, els.length); i++) {
        components.cards.push({
          selector: sel,
          class: els[i].className?.toString().slice(0, 100) || '',
          ...getStyles(els[i]),
          hasImage: !!els[i].querySelector('img'),
        });
      }
      break;
    }
  }

  // Forms / Inputs
  const formEls = document.querySelectorAll('input[type="text"], input[type="email"], input[type="search"], textarea');
  const seenInputStyles = new Set();
  for (const input of formEls) {
    const cs = getComputedStyle(input);
    const key = `${cs.border}|${cs.borderRadius}|${cs.backgroundColor}`;
    if (!seenInputStyles.has(key)) {
      seenInputStyles.add(key);
      components.forms.push({
        type: input.type || input.tagName.toLowerCase(),
        ...getStyles(input),
      });
    }
    if (components.forms.length >= 3) break;
  }

  // Footer
  const footerEl = document.querySelector('footer') || document.querySelector('[role="contentinfo"]');
  if (footerEl) {
    components.footer = {
      tag: footerEl.tagName.toLowerCase(),
      ...getStyles(footerEl),
      links: footerEl.querySelectorAll('a').length,
      columns: footerEl.querySelectorAll('div > ul, nav').length || footerEl.querySelectorAll('[class*="col"]').length,
    };
  }

  // Sections — collect all major sections
  const sectionEls = document.querySelectorAll('section, [class*="section"]');
  for (const section of sectionEls) {
    const rect = section.getBoundingClientRect();
    if (rect.height > 100) {
      const cs = getComputedStyle(section);
      components.sections.push({
        class: section.className?.toString().slice(0, 100) || '',
        background: cs.backgroundColor,
        color: cs.color,
        height: rect.height,
        padding: cs.padding,
      });
    }
    if (components.sections.length >= 15) break;
  }

  return components;
}
```

## extractAnimations

Extracts CSS transitions from elements and `@keyframes` from stylesheets.

```javascript
async function extractAnimations() {
  const animations = {
    transitions: new Map(),
    keyframes: [],
    animatedElements: [],
  };

  // 1. Scan elements for transitions and animations
  const elements = document.querySelectorAll('body *');
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'META', 'LINK']);

  for (const el of elements) {
    if (skip.has(el.tagName)) continue;
    const cs = getComputedStyle(el);

    // Transitions
    const transition = cs.transition;
    if (transition && transition !== 'all 0s ease 0s' && transition !== 'none') {
      animations.transitions.set(transition, (animations.transitions.get(transition) || 0) + 1);
    }

    // Active animations
    const animName = cs.animationName;
    if (animName && animName !== 'none') {
      animations.animatedElements.push({
        tag: el.tagName.toLowerCase(),
        class: el.className?.toString().slice(0, 100) || '',
        animationName: animName,
        animationDuration: cs.animationDuration,
        animationTimingFunction: cs.animationTimingFunction,
        animationIterationCount: cs.animationIterationCount,
      });
    }
  }

  // 2. Extract @keyframes from stylesheets
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSKeyframesRule) {
          const frames = [];
          for (const frame of rule.cssRules) {
            frames.push({
              keyText: frame.keyText,
              cssText: frame.cssText.slice(0, 300),
            });
          }
          animations.keyframes.push({
            name: rule.name,
            frames,
          });
        }
      }
    } catch (e) { /* cross-origin */ }
  }

  const sortMap = (m) => [...m.entries()].sort((a, b) => b[1] - a[1]).map(([value, count]) => ({ value, count }));

  return {
    transitions: sortMap(animations.transitions).slice(0, 15),
    keyframes: animations.keyframes.slice(0, 20),
    animatedElements: animations.animatedElements.slice(0, 15),
  };
}
```

## detectIcons

Checks for known icon libraries and counts inline SVGs.

```javascript
async function detectIcons() {
  const icons = {
    libraries: [],
    inlineSvgCount: 0,
    svgSprites: false,
    iconFonts: [],
  };

  // Check for icon library stylesheets/scripts
  const knownLibraries = [
    { name: 'Lucide', patterns: ['lucide', 'lucide-react'] },
    { name: 'Heroicons', patterns: ['heroicon', 'heroicons'] },
    { name: 'Font Awesome', patterns: ['font-awesome', 'fontawesome', 'fa-'] },
    { name: 'Material Icons', patterns: ['material-icons', 'material-symbols'] },
    { name: 'Phosphor', patterns: ['phosphor'] },
    { name: 'Feather', patterns: ['feather'] },
    { name: 'Tabler Icons', patterns: ['tabler-icon'] },
    { name: 'Remix Icons', patterns: ['remixicon', 'ri-'] },
  ];

  const html = document.documentElement.outerHTML.toLowerCase();
  for (const lib of knownLibraries) {
    if (lib.patterns.some(p => html.includes(p))) {
      icons.libraries.push(lib.name);
    }
  }

  // Count inline SVGs
  icons.inlineSvgCount = document.querySelectorAll('svg').length;

  // Check for SVG sprites
  const spriteUse = document.querySelectorAll('use[href], use[xlink\\:href]');
  icons.svgSprites = spriteUse.length > 0;

  // Check for icon fonts
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSFontFaceRule) {
          const family = rule.style.getPropertyValue('font-family').toLowerCase();
          if (/icon|symbol|glyph/i.test(family)) {
            icons.iconFonts.push(family.replace(/['"]/g, ''));
          }
        }
      }
    } catch (e) { /* cross-origin */ }
  }

  return icons;
}
```

## Running All Extractors

Call all functions in a single `page.evaluate()`:

```javascript
const data = await page.evaluate(async () => {
  // paste all functions above, then:
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
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
    },
  };
});
```
