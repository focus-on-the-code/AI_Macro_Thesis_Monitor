# AI / Macro Thesis Monitor - PRD handoff bundle

Version 0.91 | October 4, 2026

This bundle contains the approved pre-build specification for the AI / Macro Thesis Monitor.

## Files
- `AI_Macro_Thesis_Monitor_PRD_v0.91.docx` - human-readable PRD
- `AI_Macro_Thesis_Monitor_PRD_v0.91.md` - LLM/agent-friendly PRD
- `AI_Macro_Thesis_Monitor_Agent_Build_Spec_v0.91.yaml` - machine-readable panels, requirements, roadmap, coordination contract and tests
- `dashboard_mockup.png` - approved visual direction

## Builder rule
Work one phase at a time using **Build -> Assess -> Fix -> Verify -> Phase Report -> Exit Gate**. Do not advance until the phase exit criteria pass. Do not connect a paid service without explicit owner approval.

## Work / Codex coordination rule
The default operating model is **Work (or equivalent) as coordinator** and **Codex (or equivalent) as implementation agent**. The GitHub repository and GitHub artifacts are the shared state layer.

Do **not** rely on one agent having access to another agent's private chat history, and do **not** require the owner to copy/paste routine prompts, implementation results, tests, or status between agent chats.

The implementation repo must persist, at minimum:
- `docs/phase-status.md`
- `docs/handoffs/current-task.md`
- `docs/verification/<phase>-report.md`
- `docs/decision_log.md`
- relevant commits, pull requests/issues, CI results, and artifacts

Before a phase exits, run **P0-T05 / the fresh-agent handoff test**: a fresh implementation-agent session with repo access but no prior coordinator chat must be able to identify the active phase, current task, applicable requirement/test IDs, latest verification status, and blockers without owner relay.

Owner intervention is reserved for credentials/permissions, paid-service approval, unresolved product decisions, external-account actions, or blockers that genuinely require human judgment.
