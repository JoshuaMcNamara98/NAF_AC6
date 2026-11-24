---
name: tests
description: Create and run requirement-driven unit tests for an implemented feature using available specifications and existing project test conventions, preferably in a separate agent session.
disable-model-invocation: true
---

# Test an implemented feature

Read and follow [the shared workflow](../../docs/workflow.md), including its tests-only
exception. This skill supplements implementation-stage tests; it does not implement
or fix production code.

1. Confirm the target repository and intended feature. Recommend running this skill in
   a fresh agent session, separate from the session that implemented the feature. If the
   visible conversation shows this session authored the implementation, warn about the
   independence concern and ask for confirmation before authoring tests. Do not claim
   separation was verified or enforced, inspect session histories, or launch another
   agent to enforce it.
2. Resolve the feature inputs without writing workflow files:
   - An explicitly supplied specs directory takes precedence over feature selection.
     Verify it exists and describes the intended feature; ask which feature to use if
     it contains several. Report an invalid path instead of silently falling back.
   - Without an explicit path, if compatible project tooling and a selection exist,
     use the verified Python 3.10+ executable to run:
     ```sh
     python .specify/scripts/speckit.py --project . paths
     ```
     Verify that the returned feature matches the request. If tooling, selection, or
     required inputs are unavailable, incompatible, or stale, report the reason and
     ask for the intended feature or available documents. Do not initialize, select,
     create, or seed artifacts. Never invent paths after a command failure.
3. Read available specifications, plan, tasks, checklists, verification or analysis
   evidence, project governance and documentation, and relevant implementation.
   Report missing inputs without requiring all earlier stages to have run: support
   features implemented before this plugin was installed. No saved analysis report
   does not prove analysis never occurred. Expected behavior comes from requirements,
   documented project behavior, or explicit user clarification, not merely from what
   the implementation currently does. Ask about conflicting or unspecified outcomes;
   report absent implementation as a blocker rather than writing production code.
4. Inspect the initial worktree and relevant existing tests before editing. Check
   `test/`, `tests/`, `__tests__/`, colocated tests, and project-specific locations.
   Examine the relevant framework, runner configuration, naming, fixtures, helpers,
   isolation patterns, and documented commands. In multi-framework projects, choose
   the layout and runner associated with the feature, not an unrelated suite.
   If no test directory exists, infer a location only from project configuration or
   documentation and report the evidence and choice. Ask if no reliable location or
   runner can be inferred; do not add infrastructure or install dependencies.
5. Build a requirement and edge-case inventory before writing assertions. Include
   applicable normal, empty, boundary, invalid-input, failure/exception, and
   state-interaction cases, using meaningful implementation boundaries to identify
   gaps. Match cases to existing tests to avoid duplicate coverage. Prioritize
   observable behavior over executing lines or attaining a coverage percentage;
   do not promise exhaustive combinations. For cases without an established expected
   outcome or a unit-testable boundary, ask for clarification or report the specific
   gap rather than guessing assertions or changing production code for testability.
6. Add or extend focused unit-test source files using the project's existing patterns
   and helpers. Preserve unrelated changes and existing assertions. Do not modify
   production code, test configuration, dependencies, CI, or feature documents.
   Do not substitute integration, end-to-end, or performance tests for unit tests;
   follow the target project's established classification.
7. Run the narrowest relevant existing unit-test command using the project's supported
   runtime. Inspect commands and setup for unwanted writes or external effects before
   execution; do not run install, publication, or production-changing setup steps.
   Report missing tools, dependencies, or other execution blockers without installing
   or changing configuration. Do not claim unrun tests passed.
8. Investigate failures against the requirements and existing test conventions.
   Correct demonstrable defects in tests authored during this invocation, such as
   incorrect fixture setup, and rerun the focused command without changing expected
   behavior. Do not weaken assertions, skip failing cases, or alter production code
   to make an implementation/spec mismatch pass. Preserve and report genuine
   behavioral failures; distinguish pre-existing failures and uncertain causes.
9. Report evidence-backed potential production bugs, missing exception handling, and
   dead code discovered during relevant inspection. Include precise source references
   and supporting requirements, failing tests, or call-site evidence; distinguish
   suspicion from confirmed findings. An unexecuted line alone is not proof of dead
   code, and an unspecified exception is not automatically a bug. Do not fix findings.
10. Compare the final worktree to its initial state, including new files, to confirm
    this invocation changed only test source. Report in chat:
    - The target feature, inputs used, and missing inputs.
    - Added or updated test files and the requirement/edge-case inventory, mapped to
      existing or new tests; give a reason for each identified case not tested.
    - Exact commands, environment, observed results, repairs and reruns, failures,
      and checks not run.
    - Evidence-backed findings, uncertainty, remaining gaps, and decisions needed.
    Do not write verification reports, edit task status, stage, commit, push, deploy,
    or publish issues. If user feedback changes expected behavior or scope, pause
    and request revision through the appropriate feature stage rather than editing
    requirements or silently changing assertions.
