---
name: review_xlsx_workbook
description: Use when reviewing an Excel workbook or spreadsheet-based analytical artifact for workbook structure, formula safety, documentation, auditability, and silent-corruption risk.
---

# Review XLSX Workbook

## Purpose

Use this skill to review workbook-based artifacts that behave partly like data stores and partly like executable logic.

The goal is to catch structural and interpretability problems before the workbook becomes a hidden source of decision error.

## When to use

Use this skill when:

- a shared `.xlsx` workbook needs review
- a workbook feeds analysis, reporting, or operations
- the user asks whether a spreadsheet is auditable or safe
- a spreadsheet has complex formulas, multiple sheets, or refresh dependencies

## Load

- `standards/formats/xlsx/standards.md`

Then load the relevant genre standard if one clearly applies, such as:

- `standards/genres/survey/standards.md`
- `standards/genres/statistical_results/standards.md`
- `standards/genres/weekly_goals/standards.md`

Helpful template:

- `templates/codebooks/xlsx_workbook_template.md`

## Deterministic checks first

Look first for obvious workbook risks:

- missing documentation sheet
- mixed raw and output regions with no clear separation
- merged cells in working data regions
- inconsistent formulas in columns that should be uniform
- broken external links if visible
- hidden sheets or rows that materially affect interpretation

If a specialized checker does not exist, report that the workbook review is partly manual.

## Review priorities

Check:

- workbook structure and orientation
- separation of raw data, transformed data, parameters, and outputs
- formula safety and hidden constants
- unit clarity and naming
- auditability of manual edits
- external dependencies and refresh instructions
- QA sheet or equivalent check surface for larger workbooks

## Expected output

Return a concise review with:

- verdict
- blocking issues
- warnings
- structural risks
- suggested repair instructions
- human cautions

## Bottom line

The workbook should make sense to a competent stranger, not only to its creator.
