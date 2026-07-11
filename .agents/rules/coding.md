# Coding Conventions

These rules are always active in the workspace. Every agent must follow them when writing code inside notebooks.

## General Python & Notebook Rules
- Write clear, self-documenting Python code.
- Functions should do one thing and do it well.
- Keep notebook cells focused: a code cell should perform one logical task.
- Avoid writing large blocks of code in a single cell (aim for < 20 lines where possible). If code is too long, consider writing helper functions or modularizing.
- Avoid global mutable state that must be run sequentially across cells in non-intuitive ways.
- Handle errors explicitly — never swallow exceptions silently. Wrap network calls or GCP operations in try-except blocks where appropriate.

## Naming
- Variables: `snake_case` (Python standard)
- Functions: `snake_case` (e.g., `get_user_by_id`)
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Helper files: `kebab-case.py` (if any separate source files are created)
- Booleans: prefix with `is_`, `has_`, `should_`, `can_`

## Structure
- All library imports must be placed in the designated "Import libraries" cell at the beginning of the notebook.
- Group imports: standard library, external packages, GCP-specific libraries (e.g., `google.cloud.aiplatform`).
- Define helper functions at the top of the notebook or in dedicated cells before they are used.
- Prefer pure functions where possible.

## Dependencies
- Never install a dependency without human approval.
- Justify every new package added to the "Installation" section.
- Use the `--upgrade` and `--quiet` flags when installing packages inside notebooks (e.g., `! pip3 install --upgrade --quiet google-cloud-aiplatform`).
- Pin dependency major versions when appropriate to ensure long-term notebook execution stability.

## Error Handling
- Use specific exceptions, not generic ones (e.g., raise `ValueError` rather than a generic `Exception`).
- Print user-friendly error messages that help workshop attendees debug issues.
- Log or print errors with descriptive details.

## Performance
- Don't optimize prematurely, but avoid wasteful compute (e.g., loading huge datasets into memory all at once).
- Use paging or limits when fetching large lists of resources from GCP APIs.
