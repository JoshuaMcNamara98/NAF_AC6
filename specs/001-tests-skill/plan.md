# Implementation Plan: Tests Skill for Unit-Test Generation

**Date**: 2026-11-24
**Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

Add one manually invoked Markdown skill, `tests`, that authors requirement-driven unit
tests in a separate agent session. Reuse the target project's tests and commands,
systematically identify relevant edge cases, and report missing inputs and suspected
defects without modifying production code. Update only the directly related shared
workflow guidance and README. No runtime, templates, dependencies, or agents are needed.

## Repository Findings

- `skills/<name>/SKILL.md` is canonical; frontmatter names match their directories.
  `skills/implement/SKILL.md` demonstrates `disable-model-invocation: true` for a
  user-controlled writing skill. Each skill links to `../../docs/workflow.md`.
- `plugin.json` declares Agent Plugins 1.0. Skills are discovered from `skills/`;
  there is no per-skill manifest registry to update.
- `docs/workflow.md` currently requires initialized tooling, a selected feature, and
  recording verification in a feature document. Those instructions need an explicit,
  narrow exception for the tests-only skill and features predating initialization.
- `scripts/speckit.py` provides read-only `paths` resolution for initialized projects,
  but always requires a nonempty `spec.md`. `select`, `create`, and `init` write files.
  Therefore those commands cannot be used as fallbacks inside the tests skill.
- `README.md` documents invocation, workflow stages, and the available skills.
- Inspection of tracked files found no automated test suite, package manifest, build,
  type-check, or lint configuration for this plugin. Do not invent such a runner.
- The active feature is `specs/001-tests-skill/`, a shared-tooling feature, not a game.

## Technical Context

- **Languages and supported versions**: Markdown skill instructions; existing optional
  feature-path tooling requires Python 3.10+. Planning used Python 3.11.13. Consumer
  tests use the consumer project's language and supported runtime, not this plugin's.
- **Dependencies and storage**: No new dependencies. Consumers receive changes to test
  source files only; results and findings are reported in chat rather than a new file.
- **Platforms and deployment constraints**: Existing Agent Plugins 1.0 clients. Reinstall
  or refresh the development plugin and start a fresh session for live verification.
  Installed plugin caches are not canonical sources and will not be edited.
- **Compatibility and data handling**: Preserve existing skills and runtime behavior.
  No migration, manifest/runtime version change, external service, or new data policy.
  Read only relevant project inputs and do not send code or test data to external services.

## Constitution Check

Pre-design review passes all five principles: project-owned test conventions (I),
confirmed tests-only scope and explicit missing-input behavior (II), preserved production
files and reported errors (III), focused verification and honest evidence (IV), and one
skill with minimal supporting documentation changes (V).

Post-design review passes with the narrow tests workflow exception below: test execution
results are reported in chat, not written to consumer feature documents. Other skills,
including `implement`, retain their current test and verification responsibilities.
No constitution amendment is required.

## Design and Source Boundaries

### Canonical plugin changes

1. Add `skills/tests/SKILL.md` with `name: tests`, an accurate description, and
   `disable-model-invocation: true`. Link the shared workflow using the existing relative
   convention. Keep the instructions explicit and sequential, without helper scripts.
2. Update `docs/workflow.md` with a tests-only exception: no initialization, selection
   writes, document updates, dependency installation, or production fixes; read available
   inputs and report verification in chat. This exception does not relax other stages.
3. Update `README.md` with the skill table entry and a separate-session invocation
   example, such as `/speckit:tests specs/001-json-import-button`, including incomplete
   workflow support and the tests-only boundary.

Do not modify `skills/implement/SKILL.md`, `plugin.json`, `scripts/speckit.py`, templates,
or generated `.specify/` resources. The new skill supplements, rather than removes,
implementation-stage regression tests.

### Skill input and workflow

- Confirm target project and feature. An explicit specs path wins over selection; if it
  contains several features, ask which feature to test. If the supplied path is invalid,
  report it rather than silently falling back to another feature.
- With no explicit path, use read-only `paths` only if tooling and selection are present
  and compatible; verify the returned feature. If unavailable or unsuitable, report the
  reason and ask for the intended feature or documents. Do not initialize or create a
  feature. Features with absent artifacts can still proceed from sufficient documented
  expectations; never infer requirements from current code behavior alone.
- Recommend a fresh session. If visible conversation context shows this session authored
  the implementation, warn and ask before proceeding. Do not inspect session histories
  or create an agent to enforce separation, and do not claim separation was verified.
- Read available specs, plan, tasks, checklist, and verification/analysis evidence,
  project governance, relevant source, and relevant tests. Report missing artifacts;
  absence of a saved analysis report does not prove analysis was never performed.
- Inspect conventional and project-specific test locations, including colocated tests,
  configuration, fixtures, helpers, and commands. Reuse the appropriate layout in
  multi-framework projects. When no layout exists, infer only from documentation or
  configuration and report the evidence; ask if the location or runner is unclear.
- Identify expected behavior before authoring assertions. Build a requirement/edge-case
  inventory covering applicable normal, boundary, empty, invalid-input, exception,
  failure, and state-interaction cases. Reuse existing coverage and explain untestable
  cases or undocumented outcomes rather than inventing assertions.
- Author tests only, using existing fixtures and isolation patterns. Compare failures
  against documented expectations. Correct demonstrable defects in this invocation's
  tests and rerun; do not weaken assertions, skip failing cases, or change production
  behavior to obtain a pass.
- Run the narrowest known existing command. Report missing tools, dependencies, unsafe
  setup steps, or other execution blockers without installing or altering configuration.
  Preserve unrelated work and distinguish pre-existing failures.
- Review the diff relative to the invocation's initial state. Report test files,
  requirement/edge-case mappings, exact commands and results, reruns, gaps, and
  evidence-backed suspected bugs, missing exception handling, or dead code. Qualify
  uncertainty; absence of observed test coverage alone is not proof of dead code.
  Do not write verification documents, reopen tasks, or commit/publish changes.

## Verification

| Requirement | Check or command | Expected result |
| --- | --- | --- |
| FR-001 / FR-002 | Inspect frontmatter and relative links; load the development plugin in a fresh client session | `tests` is user-invokable, shared workflow resolves, and same-session warning behavior is explicit |
| FR-001 / FR-003 / FR-004 / SC-005 | Review input flow using explicit path, selected feature, invalid path, multiple features, and missing artifacts | Explicit path wins; no stale fallback, initialization, invented expectation, or strict all-artifact prerequisite |
| FR-005 / FR-006 / SC-001 | Representative target with existing tests, then target with no directory but documented tooling, then no usable tooling | Existing conventions reused; supported inference reported; ambiguity prompts rather than new infrastructure |
| FR-005 / SC-001 | Target with multiple test directories and frameworks | Only the feature's relevant framework, runner, helpers, and location are used |
| FR-007 / SC-002 | Review inventory against a representative feature's requirements and meaningful boundaries | Identified cases map to tests or documented gaps; no duplication or line-coverage-only success claim |
| FR-008 / FR-012 / SC-003 | Compare before/after target worktree, including untracked files | Skill-authored changes are test source only; no installation, production/configuration/document changes, or Git publication |
| FR-009 / FR-010 / SC-004 | Exercise a passing run, a faulty newly authored test, a genuine implementation failure, and missing runner | Exact results reported; only test defects repaired; rerun recorded; genuine failure retained and blockers explicit |
| FR-011 / SC-006 | Review findings against source references and failing tests or documented expectations | Findings have evidence and uncertainty labels; no production fix or dead-code claim based solely on unexecuted lines |
| All | `python .specify/scripts/speckit.py --project . paths --require spec plan` | Correct active feature and nonempty artifacts |
| Documentation | `git diff --check` and review new files for whitespace and broken relative links | No whitespace errors; all new skill/README links resolve |

For static metadata/link validation after implementation, run from the plugin root:

```sh
python - <<'PY'
from pathlib import Path

skill = Path("skills/tests/SKILL.md")
text = skill.read_text(encoding="utf-8")
assert text.startswith("---\n")
header = text.split("---", 2)[1].splitlines()
assert "name: tests" in header
assert any(line.startswith("description: ") and line[13:].strip() for line in header)
assert "disable-model-invocation: true" in header
assert "../../docs/workflow.md" in text
assert (skill.parent / "../../docs/workflow.md").is_file()
assert "skills/tests/SKILL.md" in Path("README.md").read_text(encoding="utf-8")
print("Skill metadata and resource links passed")
PY
```

These are static instruction checks, not proof of live client behavior. Run live scenarios
only against isolated disposable target projects with known safe test commands. No live
verification task is complete until every applicable scenario passes. Report omitted,
failed, or unavailable cases individually rather than counting partial verification as complete.
No consumer framework or command can be specified until the target is inspected. Record
actual implementation-stage results in this plugin feature's `verification.md`, including
any live cases not performed. This record is not a document generated by the tests skill
in a consumer project. No type-check/build, accessibility, or performance check applies
to the Markdown-only change; no performance target was requested.

## Risks and Decisions

- **Session independence**: A skill cannot technically enforce independent authorship.
  Use clear fresh-session guidance and a visible-context confirmation gate, not a new
  agent or runtime mechanism.
- **Shared guidance conflict**: Explicitly scope the tests-only exception; do not
  silently inherit initialization or verification-file writes.
- **Older feature support**: Read available evidence without mandatory prior-stage
  completion. Ask for missing behavioral decisions, not for ceremonial artifacts.
- **Edge-case breadth**: Systematically examine relevant boundaries and report gaps.
  Do not promise exhaustive combinations, infer unspecified exceptions, or substitute a
  numeric line-coverage target for behavioral assertions.
- **Defect attribution**: Distinguish faulty tests, implementation/spec conflicts, and
  uncertain observations; never adjust expectations merely to match existing code.
- **Verification limitation**: Static checks establish packaging/instruction consistency
  only. Live installation and agent behavior require separate recorded evidence.
- **Blockers**: None requiring a technical decision at planning time. Consumer-specific
  runner/location ambiguity is handled by the skill's documented clarification path.

## Delivery

Stop for plan review. Next generate tasks, then run consistency analysis before
implementation. Deliver one canonical skill and two related documentation updates;
do not create standalone research, contracts, data models, or quickstart documents.
Preserve all existing skills and tooling. If the design changes, revise dependent
specification/plan/tasks before implementation. Reverting this feature means removing only
its own skill and related documentation additions; no consumer migration is involved.
