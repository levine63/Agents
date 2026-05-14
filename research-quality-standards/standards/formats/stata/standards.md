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

