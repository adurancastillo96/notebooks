# Loadout — When to Use What

Quick reference for which agent, skill, or workflow to activate in each situation.

| Situation | Persona | Skill | Workflow |
|---|---|---|---|
| Plan a new notebook topic | notebook-architect | write-specs | — |
| Create a notebook from scratch | notebook-architect | create-notebook | new-notebook.md |
| Write/complete notebook content | notebook-author | create-notebook | — |
| Review a notebook PR | notebook-reviewer | review-notebook | notebook-review.md |
| Lint a notebook for issues | notebook-reviewer | notebook-lint | — |
| Fix notebook issues | notebook-author | fix-notebook | — |
| Bug reported in notebook | — | — | bug-fix.md |
| Research datasets (ESA/NASA) | researcher | research-dataset | — |
| Write workshop documentation | workshop-docs | — | — |
| Full SDD cycle for a notebook | all | all | startcycle.md |

## Recommended Model by Task

| Task Type | Model Size | Examples |
|---|---|---|
| Planning / design | Large | Workshop notebook outlines, requirements, section plans |
| Authoring / Implementation | Medium | Generating code cells, writing markdown explanations |
| Linting / syntax check | Small | Running notebook structure lint, placeholder scanning |
| Review | Medium | PR notebook reviews, security audits |
| Research | Large | Dataset identification, GCP API evaluation |

## How to Activate

- **Persona**: Reference by name (e.g., "act as the notebook-architect agent")
- **Skill**: Reference by name or trigger phrase (e.g., "use create-notebook for T001")
- **Workflow**: Reference by name (e.g., "run the new-notebook workflow")
- All definitions are in `.agents/personas/`, `.agents/skills/`, and `.agents/workflows/`
