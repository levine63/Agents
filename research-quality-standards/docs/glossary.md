# Glossary

Use this file for recurring technical terms that appear across standards, reviewer prompts, and templates.

## Unit of observation

The thing each row or case in a dataset represents.

Examples:

- one person
- one household
- one village-month
- one firm-year

This is different from measurement units such as kilograms or dollars.

## Units

The measurement units attached to a quantitative variable.

Examples:

- kilograms
- meters
- USD per month
- percentage points

## Clustering level

The level at which standard errors are adjusted to account for correlated observations.

Examples:

- village level
- school level
- firm level

This is common when observations within the same group are not independent.

## Multiple testing

The problem that arises when many hypotheses are tested at once, increasing the chance of finding a statistically significant result by luck alone.

## Fixed effects

A modeling approach that absorbs average differences across groups or time periods so the estimate is identified from within-group or within-period variation.

Examples:

- village fixed effects
- year fixed effects

## Winsorization

A transformation that caps extreme values at a specified threshold rather than deleting them entirely.

Because this changes the data, it should be documented and justified.

## Lockfile

A file that records exact package or dependency versions so another user can recreate the same software environment more reliably.

Examples:

- `poetry.lock`
- `uv.lock`
- `package-lock.json`
