---
name: review-notebook
description: >
  Validates a notebook file for template compliance, code quality,
  placeholder presence, security, and cleanup completeness.
  Optionally auto-fixes issues when run with --fix mode.
tools: [Read, Glob, Grep, Bash]
---

# Skill: Review Notebook

Perform a thorough educational and code quality review on modified or completed notebooks.

## Modes

| Mode | Behaviour |
|---|---|
| *(default)* | Review only — produces a markdown report under reports/ |
| `--fix` | Review first, then prompt to run `fix-notebook` to apply corrections |

## Steps

1. **Identify Notebooks**
   - Identify which notebook file in `src/` requires review.
   - Read the corresponding task spec (`spec/tasks/TXXX.md`) for objective context.

2. **Run Quality Checks**
   - Verify all required template sections exist and follow the exact ordering.
   - Scan for hardcoded credentials, project IDs, or bucket names.
   - Scan for unresolved `{TODO:...}` or `[TODO]` placeholders.
   - Check if all import statements are grouped in the Import libraries cell/block.
   - Verify that all code blocks have preceding markdown explanation blocks.
   - Verify that the Cleaning up section actually contains deletion statements for all created GCP resources.

3. **Check Naming & Compilation**
   - Verify file naming follows `category-name.md`.
   - Verify that a corresponding compiled notebook exists in `artifacts/category-name.ipynb` and is in sync.

4. **Produce Report**
   - Save a review report markdown file in `reports/` showing:
     - Summary (overall assessment)
     - Critical Issues (blocking merge)
     - Warnings (should address)
     - Suggestions (optional improvements)
     - Verdict (Approved or Changes Requested)

5. **Fix Issues (if --fix requested)**
   - If `--fix` mode is active, ask the user for confirmation and invoke `fix-notebook` to repair issues.
