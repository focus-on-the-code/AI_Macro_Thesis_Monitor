# AGENTS.md

## Purpose

This file defines how agents should operate inside the
`AI_Macro_Thesis_Monitor` repository.

Keep routine context small.

Do not reread the full PRD or build specification for every task.
Use progressive loading:

1. Read this file.
2. Read `docs/phase-status.md`.
3. Read `docs/handoffs/current-task.md`.
4. Consult only the relevant PRD/build-spec sections referenced by the current task.
5. Read broader project documentation only when requirements are ambiguous or the task requires it.

---

## Source of truth

Product requirements are defined in:

- `AI_Macro_Thesis_Monitor_PRD_v0.91.md`
- `AI_Macro_Thesis_Monitor_Agent_Build_Spec_v0.91.yaml`

The approved design direction is:

- `dashboard_mockup.jpeg`

Current project state is defined in:

- `docs/phase-status.md`
- `docs/handoffs/current-task.md`
- `docs/decision_log.md`
- `docs/verification/`

If these sources conflict:

1. Current owner-approved decisions take precedence.
2. Then the current PRD.
3. Then the machine-readable build spec.
4. Then older implementation artifacts.

Do not silently resolve material conflicts. Record them and escalate if needed.

---

## Operating model

The default roles are:

- **Owner:** product decisions, credentials, permissions, paid-service approval, and unresolved human-judgment decisions.
- **Coordinator:** ChatGPT Work or equivalent. Owns planning, phase orchestration, task delegation, acceptance criteria, and phase-gate decisions.
- **Implementation agent:** Codex or equivalent. Owns repository changes, tests, debugging, and implementation evidence.
- **Sub-agents:** scoped research, validation, file edits, test execution, and other delegated work.

The GitHub repository is the shared state layer.

Do not depend on another agent's private chat history.

Do not require the owner to manually copy/paste routine prompts, results, test output, or status between agents.

Persist routine handoffs in repository files, commits, pull requests, issues, CI output, or other GitHub artifacts.

---

## Required workflow

Work one phase at a time.

Use this loop:

**Build -> Assess -> Fix -> Verify -> Phase Report -> Exit Gate**

Do not advance to the next phase until the current phase's required tests and exit criteria pass.

If verification fails:

1. identify the failure,
2. create a scoped fix task,
3. implement the fix,
4. rerun the affected tests,
5. update verification evidence.

Do not present incomplete work as phase-complete.

---

## Before starting a task

Read:

- `AGENTS.md`
- `docs/phase-status.md`
- `docs/handoffs/current-task.md`

Then consult only the PRD/build-spec sections referenced in `current-task.md`.

Before modifying code, confirm that the task defines:

- active phase,
- scope,
- relevant requirement IDs,
- relevant test IDs,
- expected outputs,
- known blockers or constraints.

If these are missing or contradictory, stop and resolve the task definition before implementation.

---

## Model and reasoning policy

Agents and subagents use the lowest-cost model that can reliably satisfy the task's acceptance criteria.

### Tier 1 — routine work

Use:

- `gpt-5.6-terra`
- `reasoning_effort: low`

Typical tasks:

- routine file edits,
- documentation updates,
- repository searches,
- formatting,
- straightforward data extraction,
- running existing tests,
- simple source checks,
- repetitive validation.

### Tier 2 — normal implementation

Use a workhorse model with medium reasoning for:

- multi-file implementation,
- cross-document validation,
- nontrivial refactoring,
- ordinary debugging,
- integration work,
- writing new tests,
- implementation requiring moderate judgment.

### Tier 3 — escalation

Use a stronger model with high reasoning only when the task involves:

- architecture,
- security,
- secrets handling,
- ambiguous or conflicting requirements,
- financial-calculation methodology changes,
- difficult debugging,
- repeated verification failure,
- consequential schema or data-model changes.

If the same scoped task fails verification twice at its current tier, escalate one tier.

Do not use a higher-cost model merely because it is available.

Record the model tier and reasoning level used for delegated tasks in the handoff and phase verification report.

---

## Cost policy

This project is free-first.

Do not enable or purchase:

- paid APIs,
- paid hosting,
- licensed real-time market data,
- premium news feeds,
- managed databases,
- other paid services

without explicit owner approval.

If a paid service appears necessary:

1. document why,
2. identify free alternatives,
3. explain cost and tradeoffs,
4. stop and request owner approval.

---

## Secrets and security

Never commit:

- API keys,
- passwords,
- access tokens,
- private credentials,
- secret environment values.

Use approved secret stores such as:

- GitHub Actions Secrets,
- Streamlit Secrets,
- environment variables.

Example files may contain variable names only, never live values.

If a secret is discovered in repository history, stop normal work and treat it as a security issue.

---

## Product rules

The dashboard is a research and decision-support tool.

It is not investment advice and does not execute trades.

Maintain these product requirements:

- seven core variables remain separate;
- Energy and Labor must not be merged;
- relevant market instruments belong inside or next to each variable panel;
- every derived metric must expose its calculation;
- every displayed metric must show source and timing information;
- every panel must include a concise plain-language interpretation;
- contradictory evidence must remain visible;
- do not create an opaque master buy/sell or risk score;
- primary evidence outranks commentary;
- estimates and claims must be labeled as such;
- revisable macro data must preserve vintage/revision awareness where required;
- failed data sources must degrade gracefully rather than crash the app;
- do not add personality-specific market thresholds such as an "Eisman watch level."

Consult the PRD for exact formulas, data sources, panel definitions, and acceptance criteria.

---

## Data and evidence discipline

For displayed metrics, preserve where applicable:

- raw value,
- transformed/calculated value,
- unit,
- observation date,
- retrieval date,
- source,
- source URL or endpoint,
- source identifier/series/XBRL tag,
- revision/vintage status,
- calculation formula.

Evidence items must distinguish:

- `PRIMARY / VERIFIED`
- `SECONDARY / ESTIMATE`
- `THESIS / CLAIM`

Hypothesis impact may be:

- `SUPPORTS`
- `COUNTERS`
- `AMBIGUOUS`

Do not convert estimates or commentary into verified facts.

Do not infer causation from correlation without supporting evidence.

---

## Changes to formulas or methodology

Do not silently change:

- formulas,
- source hierarchy,
- signal logic,
- metric definitions,
- evidence classification rules,
- interpretation methodology.

If a change is necessary:

1. document the proposed change,
2. explain the reason,
3. identify affected requirements/tests,
4. update `docs/decision_log.md`,
5. obtain owner approval when the change is material.

---

## Repository coordination files

Maintain:

- `docs/phase-status.md`
- `docs/handoffs/current-task.md`
- `docs/decision_log.md`
- `docs/verification/<phase>-report.md`

`phase-status.md` should stay concise and include:

- active phase,
- phase status,
- latest verified milestone,
- blockers,
- next action.

`current-task.md` should stay scoped and include:

- task objective,
- relevant requirement IDs,
- relevant test IDs,
- files likely affected,
- constraints,
- expected outputs,
- model tier if delegated.

Do not use these files as long-form project diaries.

---

## Verification and reporting

Every phase must end with a verification report.

At minimum, record:

- phase,
- requirements tested,
- tests run,
- pass/fail results,
- defects found,
- fixes applied,
- remaining blockers,
- cost/service changes,
- model-tier exceptions,
- final exit-gate status.

A failed P0/P1 or phase-blocking test prevents phase completion.

---

## Fresh-agent handoff rule

A fresh implementation agent with repository access and no prior chat context must be able to determine:

- the active phase,
- the current task,
- applicable requirement IDs,
- applicable test IDs,
- latest verification status,
- blockers,
- next expected action.

If it cannot, the repository handoff state is incomplete.

Fix the handoff documentation before continuing.

---

## Owner escalation

Ask the owner only when necessary for:

- credentials or permissions,
- paid-service approval,
- unresolved product decisions,
- external-account actions,
- security issues,
- material methodology changes,
- genuine ambiguity that cannot be resolved from repository sources.

Do not escalate routine implementation choices that fall within approved requirements.

---

## Final rule

Optimize for:

**correctness, traceability, reproducibility, low unnecessary cost, and minimal owner coordination overhead.**

When uncertain, prefer a small verified change over a large speculative one.