**Overview**

- **Purpose:** This repository stores small static websites I build for friends, family, and lovers. Keep things simple, personal, and easy to preview.

**Repository Structure**

- **Root:** top-level project files and a folder per site.
- **Site folders:** each site lives in its own folder (for example: `archiviob/`) and should contain at minimum an `index.html`.

Example:

- `archiviob/`
	- `index.html` : site entry point
	- `style.css`  : optional styles
	- `script.js`  : optional JS
	- `assets/`    : images, fonts, etc.

**How to Add a Site**

- Create a new folder at the repo root using a short, lowercase name (use hyphens instead of spaces).
- Add an `index.html` file at minimum. Add `style.css`, `script.js`, and an `assets/` folder as needed.
- Optionally add a short `README.md` inside the site folder describing the site and any credits.

Naming conventions:

- Folder names: `lowercase-with-hyphens` (no spaces).
- Files: use descriptive names, keep `index.html` as the entry file.

**Preview Locally**

Run a simple static server from the repo root and open the site in a browser. Examples:

```
# using Python 3
python3 -m http.server 8000

# or using Node.js (if you have `serve` installed)
npx serve . -l 8000
```

Then open `http://localhost:8000/<site-folder>/` in your browser.

**Commit & Contribution Notes**

- Keep commits small and descriptive. Example: `add: archiviob initial site files`.
- If you want me to add a site for you: send me the files (zipped) or open an issue with the content and a preferred folder name.

**Next Steps / Ideas**

- Add a small site template in `templates/` for quick scaffolding.
- Optionally add a simple CI workflow to deploy a preview branch or publish to GitHub Pages.

**Contact**

- For changes, requests, or help previewing a site, open an issue or message me directly.

Enjoy building :) 
