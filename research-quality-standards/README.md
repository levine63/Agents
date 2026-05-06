# Research Quality Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06

This repository contains reusable quality standards for research assistants, interns, and AI agents.

The goal is not to make prompts longer. The goal is to make standards:

- versioned
- diffable
- testable
- reviewed
- easier to comply with through templates and positive examples

## Core Design

This repository is organized into five layers:

1. `standards/`
   Canonical policy. These files define what good work requires.
2. `reviewer/`
   Longer reviewer instructions for LLM referees or human reviewers.
3. `maker_prompts/`
   Shorter prompts for generators. These are intentionally compact.
4. `templates/` and `examples/`
   Compliance aids that make the right structure the default.
5. `scripts/`
   Deterministic lint policies and future checker scripts.

## Guiding Principles

- Standards should live in files, not in giant prompts.
- Review should be separate from generation.
- Deterministic checks should replace vague prompt reminders whenever possible.
- LLM review should cite concrete violations, not vague impressions.
- Repeated failures should trigger a standards update, template improvement, or new lint rule.

## Standard Workflow

```text
Task arrives
  ->
Artifact genre and stage are declared or inferred
  ->
Maker loads the shortest relevant prompt and template
  ->
Artifact is produced
  ->
Deterministic lint runs when feasible
  ->
Reviewer loads general standards plus 1 to 3 genre standards
  ->
Reviewer produces a structured report
  ->
Author or agent repairs blocking issues
  ->
Final output records unresolved cautions
```

## Repository Layout

- `CHANGELOG.md`
- `standards/constitution.md`
- `standards/general.md`
- `standards/software_code.md`
- `standards/stats_code.md`
- `standards/statistical_results.md`
- `standards/writing.md`
- `standards/interviews.md`
- `standards/llm_agent_work.md`
- `reviewer/genre_classifier.md`
- `reviewer/severity_levels.md`
- `reviewer/review_report_schema.md`
- `reviewer/code_review.md`
- `reviewer/interview_review.md`
- `reviewer/statistical_results_review.md`
- `reviewer/manuscript_review.md`
- `maker_prompts/*.md`
- `templates/*`
- `examples/README.md`
- `scripts/lint_rules_stub.yaml`
- `scripts/lint_mvp.py`
- `scripts/list_lint_targets.py`
- `.github/workflows/lint-mvp-changed-files.yml`

## Governance

- Every standards file must carry a version and last-updated date.
- `standards/constitution.md` is the highest-level policy layer and should change rarely.
- Substantive changes to standards should update `CHANGELOG.md`.
- Standards should be reviewed by a human before being treated as canonical.
- Deterministic lint rules should cover stable, high-confidence checks.
- LLM reviewers should focus on issues deterministic lint cannot judge well.

## MVP Lint

The repository now includes a small deterministic linter in `scripts/lint_mvp.py`.

Current MVP checks:

- Python: provenance header, module docstring, bare `except`, likely personal paths, seed when randomness appears
- Stata: provenance header, `version`, `set more off`, likely personal paths, seed when stochastic commands appear
- Markdown writing artifacts: provenance header, `Not Yet Done`, placeholder text, unfinished citation markers

Typical usage:

```powershell
python ./scripts/lint_mvp.py ./templates --json-out ./reports/lint.json --md-out ./reports/lint.md
```

Exit code is `1` when any `ERROR` is found and `0` otherwise.

## GitHub Actions

The repository includes a workflow at `.github/workflows/lint-mvp-changed-files.yml`.

It:

- runs on pull requests
- runs on pushes to `main`
- supports manual dispatch with a required `base_ref`
- detects changed lintable files only
- skips unsupported or generated files
- runs `lint_mvp.py` only on the changed targets
- uploads JSON and Markdown reports as workflow artifacts

## GitHub Workflow Notes

If you want a very short reminder of the branch and PR workflow, see [PULL_REQUEST_CHEAT_SHEET.md](./PULL_REQUEST_CHEAT_SHEET.md).

## Initial Scope

This version focuses on:

- general research quality
- software code
- statistical code
- statistical results presentation
- manuscripts and structured writing
- interviews and qualitative notes
- LLM and agent transparency

Slides, survey programming, policy briefs, and method-specific econometric modules can be added later.
