# Submissions Folder README

## Purpose

This folder is for work-product review submissions to Codex.

Use it for document-shaped artifacts such as:

- manuscript drafts
- interview notes or transcripts
- statistical result tables
- slide decks
- weekly reports
- code exports when GitHub is not being used

Do not use this folder for:

- production secrets
- raw personally identifying data unless explicitly authorized
- final code-review workflows that should go through GitHub pull requests

## Folder structure

Place files in the appropriate subfolder:

- `01_Manuscripts`
- `02_Interviews`
- `03_Statistical_Results`
- `04_Slides`
- `05_Weekly_Reports`
- `06_Code_Exports`
- `99_Admin`

If `Inbox` and `Reviewed` subfolders exist, place new submissions in `Inbox`.

## File naming convention

Use:

- `project_author_stage_YYYY-MM-DD_v01.ext`

Examples:

- `leadstudy_khan_draft_2026-05-13_v01.docx`
- `wateraccess_lee_submission_2026-05-13_v03.xlsx`
- `baseline_teamA_weeklyreport_2026-05-13_v01.md`

## Required metadata in the filename or cover note

Every submission should make it easy to identify:

- project
- author
- stage, such as `draft` or `submission`
- date
- version

## What counts as a good submission

A good submission:

- lives in the correct subfolder
- has a clear filename
- includes enough context to determine artifact genre
- is reviewable without guessing what version it is

## Review workflow

Codex or related review automation may:

- classify the artifact genre
- load the relevant standards
- run deterministic checks when possible
- generate review feedback
- log status in a dashboard or sheet

## To do

- add direct review support for native Google Docs submissions
- add direct review support for native Google Sheets submissions
- add Word `.docx` ingestion and review
- add Excel `.xlsx` ingestion and review
- detect the submitter automatically when possible
- record submitter identity and submission channel in the tracking sheet
- send a review response back to the submitter automatically when appropriate
- distinguish acknowledgment, review-complete, and needs-revision responses
- load prompts and standards automatically from the `Codex` standards folder so review behavior stays updated without manual copying
- route reviews using both artifact genre and document format standards
- add stronger review outputs for each submission beyond intake logging and placeholder review documents
- add queue rules for high-priority, ambiguous, or human-review-required submissions

## Notes

- For code review, GitHub pull requests are preferred over Drive uploads.
- For weekly reports, a Google Form may eventually replace direct file submission.
- If a file is revised, increment the version suffix rather than overwriting ambiguously named files.
