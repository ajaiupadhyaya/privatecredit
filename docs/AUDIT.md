# Completion audit — 29 October 2026

## Assessment

The project contained a large exploratory Streamlit dashboard, a saved SQLite database, unfinished analytics modules, an untouched Next.js starter, and no substantive reproduction documentation. It was not publication-ready.

## Implemented route

The canonical portfolio is a static research application with three views. A no-network build consumes the existing price snapshot and a bundled validated summary from the companion creditrisk project. The original data and research assets remain intact.

| Finding | Resolution |
|---|---|
| Frontend was a starter template | Replaced with a self-contained editorial research application |
| BDC index averaged nominal share prices | Canonical index compounds equal-weight daily returns over common dates |
| Silent synthetic macro substitution | Disabled by default; unverified bundled macro excluded from portfolio |
| No original price provenance | Explicit unverified label, exact window, source hash, methodological limitations |
| Fragility warmup filled with a neutral score | Warmup remains missing rather than inventing a signal |
| Redemption model multiplied payouts by sale price and overpaid final requests | Assets sold = cash paid / realization price; partial payments, exhaustion, unpaid requests tracked |
| CSV output was an implicit side effect | Liquidity output path is optional and explicit |
| Loan-model evidence mixed with exploratory scores | Newly generated chronological holdout evidence bundled from creditrisk |
| Missing packaging and documentation | Built dist, pinned requirements, tests, CI, publication guide, standalone report |

## Verification actually completed

- Built the static distribution from 1,680 common-date price observations and aggregate results for 50,000 synthetic loans.
- Ten Python tests pass (liquidity accounting, invalid inputs, insolvency, common-date basket construction).
- Seven Node tests pass, including 3,024 slider combinations and cross-language reference agreement.
- Four companion creditrisk tests pass.
- JavaScript syntax checks pass.
- Publication packaging test verifies local linked assets and absence of remote JavaScript dependencies.
- Full companion analysis rerun twice: all six output hashes match. Random-forest evaluation uses a single worker to eliminate floating-point accumulation order differences.
- Source hashes and library versions are recorded in `dist/research.json`.

## Verification blocked, not claimed

The built-in browser rejects file URLs. A localhost server requires sandbox escalation; the automatic approval reviewer failed because its selected model was at capacity. The same failure prevented dependency installation, which was resolved for canonical work by using available Python libraries and eliminating frontend dependency requirements.

No workaround browser or alternate execution surface was used to evade those restrictions. Browser rendering, desktop/mobile visual inspection, keyboard workflow execution, and download behavior remain unverified. There is no claim of 10/10 concept fidelity or visual sign-off.

## Design record

`design-concept.png` is the built-in Image Gen concept: white financial-editorial layout, large serif heading, thin gray rules, green line chart, open metric row, right-hand interpretation, and three research-note disclosures. The prompt specified the entire compact dashboard rather than an isolated hero.

Intentional implementation differences: actual observation years replace illustrative 2018–2026; real snapshot data replaces the concept's sketched line; measure/date selectors and inspectable tables were added to make the chart functional; model diagnostics and liquidity controls implement the additional views; provenance and downloadable evidence are explicit.

| Comparison point | Implementation evidence | Visual status |
|---|---|---|
| Copy hierarchy | Same headline, subheading, tabs, market chart title, research-note titles | Awaiting render comparison |
| Layout | Header, open metric row, 3.2:1 chart/sidebar split, horizontal notes | Awaiting render comparison |
| Typography | Georgia serif; 82px maximum headline; compact sans-serif analytical controls | Awaiting render comparison |
| Palette | White, near-black, gray rules, emerald #005c3e | Awaiting render comparison |
| Container treatment | No card grid, shadows, raster UI, or decorative gradients | Awaiting render comparison |
| Responsive layout | 680px breakpoint stacks analysis and controls; table scrolling | Awaiting mobile inspection |

## Scope retired rather than misrepresented

Legacy Streamlit, live fetchers, fragility heuristics, notebooks, and the companion 600-loan experiment are exploratory materials. They are not required to build or view the canonical portfolio, and their old numerical conclusions are not presented as validated evidence.
