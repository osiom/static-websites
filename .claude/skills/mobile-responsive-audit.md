# Mobile Responsive Audit Skill

## Purpose
Systematically audit and adjust mobile/tablet responsiveness for static websites. Ensures consistent UX across all screen sizes with proper touch targets, readable typography, and optimized layouts.

## When to Use This Skill
- After implementing new features or sections
- Before deployment/production release
- When user reports mobile usability issues
- During routine maintenance reviews
- When adding responsive breakpoints

## Scope
This skill focuses on **static websites** (HTML/CSS/JS) with emphasis on:
- Responsive breakpoints (320px - 1920px+)
- Touch target accessibility (44px minimum)
- Typography scaling
- Layout flow and spacing
- WebGL/Canvas performance on mobile
- Image sizing and optimization

---

## Audit Process

### Step 1: Identify All Breakpoints

Search for existing media queries and document current breakpoint strategy:

```bash
# Find all media queries
grep -n "@media" css/*.css
```

**Document:**
- Current breakpoints (e.g., 480px, 768px, 1024px, 1440px, 1920px)
- Mobile-first vs Desktop-first approach
- CSS variable usage for responsive values

**Standard Breakpoints:**
- **320px**: Small mobile (iPhone SE)
- **480px**: Mobile landscape
- **768px**: Tablet portrait
- **1024px**: Tablet landscape
- **1440px**: Large desktop
- **1920px**: XL desktop

---

### Step 2: Section-by-Section Analysis

For each major section of the website, check:

#### A. Typography
- [ ] Font sizes scale appropriately (CSS variables preferred)
- [ ] Line heights maintain readability (1.2-1.5 ratio)
- [ ] Text remains readable at smallest breakpoint (min 12px body, 18px headings)
- [ ] No horizontal overflow or text cutoff

**Check:**
```css
:root {
  --font-h1-size: 36px;  /* Desktop */
}

@media (max-width: 768px) {
  :root {
    --font-h1-size: 22px;  /* Mobile */
  }
}
```

#### B. Touch Targets
- [ ] Interactive elements ≥44px × 44px (WCAG AA)
- [ ] Spacing between touch targets ≥8px
- [ ] Buttons, links, icons are thumb-friendly

**Check:**
```css
.button, .social-link {
  width: 44px;   /* Minimum */
  height: 44px;  /* Minimum */
}
```

#### C. Spacing & Layout
- [ ] Padding/margins scale with screen size (CSS variables)
- [ ] Grid/flex layouts adapt (single column on mobile)
- [ ] No horizontal scroll at any breakpoint
- [ ] Content doesn't feel cramped or too sparse

**Check:**
```css
:root {
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
}

@media (max-width: 768px) {
  :root {
    --spacing-lg: 1.5rem;  /* Reduce on mobile */
  }
}
```

#### D. Images & Media
- [ ] Images scale responsively (max-width: 100%)
- [ ] Logo sizes appropriate for screen (not too large/small)
- [ ] WebGL canvases resize correctly
- [ ] Device Pixel Ratio (DPR) capped on mobile (performance)

**Check:**
```javascript
// Cap DPR at 2x on mobile
const dpr = isMobile() ? Math.min(window.devicePixelRatio, 2) : window.devicePixelRatio;
```

#### E. Navigation & Interaction
- [ ] Menus accessible on mobile (hamburger if needed)
- [ ] Scroll-driven animations don't feel too fast
- [ ] Hover states have touch equivalents
- [ ] Keyboard navigation works on tablet

---

### Step 3: Device-Specific Checks

#### Mobile Portrait (320px - 480px)
- [ ] Single column layouts
- [ ] Stacked content (no side-by-side)
- [ ] Large touch targets (52px+ for primary actions)
- [ ] Simplified animations (fewer particles)
- [ ] Reduced `will-change` hints (performance)

#### Mobile Landscape (480px - 768px)
- [ ] Horizontal space utilized efficiently
- [ ] Fixed headers don't cover content
- [ ] Viewport height issues handled (vh units)

#### Tablet (768px - 1024px)
- [ ] 2-column layouts where appropriate
- [ ] Larger typography than mobile
- [ ] Touch targets remain accessible
- [ ] Hover states gracefully degrade

---

### Step 4: Performance Audit

#### Mobile Performance
- [ ] WebGL canvases use mobile-optimized shaders
- [ ] DPR capped at 2x (reduce pixel count)
- [ ] Animation frame rates acceptable (30fps minimum)
- [ ] `prefers-reduced-motion` implemented
- [ ] Debounced scroll/resize handlers (150ms+)

**Check:**
```javascript
// Mobile detection
function isMobile() {
  return window.innerWidth <= 768 ||
         /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// DPR capping
const dpr = isMobile() ? Math.min(window.devicePixelRatio || 1, 2) : (window.devicePixelRatio || 1);
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;
```

#### Battery Considerations
- [ ] WebGL animations can be disabled on low battery
- [ ] Particle counts reduced on mobile
- [ ] Passive event listeners used

---

### Step 5: Accessibility Verification

- [ ] WCAG AA contrast ratios (4.5:1 text, 3:1 UI)
- [ ] Touch targets ≥44px × 44px
- [ ] Focus visible styles (2px outline + 2px offset)
- [ ] Screen reader friendly (ARIA labels)
- [ ] `prefers-reduced-motion` support
- [ ] Zoom works up to 200% without breaking layout

---

### Step 6: Cross-Browser Testing

**Browsers to Test:**
- [ ] Chrome mobile (Android)
- [ ] Safari mobile (iOS)
- [ ] Firefox mobile
- [ ] Samsung Internet (Android)

**Test Matrix:**
| Device | Browser | Orientation | Notes |
|--------|---------|-------------|-------|
| iPhone SE (320px) | Safari | Portrait | Smallest screen |
| iPhone 13 (390px) | Safari | Portrait/Landscape | Common iOS |
| iPad (768px) | Safari | Portrait/Landscape | Tablet |
| Pixel 5 (393px) | Chrome | Portrait/Landscape | Common Android |
| Galaxy Tab (1024px) | Samsung Internet | Portrait/Landscape | Tablet |

---

## Output Format

After completing the audit, provide:

### 1. Summary Report
```markdown
## Mobile Responsive Audit Report

**Site:** [Website Name]
**Date:** [YYYY-MM-DD]
**Breakpoints Audited:** 320px, 480px, 768px, 1024px, 1440px, 1920px

### Critical Issues (Fix Immediately)
- [ ] Issue description (e.g., "Social icons 32px, below 44px minimum")
  - **Location:** `css/styles.css:1658`
  - **Fix:** Increase to 44px × 44px

### Medium Priority (Fix Before Deploy)
- [ ] Issue description

### Low Priority (Nice to Have)
- [ ] Issue description

### Performance Notes
- Mobile DPR: [Capped/Uncapped]
- WebGL FPS: [30fps/60fps/Variable]
- Scroll performance: [Smooth/Laggy]

### Recommended Adjustments
[Specific CSS/JS changes needed]
```

### 2. Code Changes
Provide exact CSS/JS snippets ready to copy-paste:

```css
/* Mobile adjustments - Social icons */
@media screen and (max-width: 768px) {
  .social-link {
    width: 44px;   /* Increased from 32px */
    height: 44px;  /* Increased from 32px */
  }
}
```

### 3. Testing Checklist
- [ ] Tested on iPhone SE (320px)
- [ ] Tested on standard mobile (375px)
- [ ] Tested on tablet portrait (768px)
- [ ] Tested on tablet landscape (1024px)
- [ ] No horizontal scroll at any size
- [ ] All touch targets ≥44px
- [ ] Typography readable at all sizes

---

## Best Practices Reference

### CSS Organization
```css
/* 1. Mobile-first approach (preferred) */
.element {
  /* Mobile styles (default) */
  font-size: 16px;
}

@media (min-width: 768px) {
  .element {
    /* Tablet and up */
    font-size: 18px;
  }
}

/* 2. Desktop-first approach (use only if existing pattern) */
.element {
  /* Desktop styles (default) */
  font-size: 24px;
}

@media (max-width: 768px) {
  .element {
    /* Mobile */
    font-size: 16px;
  }
}
```

### Responsive Typography Scale
```css
:root {
  /* Mobile (default) */
  --font-h1-size: 22px;
  --font-h1-height: 26px;
  --font-h2-size: 14px;
  --font-h2-height: 17px;
}

@media (min-width: 768px) {
  /* Tablet */
  :root {
    --font-h1-size: 30px;
    --font-h1-height: 33px;
    --font-h2-size: 16px;
    --font-h2-height: 19px;
  }
}

@media (min-width: 1024px) {
  /* Desktop */
  :root {
    --font-h1-size: 36px;
    --font-h1-height: 38px;
    --font-h2-size: 18px;
    --font-h2-height: 21px;
  }
}
```

### Touch Target Guidelines
```css
/* Minimum touch target (WCAG AA) */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  padding: 8px; /* Spacing between targets */
}

/* Optimal touch target (better UX) */
.button-primary {
  min-width: 48px;
  min-height: 48px;
  padding: 12px 24px;
}
```

### Performance Patterns
```javascript
// Mobile detection
function isMobile() {
  return window.innerWidth <= 768 ||
         /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// DPR capping for mobile
const baseDPR = window.devicePixelRatio || 1;
const dpr = isMobile() ? Math.min(baseDPR, 2) : baseDPR;

// Debounced resize handler
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    // Resize logic here
  }, 150);
}, { passive: true });

// Reduced motion support
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReducedMotion) {
  // Disable animations
}
```

---

## Common Issues & Fixes

### Issue 1: Text Too Small on Mobile
**Symptom:** Body text < 14px, headings < 18px on mobile
**Fix:**
```css
@media (max-width: 768px) {
  body { font-size: 14px; }  /* Minimum */
  h1 { font-size: 22px; }    /* Minimum */
}
```

### Issue 2: Touch Targets Too Small
**Symptom:** Buttons/icons < 44px
**Fix:**
```css
.button, .icon {
  min-width: 44px;
  min-height: 44px;
}
```

### Issue 3: Horizontal Scroll on Mobile
**Symptom:** Content wider than viewport
**Fix:**
```css
body {
  overflow-x: hidden;
  max-width: 100vw;
}

* {
  box-sizing: border-box;
}
```

### Issue 4: WebGL Performance Issues
**Symptom:** Low FPS, battery drain
**Fix:**
```javascript
// Cap DPR
const dpr = isMobile() ? Math.min(window.devicePixelRatio, 2) : window.devicePixelRatio;

// Reduce particle count
const particleCount = isMobile() ? 20 : 50;

// Target 30fps on mobile
const targetFPS = isMobile() ? 30 : 60;
```

### Issue 5: Fixed Elements Cover Content
**Symptom:** Header/footer overlap scrollable content
**Fix:**
```css
body {
  padding-top: var(--header-height);
  padding-bottom: var(--footer-height);
}
```

---

## Invocation

To use this skill, simply invoke:

```
/mobile-responsive-audit
```

Or reference it in your request:

```
"Run a mobile responsive audit on the current website"
"Check if all sections are properly responsive for tablet and mobile"
"Audit touch targets and typography scaling"
```

---

## Maintenance

**Update this skill when:**
- New breakpoints become standard (e.g., foldable phones)
- WCAG guidelines change
- New performance best practices emerge
- Project-specific patterns need documentation

**Version:** 1.0.0
**Created:** March 9, 2026
**Last Updated:** March 9, 2026
**Author:** Claude Code + User Collaboration
