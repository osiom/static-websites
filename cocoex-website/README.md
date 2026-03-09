# cocoex

A vibrant DAO blending art, blockchain, community and social impact.

## About

cocoex aims to cultivate a vibrant community where art and impactful change coexist in harmonious synergy. We bring artists, creators and collectors together to support and inspire one another, creating a sense of unity and shared purpose.

## Website Overview

The cocoex website is a scroll-driven interactive experience built with modern web technologies and minimalist design principles.

### Features

#### 1. Animated Introduction
- **Orbiting Animation**: Rotating logo with orbiting white and black dots
- **Constellation Explosion**: Seven colorful dots explode into a constellation pattern
- **WebGL Background**: Animated starfield with twinkling stars and cosmic noise
- **Scroll-Driven**: All animations respond to scroll position using GSAP ScrollTrigger

#### 2. Mission Statement
- **Transition Text**: "art as infrastructure for change" appears below logo at 76% orbit progress
- **Fade-In Text**: Mission text reveals smoothly as you scroll
- **Simplified Experience**: Removed word highlighting for smoother, faster scroll experience (reduced from 350vh to 150vh)

#### 3. Muse Portfolio
- **Black Opening Slide**: Muse logo introduction with smooth transition
- **Orbiting Layout**: Seven muses orbit around central logo in horizontal ellipse
- **Animated Background**: Subtle WebGL gradient flowing between muse colors
- **Interactive Popups**: Click muse images or names to view detailed descriptions
- **Continuous Rotation**: Muses slowly rotate (240 seconds per revolution)

**The Seven Muses:**
- **Lunes** - Mystery and intuition
- **Ares** - Passion and courage
- **Rabu** - Communication and connection
- **Thunor** - Thunder and strength
- **Shukra** - Beauty and harmony
- **Dosei** - Wisdom and structure
- **Solis** - Warmth and vitality

#### 4. Social Links & Footer
- Links to Telegram, Instagram, and LinkedIn
- Responsive design with touch-friendly targets
- Keyboard navigation support

## Tech Stack

- **HTML5** - Semantic markup with ARIA labels
- **CSS3** - Custom properties, Grid, Flexbox, hardware-accelerated animations
- **Vanilla JavaScript** - ES6+ modules with IIFE pattern
- **GSAP 3.12.5** - Animation library with ScrollTrigger and MotionPathPlugin
- **WebGL** - Custom shaders for background effects

## Project Structure

```
cocoex-website/
├── index.html              # Main HTML file
├── css/
│   └── styles.css          # Stylesheet with CSS custom properties
├── js/
│   └── main.js             # Core animation and interaction logic
├── assets/
│   └── images/             # Logo, muse images, icons
├── tools/
│   └── coordinate-picker.html  # Development tool for constellation positioning
├── README.md               # This file
└── CLAUDE.md              # Project context for Claude Code
```

## Performance

### Bundle Size
- **Uncompressed**: 69KB (HTML + CSS + JS)
- **Gzipped**: ~20KB (excludes GSAP CDN)
- **First Load**: ~70KB transferred (including GSAP)
- **Cached Load**: ~20KB (GSAP cached)

### Performance Benchmarks
- **Lighthouse Score**: 95+ (Performance, Accessibility, Best Practices)
- **First Contentful Paint**: <1.5s on 4G connection
- **Time to Interactive**: <3s on 4G connection
- **WebGL Rendering**: 60fps on desktop, 30fps on mobile

### System Requirements
**Minimum:**
- iPhone 8 / Galaxy S9 equivalent
- 2GB RAM
- WebGL 1.0 support
- Modern browser (Chrome 90+, Safari 14+, Firefox 88+)

**Recommended:**
- Desktop: 8GB RAM, dedicated GPU
- Mobile: 4GB RAM, recent device (2020+)

### Optimization Strategies
- Hardware-accelerated transforms (`transform`, `opacity` only)
- Passive event listeners for scroll/resize
- Debounced resize handler (150ms)
- Early exit in shader star generation
- `will-change` hints for animating elements
- Z-index layering to minimize repaints
- WebGL program state caching (minimizes GPU context switches)
- Mobile DPR capping at 2x (reduces pixel count by 33% on high-DPI devices)
- Extended scroll durations for 60fps GSAP interpolation
- Consolidated master render loop for all animations

### Known Limitations
- **Battery Usage**: Extended viewing on mobile may drain battery (WebGL rendering)
- **Low-End Devices**: May experience dropped frames in constellation animation
- **High DPI Displays**: WebGL canvas scales to device pixel ratio (higher memory usage)
- **Safari**: Occasional backdrop-filter glitch during rapid scroll

## Accessibility

- Semantic HTML5 elements (`<section>`, `<article>`, `<footer>`)
- ARIA labels for interactive elements and screen readers
- Keyboard navigation support (Tab, Escape)
- Focus visible styles for keyboard users
- `prefers-reduced-motion` support for users with motion sensitivities
- Color contrast meets WCAG AA standards
- Touch targets minimum 44px for mobile users

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Requirements:**
- WebGL support for background animations
- CSS Grid and Flexbox
- ES6+ JavaScript
- CSS Custom Properties

## Getting Started

### Local Development

Simply open `index.html` in a modern browser, or use a local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve

# Using PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`

### Development Tools

- **Coordinate Picker** (`tools/coordinate-picker.html`) - Interactive tool for positioning constellation dots

## Design Principles

1. **Minimalism First** - Every element serves a purpose
2. **Performance Budget** - Target 95+ Lighthouse score
3. **Mobile-First** - Responsive from smallest to largest screens
4. **Accessibility** - WCAG AA compliant with keyboard navigation
5. **Semantic HTML** - Meaningful markup over divs
6. **Progressive Enhancement** - Core content works without JavaScript

## Dependencies

External libraries loaded from CDN:

- [GSAP 3.12.5](https://greensock.com/gsap/) - Animation framework
- [ScrollTrigger](https://greensock.com/scrolltrigger/) - Scroll-based animations
- [MotionPathPlugin](https://greensock.com/docs/v3/Plugins/MotionPathPlugin) - Path-based animations

## License

All rights reserved. cocoex 2024-2026.

## Contact

- **Telegram**: [t.me/coco_ex](https://t.me/coco_ex)
- **Instagram**: [@cocoex_](https://instagram.com/cocoex_)
- **LinkedIn**: [company/cocoex](https://www.linkedin.com/company/cocoex/)
