# Software Code Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/code/python_general/template.py`, `templates/code/stata/template.do`
Related examples: `examples/README.md`
Lint opportunities: header, purpose, docstring presence, hard-coded personal paths, bare `except`, main guard, `version`

## Scope

These standards apply to general software and scripting work, especially Python and Stata, unless a more specific standards file imposes stricter requirements.

## Required Provenance

Code submissions should include:

- author
- date
- purpose
- inputs
- outputs
- setup or dependencies
- usage instructions
- notes on assumptions or limitations

At `DRAFT` and `SUBMISSION`, missing purpose is an `ERROR`.

## Runnability

At `DRAFT` and `SUBMISSION`, a script should run end-to-end without undocumented manual intervention unless it is explicitly declared interactive.

Undocumented manual steps are an `ERROR` at `DRAFT` and `SUBMISSION`.

## Paths And Environment

- Prefer relative or centralized configurable paths
- Avoid scattered personal-machine paths
- Document non-standard environment assumptions

Hard-coded personal paths are:

- `WARNING` at `ROUGH_DRAFT` and `DRAFT`
- `ERROR` at `SUBMISSION`

## Readability And Structure

- names should be descriptive
- large scripts should have logical sections or functions
- comments should explain why, not only what
- dead code should be removed or briefly justified

At `DRAFT` and `SUBMISSION`, clearly non-descriptive names are a `WARNING`.

## Error Handling

- do not silently swallow failures
- do not use bare `except` unless immediately re-raising or handling with clear intent
- file reads and writes should fail clearly or give understandable diagnostics

Silent exception handling is an `ERROR` at `DRAFT` and `SUBMISSION`.

## Reproducibility

If randomness is used, set and document a seed unless there is a strong reason not to.

Randomness without a documented seed is:

- `WARNING` at `ROUGH_DRAFT`
- `ERROR` at `DRAFT` and `SUBMISSION`

## Language Notes

### Python

- module docstrings are expected for script-like or reusable files
- non-trivial functions and classes should have docstrings
- script-like files should usually use a main guard

### Stata

- `version` near the top is expected
- `set more off` is expected for batch runs
- globals should be minimized and justified

Missing `version` in a substantive Stata script is an `ERROR` at `DRAFT` and `SUBMISSION`.


