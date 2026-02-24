# ARCHIVIO B

A minimal, elegant photo gallery website for ARCHIVIO B.

## Overview

Clean, responsive gallery interface with slideshow functionality. Features a fixed left panel with branding and contact info, and a scrollable right panel displaying the photo collection.

## Features

- **Responsive Layout** - Two-panel design adapts to all screen sizes
- **Slideshow Modal** - Click any image to open full-screen slideshow
- **Keyboard Navigation** - Arrow keys to navigate slideshow
- **Touch/Click Zones** - Navigate by clicking left/right sides of images
- **Performance** - Lazy loading, cache control, optimized assets
- **Clean Design** - Minimal aesthetic with Inter font family

## Structure

```
archiviob/
├── index.html    # Main HTML structure
├── style.css     # All styles and responsive layout
├── script.js     # Gallery generation and slideshow logic
└── README.md     # This file
```

## Local Development

Run a local server from the project root:

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx serve . -l 8000
```

Then navigate to `http://localhost:8000/`

## Gallery Configuration

Images are loaded dynamically via `script.js`. To add/remove images, edit the image array in the script file.

## Contact

- **Email:** eb@archiviob.xyz
- **Phone:** +39 393 7807053

## Technical Details

- **No build step required** - Pure HTML/CSS/JS
- **No external dependencies** - Self-contained (except Google Fonts)
- **Cache control headers** - Versioned CSS/JS references
- **Progressive enhancement** - Critical CSS inline for fast first paint
