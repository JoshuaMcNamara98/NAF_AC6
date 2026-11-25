# Feature Specification: Tests Skill for Unit-Test Generation

**Created**: 2026-11-24
**Status**: Draft
**Input**: Add a `tests` skill that generates thorough, requirement-driven unit tests, inspects existing test layout and conventions, and is intended to run in a separate agent session from implementation.
**Branch**: `vscode_plugin` (feature documents are independent of this directory)

## User Scenarios & Testing

### US1 - Generate independent unit tests for an implemented feature (Priority: P1)

As a maintainer, I want a separate agent session to author tests after implementation so test design is independent from the code-writing session.

**Independent Test**: Invoke the skill for an implemented feature and confirm it creates requirement-driven unit tests without changing production files.

**Acceptance Scenarios**:

1. **Given** an implemented feature and available feature documents, **When** the `tests` skill runs in a separate agent session, **Then** it reviews the feature expectations and relevant implementation and creates unit tests for specified behavior, including relevant boundary, invalid-input, and failure cases.
2. **Given** the current conversation shows that this same agent session implemented the feature, **When** the skill is invoked, **Then** it warns the user about the independence concern and asks before proceeding with test authoring.
3. **Given** tests have been created, **When** the skill finishes, **Then** it reports the changed test files, the requirements and identified edge cases they cover, and the verification result.

### US2 - Follow the target project's test conventions (Priority: P1)

As a maintainer, I want generated tests to fit the project's existing test layout and tools so they can be understood and run with the rest of the suite.

**Independent Test**: Run the skill against a project with an existing test directory and test configuration, then verify the added tests use its established framework, naming, helpers, fixtures, and location.

**Acceptance Scenarios**:

1. **Given** one or more test directories and existing test files, **When** the skill prepares tests, **Then** it examines relevant examples and follows their conventions rather than introducing a parallel framework or layout.
2. **Given** no test directory exists, **When** the skill prepares tests, **Then** it inspects project configuration and documentation, infers a suitable location only when supported by that evidence, and reports the choice.
3. **Given** no reliable test location or runner can be inferred, **When** the skill reaches that decision, **Then** it reports the uncertainty and asks the user rather than adding test infrastructure or dependencies.

### US3 - Add tests for features that predate the workflow (Priority: P1)

As a maintainer, I want to add tests for already-implemented features even when the feature workflow documents are incomplete or absent.

**Independent Test**: Invoke the skill for an existing implementation with some earlier-stage artifacts missing and verify it uses available evidence while explicitly reporting those gaps.

**Acceptance Scenarios**:

1. **Given** some of the spec, plan, task, analysis, or implementation-stage artifacts are missing, **When** the skill runs, **Then** it proceeds from available specifications and relevant project evidence, and reports which inputs were unavailable.
2. **Given** no reliable behavioral expectation can be established from available specifications or other project documentation, **When** a test would require inventing expected behavior, **Then** the skill pauses for clarification instead of encoding an assumption as a test.
3. **Given** relevant implementation paths suggest a defect, missing exception handling, or potentially dead code, **When** the skill reviews the feature, **Then** it reports the observation with evidence and does not change production code.

### US4 - Verify and report generated tests (Priority: P1)

As a maintainer, I want the skill to run the narrowest relevant unit-test command and report outcomes honestly.

**Independent Test**: Invoke the skill where the project test command succeeds and where it fails; verify it reports the actual command and outcome in each case.

**Acceptance Scenarios**:

1. **Given** a known test runner and focused test command, **When** test files are added, **Then** the skill runs the smallest relevant command and reports its exact result.
2. **Given** a focused test run fails because a newly authored test is objectively defective, **When** the skill can correct it without changing expected behavior, **Then** it repairs only its own test changes and reruns the focused command.
3. **Given** a test failure indicates the implementation does not meet specified behavior, **When** the skill finishes, **Then** it leaves production code and assertions unchanged and reports the failure as a possible implementation/spec mismatch.
4. **Given** the tests cannot be run because of missing tools, dependencies, or another blocker, **When** the skill finishes, **Then** it reports the reason and does not claim the tests passed.

### Edge Cases

- The user supplies a specs directory that does not contain the intended feature's requirements.
- A repository has multiple test directories or multiple test frameworks; the skill narrows inspection to the relevant code and feature.
- Existing tests already cover a requirement; the skill avoids duplicating equivalent coverage.
- The implementation conflicts with the written requirements; the skill reports the conflict instead of weakening expected behavior to match the code.
- A relevant implementation branch has no clearly specified expected outcome; the skill identifies the gap instead of guessing an assertion.
- The project has no test runner or required dependency installed; the skill does not install dependencies or alter setup.

## Requirements

### Functional Requirements

- **FR-001**: The plugin provides a user-invoked skill named `tests` for creating unit tests for an implemented feature. A user-supplied specs directory takes precedence; when none is supplied, the skill uses the explicitly selected feature's documents.
- **FR-002**: The skill explicitly recommends a separate agent session from the implementation session. If the available conversation context shows this same session implemented the feature, it must warn the user and obtain confirmation before authoring tests; it must not claim to verify separation when it cannot.
- **FR-003**: The skill uses available feature specifications as the source of expected behavior, inspects relevant implementation to identify testable boundaries, and reports missing spec, plan, task, analysis, or implementation inputs without requiring every earlier artifact to exist.
- **FR-004**: The skill must not invent expected behavior when the available requirements and project documentation do not establish it; it must ask the user or report the specific blocker.
- **FR-005**: Before creating tests, the skill checks for existing `test`, `tests`, `__tests__`, or project-specific test locations; examines relevant tests and project test configuration; and follows the established framework, naming, fixtures, helpers, and organization.
- **FR-006**: If no existing test directory is present, the skill infers a suitable location only from project configuration or documentation and reports the evidence and choice. If no reliable location or runner is inferable, it asks the user rather than establishing new conventions.
- **FR-007**: The skill derives a thorough but relevant set of unit-test cases from requirements and implementation boundaries, including applicable normal, boundary, invalid-input, failure/exception, and state-interaction cases. It prioritizes behavioral correctness over line/statement coverage, avoids duplicating existing tests, and reports every identified requirement and edge case as tested or explains why it could not be tested.
- **FR-008**: The skill may add or edit test source files only. It must not change production code, test configuration, dependencies, or other project files; it must not install dependencies.
- **FR-009**: After authoring tests, the skill runs the narrowest relevant existing unit-test command when available and reports the command, outcome, and any failures or blockers. It never presents an unrun or failed test as passing.
- **FR-010**: If a run fails because of an objectively defective test authored during this invocation, the skill may correct only that test and rerun it. It must not change expected behavior or weaken assertions to make a failing implementation pass.
- **FR-011**: The skill reports evidence-backed potential implementation defects, missing exception handling, and dead code discovered during relevant inspection; it does not modify production code or claim unverified suspicions as confirmed defects.
- **FR-012**: The skill does not commit, stage, push, or otherwise publish changes.

### Nonfunctional Requirements

- The skill is project- and language-agnostic: the target project's documented tooling and conventions determine test syntax and commands.
- The skill is manually invoked; its instructions must not imply that separate-session use is technically enforced.

## Success Criteria

- **SC-001**: In a project with existing tests, all added test files follow the relevant existing test layout and framework, with no new test framework or test directory introduced.
- **SC-002**: Every identified requirement and relevant edge case is either traceable in the completion report to a test or accompanied by a reason it could not be tested; reports distinguish behavior coverage from line/statement coverage.
- **SC-003**: Running the skill produces changes limited to test source files; a worktree diff confirms no production, configuration, or dependency files were changed.
- **SC-004**: The completion report states the exact focused test command and observed result, or explicitly states why tests were not run; after correcting a test defect, it records the rerun.
- **SC-005**: When feature-stage artifacts are missing, the skill reports each missing input and continues only where expected behavior remains adequately supported.
- **SC-006**: Any reported potential implementation bug, missing exception handling, or dead code finding includes evidence and is not silently fixed by the tests skill.

## Scope and Dependencies

**Included**: A new `skills/tests/SKILL.md` for a separate test-authoring session; reading available feature documents and relevant source; inspecting test locations, conventions, and runner configuration; systematically identifying relevant behavioral edge cases; writing unit-test source files; and focused test verification and reporting.
**Excluded**: Implementing or changing production behavior; changing test configuration, dependency manifests, or CI; installing dependencies; writing integration, end-to-end, or performance tests unless they are already classified as unit tests by the target project's conventions; enforcing agent-session separation through runtime mechanisms; committing or publishing changes.
**Dependencies**: The target project's available specifications and implementation, its existing test conventions or documented test tooling, and a compatible test runner when verification is possible.

## Clarifications

- 2026-11-24: If no test directory exists, infer a location from project tooling and report the choice; ask if no reliable location can be inferred.
- 2026-11-24: Proceed from available specs and report missing inputs. The skill must support features implemented before the Spec Kit skills were installed.
- 2026-11-24: Add unit-test source files only, then run relevant tests.
- 2026-11-24: If a focused run exposes an objectively faulty newly authored test, repair that test and rerun. Do not change production code or weaken assertions to hide implementation/spec failures; report potential production bugs, missing exception handling, and dead code with evidence.
- 2026-11-24: Use an explicitly supplied specs directory when present; otherwise use the selected feature's documents.
- 2026-11-24: Test requirements and relevant edge cases, not merely whether lines execute. Report edge cases that cannot be tested because expected behavior is unspecified.

## Assumptions

- When no specs path is explicitly supplied, the selected feature directory is current and verified; the skill must not silently use a stale selection.
- Relevant source may be inspected to identify test imports and boundaries, but expected assertions come from requirements and documented behavior, not merely from the implementation's current behavior.
- A separate agent session reduces same-agent implementation/test-authoring bias but cannot guarantee independence; the skill should disclose this limitation.
- "Relevant edge cases" means cases supported by the feature's requirements, documented behavior, and meaningful implementation boundaries; it does not imply unbounded combinatorial testing or inventing expected behavior.
