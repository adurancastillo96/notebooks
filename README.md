# 📓 Workshop Notebooks

> A spec-driven, agent-assisted repository for creating and reviewing workshop notebooks on Google Cloud, Vertex AI, Data Science, ML/AI, and aerospace datasets.

## 🚀 Quick Start

1. Clone this repository
2. Review the notebook template: `notebook_template.md`
3. Create a task spec in `spec/tasks/` for your notebook
4. Use the agent-assisted workflow to author your notebook

## 📁 Structure

```
notebooks/
├── AGENTS.md                 ← Agent guidelines (source of truth)
├── DESIGN.md                 ← Project vision & constraints
├── notebook_template.md      ← Master notebook template (Markdown)
├── .agents/                  ← AI agent framework
│   ├── personas/             ← Agent roles (architect, reviewer, author, etc.)
│   ├── skills/               ← Agent capabilities (create, review, lint, fix)
│   ├── workflows/            ← Multi-step processes (new notebook, review, bug fix)
│   ├── rules/                ← Always-active conventions
│   └── memory/               ← Persistent context between sessions
├── .github/workflows/        ← Automated quality checks on PRs
├── spec/                     ← Notebook specifications & tasks
├── src/                      ← Authored notebooks in Markdown (category-name.md)
├── artifacts/                ← Compiled final Jupyter Notebooks (category-name.ipynb)
├── docs/                     ← Documentation & ADRs
└── reports/                  ← Generated review/lint reports
```

## 🤖 Agent-Assisted Workflow

This repository uses a **spec-driven development** approach with AI agents:

| Phase | What Happens | Agent |
|-------|-------------|-------|
| 0. Design | Define topic, audience, learning objectives | `@notebook-architect` |
| 1. Specification | Write requirements in EARS notation | `@notebook-architect` |
| 2. Technical Plan | Plan sections, GCP services, datasets | `@notebook-architect` |
| 3. Task Breakdown | Create atomic task specs | `@notebook-architect` |
| 4. Authoring | Write notebook from template + spec | `@notebook-author` |
| 5. Review & Compile | Validate, lint, compile, fix, polish | `@notebook-reviewer` |

### Starting a New Notebook

```
# Ask the architect to plan a new notebook
"Act as @notebook-architect and run the new-notebook workflow for a Vertex AI custom training notebook"

# Or start the full cycle
"Run the startcycle workflow for a BigQuery ML forecasting notebook"
```

## 🔍 Automated Quality Checks (GitHub Actions)

Every PR that modifies notebooks in `src/` is automatically checked and compiled:

| Check | What It Validates / Compiles |
|-------|------------------|
| **Structure Lint** | Template sections present and in correct order on source `.md` |
| **Code Review** | AI-powered review via Gemini (Python best practices, GCP SDK usage) |
| **TODO Check** | No unfilled `{TODO:...}` or `[TODO]` placeholders |
| **Auto-Compile** | Compiles all source `src/*.md` files into `artifacts/*.ipynb` and commits them back |

### Required Secret

Set `GEMINI_API_KEY` in your repository secrets for AI-powered code review.
Get your key from [Google AI Studio](https://aistudio.google.com/apikey).

## 📓 Notebook Naming Convention

All source notebooks in `src/` follow the pattern: `category-name.md`
All final compiled notebooks in `artifacts/` follow the pattern: `category-name.ipynb`

Examples:
- `src/vertex-ai-custom-training.md` -> `artifacts/vertex-ai-custom-training.ipynb`
- `src/bigquery-ml-forecasting.md` -> `artifacts/bigquery-ml-forecasting.ipynb`
- `src/aerospace-esa-copernicus-data.md` -> `artifacts/aerospace-esa-copernicus-data.ipynb`

## 📝 Topics Covered

- Google Cloud Platform (GCP)
- Vertex AI (Training, Prediction, Pipelines)
- BigQuery & BigQuery ML
- Data Science & Machine Learning
- AI/ML Research
- Aerospace Datasets (ESA, NASA, Copernicus)

## 📜 License

Apache 2.0 — See the license header in `notebook_template.md`
