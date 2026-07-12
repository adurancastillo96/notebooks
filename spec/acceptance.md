# Acceptance Criteria

Acceptance criteria per notebook feature, linked to requirements.

## Format
Each criterion follows Given/When/Then:
```
Given [context]
When [action]
Then [expected result]
```

## Feature: Notebook Structure Compliance

**Requirements**: FR-001 through FR-012

- [x] **AC-001**: Given a new notebook, when it is created from the template, then it contains the Apache 2.0 license header as the first cell (FR-001)
- [x] **AC-002**: Given a notebook, when reviewed, then the H1 title is not `[TODO] Add your H1 title heading here` (FR-002)
- [x] **AC-003**: Given a notebook, when reviewed, then all required sections (Overview, Objective, Dataset, Costs, Installation, Before you begin, Cleaning up) are present (FR-004 to FR-012)
- [x] **AC-004**: Given a notebook, when reviewed, then GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are parameterized and not hardcoded (FR-010, NFR-001)

## Feature: Placeholder Completion

**Requirements**: NFR-002

- [x] **AC-005**: Given a notebook submitted for review, when scanned for placeholders, then no `{TODO:...}` patterns remain
- [x] **AC-006**: Given a notebook submitted for review, when scanned for placeholders, then no `[TODO]` patterns remain
- [x] **AC-007**: Given a notebook submitted for review, when scanned, then `[your-google-cloud-project]` has been replaced with a parameterized variable

## Feature: Notebook Naming and Location

**Requirements**: FR-014

- [x] **AC-008**: Given a new notebook, when saved, then its filename follows `category-name.md` convention and compiles to `artifacts/category-name.ipynb`
- [x] **AC-009**: Given a new notebook, when saved, then it is located in the `src/` directory

---

## Feature: Autonomous Trajectory Agentic Loop

**Requirements**: FR-015, FR-016, FR-019, NFR-007

- [x] **AC-010**: Given the Vertex AI API and Google ADK initialization, when the agents are invoked with airport coordinates and runway bearing, then the agents negotiate and verify a multi-step trajectory route.
- [x] **AC-011**: Given the multi-agent system, when the `TrajectoryPlannerAgent` proposes a path that intersects with an obstacle, then the `ObstacleVerifierAgent` rejects it and triggers a path recalculation.

## Feature: OEI Flight Physics and Airport Modelling

**Requirements**: FR-017, FR-018, NFR-008

- [x] **AC-012**: Given a twin-engine aircraft specification, when the physics module is queried, then it computes the One-Engine-Inoperative (OEI) climb gradient based on aircraft weight, drag, and thrust loss.
- [x] **AC-013**: Given the Innsbruck LOWI or Aspen KASE mock profile, when queried, then it provides a set of 3D obstacles (coordinates and height) representing mountainous terrain.

## Feature: Trajectory Visualization

**Requirements**: FR-020

- [x] **AC-014**: Given the finalized trajectory, when the visualization cell runs, then it outputs a 2D elevation profile and a 3D scatter/line chart depicting the flight path and obstacle margins.

---

## How to Use This File
- Each feature section links to its requirement ID
- Acceptance criteria are checkable — mark ✅ when verified
- Tests should map 1:1 to acceptance criteria
- Update this file when requirements change
