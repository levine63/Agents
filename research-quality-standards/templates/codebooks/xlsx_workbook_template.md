# XLSX Workbook Template

Use this as a design template for a shared or durable workbook. It is intentionally modular rather than mandatory in every detail.

## Suggested workbook sheet map

| Sheet | Purpose | Editable? |
|---|---|---|
| `README` | Workbook documentation and navigation | Yes |
| `raw_*` | Imported or copied raw data | No, unless explicitly part of the workflow |
| `clean_*` | Cleaned or transformed working tables | Limited |
| `param_*` | Assumptions, thresholds, scenario settings | Yes |
| `lookup_*` | Reference mappings or code lists | Limited |
| `analysis_*` | Intermediate calculations, pivots, summaries | Limited |
| `output_*` | Final tables, charts, dashboards | Limited |
| `audit_checks` | QA checks, flags, and refresh notes | Yes |
| `data_dictionary` | Column descriptions, units, and code meanings | Yes |

Not every workbook needs all of these sheets, but substantial shared workbooks usually need at least a `README` sheet and a clear separation between data, logic, and outputs.

## README sheet template

### Workbook metadata

- Workbook title:
- Version:
- Author(s):
- Organization:
- Contact:
- Creation date:
- Last modified date:
- Purpose:
- Intended audience:
- Source(s) of data:
- Update frequency:
- Confidentiality level:
- Software/version requirements:

### Workbook structure map

| Sheet | Purpose | Editable? | Notes |
|---|---|---|---|
|  |  |  |  |

### Known limitations

- 

### Change log

| Version | Date | Changes | Author |
|---|---|---|---|
|  |  |  |  |

## Raw-data guidance

For `raw_*` sheets:

- preserve source structure where practical
- avoid manual edits
- if manual fixes are unavoidable, document them visibly

## Parameter-sheet guidance

For `param_*` sheets, capture:

- assumptions
- constants
- thresholds
- scenario toggles

Prefer referencing parameter cells rather than burying important constants in formulas.

## Audit sheet template

Recommended sheet: `audit_checks`

| Check | Result | Notes |
|---|---|---|
| Duplicate IDs | PASS / FAIL |  |
| Missing key fields | PASS / FAIL |  |
| Broken formulas | PASS / FAIL |  |
| External links | PASS / FAIL |  |
| Hidden rows or columns affecting outputs | PASS / FAIL |  |

## Data dictionary template

Recommended sheet: `data_dictionary`

| Variable | Description | Units | Allowed values or notes |
|---|---|---|---|
|  |  |  |  |

## Workbook design reminders

- Keep working data in rectangular tables.
- Avoid merged cells in data regions.
- Make units explicit.
- Document unusual assumptions.
- Use consistent formatting for editable cells versus formula cells when helpful.
- Prefer helper columns over very deep opaque formulas.
