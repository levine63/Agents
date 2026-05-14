# Create Plan

## Purpose

Use this skill before substantial implementation, refactoring, or multi-file review work.

The goal is to force a short pause before execution so the agent understands:

- the problem to solve
- the current code or artifact structure
- the relevant dependencies and runtime details
- the tests or checks that will determine success
- the files and folders likely to change

This skill is for planning, not execution.

## When to use

Use this skill when:

- the assignment is multi-step
- multiple files or folders are likely to change
- the requirements are incomplete, ambiguous, or spread across messages
- a requirements document exists and needs refinement
- the task affects logic, interfaces, workflows, or artifacts beyond a trivial edit

Do not use it for tiny typo fixes or other clearly trivial tasks.

## Inputs

Gather only what is needed:

- the user request
- any requirements or design document
- relevant source files
- package or runtime configuration
- existing tests or validators
- standards and templates that materially apply

## Workflow

### 1. Refine the problem statement

Iterate on the requirements until the task is concrete enough to plan.

The plan should identify:

- the objective
- the desired output or behavior
- constraints
- assumptions
- unresolved questions

If the requirements are incomplete, record reasonable assumptions instead of pretending the scope is fully known.

### 2. Analyze the current structure

Inspect the codebase or artifact package to understand the current state.

At minimum, identify:

- the main entry points
- relevant modules, packages, or artifact directories
- runtime or environment details that matter
- likely dependencies
- existing related tests, validators, or workflows

This step should be grounded in actual repository structure, not guessed architecture.

### 3. Define success checks

Before implementation, decide how success will be evaluated.

Prefer:

- existing unit tests
- integration tests
- linters or validators
- artifact-specific checks

If no suitable tests exist, propose the smallest useful new checks or smoke tests.

The plan should state:

- what will be run
- what a passing result means
- what remains unverified if certain checks cannot run

### 4. Map the execution surface

Identify which files and folders are likely to be modified.

Distinguish:

- files that will probably change
- files that may need inspection only
- new files that may need to be created

The purpose is to make the upcoming work reviewable before execution begins.

### 5. Break the work into steps

Create a step-by-step execution plan with manageable units.

Good steps are:

- concrete
- ordered
- testable
- small enough to review

Avoid giant plan items such as:

- `fix code`
- `update docs`
- `make it work`

### 6. Save the plan

For substantial work, save the plan in a repository-visible file when appropriate.

Preferred names:

- `plan.md`
- `docs/workflows/plan.md`
- `tmp_codex_work/work_plan.md`

Use the location that best fits the repository's conventions.

## Required outputs

The planning output should include:

- problem summary
- assumptions and open questions
- current-structure findings
- dependencies and runtime notes
- verification strategy
- file and folder impact map
- ordered execution steps

## Recommended template

Use:

- `templates/planning/plan_template.md`

when a reusable repository plan file is appropriate.

## Reviewer mindset

The point of planning is not ceremony.

The point is to reduce:

- hidden assumptions
- avoidable rework
- missed tests
- sprawling edits

If a task is too large to plan clearly, decompose it further before execution.
