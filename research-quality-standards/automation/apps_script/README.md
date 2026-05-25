# Apps Script Deployment

This folder contains the Google Apps Script source for the Drive submissions watcher.

## Supported review paths

- Native Google Docs
- Native Google Sheets
- Word `.docx` converted to Google Docs
- Excel `.xlsx` converted to Google Sheets
- PDF files sent directly to the OpenAI Responses API as file input

## Recommended workflow

Use `clasp` so you can edit locally and push directly to Apps Script instead of pasting large code blocks into the web editor.

Official references:

- https://developers.google.com/apps-script/guides/clasp
- https://github.com/google/clasp

## One-time setup

1. Install Node.js.
2. Install `clasp`:
   - `npm install -g @google/clasp`
3. Log in:
   - `clasp login`
4. Copy `.clasp.json.example` to `.clasp.json` at the repository root.
5. Replace `scriptId` with your Apps Script project ID.

Expected repo-root `.clasp.json`:

```json
{
  "scriptId": "YOUR_SCRIPT_ID",
  "rootDir": "automation/apps_script"
}
```

## Push updates

From the repository root:

```powershell
clasp push
```

To open the script in the browser:

```powershell
clasp open-script
```

After pushing code changes, if you want to test immediately:

1. Open the Apps Script project.
2. Run `scanSubmissionFolders()` once manually.
3. Approve any new permissions if prompted.
4. Leave the time trigger enabled for normal background runs.

## Required Script Properties

- `SUBMISSIONS_FOLDER_ID`
- `TRACKING_SHEET_ID`
- `OPENAI_API_KEY`

Recommended:

- `TRACKING_SHEET_NAME=Intake Log`
- `OPENAI_MODEL=gpt-5-mini`
- `EXCLUDED_FOLDER_NAMES=99_Admin`
- `REVIEW_OUTPUT_FOLDER_NAME=Review Outputs`
- `CONVERTED_SOURCE_FOLDER_NAME=Converted Review Sources`
- `KEEP_CONVERTED_SOURCES=true`
- `EXCLUDED_FILE_IDS=<comma-separated file ids>`
- `STANDARDS_BASE_URL=https://raw.githubusercontent.com/<owner>/<repo>/<branch>`
- `STANDARDS_CACHE_MINUTES=20`

## Required Apps Script service

Enable the Advanced Drive service. The included `appsscript.json` manifest already declares it for `clasp`-based pushes.

## Live standards loading

If `STANDARDS_BASE_URL` is set, the watcher fetches the latest genre and format standards from GitHub at review time and caches them briefly with `CacheService`.

Expected shape:

- `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/standards/genres/...`
- `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/standards/formats/...`

If GitHub is unavailable, the script falls back to embedded standards text so reviews still complete.

## Updating after a local patch

From the repository root:

```powershell
Set-Location "C:\Users\levine\Dropbox\Codex\GitHub\Agents\research-quality-standards"
clasp push
clasp open-script
```

Then run `scanSubmissionFolders()` once in Apps Script if you want the new logic to take effect immediately instead of waiting for the next trigger run.
