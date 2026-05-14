# Skills Index

## Purpose

This is the registry for reusable workflow skills and future plug-ins.

## Current status

Most skill directories are scaffolded. A small number now have repository-local `SKILL.md` files and can be used directly.

Use this index to distinguish:

- `active`: implemented and documented
- `integrated`: copied or adapted from an existing source and partly ready
- `planned`: scaffold only

## Skill registry

| Skill | Path | Status | Notes |
|---|---|---|---|
| `create_plan` | `skills/create_plan/` | active | Refines requirements, analyzes current structure, defines tests, and saves a step-by-step plan before execution. |
| `citation-auditor` | `skills/citation-auditor/` | active | Audits inline citations, bibliography coverage, DOI plausibility, journal style, and optionally claim-to-source support. |
| `unsupervised-overnight-execution` | `skills/unsupervised-overnight-execution/` | active | Runs long unattended work in an isolated workspace, verifies before promotion, and leaves a reviewable session record. |
| `review_weekly_goal` | `skills/review_weekly_goal/` | active | Reviews weekly goals or weekly reports for concrete deliverables, blocker honesty, and one-week feasibility. |
| `review_readme` | `skills/review_readme/` | active | Reviews repository README files with deterministic README checks first when available. |
| `review_python` | `skills/review_python/` | active | Runs Ruff for substantial Python changes when available and uses Black or mypy conditionally based on repository practice. |
| `review_statistical_results` | `skills/review_statistical_results/` | active | Reviews empirical outputs for provenance, interpretability, and claim-to-evidence alignment. |
| `review_survey` | `skills/review_survey/` | active | Reviews survey instruments for field readiness, implementation clarity, and analysis readiness. |
| `review_xlsx_workbook` | `skills/review_xlsx_workbook/` | active | Reviews workbook structure, formula safety, documentation, and auditability for spreadsheet artifacts. |
| `data_cleaning` | `skills/data_cleaning/` | planned | Data cleaning and validation workflows. |
| `pdf_table_extraction` | `skills/pdf_table_extraction/` | planned | Extract structured tables from PDFs. |
| `replication_verifier` | `skills/replication_verifier/` | planned | Re-run and compare replication artifacts. |
| `literature_review` | `skills/literature_review/` | planned | Evidence synthesis and source triage. |
| `regression_table_formatter` | `skills/regression_table_formatter/` | planned | Format and standardize regression tables. |
| `codebook_generator` | `skills/codebook_generator/` | planned | Build codebooks and variable dictionaries. |
| `blocker_triage` | `skills/blocker_triage/` | planned | Rapid diagnosis and escalation routing. |
| `task_decomposer` | `skills/task_decomposer/` | planned | Break large tasks into reviewable units. |

## Related utilities

Current integrated utilities that may later become skills:

- `scripts/utilities/gemini_referee_review.py`
- `scripts/validation/verify.py`
- `scripts/validation/detect_secrets.py`
- `scripts/validation/check_hidden_changes.py`
