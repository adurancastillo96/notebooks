# Architectural Decisions Log

Record of significant decisions made during development.
Each entry links to a full ADR in `docs/ADR/` when applicable.

| Date | Decision | Rationale | ADR |
|------|----------|-----------|-----|
| 2026-07-11 | Notebook Location | Store all completed workshop notebooks in the `src/` directory to keep the root directory clean and facilitate automated glob checks in CI/CD. | — |
| 2026-07-11 | Naming Convention | Enforce `category-name.ipynb` kebab-case naming for all notebook files to make them scannable, sortable, and descriptive of their technical focus. | — |
| 2026-07-11 | AI Review Model | Select Gemini via Google AI Studio API for pull request code reviews, aligning with the Google Cloud/Vertex AI workshop context and utilizing its free tier. | — |
| 2026-07-11 | SDD Cycle Adaptation | Tailored the spec-driven development cycle specifically for notebooks, replacing software engineering specs (DB, API) with section plans and pedagogical outlines. | — |
| 2026-07-12 | Google ADK Framework | Chosen `google-adk` Python SDK to demonstrate state-of-the-art agent coordination in Vertex AI workshops. | — |
| 2026-07-12 | Gemini 1.5 Flash Model | Selected `gemini-1.5-flash` via Vertex AI as the reasoning core for both trajectory planner and obstacle verification agents due to low latency, high context window, and cost-efficiency. | — |

## How to Use This File
- Add a new row for every significant technical decision.
- Link to a full ADR for decisions that affect architecture.
- Review this file at the start of each session for context.
- Never delete entries — they are historical record.
