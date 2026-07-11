# Notebook Rules

Rules specifically for notebook structure, cell ordering, and naming convention.

## Template Compliance
- All workshop notebooks must follow the standard structure defined in `notebook_template.ipynb`.
- The following sections must be present and ordered exactly as in the template:
  1. **License cell**: An Apache 2.0 license code cell (starts with `# Copyright 2023 Google LLC`)
  2. **H1 title heading**: A markdown cell with a single `# ` header. Must not be `[TODO]`.
  3. **Tested Environment Note**: Markdown cell specifying the tested Python version and environment.
  4. **Overview**: Explain what the tutorial demonstrates, who it's for, and prerequisites.
  5. **Objective**: List learning goals and steps performed.
  6. **Dataset**: Describe the dataset used, its source, licensing, and access.
  7. **Costs**: List billable components with links to pricing documentation.
  8. **Installation**: Code cell running `! pip3 install` for required libraries.
  9. **Before you begin**:
     - **Set your project ID**: Code cell parameterizing `PROJECT_ID`.
     - **Region**: Code cell parameterizing `REGION`.
     - **Authenticate your Google Cloud account**: Detailed instructions and commented out authentication cells.
     - **Create a Cloud Storage bucket**: Parameterizing `BUCKET_URI` and gsutil bucket creation.
  10. **Import libraries**: Code cell with all required imports.
  11. **Initialize Vertex AI SDK for Python**: Code cell calling `aiplatform.init()`.
  12. **[Main Content]**: The tutorial steps.
  13. **Cleaning up**: Code cell deleting created endpoints, models, buckets, etc.

## Cell Rules
- Every code cell should have a preceding markdown cell explaining its purpose and context.
- No empty cells.
- No code cells containing only comments.
- Code cells must be readable and educational.

## Parameterization
- `PROJECT_ID`, `REGION`, `BUCKET_URI` must be parameterized using `@param` annotations so they are easily configurable by users.
- Never hardcode user-specific project IDs, bucket names, or API credentials.

## Notebook Naming
- All notebooks in `src/` must follow the kebab-case naming convention: `category-name-of-the-notebook.ipynb`.
- Allowed categories: `vertex-ai`, `bigquery`, `data-science`, `ml`, `aerospace`, `research`, etc.
- Example: `src/vertex-ai-custom-training.ipynb`

## Outputs
- Save notebooks with empty cell outputs unless the cell displays an expected demonstration result (e.g., plot, prediction table) that workshop attendees should see pre-rendered.
