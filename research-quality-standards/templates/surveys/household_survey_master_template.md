# Household Survey Master Template

## 0. Survey Metadata

- Survey title:
- Version:
- Date:
- Country:
- Language:
- Implementing organization:
- Target population:
- Sampling frame:
- Enumerator training dates:
- Primary contact:
- Instrument ID or version:

### Change log

| Version | Date | Changes | Author |
|---|---|---|---|
|  |  |  |  |

## 1. Survey Philosophy and Rules

### Core principles

- Ask only questions tied to analysis or operations.
- Ask one concept per question.
- Prefer observable behavior over attitudes where possible.
- Avoid double negatives.
- Avoid leading wording.
- Avoid culturally ambiguous wording.
- Prefer recent recall windows.
- Minimize respondent burden.
- Keep wording at a reading level appropriate for the intended respondent population.
- Write questions that can survive translation and back-translation.

### Every question should specify

- variable name
- response type
- allowed values
- skip logic
- missingness handling
- `don't know` policy
- validation bounds
- enumerator instructions

## 2. Consent

### Enumerator script

[Insert exact consent script]

### Consent result

| Variable | Type | Values |
|---|---|---|
| consent_given | binary | yes / no |

If consent is not granted:

- terminate interview

### Interview-start metadata

- time started
- consent timestamp
- enumerator ID
- language used
- GPS when appropriate

## 3. Household Roster

### Purpose

Identify household composition and eligibility.

| Variable | Label | Type | Notes |
|---|---|---|---|
| hh_size | Number of household members | integer |  |
| hh_head | Household head ID | select_one |  |
| member_age | Age | integer | validate bounds |
| member_sex | Sex | categorical | standardized codes |

### Enumerator notes

- Define household explicitly.
- Clarify temporary migrants.
- Clarify shared cooking arrangements.

### Validation

- ages 0 to 120
- no duplicate member IDs

## 4. Module Structure

For each module, capture:

- Module name:
- Purpose:
- Target respondent:
- Recall period:
- Key outcomes:
- Expected duration:

### Example module

- Module: Water Access
- Purpose: Measure primary drinking-water source and reliability
- Recall: Current plus last 7 days
- Primary outcomes:
  - improved_source
  - minutes_to_collect
  - interruptions_last_7d

## 5. Standard Question Block

### Variable name

`water_source_main`

### Question text

What is the main source of drinking water for this household?

### Enumerator instructions

Read options exactly.
If multiple sources exist, select the source used most often in the last 7 days.

### Response type

`select_one`

### Response options

1. piped_to_dwelling
2. public_tap
3. borehole
4. protected_well
5. unprotected_well
6. surface_water
7. vendor
8. other
9. dont_know

Response-scale reminder:

- keep closely related scales consistent unless there is a reason not to
- ensure categories are mutually exclusive and collectively exhaustive where required

### Validation

Required unless consent is withdrawn.

### Skip logic

If source = piped_to_dwelling:

- skip `water_collection_time`

### Notes

Matches JMP classification.

## 6. Enumerator Instructions Layer

Keep separate:

- respondent-facing wording
- enumerator instructions

Bad:

- `How many children under 5 do you have including foster children?`

Better:

- Question: `How many children under 5 live in this household?`
- Enumerator note: `Include foster children who usually sleep here.`

## 7. Validation and Quality Rules

### Hard validations

Impossible values should be blocked.

Examples:

- age < 0
- age > 120
- diarrhea days > 30

### Soft warnings

Allow override only with confirmation when appropriate.

Examples:

- income unusually high
- child age inconsistent with grade
- implausibly low water collection time

### Consistency checks

Examples:

- no children reported but school expenditures positive
- `never attended school` but literacy = yes

## 8. Missingness Rules

Distinguish:

- refused
- don't know
- not applicable
- skipped by logic
- missing due to device or collection problem

Suggested standard codes if the project uses numeric codes:

- -97 refused
- -98 not_applicable
- -99 dont_know

## 9. Translation Rules

For every language, track:

- forward translation
- back translation or quality review
- cognitive testing or pilot testing

### Translation glossary

| English | Local language | Notes |
|---|---|---|
|  |  |  |

## 10. Metadata Collection

Collect automatically where feasible:

- start time
- end time
- duration
- enumerator ID
- GPS
- audit timestamps
- device ID
- language
- consent timestamp

## 11. Survey QA Monitoring

Daily or regular checks:

- interview duration
- missingness rates
- GPS anomalies
- duplicate households
- heaping
- straightlining
- impossible combinations

## 12. Analysis Linkage

Map each major outcome to:

- variable(s)
- planned table or figure
- hypothesis or operational use
- analysis file when known

| Outcome | Variables | Planned table |
|---|---|---|
|  |  |  |

## 13. XLSForm Readiness

Every question should imply:

- type
- constraint
- relevance
- calculation when relevant
- appearance when relevant

Suggested naming conventions:

- `q_` = raw question
- `calc_` = calculated field
- `note_` = display text
- `grp_` = groups
- `rep_` = repeats

Use snake_case for machine-facing names unless another standard is already in force.

## 14. Pilot Debrief

After piloting, document:

- misunderstood questions
- refusals
- translation issues
- skip failures
- timing problems
- sensitive questions
- enumerator confusion
- respondent fatigue points

Version updates should cite pilot findings when applicable.

Pre-deployment reminder:

- do not treat pilot testing as optional by default
- if no pilot or cognitive test was done, explain why
