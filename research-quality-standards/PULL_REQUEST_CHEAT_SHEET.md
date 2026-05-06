# Pull Request Cheat Sheet

Use this when making changes to the repository through GitHub.

## What A PR Is

A pull request, or PR, is a reviewable proposal to change the repository.

Typical flow:

1. create a branch
2. make changes on that branch
3. commit the changes
4. push the branch to GitHub
5. open a PR to `main`
6. review, fix comments if needed, and merge

## Minimal Command-Line Flow

Start from `main`:

```powershell
git switch main
git pull
```

Create a branch:

```powershell
git switch -c improve-standards
```

Check what changed:

```powershell
git status
```

Commit:

```powershell
git add .
git commit -m "Improve standards wording"
```

Push the branch:

```powershell
git push -u origin improve-standards
```

Then open a PR on GitHub from `improve-standards` into `main`.

## Good Habits

- keep one topic per PR
- make PRs small enough to review
- let GitHub Actions run before merging
- use clear branch names such as `improve-standards`, `add-lint-rule`, or `fix-template-header`
- use clear PR titles such as `Add MVP lint workflow` or `Tighten verification standards`

## Mental Model

- branch = workspace
- commit = saved checkpoint
- PR = request for review before merge
