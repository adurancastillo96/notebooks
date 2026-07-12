# Requirements — Notebook Authoring Standards (EARS Notation)

Requirements for authoring workshop notebooks, written in Easy Approach to Requirements Syntax (EARS).

## EARS Patterns Reference
- **Ubiquitous**: The [system] shall [action]
- **Event-driven**: When [event], the [system] shall [action]
- **State-driven**: While [state], the [system] shall [action]
- **Optional**: Where [condition], the [system] shall [action]
- **Unwanted**: If [unwanted condition], the [system] shall [action]

## Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | The notebook shall include an Apache 2.0 license header as the first code cell | Must | Approved |
| FR-002 | The notebook shall include an H1 title heading as the first markdown cell after the license | Must | Approved |
| FR-003 | The notebook shall include an environment compatibility note specifying the tested Python version | Must | Approved |
| FR-004 | The notebook shall include an Overview section explaining what the notebook demonstrates | Must | Approved |
| FR-005 | The notebook shall include an Objective subsection listing learning goals and steps performed | Must | Approved |
| FR-006 | The notebook shall include a Dataset subsection describing the data used and how to access it | Must | Approved |
| FR-007 | The notebook shall include a Costs subsection listing billable GCP products with pricing links | Must | Approved |
| FR-008 | The notebook shall include an Installation section with pip install commands for required packages | Must | Approved |
| FR-009 | The notebook shall include a "Before you begin" section with GCP project setup instructions | Must | Approved |
| FR-010 | The notebook shall include cells for setting GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION as parameterized variables | Must | Approved |
| FR-011 | The notebook shall include authentication instructions for Google Cloud SDK | Must | Approved |
| FR-012 | The notebook shall include a Cleaning up section with resource deletion code | Must | Approved |
| FR-013 | When a new notebook is created, the system shall generate it from `notebook_template.md` | Must | Approved |
| FR-014 | The notebook shall follow the naming convention `category-name.md` and be stored in `src/`, and compile to `artifacts/category-name.ipynb` | Must | Approved |
| FR-015 | The notebook shall define a multi-agent system using Google ADK (`google-adk`) in Python | Must | Implemented |
| FR-016 | The system shall include at least two specialized agents (e.g., `TrajectoryPlannerAgent` and `ObstacleVerifierAgent`) that communicate to design and verify flight trajectories | Must | Implemented |
| FR-017 | The notebook shall model a simplified aircraft engine-out (OEI) climb physics engine | Must | Implemented |
| FR-018 | The notebook shall mock a 3D obstacle database for a challenging airport profile | Must | Implemented |
| FR-019 | The agents shall autonomously search for and verify a trajectory path that guarantees standard engine-out obstacle clearance | Must | Implemented |
| FR-020 | The notebook shall generate 2D elevation profiles and 3D flight path visualizations of the finalized trajectory showing terrain clearance | Must | Implemented |

## Non-Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| NFR-001 | The notebook shall not contain hardcoded GCP project IDs or credentials | Must | Approved |
| NFR-002 | The notebook shall not contain unfilled `{TODO:...}` or `[TODO]` placeholders when submitted for review | Must | Approved |
| NFR-003 | The notebook shall use the latest major GA version of each Google Cloud SDK package | Should | Approved |
| NFR-004 | The notebook shall include clear markdown explanations before each code cell | Should | Approved |
| NFR-005 | The notebook shall handle errors gracefully with try/except blocks where appropriate | Should | Approved |
| NFR-006 | The notebook shall import libraries in a single "Import libraries" cell | Should | Approved |
| NFR-007 | The Google ADK agents shall use Gemini models via Vertex AI as the reasoning core | Must | Implemented |
| NFR-008 | The aircraft performance and obstacle safety margin calculations shall follow simplified standard aviation OEI guidelines | Must | Implemented |

## How to Use This File
- Write requirements using EARS patterns for consistency
- Every requirement must have a unique ID
- Priority follows MoSCoW: Must, Should, Could, Won't
- Status: Draft → Reviewed → Approved → Implemented → Verified
- Link requirements to acceptance criteria in `acceptance.md`
