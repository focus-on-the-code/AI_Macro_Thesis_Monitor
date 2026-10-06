# P1-UI-001 — Fixture-backed Streamlit dashboard shell
Status: READY FOR IMPLEMENTATION. Phase 1 only; do not begin Phase 2.

## Objective and boundaries
Recreate the approved dashboard information architecture and hierarchy with local fixture data before connecting any live source.
Build a Streamlit app with Dashboard, Evidence, About, and Definitions & Methodology pages; a Current Market & Macro Regime strip; and seven separate V1–V7 panels. Each panel must contain directly adjacent ticker/proxy rows, a chart placeholder, concise interpretation, calculation disclosure, source/timing metadata, and usable stale/unavailable fixture state.
Do not add live collectors, deployment, accounts, paid services, credentials, financial recommendations, opaque master scores, or personality-specific threshold markers.

## Applicable requirements and tests
Requirements: FR-001, FR-002, FR-003, FR-004, FR-005, FR-008, FR-009, FR-010, FR-011, FR-014, FR-015, FR-021, FR-022, FR-023.
Tests: P1-T01 Navigation; P1-T02 Panel inventory; P1-T03 Ticker proximity; P1-T04 Disclosure controls; P1-T05 Responsive smoke; P1-T06 Stale/unavailable state.

## Expected implementation outputs
- Pinned free Streamlit dependency and a documented local run command.
- Fixture module/data covering all seven panel states, including at least one stale and one unavailable state.
- App/pages/components and tests for page/panel/disclosure/state inventory.
- Persistent research-not-investment-advice disclosure and basic keyboard/readability/responsive design.
- Updated Phase 1 report with commands/output, defects/fixes, cost/service changes (expected: none), and gate status.

## Verification and handoff
Use Build → Assess → Fix → Verify → Phase Report → Exit Gate.
Run the six P1 tests; use a browser/rendered visual check for ticker proximity, disclosures and responsive widths where feasible. Record limitations honestly.
Before opening a PR, update this task, phase status and docs/verification/phase-1-report.md with the actual branch/commit, results, blockers and next action.
Delegation model tier: Tier 2 (normal implementation); use the lowest-cost available workhorse model with medium reasoning. Tier 1/low may be used for isolated formatting or routine checks.
