# Architecture — Repository Design

## Overview
A flat notebook repository with a spec-driven authoring workflow.
Notebooks live in `src/` following a `category-name.ipynb` naming convention.
Quality is enforced through local agent-assisted workflows and automated GitHub Actions.

## Architecture Diagram
```mermaid
graph TD
    A["spec/tasks/TXXX.md"] -->|"notebook-architect"| B["Notebook Spec"]
    B -->|"notebook-author + create-notebook"| C["src/category-name.ipynb"]
    C -->|"git push"| D["GitHub PR"]
    D -->|"Actions"| E["Structure Lint"]
    D -->|"Actions"| F["Gemini Code Review"]
    D -->|"Actions"| G["TODO Check"]
    E & F & G -->|"All pass"| H["✅ Merge to main"]
    C -->|"local"| I["notebook-reviewer + review-notebook"]
    I -->|"fix-notebook"| C
```

## Components

### Notebook Template
- **Responsibility**: Define the canonical structure for all workshop notebooks
- **Technology**: Jupyter Notebook (.ipynb)
- **Location**: `notebook_template.ipynb` (root)
- **Data**: Section structure, license header, parameterized variables

### Agent Framework
- **Responsibility**: Provide AI-assisted development lifecycle
- **Technology**: Markdown-based agent definitions (tool-agnostic)
- **Location**: `.agents/`
- **Components**: personas, skills, workflows, rules, memory

### GitHub Actions
- **Responsibility**: Automated quality enforcement on PRs
- **Technology**: GitHub Actions + Python scripts + Gemini API
- **Location**: `.github/workflows/`, `.github/scripts/`
- **Triggers**: PR events modifying `.ipynb` files in `src/`

### Spec Directory
- **Responsibility**: Track notebook authoring standards and task specs
- **Technology**: Markdown files in EARS notation
- **Location**: `spec/`

## Data Flow
1. Author creates a task spec in `spec/tasks/`
2. Agent generates notebook from template into `src/`
3. Author fills in content with agent assistance
4. Local review via `review-notebook` skill
5. Push to GitHub triggers automated checks
6. PR approved and merged to `main`

## Constraints
- All notebooks must follow the template structure
- Python 3.10+ compatibility required
- Notebooks must not contain hardcoded credentials
- Apache 2.0 license header required on all notebooks

## Evolution Plan
- Future: Add notebook execution tests in CI (requires GCP credentials management)
- Future: Add workshop scheduling and attendee tracking
- Future: Multi-language notebook support
