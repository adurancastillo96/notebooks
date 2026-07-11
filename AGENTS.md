# Notebook Workshop Repository — Agent Guidelines

## Project
A spec-driven repository for creating, reviewing, and maintaining workshop notebooks focused on Google Cloud, Vertex AI, Data Science, ML, AI, and aerospace datasets (ESA, NASA).
Stack: Python · Jupyter Notebooks · Google Cloud SDK

## Essential Commands
- lint:    `python .github/scripts/check_notebook_structure.py src/<notebook>.ipynb`
- todos:   `python .github/scripts/check_todos.py src/<notebook>.ipynb`
- new:     Use the `create-notebook` skill with a task spec

## Architecture in One Line
Flat notebook repository with spec-driven authoring workflow — see spec/ARCHITECTURE.md for full detail.

## Conventions
- Follow the coding rules in `.agents/rules/coding.md`
- Follow the notebook rules in `.agents/rules/notebook.md`
- Follow the security rules in `.agents/rules/security.md`
- Follow the git conventions in `.agents/rules/git.md`
- Before installing dependencies: ask for human confirmation.
- If there is ambiguity: stop and ask, do not assume.
- Every spec artifact lives in `spec/` — notebooks implement specs, never the reverse.
- All notebooks must follow the template structure defined in `notebook_template.ipynb`.

## Agent Layer
See `.agents/LOADOUT.md` to know which agent/skill to use in each situation.
Skills available in `.agents/skills/` — activated by description.
Orchestrated workflows in `.agents/workflows/`.

### Skill Folder Structure
Every skill lives in its own folder under `.agents/skills/` and follows this layout:

```
my-skill/
├── SKILL.md        # (Required) Frontmatter metadata + step-by-step instructions
├── scripts/        # (Optional) Python or Bash scripts the skill executes
├── references/     # (Optional) Text files, documentation, or templates
└── assets/         # (Optional) Images or logos used by the skill
```

| Entry | Required | Purpose |
|---|---|---|
| `SKILL.md` | ✅ Yes | Frontmatter (`name`, `description`, `tools`) + full instructions |
| `scripts/` | No | Executable helpers invoked from `SKILL.md` steps |
| `references/` | No | Static reference material: docs, templates, cheat-sheets |
| `assets/` | No | Images, diagrams, or logos referenced in instructions |

## Spec-Driven Notebook Development Cycle
1. **Design** (Phase 0) — Define the notebook topic, target audience, and learning objectives in DESIGN.md
2. **Specification** (Phase 1) — Write notebook requirements in EARS notation
3. **Technical Plan** (Phase 2) — Define sections, GCP services, datasets, code flow
4. **Task Breakdown** (Phase 3) — Atomic tasks in spec/tasks/
5. **Authoring** (Phase 4) — Create notebook from template using create-notebook skill
6. **Review** (Phase 5) — Review, lint, fix, and polish

Each phase requires a **human checkpoint** before proceeding to the next.

## Memory & Context
- Architectural decisions: `.agents/memory/decisions.md`
- Learnings: `.agents/memory/learnings.md`
- Session state: `.agents/memory/PICKUP.md`

## Rules (Always Active)
- `.agents/rules/coding.md` — Python code conventions
- `.agents/rules/notebook.md` — Notebook structure and authoring rules
- `.agents/rules/security.md` — GCP credentials and secrets handling
- `.agents/rules/git.md` — Commits, branches, PRs
- `.agents/rules/style.md` — Formatting, naming, comments
