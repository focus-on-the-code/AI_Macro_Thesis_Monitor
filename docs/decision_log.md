# Decision log
## D000 — Scope and authority
2026-10-04 owner request: execute Phase 0 only; Work coordinates and Codex implements; repository/GitHub artifacts are the shared state; no paid services; owner must approve exit before Phase 1.
Written v0.91 PRD/YAML prevail over illustrative mockup values/tickers.

## D001 — Market data
TBD, disabled. Prefer free delayed/EOD; verify licensing, caching and display rights before Phase 4. Paid feeds/real-time entitlements: APPROVAL REQUIRED.

## D002 — Visibility
Private development confirmed by GitHub metadata. No deployment/public release authorized. Production visibility TBD, owner decision before launch.

## D003 — Retention
Engineering baseline proposal: small curated Parquet and provenance in git; raw snapshot retention/size thresholds explicitly TBD before collectors. Do not delete existing data or add object storage. Recurring storage cost: APPROVAL REQUIRED.

## D004 — Cost controls
Paid API, premium news, LLM API, paid hosting, object storage, Actions overages and paid runners: APPROVAL REQUIRED; disabled/unapproved.
GitHub account spending/overage controls cannot be inferred from repository files. Verify a zero-spend limit before hosted CI runs; use local verification while that remains unverified. No service signup or billing change is authorized.

## D005 — Definition freeze
The seven panel names, questions, metric definitions, ticker lists and four page names in v0.91 are baseline definitions.
Formula IDs are absent from the supplied YAML: implement a traceable Phase 0 inventory with stable IDs or explicit TBD, without changing economic definitions. Unspecified basket membership/base dates, source mappings, windows and units must remain explicit TBD.
Preserve fiscal receipts-minus-outlays convention; do not silently flip the deficit sign. Preserve the distinction between percent yield and basis points.

## D006 — Visual review
Coordinator successfully reviewed dashboard_mockup.jpeg (blob e8895dc802d9f3793a4535b146c77f5cf447bb53) as the owner-provided alternative after the PNG reader failed.
Approved hierarchy: four-page navigation, regime strip, seven distinct panels with ticker rows/interpretations/calculation controls/source timestamps, then market performance/evidence/thesis.
Illustrative discrepancies: JPEG ticker lists differ from PRD; private companies appear as ticker chips; V1 plot legend/directions conflict with headline deltas; credit-spread chart heading refers to yields; some dual axes require justification. Use written specifications and future fixture labels, not mockup numbers or unsupported live claims.
The JPEG itself ends at the lower section; no unseen content is inferred. PNG was not independently decoded.

## D007 — Repository governance
main is currently unprotected. CODEOWNERS/owner-review policy must be added, but a text policy does not substitute for enforced branch protection. Required protection: PR review and passing checks, no force pushes/deletions, least privilege. If plan/permissions prevent enforcement, record BLOCKED and ask owner; do not enable a paid tier or waive the deliverable.
