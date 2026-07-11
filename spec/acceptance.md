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

- [ ] **AC-001**: Given a new notebook, when it is created from the template, then it contains the Apache 2.0 license header as the first cell (FR-001)
- [ ] **AC-002**: Given a notebook, when reviewed, then the H1 title is not `[TODO] Add your H1 title heading here` (FR-002)
- [ ] **AC-003**: Given a notebook, when reviewed, then all required sections (Overview, Objective, Dataset, Costs, Installation, Before you begin, Cleaning up) are present (FR-004 to FR-012)
- [ ] **AC-004**: Given a notebook, when reviewed, then PROJECT_ID and REGION are parameterized and not hardcoded (FR-010, NFR-001)

## Feature: Placeholder Completion

**Requirements**: NFR-002

- [ ] **AC-005**: Given a notebook submitted for review, when scanned for placeholders, then no `{TODO:...}` patterns remain
- [ ] **AC-006**: Given a notebook submitted for review, when scanned for placeholders, then no `[TODO]` patterns remain
- [ ] **AC-007**: Given a notebook submitted for review, when scanned, then `[your-project-id]` has been replaced with a parameterized variable

## Feature: Notebook Naming and Location

**Requirements**: FR-014

- [ ] **AC-008**: Given a new notebook, when saved, then its filename follows `category-name.ipynb` convention
- [ ] **AC-009**: Given a new notebook, when saved, then it is located in the `src/` directory

---

## How to Use This File
- Each feature section links to its requirement ID
- Acceptance criteria are checkable — mark ✅ when verified
- Tests should map 1:1 to acceptance criteria
- Update this file when requirements change
