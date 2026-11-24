# Tasks: Tests Skill for Unit-Test Generation

**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Status**: Skill and documentation implemented; static verification passed; T005 live verification blocked
**Feature directory**: `specs/001-tests-skill/` (shared tooling, not a game)

## Format

Unchecked tasks are not complete. Each task includes requirements, prerequisites,
target paths, and an acceptance check. `[P]` marks work that can proceed independently
without prerequisite or shared-file conflicts.

## US1 / US2 / US3 / US4 - Independent, project-aware test authoring

- [x] T001 [US1, US2, US3, US4] Create `skills/tests/SKILL.md` as one coherent manually invoked skill covering FR-001 through FR-012. **Prerequisites**: None. **Acceptance**: Frontmatter contains `name: tests`, a nonempty description, and `disable-model-invocation: true`; the relative shared-workflow link resolves. Instructions prioritize explicit specs paths, verify selection otherwise, report missing artifacts without initializing or writing feature selection, and ask about unsupported expected behavior. They recommend a fresh session and require confirmation when visible context shows same-session implementation. They inspect existing and colocated test conventions, infer a location only from project evidence, inventory relevant behavioral edge cases, reuse coverage, write test source only, run focused existing commands, repair only this invocation's demonstrably faulty tests, and report evidence-backed defects and untested cases in chat without production/configuration/dependency/document changes or publication.

## Documentation - User controls and workflow compatibility

- [x] T002 [P] [US1, US3, US4] Add a narrowly scoped tests-skill exception in `docs/workflow.md` for FR-003, FR-008, FR-009, and FR-012. **Prerequisites**: None. **Acceptance**: The exception explicitly permits reading available inputs without initialization or selection writes and reports verification in chat, not consumer documents. Existing initialization, feedback, testing, and verification requirements remain unchanged for all other skills; `skills/implement/SKILL.md` is untouched.
- [x] T003 [P] [US1, US2, US3, US4] Update `README.md` with the `tests` skill entry and a separate-session `/speckit:tests specs/001-json-import-button` example for FR-001, FR-002, FR-003, FR-005, FR-007, FR-008, and FR-009. **Prerequisites**: None. **Acceptance**: Documentation explains existing-test reuse, support for incomplete feature documents, behavioral edge-case testing, tests-only changes, and honest results; it does not promise enforced independence or removal of implementation-stage regression tests.

## Verification - Packaging, behavior, and evidence

- [x] T004 [US1, US2, US3, US4] Verify the completed `skills/tests/SKILL.md`, `docs/workflow.md`, and `README.md` against all FR-001 through FR-012 using the static metadata/link command and instruction-review matrix in `specs/001-tests-skill/plan.md`. **Prerequisites**: T001, T002, T003. **Acceptance**: Static command passes; new Markdown links resolve; `git diff --check` passes; each requirement has consistent skill instructions and documentation. Inspect newly added files as well as tracked diffs. No runtime, manifest, template, generated `.specify/` resource, or implementation-skill changes are introduced.
- [ ] T005 [US1, US2, US3, US4] Exercise the new `skills/tests/SKILL.md` in a fresh compatible client session against isolated disposable target projects using the live scenario matrix below. **Prerequisites**: T004. **Acceptance**: Every applicable matrix case must pass with recorded observed behavior for SC-001 through SC-006; confirm target changes are limited to test source relative to the initial worktree. Do not claim static inspection proves live installation or behavior. If any applicable case is omitted, fails, or cannot be exercised, leave this task incomplete and record that case as failed or unverified. If a live client or suitable isolated target is unavailable, mark this task blocked rather than marking it complete.
- [x] T006 [US1, US2, US3, US4] Record actual verification evidence in `specs/001-tests-skill/verification.md` using `.specify/templates/verification-template.md`, and reconcile task status in `specs/001-tests-skill/tasks.md`. **Prerequisites**: T004 and the T005 verification attempt or explicit blocker determination. **Acceptance**: Record exact static commands, live procedures, environment, results, failures, and checks not run. Distinguish verified packaging from live behavior and map evidence/gaps to requirements and SC-001 through SC-006. T005 remains blocked if live verification did not occur. This plugin feature record is not a document the tests skill may generate in a consumer project.

### T005 live scenario matrix

Use only inspected, safe commands supplied by each disposable target's tooling. Do not
install frameworks or add a permanent test harness to this plugin.

| Case | Requirements / criteria | Expected observation |
| --- | --- | --- |
| Explicit feature path and existing tests | FR-001, FR-005, FR-007 / SC-001, SC-002 | Explicit input wins over any selection; existing layout, helpers, and framework are reused; cases map to requirements and boundaries without duplication |
| Multiple test directories and frameworks | FR-005, FR-007 / SC-001 | Only the feature's relevant framework, runner, helpers, and test location are used; unrelated suites and layouts remain unchanged |
| No explicit path, valid selected feature | FR-001 | Selected feature is verified before authoring |
| Invalid path, ambiguous multi-feature directory, or unavailable selection | FR-001, FR-004 | Specific input error or clarification; no silent fallback or feature creation |
| Older implementation with missing workflow artifacts | FR-003, FR-004 / SC-005 | Available expectations suffice where documented; missing inputs reported, unspecified outcomes prompt, and no initialization or feature documents are written |
| No test directory but documented tooling, then no inferable tooling | FR-006 / SC-001 | Evidence-based location reported in the first case; clarification or explicit blocker in the second |
| Passing focused run and objectively faulty newly authored test | FR-009, FR-010 / SC-004 | Exact command/results reported; test defect may be repaired without changing expected behavior, followed by a recorded rerun |
| Implementation/spec failure and relevant defect observations | FR-007, FR-010, FR-011 / SC-002, SC-006 | Failing behavioral assertion retained; potential bugs, missing exception handling, and dead code qualified and evidence-backed; no production repair |
| Missing runner or dependency | FR-008, FR-009 / SC-003, SC-004 | No installation or configuration change; execution blocker explicit, no passing claim |
| Same-session implementation visible in context | FR-002 | Warning and confirmation before test authoring; no claim of technically enforced separation |
| Before/after worktree for each authoring case | FR-008, FR-012 / SC-003 | Skill-authored changes are test source only; unrelated work preserved; no staging, commits, or publication |

## Dependencies and Checkpoints

- T001, T002, and T003 have no implementation prerequisites and touch distinct canonical
  files. T002 and T003 may run in parallel with T001 using the agreed spec and plan;
  cross-file consistency is checked in T004.
- T004 depends on T001, T002, and T003. T005 depends on T004. T006 depends on T004 and
  the outcome of attempting T005, including an explicit blocked outcome.
- Review these tasks and run `/speckit:analyze` before `/speckit:implement`. Generation of
  this document does not authorize implementation or bypass review checkpoints.
- If scope or requirements change, revise the spec/plan and affected pending tasks first;
  reopen completed tasks only when their evidence is invalidated.
- No commits, pushes, deployment, publication, or additional agents are authorized.

## Requirement Coverage

| Requirements | Implementation / documentation | Verification |
| --- | --- | --- |
| FR-001, FR-002 | T001, T003 | T004, T005, T006 |
| FR-003 | T001, T002, T003 | T004, T005, T006 |
| FR-004, FR-006, FR-010, FR-011 | T001 | T004, T005, T006 |
| FR-005, FR-007 | T001, T003 | T004, T005, T006 |
| FR-008, FR-009 | T001, T002, T003 | T004, T005, T006 |
| FR-012 | T001, T002 | T004, T005, T006 |

All tasks implement, document, or verify agreed requirements. No new runtime, test
framework, helper script, or unrelated source change is included.

## Blockers

T005 is blocked: `command -v copilot` and `command -v code` returned no executable in
this shell. A fresh isolated compatible client session was not available for live
invocation of the new skill. All live matrix cases remain unverified. No additional
agent sessions or installed-cache changes were made. See [verification.md](verification.md)
for static results and remaining work.

## Convergence Review - 2026-11-24

- Compared all acceptance scenarios and FR-001 through FR-012 with the canonical skill,
  shared workflow, README, and recorded evidence. No missing instruction behavior or
  failed static check was identified. T001-T004 and T006 remain complete for their
  documented creation, static-review, and evidence-recording acceptance checks.
- Rechecked metadata, relative Markdown links, whitespace (including untracked files),
  and unchanged tracked runtime/manifest/templates/implementation-skill resources.
  Checks passed. `copilot` and `code` remain unavailable in this shell.
- SC-001 through SC-006 remain unverified in live execution. T005 already covers every
  remaining case and remains blocked; no duplicate task was added and no completed task
  was incorrectly reopened.
- Next action: refresh/reinstall this canonical plugin in a compatible client, execute
  every applicable T005 case in fresh isolated sessions, and update `verification.md`
  and task status with actual results. Keep T005 incomplete for omitted, failed, or
  unavailable cases. No implementation resumed during this convergence review.
