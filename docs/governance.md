# Owner review and cost controls
All changes use branches and draft PRs with requirement/test IDs and evidence. Owner review is required before merge; never self-approve a phase exit. CODEOWNERS is a routing policy, not enforcement.

The owner confirmed public visibility and configured branch protection on `main`. GitHub branch metadata now reports `protected=true`. The rule requires a pull request and one approval, prevents force pushes/deletions, and does not allow bypass. CODEOWNERS is still a routing policy; the protection rule supplies enforcement.

The owner confirmed a $0 GitHub Actions budget/overage limit. The PR workflow is enabled with read-only contents permission, pinned actions, full-history checkout, and no deployment or scheduled jobs. It does not enable paid runners or any paid data/service. A successful PR run is still required before a status check can be selected as required in the GitHub rule.

Every service in config/services.json is disabled, including free candidates; no collectors are implemented. Potential costs are APPROVAL REQUIRED. Credentials remain local/approved secret stores. .env.example contains names and empty values only. Product provider, visibility and retention decisions remain in decision_log.md.
