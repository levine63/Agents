# Workflow: Approvals for Destructive or High-Risk Actions

## Purpose

Some actions require explicit approval, especially in headless or CI-like agent sessions.

## Actions requiring approval

Approval is required before:

- deleting files
- moving files
- overwriting large existing files
- changing database schemas or migrations
- changing deployment, CI, permissions, or security
- using elevated commands, privilege escalation, or permission changes
- rewriting major architecture
- changing public APIs
- modifying files outside allowed project paths
- irreversible data transformations

Before HIGH-risk or destructive execution:

- generate a diff, preview, or change summary when feasible
- preserve a rollback path
- prefer reversible operations
- do not rely on file age alone as evidence that a change is low-risk

## Approval mechanisms

Use the first available approved mechanism.

### 1. Interactive approval

If running in an interactive terminal, ask the user to approve the exact action.

The approval request must include:

- task ID
- action
- files affected
- why needed
- expected risk
- rollback plan

### 2. File-based approval

For headless runs, use `.codex_approvals/`.

Codex creates:

```text
.codex_approvals/[task_id].pending
```

A human approves by creating:

```text
.codex_approvals/[task_id].approve
```

The approval file should include:

```json
{
  "task_id": "task-id",
  "approved_by": "name-or-email",
  "timestamp": "ISO-8601",
  "action": "brief description",
  "files": ["path1", "path2"],
  "rollback_plan_reviewed": true
}
```

Approval files are single-use. After use, move them to `tmp_codex_work/archive/`.

The agent that consumed the approval should archive the used approval file after execution or, at the latest, before writing the final report. If the file cannot be archived, note that in the final report.

### 3. CLI approval flag

A wrapper may provide flags such as:

```bash
--approve-destructive
--approve-task task-id
```

Only use these if the wrapper is trusted and logs approval.

## If approval is missing

Stop and mark task:

```text
BLOCKED: destructive approval required
```

Do not perform the action.

## Dry run preference

For HIGH-risk tasks, prefer:

1. dry run
2. diff preview
3. approval
4. execution
5. verification
6. report
