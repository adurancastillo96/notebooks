# Technical Plan

## Overview
This plan covers the implementation of the notebook workshop repository
with spec-driven development and automated quality enforcement.

## Components

| Component | Technology | Complexity | Priority |
|-----------|-----------|------------|----------|
| Notebook Template | Markdown (.md) | Low | P0 — Exists |
| Agent Framework | Markdown (.agents/) | Medium | P0 |
| GitHub Actions | YAML + Python | Medium | P0 |
| Spec Directory | Markdown (spec/) | Low | P0 |

## Implementation Order
1. Repository structure and root files
2. Agent rules (always-active conventions)
3. Agent personas and skills
4. Agent workflows
5. GitHub Actions and scripts
6. First notebook authored using the framework

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|----------|
| Notebook location | `src/` directory | Keeps root clean, easy to glob for CI |
| Naming convention | `category-name.md` | Sortable, scannable, descriptive (compiled to `artifacts/category-name.ipynb`) |
| AI review model | Gemini via Google AI Studio | Aligns with GCP focus, free tier available |
| Agent framework | `.agents/` (tool-agnostic) | Works with any AI coding tool |

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Gemini API rate limits | Medium | Low | Use caching, review only changed cells |
| Template drift | High | Medium | Lint checks enforce structure compliance |
| Agent prompt quality | Medium | Medium | Iterative improvement via learnings.md |

## Estimated Effort
- Phase 2 (Agents): 2-3 hours
- Phase 3 (Specs): 30 minutes
- Phase 4 (GitHub Actions): 1-2 hours

---

# Technical Plan — Autonomous EOSID Trajectory Generation Notebook

## Notebook Outline

| Section | Cell Type | Description |
|---------|-----------|-------------|
| **1. License** | Code | Apache 2.0 copyright header cell. |
| **2. H1 Title** | Markdown | `# Autonomous EOSID Trajectory Generation with Google ADK` |
| **3. Env Compatibility** | Markdown | Specifies Python version 3.10.13 and required packages. |
| **4. Overview** | Markdown | Introduces Engine Out Standard Instrument Departure (EOSID), Google Agent Development Kit (ADK), and the pedagogical goals. |
| **5. Objective** | Markdown | Outlines learning outcomes (agent definitions, physics constraints, ADK loops, path plotting). |
| **6. Dataset** | Markdown | Details mock "Innsbruck LOWI" runway coordinates, mountain terrain heights, and twin-engine jet specifications. |
| **7. Costs** | Markdown | Billable products warning (Vertex AI Gemini API usage). |
| **8. Installation** | Code | `! pip3 install --upgrade google-adk google-cloud-aiplatform matplotlib` |
| **9. Before you begin** | Markdown & Code | Project/Region variables parameterization (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `BUCKET_URI`) and auth setup. |
| **10. Import libraries** | Code | Standard imports (`google.adk`, `matplotlib.pyplot`, etc.). |
| **11. Initialize SDK** | Code | `aiplatform.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)` |
| **12. Physics & Airport Setup**| Code | Simple mathematical equations for OEI climb gradient; definition of obstacle coordinates and elevations. |
| **13. Google ADK Agent Setup**| Code | Configures `TrajectoryPlannerAgent` and `ObstacleVerifierAgent` with ADK system instructions and tools. |
| **14. Trajectory Resolution Loop**| Code | Runs ADK agent conversation team to iteratively search for a path that clears all obstacles. |
| **15. Visualization** | Code | `matplotlib` script rendering a 3D trajectory line and 3D terrain/obstacles. |
| **16. Cleaning up** | Code | standard resources cleanup code. |

## Implementation Steps
1. **Mock Data Definitions**: Establish coordinates (X, Y, Z) relative to the runway. Place obstacles at key departure headings. Define thrust/weight equations.
2. **ADK Agent Configuration**: Initialize Gemini model wrapper, define `google-adk` agents, and set up communication channels.
3. **Trajectory Finder Logic**: The agent uses feedback (terrain height checks) to adjust flight paths (turns, headings) until clearance is verified.
4. **Plotting**: Use 3D plots showing the runway, obstacle cones/spheres, and the generated safe flight path.

