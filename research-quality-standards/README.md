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

## Genre

`library_or_tooling`

## Summary

This repository defines reusable quality standards, reviewer instructions, maker prompts, templates, and lightweight linting for research, code, writing, README files, interviews, and LLM-assisted work.

## Quick Start

```bash
python ./scripts/check_readme.py README.md && python ./scripts/lint_mvp.py ./templates
```

**Expected output**

```text
README QUALITY CHECK
No issues found by static checker.
# MVP Lint Report
Files checked: 10
Errors: 0
```

## Environment

- Python: 3.11 or newer
- Node: 20.x only if you want to run `markdownlint-cli2`
- OS tested: Windows 11
- Install step: no package install is required for the Python checks beyond a stock Python runtime, because the scripts use the standard library only
- Lockfile: not currently included; rationale: the Python scripts use the standard library only and the Node lint step installs its CLI in CI
- System dependencies: none for the Python checks; Node only for markdown style lint

## Data And Inputs

- Main inputs:
  - standards files in `./standards/`
  - reviewer instructions in `./reviewer/`
  - templates in `./templates/`
  - target `README.md` files or other lintable files when the scripts are run
- Minimal example:
  - `./templates/` serves as the smallest built-in lint target set; `./examples/minimal/` is not needed for this repo because the repository is itself a standards and tooling library rather than an executable data pipeline
- Sensitive data:
  - not required for the built-in examples

## Outputs

- `./generated/lint/` when GitHub Actions or lint scripts write reports
- console output showing README findings or MVP lint findings

## Reproducibility

- The standards files are versioned in the repository.
- The Python README checker and MVP linter are deterministic for the same file contents.
- No model calls are required for the built-in static checks.

## Tests And Validation

- Run:
  - `python -m unittest scripts.tests.test_check_readme scripts.tests.test_lint_mvp`
- Smoke check:
  - the `Quick Start` command is the minimal integration check; passing means the README checker reports no issues and the template lint run completes without errors
- Coverage:
  - unit tests for the README checker and MVP linter
- Not covered:
  - live GitHub Actions execution
  - `markdownlint-cli2` local execution unless Node is installed

## Assumptions

- users will adapt the standards to their local workflow
- human review remains the final authority for policy changes

## Limitations And Risks

- standards are still evolving and may over- or under-specify some genres
- the README checker is static only and does not prove commands really run
- the markdown style lint step depends on Node when run outside GitHub Actions

## Not Included

- real credentials or secrets
- proprietary data
- project-specific lockfiles for every possible downstream environment

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
- `standards/readme.md`
- `standards/software_code.md`
- `standards/stats_code.md`
- `standards/statistical_results.md`
- `standards/writing.md`
- `standards/interviews.md`
- `standards/llm_agent_work.md`
- `reviewer/genre_classifier.md`
- `reviewer/readme_review.md`
- `reviewer/severity_levels.md`
- `reviewer/review_report_schema.md`
- `reviewer/code_review.md`
- `reviewer/interview_review.md`
- `reviewer/statistical_results_review.md`
- `reviewer/manuscript_review.md`
- `maker_prompts/*.md`
- `templates/*`
- `examples/README.md`
- `scripts/check_readme.py`
- `scripts/lint_rules_stub.yaml`
- `scripts/lint_mvp.py`
- `scripts/list_lint_targets.py`
- `.github/workflows/lint-mvp-changed-files.yml`
- `.github/workflows/readme-quality.yml`

## File Structure

```text
research-quality-standards/
|- standards/
|- reviewer/
|- maker_prompts/
|- templates/
|- examples/
|- scripts/
|  |- tests/
|- .github/
|  \- workflows/
|- README.md
|- CHANGELOG.md
```

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

## README Quality Check

The repository also includes a warning-first static README checker in `scripts/check_readme.py`.

Typical usage:

```powershell
python ./scripts/check_readme.py README.md
python ./scripts/check_readme.py README.md --strict
```

Default mode exits `0` and reports blocking issues and warnings without gating work. `--strict` exits `1` only when blocking issues are found.

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

It also includes `.github/workflows/readme-quality.yml`, which:

- runs markdown style lint on the top-level `README.md`
- runs the warning-first static README checker
- stays advisory by default
- can be made stricter later by switching the checker to `--strict`

## Troubleshooting

**Error:** `python: can't open file './scripts/check_readme.py'`  
**Context:** command run from the wrong directory  
**Fix:** run from the repository root or use the correct relative path

**Error:** `markdownlint-cli2: command not found`  
**Context:** local markdown style linting  
**Fix:** install Node 20 and run `npm install -g markdownlint-cli2`, or rely on the GitHub Action

## Contributing Or Workflow

- make focused changes by topic
- update `CHANGELOG.md` when standards change materially
- run the unit tests and relevant local checks before review
- use pull requests for coherent change sets when possible

## Contact Or Ownership

- Owner: project maintainer for the standards repo
- Review authority: human maintainer or PI-equivalent for policy changes

## License

- Internal working draft until a license is chosen

## Initial Scope

This version focuses on:

- general research quality
- README and project handoff quality
- software code
- statistical code
- statistical results presentation
- manuscripts and structured writing
- interviews and qualitative notes
- LLM and agent transparency

Slides, survey programming, policy briefs, and method-specific econometric modules can be added later.
