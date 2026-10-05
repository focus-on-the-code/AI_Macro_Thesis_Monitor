# P0-SETUP-001 — Phase 0 implementation handoff
Status: READY FOR IMPLEMENTATION. Phase 0 only. Read all source files and coordination documents from this repository; no private chat context is needed.

## Objective and boundaries
Create reproducible setup, approval controls and specification-freeze evidence. No Phase 1 UI, live collectors, deployment, paid services or account upgrades.
Use Build → Assess → Fix → Verify → Phase Report → Exit Gate.
Applicable IDs: FR-001, FR-003, FR-009, FR-015, FR-016, FR-017, FR-023; P0-T01–P0-T05.

## Tasks
1. Add Python requirements/lockfile, minimal hello module/test, lint configuration and README-only clean bootstrap instructions. Pin chosen dependencies. Add .gitignore and secrets example with variable names and empty values only.
2. Add CODEOWNERS for repository owner and an owner-review policy. Record actual branch-protection evidence separately; do not claim enforcement from files alone.
3. Add PR-triggered lint/tests/secret-scan CI skeleton with read-only permissions, no deployment or scheduled jobs. Prevent execution until zero-spend hosted Actions controls are confirmed; document the resulting CI exit blocker honestly. Do not enable paid Actions runners/overages.
4. Add a build-spec schema and validation against all seven PRD panels: names, metric definitions/formulas, page names and ticker mappings. Create formula-ID/status inventory with unresolved choices explicitly TBD. Preserve originals.
5. Add explicit cost/provider inventory with unapproved services disabled and potential costs marked APPROVAL REQUIRED. Keep market provider TBD.
6. Run P0-T01 from a clean clone/environment using README only; P0-T02 automated full-history secret scan plus manual secrets-example inspection; P0-T03 configuration/cost scan; P0-T04 schema and cross-document integrity. Record command, tested commit, result and evidence location, including failures and limits.
7. Update docs/verification/phase-0-report.md and docs/phase-status.md after each work unit. Submit reversible commits/PR with requirement/test mapping. Never report tests as passed without execution.
8. Fresh-agent P0-T05 is performed separately after artifacts exist: reconstruct phase, task, IDs, latest verification and blockers from repo only; persist result.

## Return contract
Provide branch/commit/PR links, changed files, actual test output, unresolved blockers and exact next task through repository artifacts.
Owner decisions are limited to genuine permission/account/paid-service/product blockers. No routine owner copy/paste.
Exit remains CLOSED until all deliverables/criteria pass and owner explicitly approves. A blocked gate does not authorize Phase 1.
