# Google Drive Submissions Workflow

## Purpose

This workflow describes how to use a Google Drive submissions folder for Codex review intake.

## Recommended folder structure

Top-level submission folder:

- `Submissions`

Recommended subfolders:

- `01_Manuscripts`
- `02_Interviews`
- `03_Statistical_Results`
- `04_Slides`
- `05_Weekly_Reports`
- `06_Code_Exports`
- `99_Admin`

Optional per-folder subfolders:

- `Inbox`
- `Reviewed`

## Recommended use by artifact type

- `GitHub PRs`: code, configuration, notebooks exported to `.py`, markdown docs tied to code review
- `Drive folders`: `.docx`, `.pptx`, `.xlsx`, memos, transcripts, manuscript drafts
- `Google Form`: recurring weekly reports and structured intern updates

## Monitoring model

The simplest monitoring model is a standalone Google Apps Script with a time-based trigger.

Recommended behavior:

1. scan the submission subfolders every 15 to 60 minutes
2. ignore admin folders and self-referential tracker files
3. detect files not yet logged in a tracking sheet
4. classify folder-based genre
5. convert `.docx` and `.xlsx` submissions into temporary Google-native review sources when needed
6. create a review-output Google Doc for each new submission
7. fetch current standards from GitHub when configured, using a short cache window
8. write a row to a submissions log sheet with queue status and review-doc link

## Why use Apps Script

Apps Script is the most natural first monitoring layer because it already has:

- Drive access
- Sheets access
- triggers
- lightweight deployment inside Google Workspace

It is better as a first pass than email scraping or a desktop watcher.

For development and deployment, prefer `clasp` over browser copy-paste so the script can be edited locally and pushed cleanly.

## Limitations

- Drive tools do not give a true real-time watcher in this setup; the workflow is polling-based
- private-file access and external LLM calls need explicit handling
- long documents and large workbooks still require compressed review inputs, even with smarter extraction
- genre classification from folder alone is helpful but imperfect
- live GitHub standards loading depends on a reachable raw-content URL and will fall back to embedded defaults if unavailable

## Next steps

- create the folder structure in Drive
- place the folder README in the root of `Submissions`
- create a linked tracking Sheet
- deploy the Apps Script watcher
- add genre-specific review routing
- load reviewer prompts automatically from the canonical standards source, not just embedded defaults
- optionally add a manual Codex review pass for cases the automated reviewer flags as ambiguous or high risk
