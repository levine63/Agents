# Agents

## Genre

`custom`

Justification: this is a top-level collection repository that currently organizes one contained project rather than exposing one standalone runtime of its own.

## Summary

This repository is a container for agent-related projects and supporting materials. Its current primary subproject is `./research-quality-standards/`, which defines reusable quality standards, reviewer instructions, templates, and lightweight linting for research, code, writing, README files, interviews, and LLM-assisted work.

## Quick Start

```bash
python ./research-quality-standards/scripts/check_readme.py ./research-quality-standards/README.md
```

**Expected output**

```text
README QUALITY CHECK
No issues found by static checker.
```

## Environment

- Python: 3.11 or newer
- Tested operating systems: Windows 11
- System dependencies: none for the quick start
- Install step: no package install is required for the quick start because the checker uses the Python standard library only
- Lockfile: no top-level lockfile; rationale: the top-level repo is a thin collection layer and the current quick start uses only standard-library Python inside the contained standards project

## Data And Inputs

- Main inputs:
  - `./research-quality-standards/README.md`
  - the contained standards, reviewer, template, and script files under `./research-quality-standards/`
- Primary contained project:
  - `./research-quality-standards/`
- Minimal example:
  - `./examples/minimal/` is not needed at the top level because this repository is a collection repo and the meaningful runnable example lives inside the contained standards project
- Sensitive or restricted material:
  - none required for the top-level quick start

## Outputs

- Visible result from the quick start:
  - console output confirming whether `./research-quality-standards/README.md` passes the static README checker
- Main generated artifacts:
  - none at the top level for the default quick start
- Determinism:
  - the quick start is deterministic for the same file contents

## Reproducibility

- Re-run the exact quick-start command above from the repository root.
- The top-level quick start is deterministic.
- Behavior outside the top-level quick start depends on the contained subproject and its own documented workflow.

## Tests And Validation

- Smoke check:
  - `python ./research-quality-standards/scripts/check_readme.py ./research-quality-standards/README.md`
- Deeper validation:
  - `python -m unittest scripts.tests.test_check_readme scripts.tests.test_lint_mvp`
  - run this from `./research-quality-standards/`
- Not covered at the top level:
  - there is no separate top-level test suite yet
  - live GitHub Actions execution is not verified by the quick start

## Assumptions

- the main maintained content currently lives inside `./research-quality-standards/`
- future agent-related projects may be added as separate top-level directories

## Limitations And Risks

- this top-level repo is currently thin and depends on subproject documentation for most operational detail
- if additional subprojects are added later, the top-level README could drift unless it is kept in sync
- the quick start validates documentation quality for one contained project; it does not validate every future subproject automatically

## Not Included

- a standalone top-level application runtime
- large data, secrets, or private credentials
- unified top-level tooling for every future subproject

## File Structure

```text
Agents/
|- research-quality-standards/
|  |- standards/
|  |- reviewer/
|  |- maker_prompts/
|  |- templates/
|  |- scripts/
|  \- README.md
|- README.md
```

## Troubleshooting

**Error:** `python: can't open file './research-quality-standards/scripts/check_readme.py'`  
**Cause:** the command was run from the wrong directory or the repo was not cloned fully  
**Fix:** run the command from the `Agents` repository root and confirm `./research-quality-standards/` exists

**Error:** `No module named 'scripts'`  
**Cause:** deeper tests were run from the wrong directory  
**Fix:** `cd ./research-quality-standards` before running `python -m unittest scripts.tests.test_check_readme scripts.tests.test_lint_mvp`

## Contributing Or Workflow

- make changes inside the relevant subproject when possible rather than inventing top-level duplicates
- keep the top-level README synchronized when new top-level subprojects are added
- use focused branches and pull requests for coherent change sets when practical

## Contact Or Ownership

- Owner: repository maintainer for `Agents`
- Current primary subproject maintainer: see `./research-quality-standards/README.md`

## License

- Internal working repository unless a top-level license is added later
