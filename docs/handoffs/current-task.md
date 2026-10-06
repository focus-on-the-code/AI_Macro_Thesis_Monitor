# P0-FIX-002 — Reconcile Phase 0 handoff artifacts
Status: IN PROGRESS. Phase 0 only. Read all source files and coordination documents from this repository; no private chat context is needed.

## Objective and boundaries
Resolve the P0-T05 reconstruction finding: all active-task references and pending/completed evidence must agree. Then perform a new fresh-agent reconstruction against these updated artifacts.
No Phase 1 UI, live collectors, deployment, paid services or account upgrades.
Use Build → Assess → Fix → Verify → Phase Report → Exit Gate.
Applicable IDs: FR-001, FR-003, FR-009, FR-015, FR-016, FR-017, FR-023; P0-T01–P0-T05.

## Tasks
1. Keep docs/phase-status.md, this handoff, and docs/verification/phase-0-report.md aligned on the sole active task: P0-FIX-002.
2. Record that enabled PR CI passed on PR #4 and that the phase0 check is required on main.
3. Run P0-T05 in a fresh agent session with only repository access. It must identify Phase 0, P0-FIX-002, the applicable IDs, current evidence, and remaining owner-only exit approval without relying on private chat.
4. Persist the result in docs/verification/, update the phase status and report, and open a PR. Its required phase0 check must pass.
5. After merge, present the complete evidence to the owner for an explicit Phase 0 exit decision. A passing test suite does not authorize Phase 1 by itself.

## Return contract
Provide branch/commit/PR links, changed files, actual test output, unresolved blockers and exact next task through repository artifacts.
Owner decisions are limited to genuine permission/account/paid-service/product blockers. No routine owner copy/paste.
Exit remains CLOSED until all deliverables/criteria pass and owner explicitly approves. A blocked gate does not authorize Phase 1.
