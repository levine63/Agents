---
name: review_python
description: Use when reviewing Python code changes, especially before substantial commits, pushes, pull requests, or handoff, to run deterministic checks first and then assess readability, reproducibility, and maintainability against the repository's Python standards.
---

# Review Python

## Purpose

Use this skill to review Python code changes with a deterministic-first workflow.

The point is to catch:

- lint failures
- formatting drift
- obvious type issues
- broken assumptions
- reproducibility problems
- maintainability risks

before the code is pushed, shared, or treated as complete.

## When to use

Use this skill when:

- Python files changed materially
- a Python bugfix or feature is ready for review
- a substantial Python commit is being prepared
- a push or PR is likely soon
- the user asks for Python review, code-quality review, or pre-push checks

For tiny typo-only edits, a full review may be unnecessary.

## Standards to load

Load:

- `standards/formats/python/standards.md`
- `standards/formats/python/reviewer_prompt.md`
- `standards/formats/python_stats/standards.md` when the code performs data cleaning, analysis-dataset construction, statistical modeling, simulations, or table/figure generation for empirical work
- `standards/formats/python_stats/reviewer_prompt.md` when the code is statistical or research code
- `standards/genres/README/standards.md` if the change affects a Python project README materially
- any relevant genre standard if the Python code supports a specific artifact, such as `survey` or `statistical_results`

## Deterministic checks first

### Ruff

For major Python changes or before a push, run `Ruff` when available.

This is the default deterministic review tool.

At minimum, prefer:

- `ruff check`

If the project already uses Ruff formatting, also consider:

- `ruff format --check`

If the repository has a known configured command, use that instead of inventing a new one.

### Black

`Black` is useful when:

- the repository already uses `Black`
- the repository's formatting expectations clearly align with `Black`
- formatting drift is part of the review surface

Do not introduce `Black` to a repo that does not already use it unless the user asks.

If `Black` is already part of the project, prefer:

- `black --check`

### mypy

`mypy` is useful when:

- the repository already has `mypy` configuration
- the codebase uses type hints meaningfully
- the changed files are type-checked in normal workflow

`mypy` is often high-value for libraries, APIs, and typed application code.
It is often lower-signal for lightly typed research scripts.

Use it when it is already part of the project's expectations or when the typed surface is important enough to justify it.

### Tests

Run relevant tests when available, especially for major changes or pre-push review.

Use project-native test commands when they exist.

## Review priorities

After deterministic checks, review for:

1. correctness risk
2. reproducibility and seed handling
3. path and environment safety
4. exception handling quality
5. statistical and data-integrity risks when relevant
6. readability and decomposition
7. duplication and hidden assumptions
8. whether the change fits existing project conventions

## Output expectations

A good Python review should report:

- what deterministic checks were run
- what passed or failed
- whether `Ruff`, `Black`, or `mypy` were unavailable, not configured, or not applicable
- whether the code was reviewed against generic Python only or against both generic Python and the Python statistics add-on
- the highest-risk findings first
- suggested repairs when practical

## Practical guidance

- Prefer project-native commands over generic guessed commands.
- Do not add new lint or type tools just to satisfy the review unless the user asks.
- For major changes and pushes, `Ruff` should usually run if available.
- `Black` and `mypy` are useful, but conditional on repository conventions and codebase maturity.

## Bottom line

For major Python changes:

- run `Ruff` first when available
- run tests when available
- use `Black` if the repo already uses it
- use `mypy` if the repo already uses it or the typed surface makes it worth the signal

Then perform the human-style code review.
