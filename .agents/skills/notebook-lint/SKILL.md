---
name: notebook-lint
description: >
  Scans notebook files for template structure compliance, file naming conventions,
  and resource cleanup code. Standalone check that reports specific issues.
tools: [Read, Glob, Grep, Bash]
---

# Skill: Notebook Lint

Automated check for template adherence and common formatting errors.

## Steps

1. **Locate Target Files**
   - Find all `.md` files in the specified path or in the `src/` directory.

2. **Check Structure**
   - Check if the Apache 2.0 license block is the first block/cell.
   - Verify the second block is an H1 title that does not contain `[TODO]`.
   - Verify existence of all H2 headers: `## Overview`, `## Installation`, `## Before you begin`, `## Cleaning up`.
   - Verify existence of subsections: `### Objective`, `### Dataset`, `### Costs`.

3. **Check Variables**
   - Scan code cells for `GOOGLE_CLOUD_PROJECT =` and `GOOGLE_CLOUD_LOCATION =` (or `PROJECT_ID` and `REGION`) variable initializations.
   - Flag any hardcoded project IDs or buckets.

4. **Verify Imports**
   - Check if import statements exist outside the designated "Import libraries" cell/block.

5. **Verify Naming**
   - Ensure the notebook filename matches `category-name.md` (lowercase, hyphens, no spaces).

6. **Log Results**
   - Output lint report with:
     - **ERROR**: Blocks PR merging (missing license, wrong naming, missing required sections, hardcoded project IDs).
     - **WARNING**: Should be corrected (empty cells/blocks, imports outside designated cell/block, missing cleanup steps).
     - **INFO**: Suggestions (markdown cell comments, code line lengths).
