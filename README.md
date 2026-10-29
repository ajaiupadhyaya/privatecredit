# Credit Observatory

**Where credit becomes fragile.** A portfolio research experience by Ajai Upadhyaya, joining market structure, synthetic credit classification, and liquidity accounting.

[Open the portfolio](dist/index.html) · [Read the credit-risk report](dist/credit-report.html) · [Download the research snapshot](dist/research.json) · [Audit and verification](docs/AUDIT.md)

## What is finished

- **Market structure:** a properly compounded equal-weight basket of five listed BDCs, monthly observations, drawdown view, date filtering, and inspectable chart values.
- **Loan portfolio:** freshly evaluated logistic and random-forest models on 10,103 held-out synthetic loans, ROC and calibration diagnostics, bootstrap intervals, sector concentration, and stress scenarios.
- **Liquidity lab:** interactive requests, gates, and sale haircuts, with complete quarterly accounting and explicit unfunded redemptions when assets are exhausted.
- **Evidence:** methodology, source hashes, limitations, downloadable aggregates, a printable report, and regression tests.

The site is self-contained HTML/CSS/JavaScript. It needs no API keys, backend, CDN, font downloads, or npm dependencies. It has responsive layouts, native accessible controls, keyboard focus styles, a skip link, chart tables, print styles, and reduced-motion support. Browser visual verification is outstanding due to environment restrictions; see the audit.

## View

Open `dist/index.html` in a browser, or serve only the publication folder:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Then visit `http://127.0.0.1:4173`. The three views also support direct links: `#market`, `#loans`, and `#liquidity`.

## Reproduce

Python 3.11 is the reference runtime; Node 18+ runs the frontend tests.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build_portfolio.py
.venv/bin/python -m pytest tests -q
node --test frontend/tests/*.test.cjs
```

The build reads the local SQLite snapshot and the bundled, validated credit summary in `data/portfolio/`. It never fetches external data. `dist/` is the publication artifact and is already built.

To refresh credit results from the companion repository:

```sh
# In ../creditrisk, run its run_analysis.py with its documented environment first.
.venv/bin/python scripts/build_portfolio.py --credit-summary ../creditrisk/outputs/validated/summary.json
```

The two repositories remain independently usable. To change the standalone default snapshot, copy the refreshed summary and report to `data/portfolio/credit_summary.json` and `credit_report.html`.

## Evidence boundaries

The price snapshot covers **18 July 2019 to 24 March 2026**, the common window for ARCC, FSK, MAIN, OBDC, and PSEC. Original download timestamps and price-adjustment metadata were not recorded. It is labeled **unverified**, not current or verified investment performance.

The original macro loader silently substituted synthetic data when FRED was unavailable. The bundled macro table is therefore excluded from all portfolio conclusions. Future fetches now fail explicitly unless simulation is requested.

The 50,000-loan dataset is synthetic. The original external dataset listing and license are unrecorded. Only aggregate results are packaged for the site. Classifier scores describe the supplied varied-lifetime default flags, not one-year PDs. Stress estimates use supplied annual PD and LGD separately.

## Project layout

| Path | Purpose |
|---|---|
| `frontend/index.html`, `styles.css`, `app.js`, `domain.js` | Canonical portfolio source |
| `scripts/build_portfolio.py` | Offline deterministic artifact build |
| `src/models/liquidity_stress.py` | Tested Python reference simulator |
| `tests/`, `frontend/tests/` | Numerical, accounting, data, and packaging checks |
| `data/db/privatecredit.db` | Existing research snapshot; unmodified |
| `data/portfolio/` | Validated aggregate companion results |
| `dist/` | Self-contained publication output |
| `dashboard/`, `notebooks/`, other `src/` modules | Legacy exploratory research; not portfolio evidence |

The unused Next.js starter has been replaced by the dependency-free site. The legacy Streamlit view carries a provenance warning. Existing screenshots, notebooks, and source data are preserved.

## Publish

Upload the **contents of `dist/`** to a static host, including `data.js`, `domain.js`, styles, JSON, and the report. Relative URLs support hosting under a portfolio subdirectory. No build command is needed when publishing the committed artifact. CI builds and checks the site and produces a downloadable artifact; it does not publish automatically.

Do not publish the entire workspace: it contains original data, exploratory results, and unrelated local files. See [PUBLICATION.md](docs/PUBLICATION.md) for the release boundary and remaining browser check.
