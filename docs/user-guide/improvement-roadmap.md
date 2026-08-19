# How To Make EduHarness Better

This section is the practical roadmap to move from a strong prototype to a robust production/research platform.

## 1) Remove hardcoding first (highest priority)

## Model runtime
- Replace fixed model initialization with registry-based runtime selection.
- Add active model key environment variable + validation.

## Teacher queue and class data
- Replace in-memory queue with database-backed escalation records.
- Replace static student list and static mastery with DB-derived aggregates.

## Sessions and metrics
- Replace demo session list with queryable session store.
- Ensure all KPI cards read from computed metrics artifacts or DB.

## 2) Improve governance maturity

- Add escalation ownership/assignment for multi-teacher workflow.
- Add SLA fields (opened_at, resolved_at, response_time).
- Add policy versioning and rollback history.
- Add action rationale requirements for sensitive overrides.

## 3) Improve pedagogy quality

- Strengthen mastery estimator beyond keyword/heuristic inference.
- Add concept dependency-aware scaffolding decisions.
- Add long-horizon progress plans per student.

## 4) Improve evaluation rigor

- Add run manifests: model/harness/data/hash seed versions.
- Add confidence intervals and significance testing in result pages.
- Add direct compare view: model-only gain vs harness-only gain.

## 5) Improve frontend product quality

- Add authentication and role-based access control.
- Add robust error UX and retry actions.
- Add charting and filtering capabilities.
- Add accessibility checks and keyboard-first navigation.

## 6) Improve operations

- Move SQLite local prototypes to Postgres for shared environments.
- Add background job queue for long-running experiments.
- Add structured logging, traces, and health dashboards.

## Suggested next sprint

1. Runtime model config (registry-driven)
2. DB-backed teacher queue + actions
3. Dynamic student/session APIs
4. Research run config matrix (multi-model x multi-harness)
5. Dashboard KPI cards sourced from real data
