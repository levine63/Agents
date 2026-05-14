# Survey Standards

Version: 0.1.0
Status: Draft


Related template: [household_survey_master_template](../../../templates/surveys/household_survey_master_template.md)

## Scope

These standards apply to survey instruments before field deployment, including paper forms and digital instruments implemented in tools such as ODK, SurveyCTO, REDCap, Kobo, Qualtrics, or CommCare.

They are designed for real field conditions, including:

- respondents with limited literacy, patience, or privacy
- enumerators who are hurried, variably trained, and likely to improvise under pressure
- translations that may shift meaning
- platforms that may mishandle ambiguous logic
- downstream analysts who will inherit the data without perfect context

The goal is operationally reliable measurement, not elegant wording alone.

## Survey package architecture

A strong survey is not just a questionnaire.

It is usually a package with:

1. a human-readable master survey
2. a structured implementation file, often XLSForm
3. a variable dictionary or codebook
4. an analysis linkage or analysis plan
5. enumerator instructions or manual
6. QA or lint checks

Bad surveys often fail because these layers are mixed together inconsistently or left implicit.

## Core principles

A good survey should be:

- answerable by the intended respondent
- administrable at field speed with minimal enumerator judgment
- programmable without ambiguity
- analyzable months later without reconstructing intent from memory

If a question fails any of those tests, it should be flagged.

Additional principles:

- ask only questions tied to analysis or operations
- ask one concept per question
- prefer observable behavior over attitudes when possible
- avoid double negatives
- avoid leading wording
- minimize respondent burden
- keep wording at a reading level appropriate for the intended respondent population
- write questions that survive translation and back-translation

## Metadata and versioning

A deployable survey package should record:

- survey title
- version
- date
- country
- language
- implementing organization
- target population
- sampling frame when relevant
- instrument identifier
- primary contact

Version changes should be documented in a changelog with:

- version
- date
- change summary
- author

Ambiguous versioning is a quality problem because field teams, programmers, and analysts may otherwise use different instruments without noticing.

## High-stakes elements

Review these with extra scrutiny:

- screening and eligibility questions
- questions that determine skip paths
- sensitive questions requiring privacy protections
- free-text and `Other, specify` fields
- recall-based measures
- primary outcomes or treatment-comparison variables

Errors in these areas propagate through fieldwork, programming, and analysis.

## Consent and interview-start standards

The survey package should include:

- exact respondent-facing consent language when consent is required
- a clearly defined consent result field
- a clear termination rule if consent is not granted

Where feasible, the instrument should also capture:

- interview start time
- consent timestamp
- enumerator ID
- language used

Sensitive questions should be paired with a privacy-aware administration plan.

## Survey design standards

### Skip logic and flow

The instrument should make every path explicit.

Check that:

- all paths are possible and non-contradictory
- downstream questions have a clearly defined eligible population
- eligibility is established before it is assumed
- logic can be executed by a machine without enumerator memory
- respondents are not incorrectly routed into irrelevant or impossible questions

Undefined or contradictory skip logic is a serious error.

### Response options should be usable

Response options should be appropriately exhaustive and, where required, mutually exclusive.

Check for:

- overlapping age, time, or income bands
- gaps in categories
- ambiguous `select one` options
- unlabeled `select all that apply`
- scales that mix different concepts, such as intensity and frequency
- inconsistent response scales across closely related questions when consistency would reduce respondent and enumerator confusion
- `Other` categories that are likely to absorb a large share of responses

If `Other` is likely to capture a large share of valid responses, the categories are underspecified.

### Question clarity

Questions should be understandable to both respondents and enumerators.

Flag:

- jargon
- unexplained acronyms
- double negatives
- vague time windows
- culturally specific framing that may not travel
- hidden assumptions about household structure, gender roles, literacy, technology, or authority
- wording that is likely to shift meaning in translation
- questions the respondent cannot realistically answer accurately

### Module structure should be explicit

For substantial surveys, each module should usually state:

- module name
- purpose
- target respondent
- recall period
- key outcomes
- expected duration when useful

This reduces drift between design, programming, training, and analysis.

### Measurement quality

Questions should map cleanly to the intended construct.

Prefer:

- behavioral measures where possible
- explicit time windows
- answerable factual questions over vague attitudes when behavior is what matters

Flag:

- confounded constructs
- yes-biased framing
- socially desirable wording
- demand effects
- anchoring from nearby questions
- recall windows that exceed realistic memory

### Cross-question consistency

Terms, time windows, and reference populations should stay stable across related questions.

Flag:

- logical contradictions across items
- screening questions that conflict with downstream assumptions
- inconsistent definitions of the same construct across sections

### Enumerator instructions should be separated from question text

Respondent-facing wording and enumerator instructions should be visibly separated.

Do not bury implementation notes inside the respondent-facing sentence if that can be avoided.

This matters for both translation and field-speed administration.

## Enumerator and implementation standards

The instrument should minimize enumerator discretion.

Flag:

- instructions buried inside question text
- questions requiring judgment calls that should be standardized
- manual calculations that should be automated
- validations that are needed but not defined
- logic that should be handled by the device rather than by memory

If the survey is paper-based, identify which digital logic risks become training and supervision risks.

### Validation rules should be specified

The implementation should distinguish:

- hard validations that block impossible values
- soft warnings that allow override with confirmation
- cross-field consistency checks

If validation logic is needed but not defined, that is an implementation risk.

## Respondent burden

The survey should be sequenced and sized to reduce fatigue and satisficing.

Check:

- whether the sequence moves from easier or broader questions to harder or more sensitive ones
- whether sections are repetitive or unnecessarily long
- where fatigue is most likely to degrade data quality
- whether emotionally sensitive questions are placed with enough rapport and privacy

## Data and analysis readiness

The instrument should produce analyzable data without extensive guesswork.

Check that:

- units are explicit
- denominators and eligibility conditions are clear
- missingness types can be distinguished, such as `refused`, `don't know`, `not applicable`, and system missing
- IDs, dates, and structured values have clear formats
- free-text burden is justified
- key variables can be analyzed without reinterpreting original intent

### Missingness must be typed

Do not collapse all missing values into one bucket.

The survey package should distinguish at least where relevant:

- refused
- don't know
- not applicable
- skipped by logic
- missing due to device or collection failure

If standard numeric codes are used, they should be documented consistently.

### Analysis linkage should exist for major outcomes

Major outcomes should be linked to:

- the underlying variables
- planned tables or figures when known
- relevant hypotheses or operational uses

This helps prevent orphan variables that are collected but never used meaningfully.

## Documentation expectations

A deployable survey package should make available, in the instrument or its companion materials:

- question text
- response options
- variable names when assigned
- skip logic
- validation constraints
- language versions when relevant
- implementation notes for sensitive or high-risk items

For stronger packages, also include:

- coding conventions
- translation glossary
- enumerator manual or instruction layer
- analysis linkage
- pilot debrief notes after testing

Pre-deployment surveys should usually be pilot-tested or cognitively tested unless there is a documented reason not to.

## Translation and language standards

For multilingual surveys, the package should support:

- forward translation
- back translation or equivalent quality review
- cognitive or pilot testing of translated wording

Track key terms and approved translations when terminology is sensitive or technically important.

## Metadata collection standards

Collect automatically where feasible rather than asking respondents or enumerators to enter machine-collectable metadata manually.

Useful fields often include:

- start time
- end time
- duration
- enumerator ID
- GPS when appropriate
- audit timestamps
- device ID
- language

## QA monitoring expectations

A field-ready survey operation should define daily or regular QA checks such as:

- interview duration
- missingness rates
- GPS anomalies
- duplicate households
- heaping
- straightlining
- impossible combinations

The genre standard does not require one fixed dashboard, but it does require that these checks be planned rather than improvised later.

## XLSForm and implementation readiness

If the survey will be programmed in XLSForm or a similar system, each question should already imply:

- type
- constraint
- relevance
- calculation when relevant
- appearance when relevant

Naming conventions should be explicit and consistent.

Snake case is preferred for machine-facing names unless another convention is already standardized across the project.

## Common failure modes

Flag:

- broken or ambiguous skip logic
- overlapping or incomplete response categories
- vague recall periods
- translation-sensitive wording
- sensitive items with no privacy plan
- unstructured free-text overuse
- manual calculations left to enumerators
- undefined validation constraints
- inconsistent constructs across sections
- variables that will be difficult to interpret analytically
- mixed respondent wording and enumerator instructions
- missing consent logic
- undocumented missing-value codes
- no analysis linkage for major outcomes
- survey version drift across files
- no evidence of pilot or cognitive testing before deployment
- wording that is too complex for the likely respondent reading or comprehension level

## Reviewer stance

The reviewer should be skeptical and operationally realistic.

The standard is not whether the survey sounds reasonable in a meeting.
The standard is whether it will survive real field use, digital implementation, and downstream analysis.

