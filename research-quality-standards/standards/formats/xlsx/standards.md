# XLSX Workbook Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-13

## Purpose

These standards apply to spreadsheet workbooks used for data storage, cleaning, analysis, reporting, dashboards, and related research or operational workflows.

An `.xlsx` workbook is not just a container for numbers.
It may function as:

- a computational artifact
- a data pipeline
- a small database
- a reporting surface
- a decision-support system

The primary rule is:

- separate raw data, transformations, assumptions, and outputs clearly enough that another person can audit and update the workbook without guessing what happened

Not every workbook needs the same sheet structure, but every serious workbook should remain:

- interpretable
- auditable
- reproducible enough for its purpose
- resistant to silent corruption

## Scope and proportionality

These standards are intentionally less rigid than a single gold-master workbook design.

Use stronger structure for:

- analytical workbooks
- shared team workbooks
- recurring reporting files
- workbooks that feed decisions or published outputs

Use lighter structure for:

- small temporary calculations
- narrow single-table workbooks
- one-off scratch work that will not be shared or relied on

The more a workbook behaves like software, the more these standards should be applied strictly.

## Core structure expectations

### Documentation sheet

Substantial workbooks should include a documentation sheet, usually first, often named:

- `README`
- `about`
- `instructions`

That sheet should usually capture:

- workbook title
- version
- author or owner
- purpose
- intended audience
- main data sources
- update or refresh notes when relevant
- workbook map or sheet guide
- known limitations

For simple workbooks, this can be shorter, but some orientation should still exist.

### Separation of concerns

Prefer separating:

- raw imports
- cleaned or transformed data
- assumptions or parameters
- analysis logic
- presentation-ready outputs

This does not require a rigid prefix system in every file, but the distinction should be visible.

If raw data and outputs are mixed in confusing ways, the workbook becomes fragile.

### Table clarity

Prefer rectangular tables with one obvious header row.

Avoid mixing unrelated tables, decorative layouts, and machine-readable data in the same region when the sheet is meant to support filtering, export, or analysis.

### One row means one thing

Where a table is intended for analysis or reuse, each row should usually represent one unit of observation consistently.

If a table mixes units, that should be explicit.

## Data architecture and naming

### Variable and column names

Use stable, descriptive names for machine-facing fields when possible.

Snake case is preferred for exported or reusable data tables, especially if the workbook feeds code or repeated analysis.

Human-facing display labels can still be more readable, but ambiguity should be minimized.

### Units should be explicit

Quantitative fields should make units clear either in:

- the column name
- the header
- the documentation sheet
- the data dictionary

Do not rely on memory for units.

### Missingness should be interpretable

If the workbook uses special missing-value codes or textual categories, document them clearly.

Avoid collapsing all missingness into one ambiguous blank or code when distinctions matter operationally.

## Formula safety

### Avoid hidden constants

Important constants, rates, cutoffs, and thresholds should usually be centralized or documented rather than buried repeatedly inside formulas.

Hard-coded constants are not always wrong, but they should not be invisible.

### Prefer auditable logic

If a formula becomes too complex to inspect reliably:

- move logic into helper columns
- split the calculation into stages
- or consider moving the logic into code

### Formula consistency matters

Within a structured calculation column, formulas should usually be consistent except for row references.

Unexpected formula drift should be treated as a warning sign.

### Volatile functions require caution

Use functions such as `INDIRECT`, `OFFSET`, `NOW`, `TODAY`, or random generators sparingly and intentionally.

They are not banned, but they weaken reproducibility and auditability when used casually.

## Formatting and usability

### Formatting should communicate meaning consistently

If color or style is used to signal meaning, apply it consistently.

Useful distinctions may include:

- user-editable cells
- formula cells
- outputs
- warnings or errors

Do not rely on decorative formatting alone.

### Avoid merged cells in working data regions

Merged cells can break:

- sorting
- filtering
- exports
- formula fill-down
- downstream tools

They may be acceptable in presentation-only areas, but should be avoided in data tables and logic-heavy regions.

### Keep navigation usable

For large sheets, use usability aids such as:

- freeze panes
- filters
- Excel tables
- clearly separated sections

These are not universally required, but they are strongly preferred where they improve auditability.

## Charts and output surfaces

Charts and final tables should usually include:

- titles
- labels
- units
- legends where needed

Avoid misleading or hard-to-read output choices such as:

- unlabeled axes
- unexplained abbreviations
- 3D charts that obscure magnitude

## Reproducibility and refreshability

### Manual edits should be visible

If manual overrides or adjustments occur, they should be traceable in at least one of:

- the documentation sheet
- comments or notes
- a log sheet
- an audit sheet

### External dependencies should be documented

If the workbook depends on:

- linked files
- CSV imports
- Power Query
- macros
- add-ins
- external data sources

document that clearly.

Broken external links are a serious problem for any workbook that is meant to be reused.

### Refresh steps should exist when relevant

If pivots, queries, or imports require refresh actions, document how to do that.

## Quality assurance

Useful workbook QA checks may include:

- duplicate IDs
- missing keys
- impossible values
- broken formulas
- inconsistent formulas
- circular references
- hidden sheets that matter to interpretation
- hidden rows or columns that affect outputs
- external-link failures

For larger workbooks, a dedicated `audit_checks` sheet is often worthwhile.

## Protection and safety

Protecting formula regions, lookup tables, or dashboard outputs may be appropriate when the workbook is shared widely or edited by many people.

Do not protect so aggressively that legitimate maintenance becomes impossible, but do reduce accidental corruption where practical.

## Documentation aids

Helpful companion elements include:

- a data dictionary sheet
- comments for unusual assumptions
- named ranges or tables with meaningful names
- a small audit sheet

Not every workbook needs all of these, but larger analytical workbooks usually benefit from them.

## Large-workbook guidance

If a workbook:

- is very large
- recalculates slowly
- contains brittle deep logic
- behaves like a full software system

consider moving transformations or heavy computation into code or a database-backed workflow.

Excel is useful, but it is not a substitute for proper software engineering once complexity grows too far.

## Agent-specific editing rules

When agents edit `.xlsx` files:

- make scoped edits only
- preserve formulas unless explicitly changing them
- do not overwrite formulas with values unless instructed
- preserve named ranges, tables, and workbook logic
- avoid accidental formatting drift
- create a backup before risky workbook edits
- visually inspect affected sheets when possible

## Common failure modes

Flag:

- undocumented transformations
- hidden assumptions
- broken formulas
- inconsistent formulas in what should be a uniform calculation column
- mixed raw and cleaned data with no clear separation
- silent manual overrides
- ambiguous units
- merged cells in working data tables
- broken external links
- workbooks that only make sense to the creator

## Bottom line

The goal is not to force every workbook into the same tab layout.

The goal is to ensure that a stranger can:

- understand the workbook
- audit the logic
- update the inputs
- and trust the outputs enough for the workbook's intended use

without needing the original creator in the room.
