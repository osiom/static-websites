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

## Resources

**Documentation:**
- `references/gsap_scroll_patterns.md` - Complete ScrollTrigger guide
- `references/webgl_performance_guide.md` - WebGL optimization strategies
- `references/static_site_best_practices.md` - Frontend best practices

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
