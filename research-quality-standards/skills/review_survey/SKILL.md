---
name: review_survey
description: Use when reviewing a survey instrument, questionnaire, XLSForm, or field-deployment survey package for skip logic, measurement quality, implementation risk, translation robustness, and analysis readiness.
---

# Review Survey

## Purpose

Use this skill to review surveys before programming, pilot, or scale-up.

The goal is to catch failures that will break fieldwork, create ambiguous implementation, or produce low-quality data.

## When to use

Use this skill when:

- a survey instrument is drafted or revised
- an XLSForm or paper questionnaire needs review
- the user asks whether a survey is field-ready
- skip logic, response options, or enumerator instructions are in question

## Load

- `standards/genres/survey/standards.md`
- `standards/genres/survey/reviewer_prompt.md`
- `reviewer_prompts/survey_review.md`
- `standards/formats/xlsx/standards.md` if the survey is workbook-based or implemented in spreadsheet form
- `standards/formats/docx/standards.md` if the survey draft is a Word artifact and document structure matters

Helpful template:

- `templates/surveys/household_survey_master_template.md`

## Deterministic checks first

If a machine-readable implementation exists, inspect obvious structural risks first:

- missing or inconsistent skip targets
- overlapping coded categories
- obvious missing validation bounds

If no deterministic checker exists, say so and proceed with manual operational review.

## Review priorities

Check:

- skip logic and eligible populations
- response-option design
- wording clarity
- enumerator and programming ambiguity
- translation robustness
- respondent burden
- missingness handling
- analysis linkage for major outcomes

## Expected output

Return the review in the structure required by `reviewer_prompts/survey_review.md`.

Focus on failures that matter operationally in real field conditions.

## Bottom line

Treat the survey as a field instrument, a programmed logic surface, and a future dataset all at once.
