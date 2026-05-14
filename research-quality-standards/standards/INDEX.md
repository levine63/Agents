# Standards Index

## Purpose

This is the registry for standards in this repository.

Use it to find:

- genre standards
- format standards
- schemas
- canonical reference files

For day-to-day use, treat the artifact matrix below as the canonical lookup table for which standards to load together.

## Categories

| Stack | Status | Notes |
|---|---|---|
| `work_product_reviews` | active | Current integrated review stack. |
| `literature_review` | planned | Future evidence-synthesis stack. |
| `sync_results_and_text` | planned | Future consistency-check stack. |

## Artifact lookup matrix

| Artifact Genre | Format | Standards to load |
|---|---|---|
| Academic paper | DOCX / LaTeX | `genres/academic_paper` + `formats/docx` or `formats/latex` |
| Survey | XLSX | `genres/survey` + `formats/xlsx` |
| README | Markdown | `genres/README` + `formats/markdown` |
| Statistical tables | XLSX / TEX / DOCX | `genres/statistical_results` + relevant format |
| Slides | PPTX | `genres/presentation` + `formats/pptx` |
| Weekly goals/reports | Markdown / Google Form | `genres/weekly_goals` |
| Replication package | Git repo / ZIP | `genres/replication_package` |
| Python code | Python | `formats/python` |
| Python statistical / research code | Python | `formats/python` + `formats/python_stats` |
| Stata code | Stata | `formats/stata` |

## Notes on use

- Load the genre standard first, then the format standard when both exist.
- Genre standards win over format standards on semantic conflicts.
- If a required genre or format is still marked `planned`, use the closest active standard and record the gap.
- For mixed artifacts, load the smallest set that covers the actual work rather than every nearby standard.

## Genre standards

| Genre | Path | Source status |
|---|---|---|
| `academic_paper` | `standards/genres/academic_paper/` | integrated |
| `grant_proposal` | `standards/genres/grant_proposal/` | planned |
| `survey` | `standards/genres/survey/` | integrated |
| `interview` | `standards/genres/interview/` | integrated |
| `statistical_results` | `standards/genres/statistical_results/` | integrated |
| `README` | `standards/genres/README/` | integrated |
| `weekly_goals` | `standards/genres/weekly_goals/` | integrated |
| `replication_package` | `standards/genres/replication_package/` | planned |
| `presentation` | `standards/genres/presentation/` | integrated |
| `literature_review` | `standards/genres/literature_review/` | planned |
| `meeting_notes` | `standards/genres/meeting_notes/` | planned |

## Format standards

| Format | Path | Source status |
|---|---|---|
| `docx` | `standards/formats/docx/` | integrated |
| `pptx` | `standards/formats/pptx/` | integrated |
| `xlsx` | `standards/formats/xlsx/` | integrated |
| `markdown` | `standards/formats/markdown/` | planned |
| `latex` | `standards/formats/latex/` | planned |
| `python` | `standards/formats/python/` | integrated |
| `python_stats` | `standards/formats/python_stats/` | integrated |
| `stata` | `standards/formats/stata/` | integrated |
| `csv` | `standards/formats/csv/` | planned |
| `pdf` | `standards/formats/pdf/` | planned |
| `json` | `standards/formats/json/` | planned |

## Schemas

Planned:

- `tasks.schema.json`
- `weekly_reports.schema.json`
- `survey.schema.json`
- `artifact.schema.json`

## Canonical references

Planned:

- `canonical_variable_dictionary.csv`
- `missing_value_codes.csv`
- `journal_targets.csv`
