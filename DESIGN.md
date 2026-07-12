# Design — Notebook Workshop Repository

## Problem
Creating high-quality, consistent workshop notebooks is time-consuming and error-prone.
Without a structured process, notebooks lack consistent structure, contain unfilled placeholders,
missing cleanup code, hardcoded credentials, and inconsistent pedagogical flow.

## Vision
A spec-driven, agent-assisted repository where every workshop notebook follows a proven template,
is automatically reviewed for quality, and maintains consistent standards across topics including
Google Cloud, Vertex AI, Data Science, ML/AI, and aerospace datasets.

## Users
- **Workshop Author**: Needs to create high-quality notebooks quickly using a template and AI assistance
- **Workshop Reviewer**: Needs to verify notebooks meet quality standards before workshops
- **Workshop Attendee**: Needs clear, well-structured, error-free notebooks to follow during workshops

## Constraints
- **Technical**: Python 3.10+, Jupyter notebooks, Google Cloud SDK, Vertex AI SDK
- **Template**: All notebooks must follow the structure defined in `notebook_template.md`
- **Naming**: Source notebooks in `src/` follow `category-name.md` convention (e.g., `vertex-ai-training.md`), compiled to `artifacts/category-name.ipynb`
- **License**: Apache 2.0 license header required on all notebooks
- **Topics**: Google Cloud, Vertex AI, BigQuery, Data Science, ML/AI, aerospace datasets (ESA, NASA, Copernicus)

## Non-Goals (Explicit)
- We will NOT deploy notebooks as web applications.
- We will NOT build a notebook execution pipeline in CI (requires GCP credentials).
- We will NOT manage workshop logistics (scheduling, registration).

## Design References
- Notebook template: `notebook_template.md`
- Spec-driven development: `.agents/` framework

---

# Notebook Design: Autonomous EOSID Trajectory Generation with Google ADK

## Topic Statement
A hands-on workshop notebook demonstrating how to design and build an autonomous Engine Out Standard Instrument Departure (EOSID) trajectory calculation engine using a multi-agent orchestration framework (Google Agent Development Kit / ADK) on Google Cloud Vertex AI.

## Target Audience
- **Aerospace Software Engineers & Flight Operations Specialists**: Interested in applying modern AI agentic workflows to physical system simulations and trajectory safety validation.
- **AI Developers & Solutions Architects**: Looking for an advanced, non-trivial, multi-agent orchestrator example using Google ADK and Vertex AI.

## Objectives & Learning Goals
1. **Orchestrate Multi-Agent Systems**: Define and run collaborative agent schemas using Google Agent Development Kit (ADK) in Python.
2. **Aerospace Physics & Constraint Solving**: Model simplified physical variables for Engine-Out (OEI) takeoffs, obstacles (elevation, coordinates), and navigation constraints.
3. **Safety Trajectory Calculation**: Implement an agentic loop to compute and verify obstacle clearance climb profiles.
4. **Vertex AI Integration**: Use Gemini models as the core reasoning engine for ADK agents.
5. **Visualization**: Plot the generated 2D/3D flight path against surrounding terrain/obstacles in the notebook.

## Key GCP Services & Tools
- **Vertex AI (Gemini API)**: Reasoning engine for agent decision-making.
- **Google Agent Development Kit (ADK)**: Python SDK (`google-adk`) for orchestrating agents, tools, and state transitions.

## Target Dataset / Inputs
- **Airport Runway & Obstacle Profiles**: Mocked or loaded from public sources (e.g., a standard challenging departure airport profile like Aspen ASE or Innsbruck INN with terrain heights and obstacle databases).
- **Aircraft Performance Specifications**: A simplified physics model (thrust, weight, drag, OEI climb gradient) representing a standard passenger jet (e.g., a commercial twin-engine aircraft).

## Key Constraints
- Must run entirely within a Jupyter Notebook environment.
- Must avoid hardcoded credentials or project IDs.
- Must clean up any generated resources at the end.

