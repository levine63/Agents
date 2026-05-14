# Workflow: Recovery, Checkpoints, and Rollback

## Purpose

The agent must be able to recover from interruption, mistakes, and unsafe changes.

## Checkpoint rules

Create a checkpoint:

- before HIGH-risk operations
- after successful verification
- before large refactors
- before dependency updates
- at natural task boundaries

Preferred checkpoint:

```bash
git status
git diff --stat
git tag -f codex-checkpoint-YYYYMMDD-HHMMSS
```

Use repository conventions if they differ.

## When to rollback

Rollback or request rollback review if:

- a secret was written
- destructive change occurred without approval
- tests show new systemic failure
- the agent made broad unintended edits
- repository state is inconsistent
- user rejects the direction

## Recovery steps

1. Stop making changes.
2. Record current state in `progress_log.md`.
3. Identify last known safe checkpoint.
4. Summarize files changed since checkpoint.
5. Propose rollback command.
6. Execute rollback only if approved for destructive changes.

## Reporting recovery

The final report must include:

- what went wrong
- what was reverted
- what remains changed
- what checks were rerun
- what risks remain
