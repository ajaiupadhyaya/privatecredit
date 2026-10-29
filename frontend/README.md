# Credit Observatory frontend

The canonical application is plain HTML, CSS, and JavaScript. The unused Next.js starter was retired because this research artifact benefits from an offline, serverless distribution.

- `index.html`: semantic shell, methodology, research notes.
- `styles.css`: editorial design, responsive and print layouts.
- `app.js`: views, diagnostics, chart interaction, scenario controls.
- `domain.js`: independently tested liquidity accounting.
- `public/data.js` and `research.json`: generated, aggregate-only data.

From the repository root, run `python scripts/build_portfolio.py`. Serve `../dist` with `npm run dev`, or open `dist/index.html` directly. `npm test` and `npm run lint` need Node only, with no installation. The Python build dependencies are in the root `requirements.txt`.

Historical `AGENTS.md` Next.js-specific guidance applies only if that framework is reintroduced; no Next.js runtime remains in the canonical frontend.
