---
name: specify
description: Turn a software feature request into a project-aware specification with scope, user scenarios, and testable acceptance criteria.
---

# Specify a feature

Read and follow [the shared workflow](../../docs/workflow.md).

1. Initialize project tooling if needed. Read relevant project documentation and
   governance. Gather the feature goal, users, behavior, exclusions, dependencies,
   compatibility, and acceptance criteria from the request and repository evidence.
2. Ask about material gaps. Record confirmed answers separately from assumptions.
   Never invent sensitive-data policies or performance targets.
3. Choose a concise lowercase hyphenated short name. Unless the user is explicitly
   revising an existing feature, create exactly one new feature:
   ```sh
   python .specify/scripts/speckit.py --project . create --name user-auth --description "Add user authentication"
   ```
   Substitute the actual name and description. This creates and selects a numbered
   feature directory; it does not create or switch a branch. To revise an existing
   feature, use `select` and read its existing spec instead of creating another.
4. Fill the returned `FEATURE_SPEC` from its template. Include prioritized user
   journeys, Given/When/Then scenarios, edge cases, numbered requirements, measurable
   success criteria, scope, dependencies, clarifications, and explicit assumptions.
   Use the project's terminology; avoid prescribing implementation details unless
   the user or existing project requires them. Omit irrelevant optional sections.
5. Create `checklists/requirements.md` inside the selected feature. Check clarity,
   testability, completeness, scope, and absence of unresolved material questions.
   Resolve gaps with the user; record remaining blockers rather than marking them passed.
6. Report the selected directory, spec, checklist findings, and readiness for
   clarification or planning. Stop for review unless the user requested end-to-end work.
