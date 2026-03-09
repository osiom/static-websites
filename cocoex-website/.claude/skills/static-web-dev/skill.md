---
name: static-web-dev
description: Static website development with Vanilla JS, GSAP, and WebGL. Focuses on animation patterns, scroll-driven interactions, WebGL shaders, and performance optimization for modern static sites. Use when working on animations, scroll effects, WebGL graphics, or optimizing static website performance.
---

# Static Web Development

Specialized skill for building high-performance static websites with advanced animations and WebGL effects using vanilla JavaScript.

## Core Capabilities

This skill helps with:

1. **GSAP Scroll Animations** - ScrollTrigger patterns, timeline orchestration, timing coordination
2. **WebGL Shader Development** - Custom shaders, performance optimization, multi-canvas management
3. **Performance Optimization** - Bundle analysis, animation profiling, accessibility best practices
4. **Static Site Patterns** - Vanilla JS architecture, CSS custom properties, responsive design
5. **Code Cleanup & Optimization** - Remove unused code, consolidate duplicates, optimize performance WITHOUT changing working behavior

## Quick Reference

### GSAP ScrollTrigger Patterns

**Basic Scroll Animation:**
```javascript
gsap.to(element, {
  opacity: 1,
  scrollTrigger: {
    trigger: element,
    start: 'top 80%',
    end: 'top 40%',
    scrub: true,
    invalidateOnRefresh: true
  }
});
```

**Crossfade Transition:**
```javascript
gsap.timeline({
  scrollTrigger: {
    trigger: wrapper,
    start: `top+=${startVh}vh top`,
    end: `top+=${endVh}vh top`,
    scrub: true
  }
})
.fromTo(oldElement, { opacity: 1 }, { opacity: 0 }, 0)
.fromTo(newElement, { opacity: 0 }, { opacity: 1 }, 0);
```

**Centralized Timing:**
```javascript
const SCROLL_TIMING = {
  INTRO_TOTAL: 400,        // vh
  TEXT_SECTION: 350,       // vh
  CROSSFADE_DURATION: 80   // vh
};

// Use in animations
start: `top+=${SCROLL_TIMING.INTRO_TOTAL}vh top`
```

### WebGL Shader Patterns

**Shared GLSL Utilities:**
```javascript
const GLSL_UTILS = {
  SIMPLEX_NOISE: `
    vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
    // ... noise function
  `,
  STAR_FIELD: `
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }
    // ... star rendering
  `
};

// Reuse in multiple shaders
const fragmentShader = `
  ${GLSL_UTILS.SIMPLEX_NOISE}
  ${GLSL_UTILS.STAR_FIELD}
  void main() { /* ... */ }
`;
```

**Master Render Loop:**
```javascript
function masterRender() {
  const time = (Date.now() - startTime) / 1000;

  // Render all WebGL canvases
  if (canvas1.gl && canvas1.program) {
    canvas1.gl.useProgram(canvas1.program);
    canvas1.gl.uniform1f(canvas1.timeUniform, time);
    canvas1.gl.drawArrays(canvas1.gl.TRIANGLES, 0, 6);
  }

  requestAnimationFrame(masterRender);
}
```

### Performance Patterns

**Hardware-Accelerated Animations:**
```javascript
// ✅ Good - GPU accelerated
gsap.to(element, {
  x: 100,           // transform: translateX
  y: 50,            // transform: translateY
  rotation: 45,     // transform: rotate
  scale: 1.2,       // transform: scale
  opacity: 0.5      // opacity
});

// ❌ Bad - triggers layout
gsap.to(element, {
  width: '100%',
  height: '500px',
  top: '50px',
  left: '20px'
});
```

**Debounced Resize:**
```javascript
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

const handleResize = debounce(() => {
  resize();
  ScrollTrigger.refresh();
}, 150);

window.addEventListener('resize', handleResize, { passive: true });
```

### Accessibility Patterns

**Reduced Motion Support:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }

  .animated-particles {
    display: none !important;
  }
}
```

**Keyboard Navigation:**
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
  if (e.key === 'ArrowLeft') previousSlide();
  if (e.key === 'ArrowRight') nextSlide();

  // Direct access with number keys
  const num = parseInt(e.key);
  if (num >= 1 && num <= 5) goToSlide(num - 1);
});
```

## Tech Stack

**Core Technologies:**
- Vanilla JavaScript (ES6+, IIFE pattern)
- GSAP 3.x (ScrollTrigger, MotionPathPlugin)
- WebGL (custom GLSL shaders)
- HTML5 (semantic structure)
- CSS3 (custom properties, responsive)

**External Dependencies:**
- GSAP CDN (47KB cached)
- Adobe Fonts / Google Fonts

**Development:**
- Local server: `python3 -m http.server 8000`
- Testing: Chrome DevTools, Lighthouse, axe DevTools

## Project Architecture

### File Structure
```
project/
├── index.html              # Semantic HTML5
├── css/
│   └── styles.css         # Custom properties, responsive
├── js/
│   └── main.js            # IIFE pattern, modules
├── assets/
│   ├── images/
│   └── fonts/
└── tools/
    └── coordinate-picker.html  # Dev tool
```

### JavaScript Organization
```
1. IIFE Wrapper
2. GSAP Plugin Registration
3. GLSL_UTILS (shared shader code)
4. SCROLL_TIMING (centralized constants)
5. CONFIG (layout/animation constants)
6. DOM Element References
7. State Variables
8. Utility Functions
9. WebGL Shader Setup
10. Master Render Loop
11. GSAP ScrollTrigger Animations
12. Module Definitions
13. Initialization
```

### CSS Organization
```
1. CSS Custom Properties (:root)
2. Reset & Base Styles
3. Section Styles (organized by page section)
4. Component Styles
5. Responsive Media Queries
6. Utility Classes
7. Print Styles
```

## Best Practices

**Always:**
- Use centralized timing constants (`SCROLL_TIMING`)
- Share GLSL code via utility objects
- Hardware-accelerated properties only
- Debounce resize handlers (150ms)
- Support `prefers-reduced-motion`
- Test keyboard navigation
- Validate with Lighthouse (target 95+)

**Never:**
- Animate layout properties (width, height, top, left)
- Use multiple scroll listeners (use GSAP only)
- Hardcode timing values (use constants)
- Forget `invalidateOnRefresh: true`
- Deploy without accessibility audit
- Ignore mobile performance

## Common Patterns

### Fade-In Section
```javascript
gsap.fromTo(element,
  { opacity: 0 },
  {
    opacity: 1,
    scrollTrigger: {
      trigger: element,
      start: 'top 80%',
      end: 'top 40%',
      scrub: true,
      invalidateOnRefresh: true
    }
  }
);
```

### Sequential Timeline
```javascript
const timeline = gsap.timeline({
  defaults: { ease: 'power3.out' }
});

timeline
  .from(el1, { y: 50, opacity: 0, duration: 0.5 })
  .from(el2, { y: 50, opacity: 0, duration: 0.5 }, '-=0.3')
  .from(el3, { y: 50, opacity: 0, duration: 0.5 }, '-=0.3');
```

### Responsive WebGL
```javascript
function resize() {
  const dpr = isMobile() ? 1 : window.devicePixelRatio || 1;
  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;

  if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
}
```

## Performance Targets

- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Cumulative Layout Shift: <0.1
- Lighthouse Score: 95+
- FPS: 60fps desktop, 30fps mobile

## Code Cleanup & Optimization Protocol

**CRITICAL RULE:** Never change working behavior. Only remove dead code, consolidate duplicates, and optimize performance.

### Pre-Cleanup Checklist

Before making ANY changes:
1. ✅ Verify feature is working correctly
2. ✅ Test on multiple devices/browsers
3. ✅ Document current behavior
4. ✅ Create backup (git commit recommended)

### Safe Cleanup Operations

#### 1. Remove Unused CSS Selectors

**Detection:**
```bash
# Find unused CSS classes
grep -r "class=\"[^\"]*\"" *.html | grep -o "class=\"[^\"]*\"" | sort -u
# Cross-reference with styles.css
```

**Safe to Remove:**
- ✅ Classes never referenced in HTML
- ✅ IDs never referenced in HTML or JS
- ✅ Commented-out styles
- ✅ Duplicate property declarations
- ✅ Unused @media queries that don't apply

**Never Remove:**
- ❌ Classes added dynamically via JS (`.visible`, `.active`, etc.)
- ❌ Pseudo-selectors (`:hover`, `:focus`, `:before`, `:after`)
- ❌ ARIA-related selectors
- ❌ Animation keyframes currently in use

**Example:**
```css
/* ❌ Remove - never used */
.old-header {
  color: red;
}

/* ✅ Keep - added by JavaScript */
.muse-popup.visible {
  opacity: 1;
}

/* ❌ Remove - duplicate */
.text-section {
  padding: 2rem;
  padding: var(--spacing-md); /* Duplicate - keep this one */
}
```

#### 2. Remove Unused JavaScript Functions

**Detection:**
```bash
# Find function declarations
grep -n "function \w\+\|const \w\+ = " main.js

# Cross-reference with usage
grep -n "functionName" main.js
```

**Safe to Remove:**
- ✅ Functions never called
- ✅ Commented-out code blocks
- ✅ Debug console.logs (but verify not used for production logging)
- ✅ Unused variables

**Never Remove:**
- ❌ Event handler functions (even if not directly called)
- ❌ Callback functions passed to libraries
- ❌ Functions in modules that may be called externally
- ❌ GSAP callbacks (`onEnter`, `onLeave`, etc.)

**Example:**
```javascript
// ❌ Remove - never called
function oldDebugFunction() {
  console.log('debug');
}

// ✅ Keep - used as callback
function handleResize() {
  // Even if not directly called, used in addEventListener
}

// ❌ Remove - unused variable
const unusedConfig = { foo: 'bar' };

// ✅ Keep - used in event listener
document.addEventListener('click', handleClick);
```

#### 3. Consolidate Duplicate Code

**Pattern: Duplicate CSS Properties**
```css
/* Before */
.muse-logo-image {
  width: 300px;
}
@media (max-width: 768px) {
  .muse-logo-image {
    width: 180px;
  }
}

/* After - use clamp() */
.muse-logo-image {
  width: clamp(180px, 20vw, 300px);
}
```

**Pattern: Duplicate GLSL Code**
```javascript
// Before - duplicated noise function in each shader
const shader1 = `
  vec3 mod289(vec3 x) { ... }
  // ... noise code
`;
const shader2 = `
  vec3 mod289(vec3 x) { ... }
  // ... noise code
`;

// After - shared utility
const GLSL_UTILS = {
  SIMPLEX_NOISE: `vec3 mod289(vec3 x) { ... }`
};
const shader1 = `${GLSL_UTILS.SIMPLEX_NOISE} void main() { ... }`;
const shader2 = `${GLSL_UTILS.SIMPLEX_NOISE} void main() { ... }`;
```

**Pattern: Repeated Media Query Values**
```css
/* Before */
@media (max-width: 768px) { .a { font-size: 14px; } }
@media (max-width: 768px) { .b { padding: 1rem; } }

/* After - consolidate */
@media (max-width: 768px) {
  .a { font-size: 14px; }
  .b { padding: 1rem; }
}
```

#### 4. Optimize Performance (No Behavior Change)

**CSS Optimizations:**
```css
/* Before - multiple properties */
.element {
  margin-top: 1rem;
  margin-right: 2rem;
  margin-bottom: 1rem;
  margin-left: 2rem;
}

/* After - shorthand */
.element {
  margin: 1rem 2rem;
}

/* Before - inefficient selector */
div.container > div.wrapper > div.content {
  color: white;
}

/* After - use class directly */
.content {
  color: white;
}
```

**JavaScript Optimizations:**
```javascript
// Before - repeated DOM queries
function updateElements() {
  document.querySelector('.element').style.opacity = 1;
  document.querySelector('.element').style.transform = 'scale(1)';
}

// After - cache selector
function updateElements() {
  const element = document.querySelector('.element');
  element.style.opacity = 1;
  element.style.transform = 'scale(1)';
}

// Before - unnecessary calculations in loop
for (let i = 0; i < items.length; i++) {
  const radius = Math.min(window.innerWidth, window.innerHeight) * 0.3;
  items[i].style.width = radius + 'px';
}

// After - calculate once
const radius = Math.min(window.innerWidth, window.innerHeight) * 0.3;
for (let i = 0; i < items.length; i++) {
  items[i].style.width = radius + 'px';
}
```

#### 5. Clean Up Comments

**Remove:**
- ✅ Obsolete TODO comments for completed tasks
- ✅ Debug comments (`// testing`, `// temp fix`)
- ✅ Commented-out code blocks (if truly unused)
- ✅ Overly verbose explanations for self-evident code

**Keep:**
- ✅ Section dividers (`/* ========== Section Name ========== */`)
- ✅ Complex algorithm explanations
- ✅ Browser compatibility notes
- ✅ Warning comments about edge cases
- ✅ Attribution comments for external code

**Example:**
```javascript
// ❌ Remove - self-evident
// Set the opacity to 1
element.style.opacity = 1;

// ✅ Keep - explains WHY
// Safari requires explicit z-index for backdrop-filter to work
element.style.zIndex = 10;

// ❌ Remove - old debug code
// console.log('x:', x, 'y:', y);

// ✅ Keep - section organization
/* ==========================================================================
   Muse Orbit Calculation
   ========================================================================== */
```

### Cleanup Workflow

**Step-by-Step Process:**

1. **Analyze** - Understand what the code does
   ```bash
   # Check if class is used
   grep -r "className" . --include="*.html" --include="*.js"
   ```

2. **Test Before** - Verify current behavior works
   - Test all interactive features
   - Check on mobile and desktop
   - Verify animations run smoothly

3. **Make Changes** - Apply ONE cleanup at a time
   - Don't batch multiple types of changes
   - Keep changes atomic and reversible

4. **Test After** - Verify behavior unchanged
   - Run same tests as "Test Before"
   - Check browser console for errors
   - Verify no visual regressions

5. **Document** - Note what was removed/changed
   ```javascript
   // Removed unused bouncing logo slider module (lines 1841-2617)
   // Feature was replaced by static connected images layout
   ```

6. **Commit** - Save changes to version control
   ```bash
   git add .
   git commit -m "refactor: remove unused slider module (no behavior change)"
   ```

### Red Flags - Stop and Review

⚠️ **WARNING SIGNS** - If you see these, proceed with extreme caution:

- Code touches DOM elements added dynamically
- Function is passed as callback to external library
- CSS class is manipulated via `.classList.add()`
- Event listener attaches to dynamically created elements
- Code runs conditionally based on user interaction
- Style is applied based on scroll position
- Animation relies on precise timing or sequencing

### Validation Tests

After cleanup, run these tests:

**Visual Tests:**
- [ ] Intro animation plays correctly
- [ ] Text sections fade in smoothly
- [ ] Muse orbit rotates continuously
- [ ] Muse popup opens/closes correctly
- [ ] Comet section displays properly
- [ ] Footer appears at correct scroll position
- [ ] All WebGL canvases render

**Interaction Tests:**
- [ ] Click muse images to open popup
- [ ] Press Escape to close popup
- [ ] Tab through focusable elements
- [ ] Social links work
- [ ] Touch gestures work on mobile

**Performance Tests:**
- [ ] Lighthouse score unchanged or improved
- [ ] No console errors
- [ ] Animations at 60fps (desktop) / 30fps (mobile)
- [ ] Page load time unchanged or improved

### Common Cleanup Opportunities

**In cocoex.xyz project:**

1. **CometCollabSlider Module** (main.js:1841-2617)
   - Status: Not currently used in HTML
   - Action: Can be removed if slider feature is deprecated
   - Verification: Check if any HTML references `.comet-collab-bouncing-logo`

2. **Unused Media Query Variables**
   - Check for hardcoded typography in old breakpoints
   - Consolidate with new `clamp()` approach

3. **Duplicate Scroll Calculations**
   - Look for multiple `window.scrollY` calculations
   - Centralize in one place

4. **Redundant GPU Program Switches**
   - Cache last active WebGL program
   - Skip `gl.useProgram()` if already active

## Resources

**Documentation:**
- `references/gsap_scroll_patterns.md` - Complete ScrollTrigger guide
- `references/webgl_performance_guide.md` - WebGL optimization strategies
- `references/static_site_best_practices.md` - Frontend best practices
- `docs/responsive-design.md` - Responsive implementation guide

**External:**
- [GSAP Docs](https://greensock.com/docs/)
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [MDN Web Docs](https://developer.mozilla.org/)

## cocoex.xyz Specific

This skill is tailored for the cocoex.xyz project:
- 4 WebGL canvases (intro, starfield, muse gradient, comet gradient)
- Master render loop consolidates animations
- Total scroll height: ~1780vh
- Centralized `SCROLL_TIMING` (main.js:88-117)
- Shared GLSL utilities reduce duplication
- 60fps desktop, 30fps mobile target

See `CLAUDE.md` for complete project architecture.
