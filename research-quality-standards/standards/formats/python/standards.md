# Generic Python Standards

## Purpose

These standards apply to general Python code: scripts, utilities, automation, APIs, file watchers, data movers, LLM-review agents, Drive/Gmail integrations, tests, and Codex-generated code.

The goal is code that is runnable, readable, safe, maintainable, debuggable, and reviewable.

These standards are intentionally generic. Statistical analysis, data cleaning, and empirical research requirements are covered in `standards/formats/python_stats/standards.md`.

## 1. File header or module docstring

Every standalone Python script should begin with a header containing:

- Project
- File path
- Author
- Created date
- Last updated date
- Purpose
- Inputs
- Outputs or side effects
- Assumptions
- Environment or dependencies
- How to run
- Notes or limitations

The header should be specific enough that a new team member can understand the script's role without reading the whole file.

Package modules may use a shorter module docstring if the package is documented elsewhere.

## 2. End-to-end execution

Shared scripts must run end-to-end without undocumented manual steps.

If a manual step is unavoidable, document it in the header or README.

Examples of undocumented manual steps:

- "Download this file from an email first"
- "Rename this folder locally"
- "Manually edit the output before running the next script"
- "Run cell 12 before cell 4"
- "Change this path to your computer"

At `DRAFT` stage, undocumented manual steps are usually `WARN` unless they prevent review.
At `SUBMISSION` stage, undocumented manual steps are `BLOCK`.

## 3. Paths

Use project-relative paths.

Preferred:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"
```

Not allowed:

```python
"C:/Users/name/Desktop/file.csv"
"/Users/name/project/file.csv"
```

Hard-coded local paths are `WARN` at `DRAFT` stage and `BLOCK` at `SUBMISSION` stage unless clearly justified.

## 4. Configuration

Use constants at the top of the file for stable configuration.

Preferred:

```python
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
```

Avoid mutable global state.

Do not store secrets, passwords, API keys, or tokens in code. Use environment variables or approved secret-management tools.

Secrets in code are `BLOCK` at every stage.

## 5. Magic numbers

Important numeric constants should be named and explained.

Bad:

```python
if retry_count > 7:
    ...
```

Better:

```python
MAX_RETRIES = 7

if retry_count > MAX_RETRIES:
    ...
```

Not every number needs a constant. Obvious values such as `0`, `1`, or `100` in simple percent calculations may be fine.

Magic numbers are usually `NOTE` or `WARN` at `DRAFT` stage and `WARN` at `SUBMISSION` stage.

## 6. Structure

Prefer this structure for standalone scripts:

```python
def configure_logging() -> None:
    ...

def validate_inputs() -> None:
    ...

def run_task() -> None:
    ...

def main() -> None:
    ...

if __name__ == "__main__":
    main()
```

Avoid long top-to-bottom scripts with hidden state and no functions.

The main guard is required for script-like files.

Variable and function names should be meaningful enough that a reviewer can infer purpose without reverse-engineering every assignment.

## 7. Logging

Use Python's `logging` module for automation, reusable scripts, long-running jobs, APIs, file watchers, agents, and pipelines.

Use:

```python
LOG = logging.getLogger(__name__)
```

near the top of each script or module.

Then use:

```python
LOG.info("Processed %s files", n_files)
LOG.warning("Skipping missing optional file: %s", path)
LOG.error("API request failed: %s", error)
```

instead of scattered `print()` statements.

At minimum, logs should record:

- script start/end where useful
- major processing steps
- warnings
- failures
- created outputs
- counts of processed files or records
- retries or skipped items

Simple beginner or exploratory scripts may use `print()` temporarily, but production, shared, or automated scripts should use logging.

Recommended logging levels:

- `LOG.debug()` for detailed troubleshooting
- `LOG.info()` for normal workflow events
- `LOG.warning()` for recoverable problems
- `LOG.error()` for failures
- `LOG.critical()` for severe failures requiring intervention

Logs should be human-readable and actionable.

Bad:

```text
Error occurred.
```

Better:

```text
Failed to load config/settings.yaml: file missing.
```

## 8. Error handling

Fail clearly when required inputs are missing, invalid, or ambiguous.

Avoid bare exceptions:

```python
except Exception:
    ...
```

Prefer specific exceptions:

```python
except FileNotFoundError:
    ...
except ValueError:
    ...
```

Do not silently continue after serious errors.

Silent exception handling is `BLOCK` at every stage.

## 9. Type hints

Use basic type hints for important functions.

Example:

```python
def normalize_name(name: str) -> str:
    ...
```

Use type hints especially for functions that are reused, imported, tested, or likely to be modified by others.

Do not make type hints so elaborate that they obscure beginner readability.

## 10. Docstrings

Use docstrings for functions that are:

- reused
- non-obvious
- risky
- central to the project
- imported by other scripts
- likely to be modified by interns or Codex

Example:

```python
def validate_inputs(path: Path) -> None:
    """Raise a clear error if the required input file is missing."""
```

Comments should explain why, not merely what.

## 11. Dead or commented-out code

Remove dead code before submission.

Commented-out code is allowed only if it is clearly temporary and explained.

Bad:

```python
# old_df = pd.read_csv("old_file.csv")
# df = old_df.merge(other)
```

Better:

```python
# Keep this alternative import path until the 2024 data freeze is complete.
# TODO: remove after final data delivery.
```

Dead or unexplained commented-out code is usually `NOTE` at `DRAFT` stage and `WARN` at `SUBMISSION` stage.

## 12. Dependencies and environment

Project dependencies must be documented in one of:

- `requirements.txt`
- `pyproject.toml`
- `environment.yml`

The README should explain how to install dependencies.

The project should document:

- Python version where relevant
- important library versions
- dependency file used
- external services or APIs required

Do not require every script header to list every package version. Script headers should mention unusual version dependencies only when relevant.

## 13. Tests and smoke tests

For nontrivial code, include at least one smoke test, test file, or usage example.

A smoke test checks that the code runs on minimal input.

Examples:

```bash
python scripts/example.py
pytest
```

or:

```text
Run this script on tests/fixtures/example_input.csv and confirm it creates outputs/example_output.csv.
```

Smoke tests are especially important for Codex-generated code and automation scripts.

## 14. Outputs and side effects

Scripts must make outputs and side effects explicit.

Examples of side effects:

- creates a file
- modifies a database
- calls an API
- sends an email
- updates a Google Drive folder
- writes logs
- deletes or archives files

Unexpected side effects are not allowed.

Destructive actions require extra care. Prefer moving files to an archive or trash folder rather than deleting them permanently.

Destructive actions without safeguards are `BLOCK` at every stage.

## 15. Ruff

Before submission, run:

```bash
ruff check .
ruff format .
```

Recommended `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "A"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Ruff compliance is necessary but not sufficient. Ruff does not prove that the program is correct.

## 16. AI-generated code

AI-generated code must be manually reviewed.

Check especially for:

- invented paths
- invented APIs
- invented variable names
- silent failures
- wrong assumptions
- overbroad permissions
- unnecessary complexity
- misleading comments
- untested edge cases
- deleting or overwriting user files

Codex or other AI tools should run Ruff and any available tests before submitting code.

## 17. Submission checklist

Before submitting Python code, confirm:

```text
[ ] Header or module docstring complete
[ ] Inputs and outputs/side effects documented
[ ] End-to-end run instructions documented
[ ] No undocumented manual steps
[ ] No absolute local paths
[ ] Secrets are not stored in code
[ ] Configuration is clear
[ ] Important magic numbers named
[ ] Main guard used for standalone scripts
[ ] Important functions have type hints
[ ] Important functions have docstrings
[ ] Errors fail clearly
[ ] No silent bare except
[ ] Logging used appropriately
[ ] Dependencies documented
[ ] Smoke test or usage example included when relevant
[ ] Dead/commented-out code removed or explained
[ ] Ruff check run
[ ] Ruff format run
[ ] AI-generated code disclosed and checked
```

