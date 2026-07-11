# Git Conventions

Rules for commits, branches, and pull requests in this repository.

## Commit Messages
Follow Conventional Commits format:
```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: A new notebook, feature, or section
- `fix`: A notebook bug fix (e.g., code cell correction)
- `docs`: Workshop guides, README, documentation only
- `style`: Markdown cell formatting, code formatting
- `refactor`: Notebook reorganizing, renaming, cell restructuring
- `chore`: GitHub Actions configuration, workspace rules, dependencies
- `test`: Verification tests, validation scripts

### Rules
- Subject line: max 72 characters, imperative mood
- Body: explain *why* the notebook is being added/changed, not just *what* (the diff shows the cells)
- Reference task IDs: `refs T001` or `closes T001`
- Never commit secrets, credentials, or `.env` files

## Branches
- `main` — production-ready workshop material, always functional
- `notebook/<category-name>` — notebook authoring branches (e.g., `notebook/vertex-ai-training`)
- `fix/<description>` — notebook bug fixes (e.g., `fix/vertex-ai-auth-cell`)
- `chore/<description>` — automation scripts and agent config

### AI Agent Branches
- `ai/<agent-name>/<description>` (e.g., `ai/gemini/T001-add-esa-dataset`)

## Pull Requests
- PR description includes: What notebook is added/modified, Why (objectives/learning goals), How (GCP services used), and a checklist of completed sections.
- Link to related task spec: `spec/tasks/TXXX.md`
- All CI checks (structure lint, todo check) must pass before merge
- Require at least one review (human or agent)
- Squash merge to keep history clean

## What NOT to Commit
- `.env` files
- Service account credential JSON files (`service-account-key*.json`)
- `.ipynb_checkpoints/` directory and its files
- IDE configuration folders (`.vscode/`, `.idea/`)
