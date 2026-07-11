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
- **Template**: All notebooks must follow the structure defined in `notebook_template.ipynb`
- **Naming**: Notebooks follow `category-name.ipynb` convention (e.g., `vertex-ai-training.ipynb`)
- **License**: Apache 2.0 license header required on all notebooks
- **Topics**: Google Cloud, Vertex AI, BigQuery, Data Science, ML/AI, aerospace datasets (ESA, NASA, Copernicus)

## Non-Goals (Explicit)
- We will NOT deploy notebooks as web applications.
- We will NOT build a notebook execution pipeline in CI (requires GCP credentials).
- We will NOT manage workshop logistics (scheduling, registration).

## Design References
- Notebook template: `notebook_template.ipynb`
- Spec-driven development: `.agents/` framework
