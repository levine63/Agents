### Python Statistics and Research Code Standards

#### Purpose

These standards apply to Python code that cleans data, builds analysis datasets, runs statistical models, performs simulations, creates tables, creates figures, or supports empirical research.

These rules supplement the Generic Python Standards. They do not replace them.



Related template: [python_stats template](../../../templates/code/python_stats/template.py)

#### 1. Generic Python standards apply

All Generic Python Standards apply to statistics and research code.

In particular, statistics code must still follow standards on:

- file headers
- project-relative paths
- no hard-coded local paths
- logging
- clear errors
- no silent bare except
- main guard
- dependencies
- smoke tests where relevant
- Ruff
- AI-generated-code disclosure

#### 2. Data safety

`data/raw/` is read-only.

Scripts must not overwrite raw data.

Derived files should go in approved folders such as:

```text
data/clean/
data/derived/
outputs/
tmp/
```

Temporary or exploratory outputs should be clearly marked.

Raw data should remain traceable. Whenever possible, cleaned files should preserve IDs needed to link rows back to source data.

#### 3. Raw data source metadata

Data-analysis scripts, READMEs, or adjacent analysis notes must document the raw data source.

Include:

- origin/source
- access or download date
- unit of observation
- known limitations or known data issues
- whether the data are raw, cleaned, simulated, or manually constructed

At Submission stage, missing raw data source documentation is BLOCK.

#### 4. Cleaning must be reproducible

All cleaning steps should be in code.

Do not rely on silent upstream manual cleaning, manual Excel edits, or undocumented recoding.

If a manual correction is unavoidable, document:

- what was changed
- why
- who changed it
- when
- where the original can be found

At Draft stage, undocumented manual cleaning is WARN or BLOCK depending on severity.
At Submission stage, undocumented manual cleaning is BLOCK.

#### 5. Research metadata

Analysis scripts should document:

- unit of observation
- sample restrictions
- treatment/control or exposure definitions
- outcome definitions
- covariates
- weights, if used
- clustering level, if applicable
- fixed effects, if applicable
- missing-data handling
- whether outputs are exploratory, robustness checks, draft tables, or manuscript-ready

This information belongs in the file header, README, or adjacent analysis note.

#### 6. Row-count logging

Scripts must log row counts before and after:

- filters
- merges
- appends
- deduplication
- sample restrictions
- dropping missing values
- reshaping
- collapsing or aggregating
- random sampling

Example:

```python
before_n = len(df)
df = df.loc[df["age"] >= 18].copy()
after_n = len(df)
LOG.info(
    "Age restriction: rows before = %s; rows after = %s; dropped = %s",
    before_n,
    after_n,
    before_n - after_n,
)
```

Large or surprising row losses must be explained in comments, logs, or an output note.

#### 7. Merge safety

Before merges, check whether merge keys are unique when uniqueness is expected.

After merges, report:

- rows before merge
- rows after merge
- unmatched rows
- duplicate key problems
- merge type: one-to-one, many-to-one, one-to-many, or many-to-many

Many-to-many merges require explicit justification.

Unexpected many-to-many merges are a common source of incorrect results because they silently multiply rows.

#### 8. Pandas safety

Avoid chained assignment.

Bad:

```python
df[df["age"] > 18]["income"] = 0
```

This may trigger `SettingWithCopyWarning` and can silently fail to modify the intended DataFrame.

Preferred:

```python
df.loc[df["age"] > 18, "income"] = 0
```

When creating a filtered subset that will be modified, explicitly use `.copy()`:

```python
adults = df.loc[df["age"] > 18].copy()
```

Do not suppress `SettingWithCopyWarning` unless the cause has been understood and fixed.

#### 9. Type safety and import checks

Check variable types after loading data.

CSV and Excel imports may silently convert:

- IDs to floats
- zip codes to integers
- categorical values to mixed types
- date strings to object columns
- missing values to `NaN`
- large numeric IDs to rounded scientific notation

Scripts should explicitly check or set types for key variables.

Example:

```python
df["household_id"] = df["household_id"].astype("string")
```

#### 10. Missing data

Scripts should document how missing data are handled.

Examples:

- dropped
- retained as missing
- imputed
- coded as zero
- coded as an explicit category
- excluded only for specific analyses

Do not silently drop missing data in key variables.

When dropping missing observations, log the number dropped.

#### 11. Reproducibility

Set random seeds for:

- simulations
- bootstraps
- random sampling
- train/test splits
- randomized models
- Monte Carlo analysis

Example:

```python
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
```

If a package has its own random-state argument, set that too.

Randomness without a seed is BLOCK at every stage unless explicitly justified.

#### 12. Variable labels and data dictionary

Cryptic variable names must be mapped to plain-English meanings.

This can be done in:

- code comments
- a data dictionary
- variable labels
- README
- table notes

Example:

```text
hhid = household ID
treat = assigned treatment group
ors_any = caregiver reports child received any ORS during illness episode
```

This is especially important for Stata-like or survey-export variable names.

#### 13. Functional-form rationale

Non-obvious modeling choices should have a brief rationale.

Examples:

- log outcome
- quadratic term
- winsorization
- spline
- interaction term
- nonlinear transformation
- index construction

Bad:

```python
df["log_income"] = np.log(df["income"])
```

Better:

```python
# Use log income because income is highly right-skewed and the coefficient is interpreted approximately as a percent change.
df["log_income"] = np.log(df["income"])
```

Do not require long rationales for standard or purely mechanical transformations.

#### 14. Model transparency

Regression or model scripts should make clear:

- outcome
- treatment/exposure
- covariates
- fixed effects
- weights
- clustering level
- sample restrictions
- estimation method
- whether the model is exploratory or confirmatory

A table-generating script should make it possible to trace each column of a table back to a model specification.

#### 15. Units in summary statistics

Summary statistics tables should show units for measured quantities.

Examples:

- age in years
- income in local currency/month
- temperature in C
- distance in km
- blood lead level in ug/dL
- time in minutes

Missing units in summary statistics are WARN at Draft stage and WARN or BLOCK at Submission stage depending on importance.

#### 16. Output discipline

Tables and figures should have clear, stable names.

Good:

```text
outputs/tables/table_1_summary_stats.xlsx
outputs/figures/figure_2_treatment_effects.png
```

Bad:

```text
final_table.xlsx
newnewfigure.png
test_output.csv
```

Generated outputs should not require manual editing whenever avoidable.

If manual editing is unavoidable, document what was edited.

#### 17. Graph and table provenance

Tables and figures should be reproducible from code.

Each manuscript-relevant output should be traceable to:

- source script
- input data
- sample
- model specification, if relevant
- date generated

If possible, write a small metadata note or log line when creating major outputs.

#### 18. Scientific caution

Ruff-clean code is not necessarily valid analysis.

A script can pass Ruff and still:

- use the wrong unit of observation
- cluster at the wrong level
- leak treatment assignment
- define the outcome incorrectly
- drop the wrong sample
- merge incorrectly
- use inappropriate weights
- report exploratory results as confirmatory
- misinterpret coefficients

Code review must therefore include scientific and statistical review, not just linting.

#### 19. AI-generated statistical code

AI-generated statistical code must be checked especially carefully.

Common AI errors include:

- inventing variable names
- assuming treatment coding
- choosing the wrong standard errors
- using inappropriate models
- silently dropping missing data
- merging on the wrong keys
- generating plausible but false comments
- producing tables that do not match the intended specification

AI-written analysis code should not be treated as valid until a human verifies the research logic.

#### 20. Statistics-code submission checklist

Before submitting Python statistics or research code, confirm:

```text
[ ] Generic Python checklist completed
[ ] Research context documented
[ ] Raw data source documented
[ ] Unit of observation stated
[ ] Sample restrictions stated
[ ] Outcomes defined, with units where relevant
[ ] Treatment/control or exposure variables defined
[ ] Missing-data handling documented
[ ] data/raw/ not modified
[ ] Required columns checked
[ ] Key variable types checked
[ ] Row counts logged after filters/merges/restrictions
[ ] Merge keys checked where relevant
[ ] Many-to-many merges justified or removed
[ ] Chained assignment avoided
[ ] .loc used for assignment
[ ] .copy() used for modified filtered subsets
[ ] Random seed set where randomness is used
[ ] Variable labels or data dictionary supplied for cryptic names
[ ] Non-obvious functional forms briefly justified
[ ] Summary statistics include units
[ ] Tables/figures have clear names
[ ] Outputs are reproducible from code
[ ] AI-generated analysis code disclosed and manually checked
```

