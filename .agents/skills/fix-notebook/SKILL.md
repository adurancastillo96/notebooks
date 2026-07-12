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
   - **Missing License**: If missing, prepend the Apache 2.0 license block to the markdown file.
   - **Missing Sections**: Append placeholder template sections (e.g., Overview, Cleaning up) if they were accidentally deleted.
   - **Imports Restructuring**: Move all imports found throughout the notebook into the designated "Import libraries" cell/block.
   - **Empty Cells/Blocks**: Remove any cells/blocks that are entirely empty or contain only comments.
   - **Filename Correction**: If filename naming is incorrect, rename the file following the kebab-case category pattern with `.md` extension.

3. **Re-Lint & Compile**
   - Run `notebook-lint` again to verify that all auto-fixable errors have been successfully resolved.
   - Re-compile the notebook to `artifacts/` using `.github/scripts/convert_notebook.py --to-ipynb src/category-name.md artifacts/category-name.ipynb`.

4. **Report Changes**
   - Report exactly what changes were applied.
