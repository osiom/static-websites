# cocoex.xyz Website

## Project Overview
Static portfolio website for cocoex e.V. - a vibrant DAO blending art, blockchain, community and social impact. Core values: **usability**, **design**, **minimalism**.

## Site Architecture

### Section 1: Landing/Intro (`.intro`)
**Scroll Range:** 0-400vh
**Positioning:** Fixed, overlays content
**Animation Phases:**
- **Phase 1 (0-40%)**: Orbiting dots convergence with logo rotation
- **Phase 2 (30.4-50%)**: Transition text "art as infrastructure for change" (appears at 76% orbit progress)
- **Phase 3 (50-100%)**: Constellation explosion into 7 colored dots with z-depth rendering

**Key Features:**
- WebGL starfield background (twinkling stars + simplex noise)
- Orbiting dots (white/black) converge to center
- Logo scales from 80px to 250px with 2 full rotations
- Transition text appears below logo at 76% orbit progress, fades out before explosion
- Big bang pulse effect at explosion start (dispersive wave)
- 7 constellation dots with depth layering (-0.5 to 0.6 range)

### Section 2: Mission Text (`.text-section-wrapper`)
**Scroll Range:** 400-550vh
**Positioning:** Sticky, full viewport height
**Animation Timing:** Centralized via `SCROLL_TIMING` constants

**Key Features:**
- Simple fade-in reveal (opacity 0 → 1)
- Simplified from 350vh to 150vh scroll height
- No word highlighting (removed for smoother scroll experience)
- Italic words remain styled but static (community, art, impactful)
- GSAP-driven scroll interpolation with `scrub: true` for 60fps smoothness

### Section 3: Muse Portfolio (`.muse-section-wrapper`)
**Scroll Range:** 550-730vh (180vh total)
**Positioning:** Sticky content with crossfade overlay intro

**Scroll Breakdown:**
- **0-100vh**: Intro page hold (white inverted logo + description)
- **100-180vh**: Crossfade to orbiting content (80vh transition)

**Key Features:**
- Intro fades in when section enters viewport (80% → 40%)
- Crossfade smoothly transitions intro to orbiting layout
- 7 muses orbit in horizontal ellipse (240s continuous rotation)
- Click image/title to open modal with colored aura effects
- WebGL animated gradient (muse colors blending with white/black)
- Unified starfield canvas beneath gradient (shared with Comet)
- Modal uses GSAP animations with floating particles

### Section 4: Comet Collab (`.comet-collab-wrapper`)
**Scroll Range:** 730-1580vh (850vh total)
**Positioning:** Sticky slider with scroll-driven phase changes

**Scroll Breakdown:**
- **0-80vh**: Intro hold (white logo + description static)
- **80-380vh**: Logo descends to bottom, text moves up (300vh movement)
- **380-500vh**: Crossfade intro to slider (120vh transition)
- **500-850vh**: Scroll-driven phase changes (5 phases × 70vh each)
- **850vh+**: Natural page end with footer reveal

**Key Features:**
- Intro fades in when section enters viewport (80% → 40%)
- Logo animation reverses correctly when scrolling up
- Bouncing DVD-style logo (velocity: 2px/1.5px) with drag support
- Colored spark particles on bounce (12 particles, varying sizes)
- Scroll-driven phase transitions with particle bursts
- Manual navigation via arrows, dots, or number keys (1-5)
- Parallax effect between image and text reels
- WebGL gradient background (identical shader to Muse)

### Footer
**Positioning:** Fixed, revealed at comet section end
**Trigger:** `comet-collab-section bottom-=20% bottom`

**Contents:**
- Social links: Telegram, Instagram, LinkedIn (52px touch targets)
- Cocoex text logo (172px width)
- Hover states with scale transform

## DOM Reference Guide

### Communication Best Practices

When requesting changes, combine **visual description + DOM selector** for precision.

**Identification Methods:**
- CSS selectors: `.intro`, `.text-section-wrapper`, `.muse-section-wrapper`, `.comet-collab-wrapper`
- Canvas IDs: `#bg-canvas`, `#constellation-canvas`, `#unified-starfield-canvas`, `#muse-background-canvas`, `#comet-collab-background-canvas`
- Component IDs: `#muse-section`, `#comet-collab-section`, `#comet-collab-bouncing-logo`
- ARIA labels: `aria-label="Muse portfolio"`, `aria-label="Comet collab phases showcase"`

**Examples:**
```
❌ Poor:  "The icons at the bottom"
✅ Good:  "The footer with Instagram, Telegram, LinkedIn icons"
✅ Best:  "The .social-links footer (styles.css:1029)"
```

### Quick Reference Table

| Element | Selector | Module | Line References |
|---------|----------|--------|-----------------|
| Intro starfield | `#bg-canvas` | Main render loop | main.js:270-386 |
| Orbiting dots | `.orbit-dot-white`, `.orbit-dot-black` | updateOrbitPositions | main.js:1083-1142 |
| Logo rotation | `#intro-logo` | GSAP orbitState | main.js:772-793 |
| Transition text | `#transition-text` | GSAP timeline | main.js:891-913 |
| Constellation explosion | `#constellation-canvas` | updateFireworkDots | main.js:449-491, 518-664 |
| Big bang pulse | `u_pulse` uniform | Intro shader | main.js:287, 313-338 |
| Text reveal | `.reveal-text` | GSAP fade-in | main.js:936-951 |
| Muse intro page | `.muse-intro-page` | GSAP ScrollTrigger | main.js:914-976 |
| Muse gradient | `#muse-background-canvas` | MuseBackground | main.js:1148-1289 |
| Unified starfield | `#unified-starfield-canvas` | UnifiedStarfield | main.js:1294-1384 |
| Orbiting muses | `.muse-orbit-item` | MuseScroll | main.js:1724-1839 |
| Muse popup | `.muse-popup` | MusePopup | main.js:1521-1719 |
| Comet intro | `.comet-collab-intro` | GSAP ScrollTrigger | main.js:979-1078 |
| Comet slider | `.comet-collab-section` | CometCollabSlider | main.js:1844-2419 |
| Bouncing logo | `#comet-collab-bouncing-logo` | CometCollabSlider.updateLogoPosition | main.js:2188-2240 |
| Comet gradient | `#comet-collab-background-canvas` | CometCollabBackground | main.js:1389-1516 |
| Footer reveal | `.social-links`, `.footer-logo` | GSAP ScrollTrigger | main.js:894-911 |

### CSS Organization (styles.css)

| Lines | Section | Key Classes |
|-------|---------|-------------|
| 1-77 | CSS Variables | `:root`, font/color/spacing definitions |
| 79-137 | Reset & Base | `*, html, body`, `prefers-reduced-motion` |
| 139-180 | Intro Section | `.intro`, `.intro-canvas`, `.intro-content` |
| 182-257 | Logo & Dots | `.logo-container`, `.orbit-dot`, `.final-dot` |
| 259-285 | Final Dot | `.final-dot` (merged state) |
| 287-313 | Transition Text | `.transition-text` (appears at 76% orbit) |
| 315-326 | Constellation Canvas | `.constellation-canvas` |
| 329-339 | Unified Starfield | `.unified-starfield-canvas` |
| 342-380 | Text Section | `.text-section-wrapper`, `.reveal-text` (simplified) |
| 363-377 | White Section | `.white-section` (container) |
| 379-892 | Comet Collab | Wrapper, intro, slider, navigation, bouncing logo, sparks |
| 1026-1091 | Footer | `.social-links`, `.footer-logo` |
| 1093-1166 | Muse Wrapper | `.muse-section-wrapper`, intro page, sticky content |
| 1169-1283 | Muse Orbiting | `.muse-orbit-container`, orbit items, center logo |
| 1285-1466 | Muse Popup | `.muse-popup`, modal content, particles, aura effects |
| 1468-1683 | Responsive | Tablet (1024px), Mobile (768px), Small (480px), Large (1440px+) |
| 1686-1728 | Utilities | `.visually-hidden`, print styles |

### JavaScript Module Reference (main.js)

| Lines | Module | Purpose | Key Properties |
|-------|--------|---------|----------------|
| 16-85 | GLSL_UTILS | Shared shader code | SIMPLEX_NOISE, STAR_FIELD |
| 88-117 | SCROLL_TIMING | Centralized timing | All section scroll ranges |
| 119-190 | CONFIG + DATA | Constants & coordinates | DOT_COLORS, CONSTELLATION_REF |
| 194-225 | DOM + STATE | Element refs & state vars | pulseValue, constellationRotation |
| 270-386 | WebGL Intro | Starfield + pulse shader | Twinkling stars, big bang effect |
| 408-664 | Constellation | Explosion animation | Z-depth rendering, rotation |
| 667-727 | Master Render Loop | Consolidated animation | Renders all WebGL canvases |
| 732-1078 | GSAP Animations | Scroll-driven timelines | All section transitions |
| 1083-1142 | updateOrbitPositions | Phase 1 orbit logic | GSAP-driven positioning |
| 1148-1289 | MuseBackground | Gradient shader module | 7-color animated blend |
| 1294-1384 | UnifiedStarfield | Shared starfield canvas | Muse + Comet background |
| 1389-1516 | CometCollabBackground | Gradient shader (reused) | Identical to MuseBackground |
| 1521-1719 | MusePopup | Modal with particles | GSAP animations, aura effects |
| 1724-1839 | MuseScroll | Orbiting layout | 240s rotation, ellipse math |
| 1844-2419 | CometCollabSlider | Interactive slider | Bouncing logo, drag, phases |

### Adjustment Examples

**Scroll Timing Adjustments:**
```javascript
// All timing centralized in SCROLL_TIMING (main.js:88-117)
SCROLL_TIMING.MUSE_INTRO_HOLD      // Change muse intro hold duration
SCROLL_TIMING.MUSE_CROSSFADE        // Adjust crossfade transition length
SCROLL_TIMING.COMET_INTRO_PAUSE     // Modify comet intro pause
SCROLL_TIMING.COMET_LOGO_MOVEMENT   // Change logo descent duration
SCROLL_TIMING.COMET_PHASE_DURATION  // Adjust phase scroll speed
```

**Animation Speed Changes:**
```javascript
MuseScroll.orbitSpeed = 0.00015;    // Muse rotation speed (240s per cycle)
CometCollabSlider.logoVelocityX = 2; // Bouncing logo horizontal speed
CometCollabSlider.logoVelocityY = 1.5; // Bouncing logo vertical speed
```

**Color Adjustments:**
```javascript
DOT_COLORS                          // Constellation colors (main.js:158-166)
MuseBackground.colors               // Muse gradient palette (main.js:1154-1162)
CometCollabSlider.museColors        // Spark particle colors (main.js:1875-1883)
```

**Layout Changes:**
```css
.social-links { bottom: calc(...); }  /* Footer positioning (styles.css:1031) */
:root { --font-h1-size: 36px; }       /* Typography scale (styles.css:52-58) */
.muse-orbit-item .muse-image { width: 140px; } /* Muse image size (styles.css:1239) */
```

## Tech Stack

**Core:**
- Vanilla HTML5/CSS3/ES6+ JavaScript (no frameworks)
- GSAP 3.12.5 (ScrollTrigger + MotionPathPlugin)
- WebGL (custom shaders: starfield, gradient, pulse effects)
- Adobe Fonts: Canela (Bold 700, Regular 400)

**Architecture:**
- IIFE module pattern with namespace isolation
- Master render loop (consolidates all WebGL animations)
- Centralized timing constants (`SCROLL_TIMING`)
- Shared GLSL utilities (simplex noise, starfield)
- Passive event listeners + debounced resize (150ms)

**Files:**
- `index.html` - Semantic HTML5 structure
- `css/styles.css` - CSS custom properties, responsive design
- `js/main.js` - Main animation logic (~2500 lines)
- `tools/coordinate-picker.html` - Dev tool for constellation positioning

## Typography System

**Font:** Canela (Adobe Fonts via Typekit: `nvc8nhy.css`)
**Fallback:** Georgia, serif

**Type Scale (CSS Custom Properties):**

| Level | Weight | Default Size | Line Height | Usage |
|-------|--------|--------------|-------------|-------|
| H1 | 700 (Bold) | 36px | 38px | Mission text, phase titles, popup titles |
| H2 | 400 (Regular) | 18px | 21px | Descriptions, muse names, body text |

**Responsive Breakpoints:**

| Screen Size | H1 Size/Height | H2 Size/Height |
|-------------|----------------|----------------|
| Desktop (default) | 36px / 38px | 18px / 21px |
| Tablet (≤1024px) | 30px / 33px | 16px / 19px |
| Mobile (≤768px) | 22px / 26px | 14px / 17px |
| Small (≤480px) | 18px / 22px | 12px / 15px |
| Large (≥1440px) | 42px / 46px | 20px / 24px |
| XL (≥1920px) | 48px / 52px | 22px / 26px |

All typography scales via CSS custom properties in media queries (styles.css:42-77, 1472-1683).

## Design Principles

**Minimalism** - Question every element. White space is a feature. Less code = faster load.

**Fluid Performance:**
- 60fps scroll animations via GSAP `scrub: true`
- Hardware-accelerated properties (`transform`, `opacity` only)
- `will-change` hints on animated elements
- Debounced resize: 150ms
- Touch targets: min 44px (52px social icons)
- Responsive breakpoints: 480, 768, 1024, 1440, 1920px

**Performance Targets:**
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Cumulative Layout Shift: <0.1
- Lighthouse score: 95+

**Accessibility:**
- Semantic HTML5 (`<section>`, `<article>`, `<footer>`)
- ARIA labels on decorative/interactive elements
- Keyboard nav: Tab, Escape, Arrow keys, Number keys (1-5)
- Focus visible styles (2px outline + 2px offset)
- WCAG AA color contrast minimum
- `prefers-reduced-motion` disables animations + particles
- Screen reader friendly (decorative elements `aria-hidden="true"`)

## Code Standards

**CSS Best Practices:**
- CSS custom properties in `:root` for theming/typography
- Mobile-first responsive design (min-width media queries)
- Section-based organization with header comments
- Avoid `!important` (exceptions: `prefers-reduced-motion` override, CSS specificity conflicts)
- Hardware acceleration via `transform`/`opacity`
- Thin scrollbar styling (6px width, subtle white)
- Use `window.getComputedStyle()` to debug style application issues

**JavaScript Best Practices:**
- IIFE pattern for global scope isolation
- Module structure: CONSTANTS → DOM → STATE → UTILS → MODULES → INIT
- Centralized timing via `SCROLL_TIMING` object
- Shared GLSL code via `GLSL_UTILS` object
- Debounced resize (150ms), passive event listeners
- Master render loop consolidates all animations
- WebGL fallback handling (console warnings)

**HTML Best Practices:**
- Semantic HTML5 elements (avoid div soup)
- W3C valid markup
- SEO: meta description, Open Graph, Twitter cards
- External links: `rel="noopener noreferrer"`
- Images: descriptive `alt` text
- Decorative elements: `aria-hidden="true"`

## File Structure

**CSS Organization (styles.css):**
1. Scrollbar styling (Firefox + Webkit)
2. CSS Custom Properties (`:root`)
3. Reset & Base Styles
4. Intro Section (fixed canvas + content)
5. Logo, Orbiting Dots, Final Dot
6. Constellation Canvas
7. Unified Starfield (Muse + Comet background)
8. Text Section (sticky with highlights)
9. White Section Container
10. Comet Collab (wrapper, intro, slider, nav, bouncing logo, sparks)
11. Social Links & Footer
12. Muse Section (wrapper, intro page, sticky content)
13. Muse Orbiting Layout
14. Muse Popup Modal
15. Responsive Media Queries (tablet → mobile → small → large)
16. Utility Classes & Print Styles

**JavaScript Organization (main.js):**
1. IIFE Wrapper + GSAP Plugin Registration
2. GLSL_UTILS (shared shader code)
3. SCROLL_TIMING (centralized timing constants)
4. CONFIG (layout/animation constants)
5. DOT_COLORS + CONSTELLATION_REF (data)
6. DOM Element References
7. State Variables
8. Utility Functions (isMobile, easing, debounce)
9. WebGL Background Shader (intro starfield + pulse)
10. Resize Handler
11. Firework/Constellation Logic
12. Master Render Loop (consolidated animations)
13. Event Listeners
14. GSAP ScrollTrigger Animations (all sections)
15. updateOrbitPositions (phase 1 logic)
16. MuseBackground Module (WebGL gradient)
17. UnifiedStarfield Module (shared starfield)
18. CometCollabBackground Module (gradient shader reuse)
19. MusePopup Module (modal interactions)
20. MuseScroll Module (orbiting layout)
21. CometCollabSlider Module (bouncing logo + phases)
22. Initialization

## Performance Profile

**Bundle Sizes:**
- HTML: 10.2KB (~3.5KB gzipped)
- CSS: 21.4KB (~5.2KB gzipped)
- JavaScript: 37.8KB (~11.3KB gzipped)
- **Total Core**: 69.4KB (~20KB gzipped)
- GSAP CDN: 47KB (cached)

**WebGL Resources:**
- Active canvases: 4 simultaneous (intro, unified starfield, muse gradient, comet gradient)
- Shader programs: 4 compiled (shared code reduces duplication by ~150 lines)
- Memory: ~50-70MB (viewport-dependent)
- GPU layers: 15-25 composited (hardware accelerated)

**Animation Performance:**
- Master render loop: 1 consolidated `requestAnimationFrame`
- Target FPS: 60fps desktop, 30fps mobile
- Scroll: GSAP ScrollTrigger (`scrub: true` for smooth 60fps interpolation)
- Resize: Debounced to 150ms, passive listeners
- Total scroll height: ~1580vh (Intro: 400 + Text: 150 + Muse: 180 + Comet: 850)

**Optimization Strategies:**
- Hardware-accelerated properties only (`transform`, `opacity`)
- GSAP replaces manual scroll listeners
- Shared GLSL utilities (simplex noise, star field)
- Muse/Comet gradient shaders identical (code reuse)
- `will-change` hints on animated elements
- Z-index layering minimizes repaints (intro: 10, text: 20, white: 30)
- Centralized `SCROLL_TIMING` prevents cascading changes
- Big bang pulse uses single WebGL uniform (no DOM manipulation)

**Known Limitations:**
- Mobile: 4+ WebGL canvases drain battery on extended viewing
- Low-end devices: May drop below 30fps during gradient + starfield overlap
- Safari: Rare `backdrop-filter` glitch on rapid scroll (slider nav)
- Chrome DevTools open: ~30% WebGL performance reduction
- Touch devices: Bouncing logo drag may conflict with scroll

## Development & Testing

**Pre-Commit Checklist:**
1. Cross-browser test (Chrome, Firefox, Safari)
2. Responsive validation (320px → 1920px+)
3. Lighthouse audit (target 95+ score)
4. HTML validation (W3C validator)
5. Keyboard navigation test (Tab, Escape, Arrows, Numbers)
6. `prefers-reduced-motion` verification

**Testing Tools:**
- Chrome DevTools (performance profiling, network analysis)
- Lighthouse (performance, accessibility, SEO)
- axe DevTools (accessibility audit)
- W3C HTML Validator
- BrowserStack/LambdaTest (cross-browser)

**Key Files:**
- `index.html` - Semantic HTML5 structure (327 lines)
- `css/styles.css` - Styling with custom properties (1729 lines)
- `js/main.js` - GSAP + WebGL animation logic (2513 lines)
- `tools/coordinate-picker.html` - Constellation positioning tool
- `README.md` - User-facing documentation
- `CLAUDE.md` - Project context (this file)

## Development Tools

**Coordinate Picker** (`tools/coordinate-picker.html`)
- Interactive tool for positioning constellation dots
- Click to save coordinates, exports as normalized (0-1) values
- Keyboard shortcuts: Z (undo), C (clear)

## Dependencies

**External CDN (GSAP 3.12.5):**
- `gsap.min.js` - Core animation library
- `ScrollTrigger.min.js` - Scroll-driven animations
- `MotionPathPlugin.min.js` - Motion path utilities (registered but unused)

**Adobe Fonts:**
- Typekit ID: `nvc8nhy` - Canela font family

## Debugging & Troubleshooting

### Common Issues and Solutions

#### Canvas Animation Flickering
**Symptoms:** Canvas-drawn elements flicker during transformations or rotations.

**Root Cause:** Double transformation - applying both manual coordinate rotation in JavaScript AND CSS transform on the canvas element.

**Solution:**
```javascript
// ❌ BAD: Manual rotation + CSS transform = double transformation
const rotatedX = Math.cos(angle + rotation) * radius;
const rotatedY = Math.sin(angle + rotation) * radius;
// Canvas also has CSS: transform: rotate(15deg)

// ✅ GOOD: Store unrotated positions, let CSS handle rotation
dot.x = Math.cos(angle) * radius;
dot.y = Math.sin(angle) * radius;
// CSS transform: rotate(15deg) handles all rotation
```

**Additional Fix:** Always use `constCtx.save()` and `constCtx.restore()` to ensure clean canvas state between frames.

#### CSS Styles Not Applying
**Symptoms:** JavaScript correctly adds CSS classes (verified via `classList.contains()`), but visual styles don't appear. `window.getComputedStyle()` shows wrong color values.

**Root Cause:** CSS specificity conflicts where parent styles override child element styles.

**Debugging Steps:**
1. Verify class is added: `element.classList.contains('classname')`
2. Check computed styles: `window.getComputedStyle(element).color`
3. Inspect CSS cascade in DevTools
4. Check parent element styles for conflicts

**Solution:**
```css
/* ❌ BAD: Child styles can be overridden by parent */
.parent { color: white; }
.parent .child { color: black; } /* May not work */

/* ✅ GOOD: Use !important for guaranteed override */
.parent .child { color: black !important; }
```

**When to use `!important`:**
- CSS specificity conflicts where architectural refactoring isn't practical
- Overriding third-party library styles
- `prefers-reduced-motion` overrides (always use `!important` here)
- Utility classes that must always apply

**Example from this project:**
```css
/* Used in prefers-reduced-motion to override all animations */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

#### Scroll Position Reads as 0
**Symptoms:** Debug logs show `[0.00vh | 0.0% | 0px]` even when user is scrolling.

**Root Cause:** Different browsers use different properties for scroll position. Single source may not be supported.

**Solution:** Use multiple fallback sources with OR operator:
```javascript
const scrollY = window.scrollY ||
                window.pageYOffset ||
                document.documentElement.scrollTop ||
                document.body.scrollTop || 0;

const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
const scrollHeight = Math.max(
  document.documentElement.scrollHeight,
  document.body.scrollHeight
);
```

**Debug Logging Pattern:**
```javascript
// Log first 3 scroll events to diagnose which property works
let scrollEventCount = 0;
window.addEventListener('scroll', () => {
  scrollEventCount++;
  if (scrollEventCount <= 3) {
    console.log(`DEBUG: Scroll event #${scrollEventCount}`, {
      'window.scrollY': window.scrollY,
      'window.pageYOffset': window.pageYOffset,
      'docElement.scrollTop': document.documentElement.scrollTop,
      'body.scrollTop': document.body.scrollTop
    });
  }
}, { passive: true });
```

#### WebGL Performance Degradation
**Symptoms:** Frame rate drops when multiple WebGL canvases are active. GPU usage spikes.

**Root Cause:** Redundant `gl.useProgram()` calls causing expensive GPU state changes every frame.

**Solution:** Cache the last active program and only switch when necessary:
```javascript
let lastActiveProgram = null;

function masterRender() {
  // Render intro background
  if (gl && program) {
    if (lastActiveProgram !== program) {
      gl.useProgram(program);
      gl.enableVertexAttribArray(posAttr);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.vertexAttribPointer(posAttr, 2, gl.FLOAT, false, 0, 0);
      lastActiveProgram = program;
    }
    // Update uniforms and draw
    gl.uniform2f(resUniform, canvas.width, canvas.height);
    gl.uniform1f(timeUniform, time);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  // Render muse background
  if (MuseBackground.gl && MuseBackground.program) {
    if (lastActiveProgram !== MuseBackground.program) {
      MuseBackground.gl.useProgram(MuseBackground.program);
      lastActiveProgram = MuseBackground.program;
    }
    // Update uniforms and draw
  }
}
```

**Mobile Optimization:** Cap Device Pixel Ratio to reduce pixel count:
```javascript
const baseDPR = window.devicePixelRatio || 1;
const dpr = isMobile() ? Math.min(baseDPR, 2) : baseDPR;
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;
```
This reduces pixel count by 33% on 3x DPR devices (e.g., iPhone 13 Pro) without noticeable quality loss.

#### GSAP ScrollTrigger Animations Too Fast/Jerky
**Symptoms:** Scroll-driven animations feel rushed, skip frames, or don't interpolate smoothly.

**Root Cause:** Scroll distances are too short for GSAP to interpolate at 60fps. Not enough frames between keyframes.

**Solution:** Increase scroll duration values in `SCROLL_TIMING`:
```javascript
// ❌ BAD: Too short for smooth 60fps interpolation
COMET_PHASE_DURATION: 50  // vh per phase

// ✅ GOOD: 2x longer allows smooth interpolation
COMET_PHASE_DURATION: 100  // vh per phase
```

**General Rule:** For smooth 60fps at typical scroll speed (1-2 vh/frame), each animation phase should span at least 2-3vh. Complex animations need 4-5vh minimum.

**Scroll Timing Changes Applied:**
- Word highlights: **REMOVED** (simplified text section from 350vh → 150vh for smoother scroll)
- Muse crossfade: 100 → 120 vh (+20%)
- Comet logo movement: 250 → 280 vh (+12%)
- Comet phase duration: 80 → 100 vh (+25%)

### Debugging Techniques

#### 1. Cross-Browser Scroll Position Debugging
Always test scroll position reading with multiple sources:
```javascript
const log = (msg) => {
  const scrollY = window.scrollY || window.pageYOffset ||
                  document.documentElement.scrollTop ||
                  document.body.scrollTop || 0;
  const vh = (scrollY / window.innerHeight).toFixed(2);
  console.log(`[${vh}vh | ${scrollY}px] ${msg}`);
};
```

#### 2. CSS Computed Style Inspection
When styles don't apply as expected:
```javascript
const activeWord = document.querySelector('.highlight-active');
const computed = window.getComputedStyle(activeWord);
console.log({
  hasClass: activeWord.classList.contains('highlight-active'),
  computedColor: computed.color,
  computedStroke: computed.webkitTextStroke,
  computedShadow: computed.textShadow
});
```

#### 3. GSAP Timeline Progress Monitoring
Debug scroll-triggered animations:
```javascript
highlightTimeline.eventCallback('onUpdate', function() {
  const progress = highlightTimeline.progress();
  console.log(`Timeline progress: ${(progress * 100).toFixed(1)}%`);

  // Check which elements are active
  const activeElements = document.querySelectorAll('.highlight-active');
  console.log(`Active elements: ${activeElements.length}`, activeElements);
});
```

#### 4. WebGL State Debugging
Track WebGL program switches to identify performance issues:
```javascript
let programSwitchCount = 0;
function masterRender() {
  if (lastActiveProgram !== program) {
    programSwitchCount++;
    console.log(`Program switch #${programSwitchCount}`);
    gl.useProgram(program);
    lastActiveProgram = program;
  }
}
// Excessive switches (>10 per second) indicate optimization opportunity
```

#### 5. Canvas State Verification
Always save/restore canvas context to prevent state leaks:
```javascript
function drawAnimation(ctx) {
  ctx.save(); // Save current state

  // Your drawing code here
  ctx.clearRect(0, 0, width, height);
  ctx.globalAlpha = 0.5;
  ctx.fillStyle = 'red';
  // ... more drawing

  ctx.restore(); // Restore to clean state
}
```

### Performance Profiling Workflow

**Before Optimizing:**
1. Open Chrome DevTools Performance tab
2. Record 10 seconds of scrolling through problematic section
3. Analyze:
   - Frame rate (target: 60fps desktop, 30fps mobile)
   - Long tasks (target: <50ms)
   - GPU memory usage
   - Paint/composite operations

**Optimization Priorities:**
1. **Eliminate redundant work** (e.g., cached WebGL programs)
2. **Reduce pixel count** (e.g., DPR capping on mobile)
3. **Increase scroll distances** (e.g., longer GSAP durations)
4. **Hardware acceleration** (e.g., `transform` over `left/top`)

**After Optimizing:**
1. Re-record same 10-second segment
2. Compare metrics to baseline
3. Verify visual quality unchanged
4. Test on low-end device (iPhone SE, mid-range Android)

### Development Environment Setup

**Required Browser Extensions:**
- Chrome DevTools (built-in)
- React Developer Tools (if using React - not applicable here)
- axe DevTools (accessibility testing)

**Recommended VS Code Extensions:**
- Live Server (real-time preview)
- ESLint (code quality)
- Prettier (formatting)
- GLSL Lint (shader validation)

**Local Server:**
```bash
# Python (recommended for static sites)
python3 -m http.server 8000

# Node.js alternative
npx serve . -l 8000
```

**Hard Refresh for CSS Changes:**
- Mac: `Cmd + Shift + R`
- Windows/Linux: `Ctrl + Shift + R`
- Always hard refresh after CSS changes to clear browser cache

## Best Practices

**Always:**
- Mobile-first responsive design
- Profile before optimizing (Chrome DevTools Performance tab)
- Test on real devices when possible
- Use semantic HTML over divs
- Validate with Lighthouse before deploying (target 95+)
- Hardware-accelerated properties only (`transform`, `opacity`)
- Debounce resize/scroll handlers (150ms minimum)
- Add `aria-hidden="true"` to decorative elements
- Support `prefers-reduced-motion`
- Test keyboard navigation
- Use `ctx.save()`/`ctx.restore()` for canvas operations
- Multiple fallback sources for scroll position
- Cache WebGL program state to minimize GPU switches

**Never:**
- Add frameworks for simple interactions
- Sacrifice accessibility for aesthetics
- Hardcode values that should be in `SCROLL_TIMING`
- Use animations without reduced motion support
- Deploy without Lighthouse audit
- Use `!important` habitually (exceptions: specificity conflicts, reduced motion overrides)
- Ignore keyboard navigation
- Commit unused code
- Apply both manual rotation and CSS transform (double transformation)
- Assume single scroll position source works cross-browser

## Implementation Status

**Current Features (March 2026):**
- ✅ Intro: Orbiting dots, logo rotation, constellation explosion with z-depth
- ✅ Transition text "art as infrastructure for change" (appears at 76% orbit progress)
- ✅ Big bang pulse effect (dispersive wave from center)
- ✅ WebGL starfield backgrounds (intro + unified for Muse/Comet)
- ✅ Simplified text reveal (fade-in only, no word highlighting)
- ✅ Muse intro page with white inverted logo + 80vh crossfade
- ✅ Orbiting muse layout (240s continuous rotation, horizontal ellipse)
- ✅ Interactive muse popup modals (click image/title, colored aura, particles)
- ✅ WebGL animated gradient (Muse/Comet sections)
- ✅ Comet intro page with descending logo (300vh animation)
- ✅ Comet slider with 5 scroll-driven phases (70vh per phase)
- ✅ Bouncing DVD-style logo (drag support, colored sparks, 12 particles)
- ✅ Orbital slider navigation (prev/next buttons, dots, keyboard: arrows + 1-5)
- ✅ Footer reveal at page end (social icons + logo)
- ✅ Full keyboard navigation support
- ✅ `prefers-reduced-motion` disables animations + particles
- ✅ Responsive design (320px → 1920px+)

**Performance:**
- Master render loop consolidates all animations
- GSAP ScrollTrigger handles all scroll (no manual listeners)
- Debounced resize: 150ms
- Hardware acceleration: `will-change` hints
- Shared GLSL code reduces duplication
- Z-index layering minimizes repaints

---

**Last Updated:** March 9, 2026 - Added comprehensive "Debugging & Troubleshooting" section with lessons learned from performance optimization session
