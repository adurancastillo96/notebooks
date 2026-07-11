# Style Guide

Formatting and style standards for Python code and markdown cells in notebooks.

## Python Code Formatting
- Code cells should follow PEP 8 styling conventions.
- Use 4 spaces for indentation in Python code.
- Keep line lengths in code cells under 100 characters to prevent horizontal scrolling in Jupyter UI.
- Use f-strings for string interpolation instead of format or % operator.
- Comment complex code logic inside code cells explaining *why* a particular SDK method is called, rather than *what* it does.

## Markdown Cells
- Use one sentence per line in markdown cells where possible (leads to better Git diffs).
- Use ATX headers (`#`, `##`, `###`) instead of underlined headers.
- Use bold text for emphasizing keywords or user actions.
- Use backticks (`` ` ``) for code blocks, terminal commands, file paths, variables, and API/SDK names inside markdown text.
- Use bullet points for structured lists (like steps or prerequisites) to improve readability.
- Maintain an encouraging, clear, educational tone suitable for technical workshops.

## TODO & FIXME Format
- Any temporary TODO markers in notebooks must follow: `# TODO(author): message — refs TXXX`
- No TODO markers should remain in the notebook when submitting a PR for merge. Use the todo-check workflow to verify.
- If a section is incomplete, mark it as `[TODO] Add your content here`.
