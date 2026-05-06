# Statistical Results Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/statistical_results_template.md`
Related examples: `examples/README.md`
Lint opportunities: units markers, N/mean/spread presence, missingness fields, inconsistent numbers across linked files

## Scope

These standards apply to reader-facing statistical outputs such as summary tables, regression tables, simulation outputs, cost-effectiveness tables, and notebook sections that present empirical results.

## Summary Statistics

For each quantitative variable, provide:

- N
- mean
- a measure of spread, usually SD or IQR
- units

At `DRAFT` and `SUBMISSION`, missing N, mean, or spread is an `ERROR`.
At `SUBMISSION`, missing units is an `ERROR`.

## Sample Definition

The reader should be able to tell:

- which sample or population is being described
- how missing data affected the reported sample

Undefined sample is a `WARNING` at `DRAFT` and may be an `ERROR` if it makes interpretation impossible.

## Model Description

Before or with model results, state:

- outcome variable
- key regressors
- controls or adjustment set
- estimator or model family
- level of observation
- standard-error treatment, including clustering or stratification when relevant

Missing model specification at `DRAFT` and `SUBMISSION` is an `ERROR`.

## Interpretability

The reader should be able to interpret:

- coefficient units
- whether changes are one-unit, log-point, percentage-point, or another quantity
- whether estimates are descriptive, predictive, or causal

If the text overstates what the model supports, that is an `ERROR`.

## Naming And Labeling

- reader-facing tables should not use cryptic internal variable codes
- abbreviations should be defined
- table notes should explain non-obvious transformations or denominators

Cryptic labels in reader-facing output are a `WARNING` at `DRAFT` and `SUBMISSION`.

## Internal Consistency

Numbers cited in text should match the underlying tables and figures.

Inconsistency between text and tables is an `ERROR` at all stages beyond `EXPLORATORY`.
