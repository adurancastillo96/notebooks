# Workflow: Notebook Review

Structured review and quality verification process before merging notebook PRs.

## Step 1 — Identify Target
- Find which notebook in `src/` requires review (from active PR or specified paths).
- Read the related task spec to understand the intended learning objectives.

## Step 2 — Structure Compliance Check
- Run the `notebook-lint` skill to verify structure compliance:
  - Verify license header, H1 title, environment note.
  - Verify presence of required H2 sections (Overview, Installation, Before you begin, Cleaning up).
  - Verify file naming convention (`category-name.ipynb`).

## Step 3 — Quality and Security Review
- Run `review-notebook` on the cells:
  - Ensure no hardcoded credentials or project IDs.
  - Verify all TODOs, project IDs, and bucket placeholders are filled or parameterized.
  - Check Python style and GCP SDK usage guidelines.
  - Verify that all libraries installed are listed in the Installation section.

## Step 4 — Pedagogical Review
- Verify that:
  - Objectives are clear and progressive.
  - Every code cell has a preceding markdown cell explaining what it does.
  - No empty or comments-only cells exist.
  - Examples are practical and direct.

## Step 5 — Verify Cleanup
- Double-check that the "Cleaning up" code cell correctly deletes all endpoints, models, buckets, or datasets created during the tutorial.

## Step 6 — Fix Findings
- If linter or review findings can be auto-resolved, run the `fix-notebook` skill after human confirmation.

## Step 7 — Verdict
- Produce the final review report containing the verdict:
  - ✅ **Approved**: Ready for merging.
  - ❌ **Changes Requested**: Detailed action items for the author.
- **CHECKPOINT**: Human reviews the verdict and approves.
