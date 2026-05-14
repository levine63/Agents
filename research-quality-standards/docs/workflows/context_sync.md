# Workflow: Context Sync and Stateful Resumption

## Purpose

AI sessions can be interrupted. The agent must resume work safely instead of restarting blindly.

This workflow is mandatory for Tier 2 work and recommended for Tier 1 work that may span turns. Tier 0 work may skip it.

## Required files

Runtime files live in `tmp_codex_work/`:

- `progress_log.md`
- `work_plan.md`
- `final_report.md`
- `checkpoints/`
- `archive/`

## Lifecycle and retention

- Keep only the current active session files at the top level of `tmp_codex_work/`.
- When a Tier 1 or Tier 2 session is complete and a new session begins, move the prior session's `progress_log.md`, `work_plan.md`, and related checkpoints into `tmp_codex_work/archive/`.
- Preserve the prior `final_report.md` either in the archive bundle or in another clearly named retained copy before replacing it.
- Do not silently delete prior session records. Archive first.
- If stale runtime files accumulate, archive them during the next non-trivial maintenance pass rather than deleting them ad hoc.

## Mandatory start procedure

Before planning or execution:

1. Check whether `tmp_codex_work/progress_log.md` exists.
2. Check whether `tmp_codex_work/final_report.md` exists.

### Case A: neither exists

Fresh session.

Actions:

- create `progress_log.md`
- create `work_plan.md` after planning

### Case B: progress log exists, final report does not

Interrupted session.

Actions:

- read `progress_log.md`
- read `work_plan.md` if present
- identify completed tasks
- identify current or partial task
- resume from the next safe step
- do not redo completed work unless necessary
- append a resumption entry

### Case C: both exist

Prior session completed.

Actions:

- archive prior runtime files if needed
- start a new session
- preserve old final report

## Required progress log fields

`progress_log.md` should contain:

- session ID
- start time
- last update time
- mode
- current task
- completed tasks
- files changed
- commands run
- verification results
- blockers
- reviewer results

Use `templates/progress_log_template.md`.

## Resumption validation

Before resuming:

- check `git status`
- check whether partial files were written
- compare progress log to actual file changes
- rerun relevant tests if the last task was interrupted during verification

## Stale sessions

If a session appears stale or inconsistent:

- do not guess
- write a status summary
- mark status as BLOCKED
- ask for human review
