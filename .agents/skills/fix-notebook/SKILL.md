---
name: fix-notebook
description: >
  Auto-fixes common formatting and template structural issues in notebooks.
  Adds missing sections, restructures imports, and removes empty cells.
tools: [Read, Write, Bash]
---

# Skill: Fix Notebook

Repair common notebook linter findings and formatting errors.

## Steps

1. **Parse Lint Report**
   - Read the issues identified by `notebook-lint` or `review-notebook`.

2. **Apply Auto-fixes**
   - **Missing License**: If missing, prepend the Apache 2.0 license block cell to the notebook.
   - **Missing Sections**: Append placeholder template cells for missing sections (e.g., Overview, Cleaning up) if they were accidentally deleted.
   - **Imports Restructuring**: Move all imports found throughout the notebook into the designated "Import libraries" cell.
   - **Empty Cells**: Remove any cells that are entirely empty or contain only comments.
   - **Filename Correction**: If filename naming is incorrect, rename the file following the kebab-case category pattern.

3. **Re-Lint**
   - Run `notebook-lint` again to verify that all auto-fixable errors have been successfully resolved.

4. **Report Changes**
   - Report exactly what cell indexes were modified and what fixes were applied.
