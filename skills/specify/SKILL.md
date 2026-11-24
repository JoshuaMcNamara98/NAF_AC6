---
name: specify
description: Turn a software feature request into a project-aware specification with scope, user scenarios, and testable acceptance criteria.
---

# Specify a feature

Read and follow [the shared workflow](../../docs/workflow.md).

1. Confirm the target repository and inspect its current Git branch. At the start of
   every Git-backed invocation, ask whether this feature belongs on the current branch
   or needs a new feature branch—even when the current branch is already a feature
   branch. Do not infer the answer from its name. Do this before project initialization,
   feature-specific investigation, or clarification.
   - Require a new feature branch on `main`, `master`, `develop`, `development`,
     `staging`, `production`, or a branch matching `release/*`, even if the user
     initially chooses to stay on it.
   - If another branch name is ambiguous, ask whether it is shared. If it is, require a
     new feature branch. If it is not shared and the user chooses it, continue there
     and record its actual name.
   - If a new branch is requested or required by the shared-branch rule, continue
     through steps 2 and 3: initialize/verify managed tooling if needed, then
     automatically invoke and follow the `git-feature` skill in this same invocation
     before feature-specific investigation. Keep all of its confirmations: confirm
     repository, current branch, worktree, intended base, and branch name; disclose and
     get approval for fetch/prune of remote-tracking refs. The creation script starts
     from current `HEAD`, so verify it is the approved base. Verify the resulting
     branch before continuing. A decline, missing confirmation, or failure stops
     specification work before any feature documents are written.
   - If Git or a repository is unavailable, explain the limitation and ask whether to
     proceed without branch creation. Continue only if the user confirms; otherwise
     stop. Never initialize Git or switch branches silently.
2. Initialize project tooling if needed. Check `.specify/speckit-plugin.json`; if
   tooling is missing, run the `init` skill after the branch choice. If `.specify/` is
   unmanaged or incompatible, stop and explain the migration needed.
3. If a new branch is requested or required, automatically invoke and follow
   `git-feature` in this same invocation. If the target extension is missing, follow
   its ask-before-copy rule; do not overwrite existing files. Keep all branch, base,
   worktree, name, and fetch/prune confirmations from step 1. Verify the resulting
   branch before continuing. If the step fails or is declined, stop before
   feature-specific work or document writes.
4. Read relevant project documentation and governance. Gather the feature goal, users,
   behavior, exclusions, dependencies, compatibility, and acceptance criteria from the
   request and repository evidence.
5. Ask about material gaps. Record confirmed answers separately from assumptions.
   Never invent sensitive-data policies or performance targets.
6. Choose a concise lowercase hyphenated short name. Unless the user is explicitly
   revising an existing feature, create exactly one new feature:
   ```sh
   python .specify/scripts/speckit.py --project . create --name user-auth --description "Add user authentication"
   ```
   Substitute the actual name and description. This creates and selects a numbered
   feature directory; it does not create or switch a branch. To revise an existing
   feature, use `select` and read its existing spec instead of creating another.
7. Fill the returned `FEATURE_SPEC` from its template. Include prioritized user
   journeys, Given/When/Then scenarios, edge cases, numbered requirements, measurable
   success criteria, scope, dependencies, clarifications, and explicit assumptions.
   Use the project's terminology; avoid prescribing implementation details unless
   the user or existing project requires them. Omit irrelevant optional sections.
8. Create `checklists/requirements.md` inside the selected feature. Check clarity,
   testability, completeness, scope, and absence of unresolved material questions.
   Resolve gaps with the user; record remaining blockers rather than marking them passed.
9. Report the selected directory, spec, checklist findings, and readiness for
   clarification or planning. Stop for review unless the user requested end-to-end work.
