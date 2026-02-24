# Static Websites Repository

## Overview

This repository serves as a centralized collection of static websites generated across multiple projects. Each site is self-contained, lightweight, and deployable independently.

## Repository Structure

```
static-websites/
├── site-one/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── site-two/
│   └── index.html
└── README.md
```

Each project folder contains:
- `index.html` - Entry point (required)
- `css/` - Stylesheets (optional)
- `js/` - JavaScript files (optional)
- `assets/` - Images, fonts, media (optional)
- `README.md` - Project-specific documentation (optional)

## Adding a New Site

1. **Create a project folder** at the root using `lowercase-with-hyphens` naming convention
2. **Add minimum required files** - at minimum, an `index.html`
3. **Organize assets** - use `css/`, `js/`, and `assets/` subdirectories as needed
4. **Document specifics** - add a README.md if the site has unique requirements or context

## Local Development

Run a local server from the repository root:

```bash
# Python 3
python3 -m http.server 8000

# Node.js (with serve)
npx serve . -l 8000
```

Access sites at `http://localhost:8000/<project-folder>/`

## Deployment

Static sites in this repository can be deployed to:
- **GitHub Pages** - enable in repo settings
- **Netlify/Vercel** - drag-and-drop or CLI deployment
- **AWS S3 + CloudFront** - for production environments
- **Any static hosting provider**

## Conventions

- **Folder names:** `lowercase-with-hyphens` (no spaces, no underscores)
- **File names:** Descriptive and lowercase (`main.js`, `styles.css`)
- **Entry file:** Always `index.html` at the project root
- **Commits:** Small, descriptive messages (e.g., `add: new landing page`, `fix: mobile responsive layout`)

## Best Practices

- Keep sites self-contained and dependency-free where possible
- Minimize external dependencies for faster load times
- Follow accessibility standards (semantic HTML, ARIA labels)
- Optimize images and assets before committing
- Test cross-browser compatibility

For detailed frontend engineering practices, see [CLAUDE.md](CLAUDE.md)
- Optionally add a simple CI workflow to deploy a preview branch or publish to GitHub Pages.

**Contact**

- For changes, requests, or help previewing a site, open an issue or message me directly.

Enjoy building :) 
