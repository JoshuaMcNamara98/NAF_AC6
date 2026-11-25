# Verification: Complete Feature Workflow Skill

**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Environment**: Linux repository checkout; Python 3.11.13. Static checks and
document-based scenario review only; no live VS Code/Copilot session was exercised.

## Results

The results below describe the original implementation, before the configured
auto-commit amendment. Its final-reminder checks are superseded by the amendment
results at the end of this report.

| Requirement / task | Command or procedure | Actual result | Status |
| --- | --- | --- | --- |
| FR-001, NFR-001 / T001 | Python 3.11 inline static assertions via `python3.11 - <<'PY'`; checked skill frontmatter/directory name, all local resource links, required stage order, and README entry | Printed `PASS: frontmatter, relative links, stage order, optional tests/commit behavior, README, tooling fixture, traceability, and whitespace`. | Passed (static) |
| FR-002 / SC-003 | The same assertions checked the current checkout's managed marker, CLI version constants, installed CLI byte equality, and non-empty constitution. Reviewed missing/incompatible setup paths in the skill instructions. | Current checkout satisfies the valid preflight fixture. Missing/incompatible consumer projects were not created or exercised; instructions explicitly block and stop without setup writes. | Passed by inspection; invalid-project runtime not run |
| FR-003, FR-004, FR-005, FR-006, FR-009 / SC-001, SC-002, SC-004, SC-007 / T001 | Manually traced the ordered skill links and task-status, approval, feedback, failure, pause, and resume rules against the specification and canonical skill files. | Required order matches. Successful handoffs continue; skill-specific prompts remain; blockers pause later stages. This was a document review, not live skill dispatch. | Passed by review |
| FR-007, FR-008 / SC-005, SC-006 / T001-T002 | Manually reviewed optional-tests and completion behavior and checked the README invocation/table entries. | Tests remain opt-in after `converge`; same-session confirmation is retained; implementation verification remains required; completion reminds the user to run `git-commit` without invoking it. | Passed by review |
| FR-001, FR-007, FR-008, NFR-001 / T002 | Inspected README workflow example, skills table, and local links. | `feature-workflow` is discoverable and the example describes optional tests and the separate commit reminder. Existing manual workflow and the prior `/speckit:converge` addition remain. | Passed |
| Feature selection / T003 | `/usr/bin/python3.11 .specify/scripts/speckit.py --project . paths --require spec plan tasks` | Resolved the selected `specs/003-feature-workflow` spec, plan, and tasks. | Passed |
| Markdown whitespace / T003 | `git diff --check`; Python inline static assertions checked trailing whitespace in the changed Markdown files. | `git diff --check` exited 0; no trailing whitespace found. | Passed |
| Runtime | `/usr/bin/python3.11 --version` | `Python 3.11.13`. | Passed |
| Live orchestration | Not run | The repository has no executable workflow dispatcher or automated plugin test harness. No claim is made that live skill invocation or VS Code behavior was tested. | Not run |
| Unit tests, build, and type checks | Not run | No test directory, test runner, build, or type-check configuration applies to this Markdown-only change. | Not applicable |

## Remaining Work

- **T005**: Validate the complete workflow in a supported Copilot/VS Code client,
  including actual stage order, task-list transitions, confirmation and pause/resume
  behavior.
- **T006**: Exercise missing/incompatible tooling and missing, empty, or unreadable
  constitution cases in disposable consumer fixtures.
- **T007**: Validate the explicitly requested optional tests stage after convergence
  and its same-session confirmation behavior.
- No automated unit tests, build, or type checks were run or added.

## Feedback and Review

- The analyze-stage traceability finding was addressed: README task T002 now includes
  US1, FR-001, and NFR-001 coverage.
- Live human review and plugin installation were not performed.

## Configured auto-commit amendment - 2026-11-25

- Updated the orchestrator and related documentation to process supported
  target-project commit events with per-commit review and approval. Removed the
  final `git-commit` stage/reminder; completion reports remaining changes instead.
- `git diff --check` passed.
- `python3 - <<'PY'` inline static assertions passed for skill frontmatter,
  relative links in all six amended Markdown files, unchanged ten-stage order,
  the eleven supported events mapped to `speckit.git.commit` in the bundled
  extension manifest, configuration/default handling, approval and unrelated-work
  controls, required trailers, duplicate/no-change handling, failure blocking,
  target-project execution, tests-only constraints, and completion reporting.
  Output: `PASS: metadata, relative links, unchanged stage order, 11 registered
  commit events, configuration/approval/failure controls, and completion rules`.
- No runtime scripts, configuration, or plugin version were changed. No files
  were staged and no commits were created during this update.
- Live client installation and commit execution were not tested. T009 remains
  pending for enabled/disabled events and error/approval scenarios in disposable
  consumer repositories. Original live checks T005-T007 also remain unverified.
