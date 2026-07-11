---
description: End-to-end workflow for planning, authoring, and review of a single new workshop notebook.
---

# Workflow: New Notebook

End-to-end workflow for planning, authoring, and review of a single new workshop notebook.

## Step 1 — Understand the Topic
- Read the notebook request.
- Read existing `spec/requirements.md` and `.agents/rules/notebook.md` for context.
- **Ask**: Is the topic and required dataset well-defined? If not, run dataset research.

## Step 2 — Create Branch
- Branch naming: `notebook/<category-name>`
- Example: `notebook/vertex-ai-custom-prediction`

## Step 3 — Write Task Spec
- Create a task spec file `spec/tasks/TXXX-<notebook-name>.md` with:
  - Topic description and learning objectives.
  - Required sections (standard template sections).
  - GCP APIs/services and target dataset.
  - Detailed task breakdown (steps for the author).
  - Acceptance criteria (DoD).
- **CHECKPOINT**: Human reviews and approves the task spec.

## Step 4 — Research Dataset (Optional)
- Use the `research-dataset` skill to find and document appropriate open datasets.

## Step 5 — Author the Notebook
- Use the `create-notebook` skill to scaffold from the template.
- Implement Python cells and markdown descriptions following repository rules.
- Ensure all created resources are deleted in the cleanup cell.

## Step 6 — Self-Review & Lint
- Use `notebook-lint` to verify structure, naming, and placeholder completion.
- Run `review-notebook` to verify pedagogical flow and code safety.
- Run `fix-notebook` to resolve any automated linter warnings.

## Step 7 — Pull Request Preparation
- Create a PR containing the notebook file in `src/` and the spec task.
- Write a clear PR description detailing:
  - Notebook topic and target audience.
  - Learning objectives achieved.
  - GCP services demonstrated.
  - Verification checklist (lint checks passed, cleanup confirmed).
- **CHECKPOINT**: Human reviews and merges the PR.

## Step 8 — Cleanup
- Mark the task ✅ completed in `spec/tasks/TXXX.md`.
- Update `.agents/memory/PICKUP.md` with session details.
