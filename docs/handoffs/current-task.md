# P0-EXIT-001 — Phase 0 verification closeout
Status: READY FOR FINAL VERIFICATION. Phase 0 only. Read all source files and coordination documents from this repository; no private chat context is needed.

## Objective and boundaries
Verify the merged setup, approval controls and specification-freeze evidence. No Phase 1 UI, live collectors, deployment, paid services or account upgrades.
Use Build → Assess → Fix → Verify → Phase Report → Exit Gate.
Applicable IDs: FR-001, FR-003, FR-009, FR-015, FR-016, FR-017, FR-023; P0-T01–P0-T05.

## Tasks
1. Review and merge the closeout PR. Do not begin Phase 1.
2. Confirm enabled PR CI passes. Once it has a successful check, select that check as required in the `main` branch rule.
3. Run P0-T05 in a fresh agent session with only repository access. Persist its reconstruction of phase, task, IDs, results, and blockers in `docs/verification/`.
4. Update this handoff, the phase status, and the Phase 0 report with the CI and final P0-T05 result.
5. Present the complete Phase 0 evidence to the owner for an explicit exit decision. A passing test suite does not authorize Phase 1 by itself.

## Return contract
Provide branch/commit/PR links, changed files, actual test output, unresolved blockers and exact next task through repository artifacts.
Owner decisions are limited to genuine permission/account/paid-service/product blockers. No routine owner copy/paste.
Exit remains CLOSED until all deliverables/criteria pass and owner explicitly approves. A blocked gate does not authorize Phase 1.
