# Frontend Engineering Practices

## Core Principles

**Performance First** - Fast load times improve UX and SEO. Profile, measure, optimize.

**Accessibility is Non-Negotiable** - Semantic HTML, ARIA labels, keyboard navigation, screen reader support.

**Progressive Enhancement** - Build for baseline functionality first, then enhance for modern browsers.

**Mobile-First Responsive** - Design for smallest screens first, then scale up.

## HTML Best Practices

### Semantic Structure
```html
<!-- Good: Semantic HTML -->
<header>
  <nav>...</nav>
</header>
<main>
  <article>
    <h1>Title</h1>
    <section>...</section>
  </article>
</main>
<footer>...</footer>

<!-- Bad: Div soup -->
<div class="header">
  <div class="nav">...</div>
</div>
```

### Accessibility Essentials
- Use proper heading hierarchy (`h1` → `h6`)
- Add `alt` text to all images
- Include `lang` attribute on `<html>`
- Use ARIA labels where semantic HTML isn't enough
- Ensure sufficient color contrast (WCAG AA minimum)
- Support keyboard navigation

### Meta Tags
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Brief, accurate description">
<title>Descriptive Page Title</title>
```

## CSS Best Practices

### Organization
```css
/* 1. CSS Variables for theming */
:root {
  --color-primary: #007bff;
  --spacing-unit: 8px;
  --font-size-base: 16px;
}

/* 2. Reset/Normalize first */
* { box-sizing: border-box; }

/* 3. Base styles */
body { font-family: system-ui, sans-serif; }

/* 4. Layout */
.container { max-width: 1200px; margin: 0 auto; }

/* 5. Components */
.btn { padding: var(--spacing-unit); }

/* 6. Utilities */
.sr-only { position: absolute; left: -10000px; }
```

### Modern CSS Patterns
- **Flexbox/Grid** - Prefer over floats for layouts
- **CSS Variables** - For theming and consistent values
- **Mobile-First Media Queries** - `@media (min-width: 768px) {...}`
- **BEM Naming** - `.block__element--modifier` for clarity

### Performance
- Minimize specificity (avoid deep nesting)
- Use shorthand properties where appropriate
- Leverage browser caching with hashed filenames
- Critical CSS inline, defer non-critical

## JavaScript Best Practices

### Modern JS (ES6+)
```javascript
// Use const/let, avoid var
const API_URL = '/api/data';
let counter = 0;

// Arrow functions for concise syntax
const double = (n) => n * 2;

// Destructuring
const { name, age } = user;
const [first, ...rest] = array;

// Template literals
const message = `Hello, ${name}!`;

// Async/await over callbacks
async function fetchData() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch failed:', error);
  }
}
```

### DOM Manipulation
```javascript
// Good: Cache selectors
const button = document.querySelector('.btn');
button.addEventListener('click', handleClick);

// Good: Event delegation
document.querySelector('.list').addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleItemClick(e.target);
  }
});

// Bad: Multiple queries in loops
// Don't: document.querySelector() inside loop
```

### Error Handling
```javascript
// Always handle errors
try {
  // risky operation
} catch (error) {
  console.error('Operation failed:', error);
  // Graceful degradation
}

// Validate inputs
function calculateTotal(items) {
  if (!Array.isArray(items)) {
    throw new TypeError('Expected array');
  }
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

## Performance Optimization

### Assets
- **Images:** WebP format, lazy loading, responsive images with `srcset`
- **Fonts:** Use `font-display: swap`, limit font variations
- **Minification:** Minify CSS/JS for production
- **Compression:** Enable gzip/brotli on server

### Loading Strategy
```html
<!-- Defer non-critical JS -->
<script src="main.js" defer></script>

<!-- Async for independent scripts -->
<script src="analytics.js" async></script>

<!-- Preload critical assets -->
<link rel="preload" href="critical.css" as="style">

<!-- Lazy load images -->
<img src="image.jpg" loading="lazy" alt="Description">
```

### Metrics to Monitor
- **FCP** (First Contentful Paint) - Target < 1.8s
- **LCP** (Largest Contentful Paint) - Target < 2.5s
- **CLS** (Cumulative Layout Shift) - Target < 0.1
- **TTI** (Time to Interactive) - Target < 3.8s

## Project Structure

```
project-name/
├── index.html
├── css/
│   ├── normalize.css      # Reset
│   ├── variables.css      # CSS variables
│   ├── base.css           # Base styles
│   ├── components.css     # Reusable components
│   └── styles.css         # Main stylesheet
├── js/
│   ├── utils.js           # Helper functions
│   ├── components/        # Component logic
│   └── main.js            # Entry point
├── assets/
│   ├── images/
│   ├── fonts/
│   └── icons/
└── README.md
```

## Testing & Quality

### Browser Testing
- Test on Chrome, Firefox, Safari, Edge
- Test on real mobile devices (iOS Safari, Android Chrome)
- Use BrowserStack/LambdaTest for cross-browser testing

### Accessibility Testing
- Use Lighthouse in Chrome DevTools
- Test with keyboard navigation only
- Use screen readers (VoiceOver, NVDA)
- Validate HTML with W3C validator

### Performance Testing
- Google PageSpeed Insights
- WebPageTest.org
- Chrome DevTools Performance tab

## Build & Deployment

### Development Workflow
```bash
# Local development server
python3 -m http.server 8000
# or
npx serve . -l 8000

# Watch for changes (if using build tools)
npm run dev
```

### Production Build
- Minify HTML/CSS/JS
- Optimize and compress images
- Generate source maps for debugging
- Cache bust with versioned filenames
- Enable compression (gzip/brotli)

### Deployment Checklist
- ✅ Test on multiple browsers/devices
- ✅ Run Lighthouse audit (score > 90)
- ✅ Validate HTML/CSS
- ✅ Check all links work
- ✅ Verify meta tags and SEO elements
- ✅ Test with slow 3G network throttling
- ✅ Enable HTTPS
- ✅ Configure caching headers

## Common Pitfalls to Avoid

❌ **Don't:** Use inline styles (`style="..."`)
✅ **Do:** Use CSS classes

❌ **Don't:** Pollute global scope with variables
✅ **Do:** Use modules or IIFE patterns

❌ **Don't:** Ignore accessibility
✅ **Do:** Use semantic HTML and ARIA

❌ **Don't:** Load massive libraries for simple tasks
✅ **Do:** Use vanilla JS or small utilities

❌ **Don't:** Commit unoptimized images
✅ **Do:** Compress and optimize assets

❌ **Don't:** Use `!important` habitually
✅ **Do:** Write specific, maintainable selectors

## Tools & Resources

### Essential Tools
- **Chrome DevTools** - Debugging, performance profiling
- **Lighthouse** - Performance and accessibility audits
- **VS Code Extensions** - ESLint, Prettier, Live Server

### Useful Libraries (Use Sparingly)
- **Alpine.js** - Lightweight reactivity (15KB)
- **htmx** - HTML-driven interactivity
- **Tailwind CSS** - Utility-first CSS (if build step acceptable)

### Learning Resources
- MDN Web Docs - Comprehensive reference
- web.dev - Performance best practices
- A11y Project - Accessibility guidelines
- Can I Use - Browser compatibility

## Version Control

### Commit Messages
```bash
# Format: <type>: <description>

add: new contact form component
fix: mobile menu z-index issue
refactor: simplify navigation styles
perf: optimize hero image loading
docs: update README with deployment steps
```

### What to Commit
- ✅ Source HTML/CSS/JS files
- ✅ Optimized images (< 500KB each)
- ✅ Documentation (README, etc.)
- ❌ node_modules or build artifacts (unless no build step)
- ❌ IDE-specific files (.vscode, .idea)
- ❌ Sensitive data (API keys, credentials)

---

**Remember:** Start simple, measure impact, iterate based on data. Don't over-engineer static sites.
