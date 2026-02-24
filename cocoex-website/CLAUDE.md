# cocoex.xyz Website

## Project Overview
Static portfolio website for cocoex - a vibrant DAO blending art, blockchain, community and social impact. Core values: **usability**, **design**, **minimalism**.

## Site Structure

**Section 1 - Landing/Intro (`.intro`)**
- Fixed-position WebGL animated canvas background (twinkling stars + cosmic noise)
- Orbiting dots (white/black) converging animation
- Center logo reveal with rotation
- Constellation explosion into 7 colored dots with depth
- Big bang pulse effect on explosion
- Z-axis rotation during text section scroll

**Section 2 - Mission Text (`.text-section-wrapper`)**
- Sticky-scroll text reveal with 350vh scroll height
- Mission statement with highlighted key terms (community, art, impactful)
- Sequential word highlighting (3 words total)
- Constellation rotates 15° during highlights
- Smooth fade to next sections

**Section 3 - Muse Portfolio (`.muse-section-wrapper`)**
- 300vh scroll wrapper (200vh intro hold + 100vh crossfade)
- Black intro page with Muse logo (white inverted) + description text
- Fades in when entering viewport (top 80% → 40%)
- Holds for 2 scrolls, then crossfades out over 1 scroll to reveal orbiting content
- Orbiting layout: 7 muses in horizontal ellipse (240s continuous rotation)
- Properly reverses when scrolling up (intro fades back in)
- Each muse has unique color, interactive popup modal on click
- Animated WebGL gradient background (muse colors)
- Layered over unified starfield canvas

**Section 4 - Comet Collab (`.comet-collab-wrapper`)**
- 400vh scroll wrapper (100vh intro + 200vh movement + 100vh crossfade)
- White intro page with Comet Collabs logo + description
- Fades in when entering viewport (top 80% → 40%)
- Holds for 1 scroll, then logo moves down + text moves up over 2 scrolls
- Crossfades to slideshow over 1 scroll
- Properly reverses when scrolling up (logo/text movement reverses, intro fades back in)
- Slideshow stays active until natural page end (footer)
- Bouncing DVD-style logo with spark particles on bounce (slower speed: 2px/1.5px)
- Interactive 5-phase slider with image + text reels
- Orbital navigation (prev/next buttons + dots)
- WebGL gradient background (same as Muse)

**Footer** - Fixed position, revealed at end of Comet section
- Social links (Telegram, Instagram, LinkedIn)
- Cocoex text logo

## DOM Reference Guide

### Identifying Sections for Changes

When requesting changes, the most effective approach combines **visual description + DOM selector** for clarity and precision.

**Primary Identifiers (Most Reliable):**
- CSS Classes & IDs: `.intro`, `.text-section-wrapper`, `.muse-section-wrapper`, `.comet-collab-wrapper`
- Canvas IDs: `#bg-canvas`, `#constellation-canvas`, `#unified-starfield-canvas`, `#muse-background-canvas`, `#comet-collab-background-canvas`
- Component IDs: `#muse-section`, `#comet-collab-section`, `#comet-collab-bouncing-logo`
- HTML hierarchy: parent-child relationships
- ARIA labels: `aria-label="Muse portfolio"`, `aria-label="Comet collab phases showcase"`

**Effective Communication Patterns:**

✅ **Good:** "The social media icons at the bottom"
✅ **Better:** "The footer with Instagram, Telegram, LinkedIn icons"
✅ **Best:** "The `.social-links` footer at the bottom of `.white-section`"

**Context Types That Help:**
- **Visual/Positional:** "The orbiting dots in the intro"
- **Functional:** "The popup that appears when clicking muse names"
- **Scroll Position:** "After the text section but before the white background"
- **Timing:** "The animation that plays during the first scroll"

### Section Reference Map

| Visual Description | CSS/DOM Reference | JS Module (if applicable) | Function/Area |
|-------------------|------------------|-----------|----------------|
| Intro WebGL background | `#bg-canvas` | Main render loop | render() + updatePositions() |
| Orbiting dots | `.orbit-dot-white`, `.orbit-dot-black` | updateOrbitPositions | GSAP scroll-driven |
| Logo rotation | `.logo-container`, `#intro-logo` | orbitState | GSAP timeline (phase 1) |
| Constellation explosion | `#constellation-canvas` | updateFireworkDots | Phase 3 (40%-100%) |
| Big bang pulse | `u_pulse` uniform | WebGL shader | Triggered at constellation start |
| Constellation rotation | constellationRotation | updateFireworkDots | Rotates during text highlights |
| Mission text highlights | `.text-section-wrapper`, `.reveal-text` | GSAP ScrollTrigger | 3 word highlights |
| Muse intro page | `.muse-intro-page` | GSAP ScrollTrigger | 200vh hold (2 scrolls), 100vh crossfade |
| Muse gradient background | `#muse-background-canvas` | MuseBackground module | Animated gradient shader |
| Unified starfield | `#unified-starfield-canvas` | UnifiedStarfield module | Twinkling stars (Muse + Comet) |
| Orbiting muses | `.muse-orbit-container`, `.muse-orbit-item` | MuseScroll module | 240s rotation, elliptical orbit |
| Muse popup modal | `.muse-popup`, `.muse-popup-content` | MusePopup module | Click image/title to open |
| Comet intro page | `.comet-collab-intro` | GSAP ScrollTrigger | 100vh hold, 200vh logo descent + text up, 100vh crossfade |
| Comet slider | `.comet-collab-section` | CometCollabSlider module | 5-phase reel with navigation |
| Bouncing logo | `#comet-collab-bouncing-logo` | CometCollabSlider | DVD-style bounce (velocity: 2, 1.5) with sparks |
| Comet background | `#comet-collab-background-canvas` | CometCollabBackground | Same gradient as Muse |
| Footer (social + logo) | `.social-links`, `.footer-logo` | GSAP ScrollTrigger | Reveals at comet section end |

### CSS Organization Reference

- **Lines 1-35:** Variables (colors, fonts, spacing, z-index, transitions)
- **Lines 37-95:** Reset & base styles (`prefers-reduced-motion` override)
- **Lines 96-137:** Intro section (fixed positioning)
- **Lines 139-251:** Logo, orbiting dots, final dot, constellation canvas
- **Lines 253-265:** Unified starfield canvas (Muse + Comet background)
- **Lines 267-318:** Text section with word highlights
- **Lines 320-333:** White section wrapper
- **Lines 335-791:** Comet Collab (wrapper, intro, slider, nav, reels, logo bounce)
- **Lines 938-1003:** Social links & footer
- **Lines 1005-1077:** Muse section wrapper & intro page
- **Lines 1079-1194:** Muse orbiting layout
- **Lines 1196-1290:** Muse popup modal
- **Lines 1292-1521:** Responsive breakpoints (tablet → mobile → small mobile → large desktop)

### JavaScript Module Reference

- **GLSL_UTILS (16-85):** Shared GLSL shader utilities (simplex noise, star field)
- **SCROLL_TIMING (88-115):** Centralized scroll timing constants (all sections)
- **CONFIG (117-164):** Layout constants, sizes, timing, breakpoints
- **DOT_COLORS (156-164):** 7 muse colors for constellation
- **CONSTELLATION_REF (168-176):** Constellation dot positions with z-depth
- **DOM Elements (191-205):** All element references
- **STATE (212-222):** Animation state variables (pulseValue, constellationRotation, etc.)
- **WebGL Background (270-386):** Intro starfield shader with big bang pulse
- **Firework/Constellation (408-659):** Explosion with z-depth and rotation
- **Render Loop (662-696):** Main animation frame
- **GSAP Animations (732-1023):** Scroll-driven animations (all sections)
- **updateOrbitPositions (1026-1087):** GSAP-driven orbit animation (phase 1)
- **MuseBackground (1090-1249):** Muse gradient WebGL shader
- **UnifiedStarfield (1251-1357):** Shared starfield for Muse + Comet sections
- **CometCollabBackground (1359-1502):** Comet gradient (reuses Muse shader)
- **MusePopup (1504-1626):** Modal interactions with GSAP animations
- **MuseScroll (1628-1745):** Orbiting layout with continuous rotation
- **CometCollabSlider (1747-2189):** Bouncing logo + 5-phase slider with drag support

### Communication Examples

**Positioning Changes:**
> "Move the social links higher on the page"
→ Target: `.social-links` in styles.css:942 and GSAP ScrollTrigger in main.js:827-839

**Animation Adjustments:**
> "Speed up the muse orbit rotation"
→ Target: `MuseScroll.orbitSpeed` property (default: 0.00015 for 240s rotation)

> "Change bounce speed of comet logo"
→ Target: `CometCollabSlider.logoVelocityX` (default: 5) and `logoVelocityY` (default: 4)

**Styling Updates:**
> "Change the constellation dot colors"
→ Target: `DOT_COLORS` constant in main.js:156-164

> "Adjust muse gradient colors"
→ Target: `MuseBackground.colors` array in main.js:1099-1107

**Scroll Behavior:**
> "Make the text section scroll slower"
→ Target: `SCROLL_TIMING.TEXT_HIGHLIGHT_START` and `.text-section-wrapper` height in styles.css:271

> "Adjust muse intro hold time"
→ Target: `SCROLL_TIMING.MUSE_INTRO_HOLD` (default: 200vh) - Note: Update MUSE_TOTAL and CSS accordingly

> "Adjust muse crossfade duration"
→ Target: `SCROLL_TIMING.MUSE_CROSSFADE` (default: 100vh) - Transition from intro to orbiting content

> "Change comet intro pause duration"
→ Target: `SCROLL_TIMING.COMET_INTRO_PAUSE` (default: 100vh)

> "Adjust comet logo movement duration"
→ Target: `SCROLL_TIMING.COMET_LOGO_MOVEMENT` (default: 200vh - 2 full scrolls)

> "Adjust comet crossfade duration"
→ Target: `SCROLL_TIMING.COMET_CROSSFADE_DURATION` (default: 100vh)

> "Adjust bouncing logo speed"
→ Target: `CometCollabSlider.logoVelocityX` (default: 2) and `logoVelocityY` (default: 1.5) in main.js:1779-1780

## Tech Stack
- **Vanilla HTML/CSS/JS** - No framework overhead
- **GSAP 3.12.5** - ScrollTrigger, MotionPathPlugin for scroll-driven animations
- **WebGL** - Custom shaders for background effects
- **Adobe Fonts (Typekit)** - Canela font family (Bold + Regular)
- **Structure:** `index.html` | `css/styles.css` | `js/main.js` | `tools/coordinate-picker.html`
- Modern CSS (Grid/Flexbox, custom properties, animations)
- ES6+ JavaScript with IIFE pattern

## Typography System

**Font Family**: Canela (via Adobe Fonts)
- Loaded via Typekit embed in `<head>` (replace `YOUR_KIT_ID` with actual project ID)
- Fallback: Georgia, serif

**Type Scale** (CSS Custom Properties):
- **H1 (Header 1)**: Canela Bold, 36px / 38px line-height
  - Variables: `--font-h1-size`, `--font-h1-height`, `--font-h1-weight: 700`
  - Used for: Mission text, comet phase titles, muse popup titles
- **H2 (Header 2)**: Canela Regular, 18px / 21px line-height
  - Variables: `--font-h2-size`, `--font-h2-height`, `--font-h2-weight: 400`
  - Used for: Intro text, phase descriptions, muse names, popup descriptions

**Responsive Scaling**:
- **Desktop (default)**: H1: 36/38px, H2: 18/21px
- **Tablet (≤1024px)**: H1: 30/33px, H2: 16/19px
- **Mobile (≤768px)**: H1: 22/26px, H2: 14/17px
- **Small Mobile (≤480px)**: H1: 18/22px, H2: 12/15px
- **Large Desktop (≥1440px)**: H1: 42/46px, H2: 20/24px
- **XL Desktop (≥1920px)**: H1: 48/52px, H2: 22/26px

All typography scales automatically via CSS variables in media queries.

## Design Principles

### Minimalism First
Remove before adding. Question every element. White space is a feature. Less code = faster load = better UX.

### Fluid UI
- Smooth transitions and animations (60fps target)
- Responsive breakpoints: 480px, 768px, 1024px, 1440px, 1920px
- Hardware-accelerated animations (`transform`, `opacity`, `filter`)
- Touch-friendly targets (min 44px)
- Debounced resize handlers

### Performance Budget
- **First Contentful Paint:** <1.5s
- **Time to Interactive:** <3s
- **Lighthouse score:** 95+
- Optimize images (consider WebP, lazy load if needed)
- Inline critical CSS, defer non-critical
- No layout shifts (CLS < 0.1)
- `will-change` for animated elements

### Accessibility
- Semantic HTML5 elements (`<section>`, `<article>`, `<footer>`)
- ARIA labels for decorative and interactive elements
- Keyboard navigation (Tab, Escape for modal)
- Focus visible styles (outline + outline-offset)
- Color contrast WCAG AA minimum
- `prefers-reduced-motion` support
- Screen reader friendly

## Frontend Standards

**CSS:**
- CSS custom properties for theming and typography (`:root`)
- Responsive typography via CSS variables (automatic scaling)
- Mobile-first media queries
- Organized by section with header comments
- Avoid `!important` (only exception: reduced motion override)
- Hardware acceleration: `transform: translateZ(0)`

**JavaScript:**
- IIFE pattern for encapsulation
- Module organization: CONFIG → DOM → STATE → FUNCTIONS → INIT
- Event delegation where applicable
- Debounced scroll/resize handlers
- Error handling for WebGL fallback
- Passive event listeners for performance
- No dependencies except GSAP

**HTML:**
- Semantic elements over divs
- Valid W3C markup
- Meta tags for SEO + Open Graph
- `rel="noopener noreferrer"` on external links
- Descriptive `alt` text on images
- `aria-hidden="true"` on decorative elements

## Code Organization

**CSS Structure:**
```
1. Custom Properties (variables)
2. Reset & Base Styles
3. Layout - Scroll Container
4. Intro Section
5. Logo & Orbiting Dots
6. Constellation Canvas
7. Text Section
8. White Section (Muse)
9. Muse Opening Slide
10. Muse Orbiting Layout
11. Muse Popup Modal
12. Social Links & Footer
13. Responsive (Tablet → Mobile → Small Mobile → Large Desktop)
14. Utility Classes
15. Print Styles
16. Reduced Motion Override
```

**JavaScript Structure:**
```
1. IIFE Wrapper
2. GSAP Plugin Registration
3. Configuration Constants
4. DOM Element References
5. State Variables
6. Utility Functions
7. Easing Functions
8. WebGL Shader Setup
9. Resize Handler
10. Firework/Constellation Logic
11. Position Updates (scroll-driven)
12. Animation Loop
13. Event Listeners
14. GSAP ScrollTrigger Animations
15. Muse Opening Slide Module
16. Muse Background Module (WebGL)
17. Muse Popup Module
18. Muse Scroll Module (orbiting)
19. Initialization
```

## Performance Characteristics

### Bundle Composition
- **HTML**: 10.2KB (gzipped: ~3.5KB)
- **CSS**: 21.4KB (gzipped: ~5.2KB)
- **JavaScript**: 37.8KB (gzipped: ~11.3KB)
- **Total Core**: 69.4KB (gzipped: ~20KB)
- **GSAP CDN**: 47KB (cached after first visit)

### WebGL Resources
- **Active Canvases**: 4 simultaneous (intro bg, unified starfield, muse gradient, comet gradient)
- **Shader Programs**: 4 compiled programs (intro, starfield, muse/comet gradient shared)
- **Memory Usage**: ~50-70MB (varies by viewport size)
- **GPU Layers**: 15-25 composited layers (hardware accelerated)
- **Shared GLSL**: Simplex noise + star field utilities (~150 lines saved via reuse)

### Animation Performance
- **RequestAnimationFrame Loops**: 5 independent loops (intro, muse bg, unified starfield, comet bg, muse orbiting)
- **Additional Loops**: 1 conditional (bouncing logo when active)
- **Target FPS**: 60fps desktop, 30fps mobile
- **Scroll Events**: Handled by GSAP ScrollTrigger (optimized)
- **Resize Events**: Debounced to 150ms
- **GSAP ScrollTrigger**: ~60fps interpolation with `scrub: true`

### Scroll Timing Architecture
Centralized timing constants (`SCROLL_TIMING` object) define all scroll-based animations:
- **Intro Section**: 400vh total (orbit + constellation explosion)
- **Text Section**: 350vh with sequential word highlights
- **Muse Section**: 300vh (200vh intro hold + 100vh crossfade to orbiting content)
- **Comet Section**: 400vh (100vh intro + 200vh logo/text movement + 100vh crossfade, then natural page end)

All timing values are stored in constants for easy adjustment without cascading changes.

### Optimization Strategies
- Hardware-accelerated transforms (`transform`, `opacity` only)
- GSAP ScrollTrigger replaces manual scroll listeners
- Debounced resize handler (150ms) with passive listeners
- Shared GLSL utilities (simplex noise + star field) reduce duplication by ~150 lines
- Muse and Comet gradient shaders share identical code
- `will-change` hints on animated elements (logo, dots, sections)
- Z-index layering to minimize repaints (intro: 10, text: 20, muse/comet: 30+)
- Centralized `SCROLL_TIMING` constants prevent cascading changes
- WebGL context reuse across multiple canvases
- Big bang pulse effect uses single uniform (no DOM manipulation)

### Known Limitations
- **Mobile WebGL**: 4+ active canvases can drain battery on extended viewing
- **Low-end devices**: May drop below 30fps during starfield + gradient overlap
- **Safari**: Occasional `backdrop-filter` glitch on rapid scroll (slider nav)
- **Chrome DevTools**: Open reduces WebGL performance by ~30%
- **Touch devices**: Bouncing logo drag may conflict with scroll on some browsers
- **Total scroll height**: ~2050vh (Intro: 400 + Text: 350 + Muse: 300 + Comet: 400 + natural page end with footer)

## Development Workflow

**Before commits:**
1. Test across browsers (Chrome, Firefox, Safari)
2. Validate responsive design (mobile → desktop)
3. Check Lighthouse performance (target 95+)
4. Validate HTML (W3C validator)
5. Test keyboard navigation
6. Verify `prefers-reduced-motion` behavior

**Testing:**
- Manual cross-browser testing
- Performance profiling (DevTools)
- Accessibility audit (axe DevTools)
- Visual regression for design changes

## Key Files
- `index.html` - Main entry point with semantic HTML
- `css/styles.css` - Complete styling with custom properties
- `js/main.js` - Animation logic and GSAP integration
- `tools/coordinate-picker.html` - Dev tool for constellation positioning
- `README.md` - User-facing documentation
- `CLAUDE.md` - This file (project context)

## Development Tools

**Coordinate Picker** (`tools/coordinate-picker.html`)
- Interactive tool for positioning constellation dots
- Click to save coordinates
- Exports as normalized (0-1) values
- Keyboard shortcuts: Z (undo), C (clear)

## Dependencies

External CDN libraries:
- GSAP 3.12.5 (`gsap.min.js`)
- ScrollTrigger plugin (`ScrollTrigger.min.js`)
- MotionPathPlugin (`MotionPathPlugin.min.js`)

## Always/Never

**Always:**
- Mobile-first responsive design
- Profile performance before optimizing
- Test in real devices when possible
- Use semantic HTML over divs
- Add `aria-hidden="true"` to decorative elements
- Use hardware-accelerated properties (`transform`, `opacity`)
- Debounce resize/scroll handlers
- Validate with Lighthouse before deploying

**Never:**
- Add frameworks for simple interactions
- Sacrifice accessibility for aesthetics
- Hardcode breakpoints without testing
- Use animations without `prefers-reduced-motion` support
- Deploy without Lighthouse audit
- Use `!important` (except for reduced motion override)
- Ignore keyboard navigation
- Add unused code or dependencies

## Current State (February 2026)

**Implemented:**
- ✅ Intro animation with orbiting dots, logo rotation, constellation explosion
- ✅ Big bang pulse effect (subtle dispersive wave from center)
- ✅ WebGL starfield background with twinkling stars (intro + unified)
- ✅ Constellation with z-depth rendering and scroll-driven rotation
- ✅ Scroll-driven mission text reveal with 3 sequential word highlights
- ✅ Muse intro page with white inverted logo + crossfade transition
- ✅ Orbiting muse layout with continuous 240s rotation (horizontal ellipse)
- ✅ Interactive popup modals for muse details (click image or title)
- ✅ WebGL animated gradient background for muse section
- ✅ Comet intro page with descending logo animation
- ✅ Comet slider with 5 phases (image + text reels)
- ✅ Bouncing DVD-style logo with colored spark particles
- ✅ Drag-and-throw bouncing logo interaction
- ✅ Orbital slider navigation (prev/next buttons + dots)
- ✅ Social links footer with hover/focus states (revealed at end)
- ✅ Semantic HTML5 structure with ARIA labels
- ✅ `prefers-reduced-motion` support (disables animations + sparks)
- ✅ Keyboard navigation (Tab, Escape, Arrow keys)
- ✅ Responsive design (mobile to 4K)

**Performance Notes:**
- WebGL fallback: Background animations disabled if WebGL unavailable
- GSAP ScrollTrigger handles all scroll events (no manual scroll listeners)
- Debounced resize handler: 150ms delay for performance
- Passive event listeners on window resize
- Hardware acceleration on all animated elements (`will-change`)
- Z-index layering for proper stacking context (intro: 10, text: 20, muse/comet: 30+)
- Shared GLSL shaders reduce code duplication
- Centralized timing constants (`SCROLL_TIMING`) for easy adjustments

**Key Interactive Features:**
- Click muse images or titles to open detailed popup modals
- Drag bouncing logo to throw it around (desktop + touch)
- Use arrow keys to navigate comet slider phases
- Press Escape to close muse popup modal
- Slider dots are clickable for direct phase navigation

---

**Document Version**: February 2026 | **Word count**: ~2500 words
