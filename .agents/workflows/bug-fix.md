# Workflow: Bug Fix

Diagnose, fix, and verify a reported notebook bug.

## Step 1 — Understand the Bug
- Read the bug report carefully.
- Identify the target notebook and the specific code or markdown cell affected.
- Identify expected behavior vs actual behavior (e.g., API call fails, outdated package version, missing variable).
- **Ask**: Is there enough information to reproduce the bug?

## Step 2 — Reproduce
- Replicate the issue locally or in a test workbench environment.
- Document the reproduction steps (cell inputs and execution output errors).
- Do not make changes before reproducing.

## Step 3 — Diagnose
- Trace the code cell logic or API call to locate the root cause (e.g., outdated SDK syntax, service account permission gap, broken dataset link).
- Check if this is a single cell issue or affects other notebooks in the repo.
- Document the diagnosis.

## Step 4 — Fix
- Create a fix branch: `fix/<description>` (e.g., `fix/vertex-training-args`).
- Make the minimal change that fixes the bug. Do not rewrite unrelated cells.
- Ensure the notebook executes cleanly after the fix.

## Step 5 — Verify
- Run `notebook-lint` to check structure compliance.
- Run `review-notebook` to verify code quality and security conventions.
- **CHECKPOINT**: Human reviews and approves the fix.

## Step 6 — Document
- Update `.agents/memory/learnings.md` with details on what caused the bug and how it was resolved.
- If the bug was caused by a missing convention, update the rules in `.agents/rules/`.
