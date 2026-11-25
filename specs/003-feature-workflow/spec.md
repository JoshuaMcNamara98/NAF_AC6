# Feature Specification: Complete Feature Workflow Skill

**Created**: 2026-11-25
**Status**: Draft
**Input**: Add one skill that guides a user through the full feature-development workflow in a fixed order, optionally including the tests skill.
**Branch**: `003-feature-workflow` (feature documents are independent of this directory)

## User Scenarios & Testing

### US1 - Run the complete feature workflow in order (Priority: P1)

As a developer, I want one skill to guide a feature from branch creation through
implementation and convergence so I can complete the established workflow without
manually coordinating each skill.

**Independent Test**: Start the workflow with initialized project tooling and a
constitution. Verify the skill presents and advances through each required stage in
order, applies the corresponding skill's behavior and user controls, and stops when a
stage cannot proceed.

**Acceptance Scenarios**:

1. **Given** a feature request and valid setup, **When** the user starts the workflow,
   **Then** it runs `git-feature`, `git-remote`, `specify`, `git-validate`, `clarify`,
   `plan`, `tasks`, `analyze`, `implement`, and `converge` in that order.
2. **Given** the workflow is active, **When** a stage starts or finishes, **Then** the
   user can see a task list showing every stage's status and which skill is currently
   running.
3. **Given** a stage requires user input or approval, **When** the workflow reaches
   that decision, **Then** it preserves that skill's normal confirmation and feedback
   behavior rather than inferring approval or silently skipping the stage.
4. **Given** a stage completes successfully without a pending decision, **When** it
   finishes, **Then** the workflow automatically advances to the next stage without
   asking for extra approval at every handoff.
5. **Given** a stage fails, is declined, or lacks a required input, **When** it cannot
   complete, **Then** the workflow reports the blocker, marks the stage accordingly,
   and does not start later stages.

### US2 - Verify project setup before starting (Priority: P1)

As a developer, I want the workflow to verify its prerequisites before changing
branches or writing feature documents so it does not operate on a project that has not
been prepared for Spec Kit.

**Independent Test**: Run preflight against projects with compatible setup, missing
setup, and incompatible or incomplete setup; confirm that only a valid project proceeds.

**Acceptance Scenarios**:

1. **Given** the target project has compatible managed Spec Kit tooling and a
   readable, populated `.specify/memory/constitution.md`, **When** preflight runs,
   **Then** it proceeds to the first workflow stage.
2. **Given** tooling is missing or incompatible, or the constitution is absent,
   unreadable, or empty, **When** preflight runs, **Then** it explains the missing
   or invalid prerequisite and stops without running setup or later stages.
3. **Given** the current plugin checkout is not the target project, **When** preflight
   runs, **Then** it checks the confirmed target repository rather than assuming the
   plugin checkout is the consumer project.

### US3 - Include the separate tests stage only when requested (Priority: P2)

As a developer, I want the standalone `tests` stage to be optional so the workflow
does not run it unless I ask, while still retaining the implementation stage's own
verification responsibilities.

**Independent Test**: Complete the workflow once without requesting `tests` and once
with an explicit request; verify stage status, ordering, and the final reminder.

**Acceptance Scenarios**:

1. **Given** the user did not request the separate tests skill, **When** convergence
   finishes, **Then** the tests stage is marked skipped and is not run.
2. **Given** the user explicitly requested the separate tests skill, **When** the
   workflow reaches the optional stage after convergence, **Then** it runs `tests`
   using that skill's normal constraints and records the result.
3. **Given** all requested stages finish, **When** the workflow reports completion,
   **Then** it reminds the user to run `git-commit` to finalize the changes and does
   not commit on the user's behalf.

### Edge Cases

- The target repository cannot be confirmed, is not a Git repository, or is on a
  branch that requires a new feature branch.
- The target project is missing the Git extension needed by a Git skill, or an
  operation would fetch, prune, switch branches, stage, or commit without the required
  approval.
- A skill's required feature selection, specification, plan, tasks, or verification
  input is missing, stale, or points to a different feature.
- A user declines a stage's confirmation, gives feedback that changes the agreed
  scope, or asks to pause before a later stage.
- The optional tests stage is not requested; this must not suppress tests or checks
  required by `implement`.

### Functional Requirements

- **FR-001**: The plugin provides one discoverable skill for orchestrating a feature
  workflow; it does not replace or create duplicate versions of the existing stage
  skills.
- **FR-002**: Before starting, the skill confirms the target project and verifies
  compatible managed Spec Kit tooling and that `.specify/memory/constitution.md`
  exists, is readable, and is non-empty. This checks for the expected artifact; it
  does not infer that the `constitution` skill was invoked or require project-specific
  customization. If either prerequisite is missing, empty, unreadable, or
  incompatible, it reports the issue and stops; it does not run `init` or
  `constitution` automatically.
- **FR-003**: After a successful preflight, the skill runs the required stages in this
  exact order: `git-feature`, `git-remote`, `specify`, `git-validate`, `clarify`,
  `plan`, `tasks`, `analyze`, `implement`, and `converge`.
- **FR-004**: The skill follows the corresponding canonical skill instructions at
  each stage, including target-repository scope, confirmations, user feedback,
  safety controls, failure reporting, and any stage-specific stop conditions. It does
  not treat listing or mentioning a skill as having run it.
- **FR-005**: The skill presents and maintains a user-visible task list for the
  workflow, indicating pending, current, completed, skipped, or blocked status for
  each stage and clearly identifying the stage currently being run.
- **FR-006**: After a stage succeeds with no pending decision, the skill advances to
  the next stage without asking for additional approval at every handoff. If a stage
  fails, is declined, or lacks required input, the skill reports the reason, preserves
  the current feature state, and waits for user direction before resuming or stopping;
  it does not start later stages until the blocker is resolved.
- **FR-007**: The separate `tests` stage runs after `converge` only when the user
  explicitly requests it. Omitting that stage does not bypass verification required
  by `implement`.
- **FR-008**: On successful completion of all requested stages, the skill reminds
  the user to run `git-commit` to finalize the feature. It does not invoke `git-commit`
  or stage, commit, push, or deploy changes automatically.
- **FR-009**: The skill reports the outcome and any remaining blockers or skipped
  stages, and does not claim that a stage or verification passed unless it actually
  completed.

### Nonfunctional Requirements

- **NFR-001**: The skill works with the invocation forms supported by the client
  (plugin-qualified skill names or plain skill names) without assuming a specific
  consumer-project language, framework, or source layout.
- **NFR-002**: Stage status and user-facing instructions remain clear if the user
  pauses, provides feedback, or blocks a stage; no performance threshold is needed
  for this interactive workflow.

## Success Criteria

- **SC-001**: In a successful workflow run, all ten required skills are executed in
  the specified order, verified from the visible stage list and stage outcomes.
- **SC-002**: At every transition, the visible task list identifies exactly one
  current stage or indicates that the workflow is paused, complete, or blocked.
- **SC-003**: In setup-failure checks, no listed workflow stage starts and no setup
  files are changed.
- **SC-004**: In failure, missing-input, and declined-confirmation checks, no later
  stage starts before the blocker is resolved.
- **SC-005**: The separate `tests` stage runs only after an explicit user request;
  implementation verification still occurs whether or not that stage is requested.
- **SC-006**: Every successful run ends with a `git-commit` reminder and makes no
  commit or push through the orchestrator.
- **SC-007**: A successful stage with no pending decision automatically advances to
  the next stage; a stage-specific approval or blocker still pauses progression.

## Scope and Dependencies

**Included**: One orchestration skill for the defined feature-development stages,
setup preflight, visible task status, optional separate tests, and a final
`git-commit` reminder.
**Excluded**: Automatically running `init` or `constitution`; changing the behavior
of existing skills; bypassing their user controls; automatically committing, pushing,
deploying, or publishing; automatically running the separate tests stage when it was
not requested.
**Dependencies**: The target project has compatible managed Spec Kit tooling and a
populated constitution. The existing `git-feature`, `git-remote`, `specify`,
`git-validate`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `converge`,
`tests`, and `git-commit` skills are available to the plugin client. Git and
project-local feature artifacts are required only where the corresponding stage
requires them.

## Clarifications

- 2026-11-25: If preflight finds missing or incompatible Spec Kit tooling or a missing
  constitution artifact, stop with guidance instead of running `init` or
  `constitution`.
- 2026-11-25: The constitution preflight checks the expected project artifact at
  `.specify/memory/constitution.md`. Repository skill documentation shows that
  `init` seeds this file and `constitution` edits it in place; artifact presence does
  not prove which skill was invoked or whether project-specific tailoring occurred.
- 2026-11-25: After a stage succeeds, continue to the next stage automatically unless
  the stage's own instructions require a user decision, or a failure or changed
  requirement requires a pause.

## Assumptions

- The new skill is named `feature-workflow`; this is a proposed concise name, not a
  user-confirmed requirement.
- A constitution is considered ready for preflight when the canonical project-local
  file exists, is readable, and is non-empty; no proof of skill invocation or
  project-specific tailoring is required.
- `tests` means the separate standalone `tests` skill. It remains optional even though
  `implement` runs the verification required by its own instructions.
- The user-visible task list is maintained in the skill's conversational output; no
  separate project task-tracking files are required by this feature.
