---
name: write-specs
description: >
  Turns a raw workshop notebook idea into a rigorous technical spec.
  Populates requirements.md, acceptance.md, ARCHITECTURE.md and plan.md in sequence,
  then halts for human approval before proceeding.
tools: [Read, Write]
---

# Skill: Write Specs

Plan and document the outline, goals, and technical dependencies for a workshop notebook inside the `spec/` folder.

## Steps

1. **Phase 0 — Design**
   - Clarify the notebook topic, target audience, and primary learning objectives.
   - List the GCP services (Vertex AI, BigQuery, GCS) and external APIs/datasets (NASA, ESA) that will be demonstrated.

2. **Phase 1 — Specification**
   - Read the current `spec/requirements.md` and add specific requirements for the notebook using EARS notation (e.g., "The notebook shall use the Sentinel-2 API to fetch satellite imagery").
   - Link these requirements to acceptance criteria in `spec/acceptance.md` using Given/When/Then format.

3. **Phase 2 — Technical Plan**
   - Outline the logical steps and flow of the notebook in `spec/plan.md`.
   - Update `spec/ARCHITECTURE.md` with components and data flows specific to this topic.
   - List decisions and alternatives (e.g., using a pre-downloaded dataset versus fetching it live).

4. **Approval Checkpoint**
   - Stop and request human approval of the spec sheet before generating any task files.
