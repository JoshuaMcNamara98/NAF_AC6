# Tasks: Complete Feature Workflow Skill

**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## US1 / US2 - Orchestrate the agreed workflow safely

- [x] T001 [US1] Implement `skills/feature-workflow/SKILL.md` with matching
  `feature-workflow` frontmatter, confirmed-target preflight for managed Spec Kit
  tooling and a readable non-empty `.specify/memory/constitution.md`, and a visible
  task list that tracks preflight and the requested stages. Follow the canonical
  skills in the specified order, preserve their confirmations and feedback behavior,
  advance automatically only after successful stages, and stop/report blockers
  without starting later stages. Include the opt-in `tests` stage after `converge`
  and configured before/after commits with per-event approval, without a final
  `git-commit` stage or reminder. Cover
  FR-001 through FR-009, NFR-001 and NFR-002, and acceptance scenarios US1.1-1.5,
  US2.1-2.3, and US3.1-3.3. **Acceptance check**: inspect all relative skill links;
  walk valid and invalid preflight, success, prompt, decline, failure, pause,
  optional-tests, and completion paths; confirm stage ordering/status, no setup
  writes, and no unapproved stage execution or commit.

## US1 / US3 - Document the feature workflow

- [x] T002 [US1] Extend `README.md` with the `feature-workflow` entry, invocation
  example, and its optional `tests` stage and configured commit behavior.
  Preserve the existing manual workflow and unrelated README edits. Covers FR-001,
  FR-007, FR-008, NFR-001, and acceptance scenarios US1.1 and US3.1-3.3.
  **Acceptance check**: the skill table and usage example agree with the canonical
  skill name and documented stage order. Depends on T001.

## Verification and delivery evidence

- [x] T003 Perform the manual acceptance walkthrough mapped to FR-001 through FR-009
  and SC-001 through SC-007. Confirm optional tests run only on explicit request,
  implementation verification remains required, and no unapproved commit or push
  is performed.
  Run `git diff --check` and inspect new relative links and metadata.
  **Acceptance check**: record observed pass/fail/unrun results; do not add a test
  framework or claim unexecuted scenarios passed. Depends on T001 and T002.
- [x] T004 Record exact commands, environment, outcomes, failures, and untested
  checks in `specs/003-feature-workflow/verification.md` using the project template.
  **Acceptance check**: the report reflects T003's actual results and distinguishes
  manual checks from automated checks. Depends on T003.

## Dependencies and Checkpoints

- Execution order: T001 → T002 → T003 → T004. Each step builds on the previous
  artifact or its verification evidence; no tasks are marked parallel.
- Review the finished skill and README before the manual walkthrough. Preserve the
  existing `README.md` modification throughout.
- No production-code tests or new test infrastructure are planned; the repository
  has no existing test directory or plugin-specific runner.

## Blockers

- No blocked tasks. The live runtime acceptance checks below remain unverified.

## Convergence - Runtime acceptance still unverified

- [ ] T005 [US1] Exercise the complete required workflow in a supported Copilot/VS
  Code client using a disposable consumer repository with compatible initialized
  tooling and a non-empty constitution. Record the observed task-list transitions,
  actual stage order, successful handoffs, required approval/feedback pauses, and
  configured commit outcomes in `specs/003-feature-workflow/verification.md`.
  Commit only with explicit approval in disposable fixtures; do not push or use a
  production repository. **Acceptance check**: all ten
  required stages actually run in order, omitted `tests` is skipped, required
  controls remain visible, and no workflow stage is claimed complete without
  evidence. Covers FR-003 through FR-006, FR-008, FR-009, and SC-001, SC-002,
  SC-004, SC-006, SC-007. Depends on T001 and T002.
- [ ] T006 [US2] Exercise preflight in disposable consumer fixtures with missing or
  incompatible managed tooling and with missing, empty, or unreadable
  `.specify/memory/constitution.md`. Record each fixture's before/after state and
  result in `specs/003-feature-workflow/verification.md`. **Acceptance check**: each
  invalid fixture is blocked before `git-feature`, reports its specific prerequisite,
  and has no setup or feature-workflow writes. Covers FR-002 and SC-003. Depends on
  T001.
- [ ] T007 [US3] In a disposable consumer workflow, explicitly request the
  optional `tests` stage and verify its post-`converge` behavior, including the
  same-session warning and confirmation when applicable. Record results in
  `specs/003-feature-workflow/verification.md`. **Acceptance check**: tests run only
  after explicit request and after `converge`; implementation verification remains
  required and no tests-stage commit or push occurs. Covers FR-007, FR-008, SC-005,
  and SC-006.
  Depends on T001 and T002.

The completed implementation tasks T001-T004 have no outstanding prerequisites.
T005-T007 use separate disposable workflow scenarios, but all append evidence to the
same verification report; run them sequentially to avoid conflicting edits. They do
not otherwise depend on one another.

## Configured auto-commit amendment

- [x] T008 Update the orchestrator, shared guidance, README, specification, and plan
  to process supported target-project before/after commit events with explicit
  per-commit approval and no final `git-commit` stage/reminder. Covers FR-008 and
  SC-006. **Acceptance check**: statically verify event registration, relative
  resources, disabled/default handling, target scope, approval/failure controls,
  duplicate/no-change handling, and unchanged tests constraints.
- [ ] T009 Exercise enabled, disabled, default-enabled, malformed configuration,
  missing-script, unrelated-work, declined-approval, no-change, duplicate-hook,
  and failed-commit cases in a supported client using disposable consumer fixtures.
  **Acceptance check**: record actual commit hashes and remaining Git state; enabled
  approved events commit once, disabled events do not stage, errors block later
  stages, and completion has no final commit stage/reminder. Depends on T008.
