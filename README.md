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


## Phase 0 bootstrap (Python 3.12, Git)
Authenticate Git with repository access using your approved credential manager. No API keys are needed. From a new directory:

```sh
git clone https://github.com/focus-on-the-code/AI_Macro_Thesis_Monitor.git
cd AI_Macro_Thesis_Monitor
git switch codex/phase-0-setup
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m monitor
python -m unittest discover -s tests -v
python -m ruff check .
python scripts/validate_phase0.py
python scripts/scan_secrets.py --history
```

Requirements pin all direct/transitive Phase 0 tools. No application service is connected. Windows activation: `.venv\Scripts\activate`. Use `python` for venv creation if that command is Python 3.12. Scan output is redacted; never paste a suspected credential. The custom scanner is heuristic (key prefixes/private keys/credential assignments), so review detections securely and supplement with an approved comprehensive scanner before declaring history clean. `python scripts/scan_secrets.py` scans only current files, never substitutes for the full-history test.

See `docs/governance.md` for owner review and the literal-false hosted CI gate; local checks do not count as a hosted CI pass. See `docs/verification/phase-0-report.md` for actual results and blockers. Schema scope validates the whole build-spec top-level structure and strict panel/metric/page shape; untouched future-phase payloads are preserved by source hashes. Cross-document checks compare every panel metric definition and ticker mapping directly to the PRD. Formula details remain explicitly TBD in `registry/formula-inventory.json` and `docs/formula-freeze.md`.

## Phase 1 local fixture UI

Python 3.12 is recommended. From the repository root, install the pinned free dependencies in a virtual environment and run:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use the sidebar to reach Dashboard, Evidence, About, and Definitions & Methodology. This is a local, fictional fixture preview: it makes no source requests, has no market quotes or live evidence, and must not be used for investment decisions. The seven dashboard panels disclose example inputs and the frozen formula definitions; source mappings and production calculations remain future-phase work. Run the Phase 1 structural checks with `python -m unittest discover -s tests -v`.
