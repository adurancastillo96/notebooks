---
name: create-notebook
description: >
  Generates a new workshop notebook inside src/ using the master template.
  Fills in metadata, required sections, and content from a task spec.
  Ensures parameterization and required components are pre-scaffolded.
tools: [Read, Write, Bash]
---

# Skill: Create Notebook

Scaffold and write a new workshop notebook based on the master template (`notebook_template.md`) and a task specification.

## Steps

1. **Read Specifications**
   - Read the task specification in `spec/tasks/TXXX.md`.
   - Read `spec/requirements.md` and `.agents/rules/notebook.md` to ensure all structural guidelines are met.

2. **Scaffold from Template**
   - Copy `notebook_template.md` to the destination path inside `src/`.
   - File naming must follow: `src/category-name.md` (e.g., `src/vertex-ai-tabular-training.md`).

3. **Fill required cells**
   - Replace title placeholder with your H1 Title.
   - Fill in Overview, Objective, and Dataset details based on the spec sheet.
   - Populate the Costs table with the specific GCP products used and link to pricing.
   - Add required libraries to the `! pip3 install` cell.
   - Ensure `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `BUCKET_URI` variables are properly formatted.
   - Place all import statements in the designated "Import libraries" cell.
   - Initialize the Vertex AI SDK with project details.

4. **Write Tutorial content**
   - Implement the step-by-step tutorial cells defined in the spec.
   - Ensure every code cell is preceded by an educational markdown cell explaining the operation.
   - Write fully functional Python code; do not leave code placeholders or comments like `# Implement this`.

5. **Ensure Cleanup**
   - Add appropriate code to the Cleaning up section at the end of the notebook to delete all created resources (models, endpoints, buckets, etc.).

6. **Self-Check & Compile**
   - Check the notebook markdown to verify no remaining `{TODO:...}` or `[TODO]` strings exist.
   - Verify naming matches kebab-case guidelines.
   - Compile the notebook to `artifacts/category-name.ipynb` using `.github/scripts/convert_notebook.py --to-ipynb src/category-name.md artifacts/category-name.ipynb`.
