# Statistical Code Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related template: [stata template](../../../templates/code/stata/template.do)
Related examples: `examples/README.md`
Lint opportunities: seed, data source note, N-logging markers, merge checks, stochastic command detection
See also: `docs/glossary.md` for terms such as `unit of observation`, `winsorization`, and `fixed effects`

## Scope

These standards apply to code that cleans data, constructs variables, runs statistical analyses, or produces tables and figures.

All `software_code.md` standards apply here, plus the additional requirements below.

## Replicability

The guiding principle is that another RA should be able to re-run the analysis from scratch and reproduce the reported outputs.

## Script Setup And Header

Standalone do-files should include a top-of-file header that states:

- project
- file path
- author
- created date
- last updated date
- purpose
- inputs
- outputs
- assumptions
- setup or required packages
- usage
- notes or limitations

The script should also declare:

- `version` near the top
- `clear all`
- `set more off`

Missing `version` is a `WARNING` at `DRAFT` and `SUBMISSION`.

## Paths And Folder Discipline

Use project-relative local macros for paths.

Preferred pattern:

- `local project_root "."`
- `local raw_data "..."`
- `local clean_data "..."`
- `local output_dir "..."`

Hard-coded local machine paths are a `WARNING` at `DRAFT` and an `ERROR` at `SUBMISSION` unless clearly justified.

`data/raw/` should be treated as read-only.
Derived files should be written to locations such as `data/clean/` or `outputs/`.

If output folders may not exist, create them programmatically or document the requirement clearly.

## Data Provenance

At `DRAFT` and `SUBMISSION`, the script or an accompanying note should state:

- data source or origin
- extraction or access date when relevant
- unit of observation
- known quality issues or important limitations

Missing raw data description at `DRAFT` or `SUBMISSION` is an `ERROR`.

## Transformations

All substantive transformations should be coded explicitly.

This includes:

- merges
- filters
- drops
- recodes
- winsorizing
- trimming
- capping
- imputation
- collapsing
- reshaping

Manual upstream cleaning that is not reflected in code is an `ERROR` at `DRAFT` and `SUBMISSION`.

## Counts And Validation

The code should log or otherwise make visible:

- N before and after major filters
- N before and after merges where loss or duplication is possible
- validation checks after high-risk transformations

Missing N counts after major filter or merge is a `WARNING` at `DRAFT` and `SUBMISSION`.

## Stochastic Procedures

If any stochastic component is used, the code should:

- set a seed
- document the seed or generator choice
- avoid hidden randomness

For reproducible analysis, the default expectation is a fixed documented seed.
If intentionally variable randomness is required, explain why.

Missing seed is an `ERROR` at `DRAFT` and `SUBMISSION`.

If no stochastic component is used, a commented seed reminder near the top of the file is still good practice in templates.

## Linting And Style Checks

If `repkit` or another Stata lint workflow is available for the project, run it before submission.

Lint-clean code is useful but not sufficient. It does not prove that the data construction or statistical logic is correct.

## Analytic Transparency

The code or an accompanying note should explain:

- functional form choices
- major variable constructions
- estimand or analytic target when non-obvious
- why important controls or model choices were made

Transformations such as winsorization, trimming, or capping should be explicitly justified rather than silently applied.

Unexplained functional form choices are usually a `WARNING` at `SUBMISSION`.

## Reader-Facing Outputs

If the code produces summary statistics or model outputs:

- units should be preserved or documented
- variable names should be mappable to plain language
- output directories should be created programmatically or clearly documented

Cryptic variable names with no mapping are a `WARNING` at `DRAFT` and `SUBMISSION`.

## Common Review Checks

Reviewers should pay special attention to:

- missing or undocumented user-written packages
- path macros versus hard-coded local paths
- missing merge diagnostics after `merge`
- missing N logging after filters, merges, or deduplication
- raw-data overwrites
- stochastic commands without a seed

