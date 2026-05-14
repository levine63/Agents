---
name: review_readme
description: Use when reviewing a repository README or onboarding document for completeness, handoff readiness, quick-start quality, and consistency with the README standards and reviewer prompt.
---

# Review README

## Purpose

Use this skill to review project README files and similar onboarding documents.

The goal is to determine whether a new contributor can understand the project, run the right starting workflow, and see what is still missing or risky.

## When to use

Use this skill when:

- a `README.md` is being added or revised
- the user asks for README review
- onboarding quality is in question
- a repo needs a handoff-readiness check

## Load

- `standards/genres/README/standards.md`
- `standards/genres/README/reviewer_prompt.md`
- `reviewer_prompts/README_review.md`
- relevant code or analysis standards if the README materially documents those workflows

## Deterministic checks first

When available, run:

- `scripts/lint/check_readme.py`

Prefer reviewing the top-level README first unless the user clearly wants a subproject README.

## Review priorities

Check:

- project genre clarity
- quick-start quality
- environment and dependency clarity
- inputs and outputs
- reproducibility and tests
- limitations and honesty
- path and file-reference plausibility

## Expected output

Return the review in the structure required by `reviewer_prompts/README_review.md`.

Lead with concrete problems, not general impressions.

## Bottom line

Use deterministic README checks first, then apply the README review prompt for the human-style review.
