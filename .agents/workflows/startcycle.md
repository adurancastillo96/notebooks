---
description: Start the spec-driven notebook development cycle from a new topic idea.
slash_command: /startcycle
---

# Workflow: Start Notebook SDD Cycle

Trigger: `/startcycle <notebook-topic>` — orchestrate the spec-driven development cycle for a new notebook from raw idea to verified workshop material.

---

## Before you begin
- Read `.agents/memory/PICKUP.md` — resume from any previous session state.
- Read `.agents/memory/decisions.md` — honour all prior architectural decisions.
- Rules always active: `.agents/rules/coding.md` · `.agents/rules/notebook.md` · `.agents/rules/security.md` · `.agents/rules/git.md` · `.agents/rules/style.md`

---

## Phase 0 — Design
| | |
|---|---|
| **Persona** | `@notebook-architect` |
| **Skill** | — (structured conversation) |
| **Input** | Raw user idea from `/startcycle <topic>` |
| **Output** | `DESIGN.md` updated with notebook goals, constraints, and target users |

**Steps:**
1. Restate the notebook topic in one sentence; surface all ambiguities.
2. Ask the minimum necessary questions to resolve unknowns (target dataset, required GCP products, target audience).
3. Record assumptions and goals in the root `DESIGN.md`.

> ⛔ **CHECKPOINT 0** — Human reviews the topic and goals.
> Reply **"Approved"** or provide feedback before Phase 1 starts.

---

## Phase 1 — Specification
| | |
|---|---|
| **Persona** | `@notebook-architect` |
| **Skill** | `write-specs` (Phase 1 steps) |
| **Input** | Approved `DESIGN.md` |
| **Output** | `spec/requirements.md` (EARS) · `spec/acceptance.md` (Given/When/Then) |

**Steps:**
1. Activate `write-specs` — follow its Phase 1 steps.
2. Populate `spec/requirements.md` with notebook-specific requirements.
3. Populate `spec/acceptance.md` with Given/When/Then criteria linked to each requirement ID.

> ⛔ **CHECKPOINT 1** — Human reviews requirements and acceptance criteria.
> Reply **"Approved"** or annotate the files inline before Phase 2 starts.

---

## Phase 2 — Technical Plan
| | |
|---|---|
| **Persona** | `@notebook-architect` |
| **Skill** | `write-specs` (Phase 2 steps) · `research-dataset` |
| **Input** | Approved `spec/requirements.md` |
| **Output** | `spec/ARCHITECTURE.md` · `spec/plan.md` · `docs/ADR/` (if ADR needed) |

**Steps:**
1. Run `research-dataset` if an appropriate public dataset needs to be selected.
2. Activate `write-specs` — follow its Phase 2 steps.
3. Update repository components list, variables, and data flow in `spec/ARCHITECTURE.md`.
4. Outline the notebook code cells and markdown sections in `spec/plan.md`.
5. Record any key technical choices (e.g., specific SDK libraries, models used) in `.agents/memory/decisions.md`.

> ⛔ **CHECKPOINT 2** — Human validates the technical plan.
> Reply **"Approved"** or annotate files before Phase 3 starts.

---

## Phase 3 — Task Breakdown
| | |
|---|---|
| **Persona** | `@notebook-architect` |
| **Skill** | — |
| **Input** | Approved `spec/plan.md` |
| **Output** | `spec/tasks/TXXX.md` — task specification for the notebook author |

**Steps:**
1. Decompose the plan into authoring tasks (e.g., T001: dataset prep, T002: model training, T003: evaluation).
2. Each task file must include: Goal, Inputs, Outputs, and Definition of Done.
3. Order tasks logically and number sequentially.

> ⛔ **CHECKPOINT 3** — Human reviews the task breakdown.
> Reply **"Approved"** before Phase 4 starts.

---

## Phase 4 — Authoring (Implementation)
| | |
|---|---|
| **Persona** | `@notebook-author` |
| **Skill** | `create-notebook` |
| **Input** | `spec/tasks/TXXX.md` |
| **Output** | Completed notebook at `src/category-name.md` (compiled to `artifacts/category-name.ipynb`) |

**Steps:**
1. Activate `create-notebook` for the authoring task.
2. Follow `notebook_template.md` structural sections exactly.
3. Implement fully functional Python code blocks with preceding descriptive markdown sections.
4. Verify that the cleaning up block is complete.
5. Compile the notebook to `artifacts/category-name.ipynb` using the conversion script.
6. Mark the task file complete once the notebook is successfully authored and compiled.

> ⛔ **CHECKPOINT 4** — Human reviews the notebook structure and cells.
> Reply **"Approved"** before Phase 5 starts.

---

## Phase 5 — Review (Verification)
| | |
|---|---|
| **Persona** | `@notebook-reviewer` |
| **Skills** | `review-notebook` · `notebook-lint` · `fix-notebook` |
| **Input** | Implemented notebook in `src/` |
| **Output** | `reports/lint_report.md` |

**Steps (in order):**
1. `notebook-lint` — run automated linter to check naming, required sections, and credentials.
2. `review-notebook` — review cell details, structure, pedagogical flow, and cleanup actions.
   - If issues found: run `fix-notebook` (auto-fix common lint errors) after human confirmation.
3. Confirm all checks pass and all TODO placeholders are replaced.

> ⛔ **CHECKPOINT 5** — Human approves review results and merges the notebook branch.

---

## After the cycle
- Update `.agents/memory/PICKUP.md` with session status.
- Update `.agents/memory/learnings.md` with lessons learned.
