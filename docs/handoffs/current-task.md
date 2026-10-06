# P2-FOUNDATION-001 — Provenance, calculations and methodology foundation
Status: IMPLEMENTATION VERIFIED LOCALLY; P2-T01–P2-T05 and CI-equivalent checks pass; Phase 2 exit gate CLOSED pending review.

## Required first action
Before reading or modifying any code, the implementation agent must read:
1. `AGENTS.md`
2. `docs/phase-status.md`
3. this file
Then consult only the Phase 2 sections of `AI_Macro_Thesis_Monitor_Agent_Build_Spec_v0.91.yaml` and the relevant metric definitions in the PRD.

## Objective and scope
Build the transparent foundation before connecting live sources:
- canonical metric registry with stable IDs, names, units, raw/derived type, formula metadata, source priority and cadence;
- calculation functions with explicit validation and unit handling;
- provenance records linking displayed/derived values to raw input IDs, source URL, observed_at, retrieved_at and vintage/revision state;
- data-quality flags and lineage display usable by the existing UI;
- Definitions & Methodology content generated from the same registry;
- CI/test guards preventing registry/code/spec drift.

Requirements: FR-003, FR-011, FR-012, FR-013, FR-014, FR-015, FR-018, FR-019, FR-021, FR-022, FR-023.
Tests:
- P2-T01 Formula unit tests: normal, zero, negative and missing inputs; explicit divide-by-zero behavior.
- P2-T02 Lineage round-trip: derived metric traces to all raw inputs and transformations.
- P2-T03 Registry drift: changing a formula without updating the registry snapshot fails CI.
- P2-T04 Units: basis points/percent/fraction variants are rejected or explicitly normalized.
- P2-T05 Methodology completeness: every Dashboard metric has definition, formula or raw-metric label, source and cadence.

## Constraints
- Read `AGENTS.md` before building; record this in the verification report.
- Preserve the seven-panel definitions and existing fixture behavior.
- Do not connect live sources, paid APIs, deployment, accounts or credentials.
- Do not silently change formulas, source hierarchy, signal logic or economic definitions.
- Do not create a master score or investment recommendation.
- Keep changes scoped; prefer small composable modules and tests.
- Use Tier 2 normal implementation reasoning for the main build. Use Tier 1/low reasoning for routine scans/docs; escalate only for architecture, security, methodology ambiguity, or repeated verification failure.

## Expected outputs
Implementation code and tests; generated methodology output or renderer; drift/coverage validation; updated README/run instructions if needed; `docs/verification/phase-2-report.md`; updated status and decision log; PR with passing Phase 0 and Phase 2 checks.

## Current verification handoff
Implementation is on `codex/phase-2-implementation`. All 13 `unittest` tests, Ruff, `scripts/validate_phase0.py`, secret-history scan and `git diff --check` pass. See `docs/verification/phase-2-report.md`. Next: review and close the gate through owner/coordinator approval.
