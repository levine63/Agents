---
name: review_statistical_results
description: Use when reviewing summary-statistics tables, regression outputs, figures, or other empirical result artifacts for provenance, internal consistency, interpretability, and claim-to-evidence alignment.
---

# Review Statistical Results

## Purpose

Use this skill to review statistical outputs before they move into memos, manuscripts, slide decks, or decisions.

The goal is to catch missing provenance, ambiguous estimands, mislabeled outputs, and claims that are not supported by the reported evidence.

## When to use

Use this skill when:

- a results table or figure is being finalized
- a summary-statistics or regression output needs review
- the user asks whether empirical outputs are presentation-ready
- a manuscript or slide deck depends on the outputs

## Load

- `standards/genres/statistical_results/standards.md`
- `standards/genres/statistical_results/reviewer_prompt.md`
- `reviewer_prompts/statistical_results_review.md`
- `standards/formats/xlsx/standards.md` if the results live in workbooks
- `standards/formats/docx/standards.md` or `standards/formats/pptx/standards.md` if presentation format issues matter
- relevant code standards if the result package includes code or notebooks

Helpful template:

- `templates/regression_tables/statistical_results_template.md`

## Deterministic checks first

When data-bearing files are available, inspect first for:

- missing labels
- missing units
- missing N or spread statistics
- inconsistent Ns across outputs
- obvious text-table mismatches

If the outputs are images only, say that deterministic checking is limited.

## Review priorities

Check:

- provenance and sample definition
- N, mean, spread, units, and missingness
- model specification clarity
- coefficient interpretability
- consistency across text, tables, and figures
- claim-to-evidence alignment

## Expected output

Return the structure required by `reviewer_prompts/statistical_results_review.md`.

Lead with blocking issues and reproducibility risks.

## Bottom line

Treat statistical outputs as evidence artifacts, not just presentation objects.
