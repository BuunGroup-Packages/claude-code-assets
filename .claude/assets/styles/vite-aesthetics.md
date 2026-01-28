# Vite Aesthetic

**Style Name:** Dark Grid Neon
**Mood:** Professional, Developer-focused, Futuristic, Clean

---

## Visual Identity

### Atmosphere
A midnight workspace illuminated by soft purple neon. Technical precision meets modern elegance. The design feels like a premium developer tool interface - functional yet beautiful.

### Core Characteristics
- **Dark immersive background** - Near-black canvas
- **Grid-based structure** - Content divided by thin luminous borders
- **Purple neon accents** - Electric violet glows on interaction
- **High contrast typography** - Crisp white text on dark
- **Floating 3D elements** - Isometric graphics with subtle depth
- **Minimal ornamentation** - Let content breathe

---

## Color System

### Background Layers
```
Base:        #1a1a1a  (near-black)
Surface:     #1e1e1e  (card/panel)
Elevated:    #252525  (hover states)
```

### Accent
```
Primary:     #646cff  (electric violet)
Glow:        #a855f7  (soft purple)
Deep:        #370a7f  (rich purple for panels)
```

### Text
```
Primary:     #ffffff  (pure white)
Secondary:   rgba(255,255,255,0.7)  (muted white)
Tertiary:    #888888  (grey labels)
```

### Borders
```
Default:     #2a2a2a  (subtle nickel)
Hover:       #444444  (visible on interaction)
```

---

## Typography

### Voice
Clean, confident, technical. Uses monospace for labels and data. Sans-serif for headings and body.

### Hierarchy
| Level | Style |
|-------|-------|
| Hero | 48px, Bold, White, Tight leading |
| Section | 30px, Semibold, White |
| Card Title | 20px, Semibold, White |
| Body | 16-18px, Regular, White/70 |
| Label | 12px, Mono, Uppercase, Grey, Tracked |

### Text Treatment
- Headlines use `text-balance` for even line breaks
- Body text uses `text-pretty` for optimal wrapping
- Max-width constraints (25-28rem) prevent overly long lines
- Generous line-height (1.6-1.7) for readability

---

## Grid & Layout

### The Divided Grid
Content is organized in a **2-column grid** with visible **1px borders** between cells. This creates a "panel" or "dashboard" aesthetic.

```
┌─────────────────┬─────────────────┐
│                 │                 │
│    Panel 1      │    Panel 2      │
│                 │                 │
├─────────────────┼─────────────────┤
│                 │                 │
│    Panel 3      │    Panel 4      │
│                 │                 │
└─────────────────┴─────────────────┘
```

### Edge Markers
The wrapper has **tick marks** along vertical edges - small dashed lines that suggest measurement or precision (like a ruler or terminal).

### Spacing Philosophy
- Generous internal padding (40-60px in panels)
- Consistent gaps between elements (12-20px)
- Large vertical rhythm between sections (80-120px)

---

## Visual Elements

### Isometric 3D Graphics
Feature illustrations use **floating isometric cards** with:
- Slight 3D perspective (tilted planes)
- Stacked layers suggesting depth
- Soft shadows and purple edge glows
- File type labels (.jsx, .css, .ts) as mini badges

### Terminal/Code Blocks
- Dark slate background
- Monospace font
- Syntax highlighting with purple/blue accents
- Rounded corners (8px)

### Icons & Logos
- Simple, geometric
- Single color (white or grey)
- Small size (24px)
- Used sparingly

---

## Interaction States

### Hover Effects

**Cards:**
- Border fades from nickel to transparent
- Background reveals animated purple gradient
- Gradient slowly shifts position (16s loop)

**Buttons:**
- Primary: Background lightens
- Secondary: Border brightens

**Links:**
- Color shifts to brand purple
- No underline

### The Gradient Reveal
On hover, cards reveal a **moving gradient texture** beneath:
1. Gradient starts hidden (opacity 0)
2. On hover, fades in behind content
3. Gradient slowly animates position
4. Creates "living" glowing effect

---

## Animation Style

### Motion Principles
- **Subtle** - Never distracting
- **Purposeful** - Indicates state or draws attention
- **Smooth** - Eased transitions (ease-in-out)
- **Slow** - Long durations (10-20s for ambient, 0.1-0.2s for interactions)

### Rive Animations
Complex illustrations are **vector animations** created in Rive:
- Floating/bobbing motion
- Assembly/connection animations
- Particle effects
- State machine driven (responds to scroll/hover)

### CSS Animations
- Background position shifts
- Opacity fades
- Border color transitions
- Scale on hover (subtle, 1.02x)

---

## Component Patterns

### Feature Panel
```
┌────────────────────────────────┐
│  Title                         │
│  Description paragraph         │
│                                │
│  ┌──────────────────────────┐  │
│  │                          │  │
│  │   Visual / Animation     │  │
│  │   (purple tinted bg)     │  │
│  │                          │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
```

### Testimonial Card
- Rounded corners (8px)
- Slate background
- Nickel border (fades on hover)
- Avatar (small, rounded)
- Quote text (white/70)
- Author name (mono, grey)
- Handle (mono, muted)

### Stats Block
```
75k+
───────
[icon] GitHub Stars
```
- Large number (h2 size, white)
- Icon + label below (grey, small)

### Section Header
- Centered text
- Balanced headline
- Optional muted subheadline
- Generous vertical padding

---

## Page Rhythm

```
[Nav - sticky, minimal]
     ↓
[Hero - 2 columns, animation right]
     ↓
[Trust bar - logo strip]
     ↓
[Heading - centered]
     ↓
[Feature grid - 2x2]
     ↓
[Heading - centered]
     ↓
[Feature grid - 2x2]
     ↓
[Framework logos - full width image]
     ↓
[Community - stats + testimonial masonry]
     ↓
[Sponsors - logo grid]
     ↓
[CTA Footer - heading + button]
```

---

## Do's and Don'ts

### Do
- Use the dark background consistently
- Let borders define structure
- Keep text high contrast
- Use purple sparingly (accents only)
- Add subtle motion to key elements
- Maintain generous whitespace
- Use isometric/3D for illustrations

### Don't
- Use light backgrounds
- Add too many colors
- Overuse animations
- Crowd content together
- Use decorative elements without purpose
- Make borders thick or prominent
- Use gradients for backgrounds (only for hover effects)

---

## Reference Keywords

When prompting for this style:
- "Dark developer aesthetic"
- "Neon grid layout"
- "Purple accent dark theme"
- "Technical minimalist"
- "Isometric 3D illustrations"
- "Dashboard-style panels"
- "Vite/VoidZero aesthetic"
- "Midnight workspace"
