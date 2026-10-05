# Owner review and cost controls
All changes use branches and draft PRs with requirement/test IDs and evidence. Owner review is required before merge; never self-approve a phase exit. CODEOWNERS is a routing policy, not enforcement.

main protected=false was observed. Rulesets GET returned 403 with upgrade/public-repository guidance. Legacy protection GET returned 403 Resource not accessible by integration. Private/free boundaries remain unchanged; do not infer all protection options require payment. Owner must resolve enforceable protection through authorized account controls. No upgrade or public conversion is authorized.

Hosted CI is deliberately blocked with literal `if: ${{ false }}`. PR events may create skipped workflow records but no jobs allocate runners. This does NOT pass the CI exit criterion. Before enabling, persist owner-verified zero-overage controls and plan/quota evidence, review pinned actions, then separately approve removal of the literal gate. Do not replace it with an unchecked repository variable. Required checks must be selected after real CI succeeds. Configure required owner review, no force pushes/deletions, and least privilege where available.

Every service in config/services.json is disabled, including free candidates; no collectors are implemented. Potential costs are APPROVAL REQUIRED. Credentials remain local/approved secret stores. .env.example contains names and empty values only. Product provider, visibility and retention decisions remain in decision_log.md.
