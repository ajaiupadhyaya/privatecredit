# Publication handoff

## Hosting

The publication destination is https://ajaiupadhyaya.github.io/privatecredit/. The GitHub Actions workflow `.github/workflows/publish.yml` runs the Python and Node checks before deploying only `dist/` on pushes to `main`. Both project repositories are saved to their existing GitHub remotes.

## Deliverable

Publish only `dist/`. It contains the HTML application, local styles and scripts, aggregate research JSON, and standalone credit-risk report. All paths are relative; it can live at `/research/credit/` as well as a site root. The built artifact needs no server-side runtime, build service, API keys, or database.

The source database, raw loans, row-level predictions, environment files, screenshots, and unrelated usage export are not included. The research JSON carries aggregate model diagnostics and source hashes.

## Release approval

The user reviewed the delivered work and approved it as ready for publishing on 29 October 2026. All deliverables are saved locally. Automated browser verification remains unperformed for the environment reasons recorded in the audit; the following checklist is retained for future releases.

## Browser checklist for future releases

This environment could run numerical and packaging checks but could not open a browser preview. On a machine with normal local preview access:

1. Open `dist/index.html` or run the README's localhost command.
2. Inspect at 1536×1024 and 390×844. Check for horizontal overflow.
3. Switch all three tabs and verify direct links with `#loans` and `#liquidity`.
4. Change index/drawdown and full/recent windows; inspect data table.
5. Switch ROC/calibration, sector sorting, and all stress scenarios.
6. Set liquidity request to 0%, then 100% with 75% haircut; verify zero-request and insolvency messages; reset.
7. Open/close methodology with keyboard and Escape; check focus return.
8. Expand all research notes; download JSON and open the standalone report.
9. Compare the desktop render with `docs/design-concept.png`, allowing the documented data-driven differences.

## Suggested portfolio description

**Credit Observatory — interpretable credit risk research**

Built a reproducible research experience connecting listed BDC market proxies, a 50,000-loan synthetic classification experiment, and an interactive liquidity stress model. Replaced permissive exploratory validation with a chronological holdout and training-only preprocessing. Implemented auditable redemption accounting, model diagnostics, explicit provenance, and a self-contained static publication.

The synthetic experiment reports holdout AUCs of 0.877 and 0.882. These are methodological results, not real-world investment performance. Market data are archived and unverified; this project makes no current-market claims.
