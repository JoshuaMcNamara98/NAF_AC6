# Implementation Plan: Complete Feature Workflow Skill

**Date**: 2026-11-25
**Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

Add one `feature-workflow` skill that guides a user through the existing canonical
skills in the specified order. The skill will check the confirmed target project's
managed Spec Kit marker/CLI and constitution before beginning, display a conversational
task list that identifies the current stage, and follow each stage's canonical
instructions rather than merely printing skill names. Successful stages advance
automatically unless a canonical skill requires user input or a blocker occurs.
The separate `tests` stage remains opt-in after `converge`. Process supported
target-project Git extension commit events before/after stages with per-commit
approval; completion reports commits and remaining changes without a final
`git-commit` stage or reminder.

## Repository Findings

- This repository packages Agent Plugin skills as `skills/<name>/SKILL.md`; the
  frontmatter `name` matches the directory name. Existing skills link to shared
  workflow documentation and other resources with paths relative to their own file.
- `plugin.json` contains plugin-level metadata and does not enumerate individual
  skills. The README maintains the discoverability table and the feature workflow
  example, so those are the related documentation surfaces.
- The specified stages already exist as canonical skills:
  `skills/git-feature/SKILL.md`, `skills/git-remote/SKILL.md`,
  `skills/specify/SKILL.md`, `skills/git-validate/SKILL.md`,
  `skills/clarify/SKILL.md`, `skills/plan/SKILL.md`,
  `skills/tasks/SKILL.md`, `skills/analyze/SKILL.md`,
  `skills/implement/SKILL.md`, `skills/converge/SKILL.md`,
  `skills/tests/SKILL.md`, and `skills/git-commit/SKILL.md`.
- The existing skills define important interactions that must not be bypassed:
  branch and commit approvals, user clarification and review, explicit failure
  reporting, the separate-session recommendation and same-session confirmation for
  `tests`, and the prohibition on unapproved commits or pushes.
- `docs/workflow.md` requires a confirmed target project, Python 3.10+ for Spec Kit
  CLI operations, explicit branch/commit control, and no claim that printing a skill
  command invokes it. `init` seeds `.specify/memory/constitution.md`, and
  `constitution` edits that file in place.
- No repository test directory or plugin-specific test runner was found. The
  feature changes skill instructions and documentation; there is no runtime dispatcher
  or dependency manifest to extend. The current worktree also has a pre-existing
  modified `README.md`; preserve and integrate its existing content when documenting
  the new skill.

## Technical Context

- **Languages and supported versions**: Markdown skill content; plugin clients must
  support the Agent Plugins skill invocation forms documented in the README. Where
  the skill runs the project's Spec Kit CLI, use a verified Python 3.10+ executable.
- **Dependencies and storage**: No new packages, runtime code, or persistent
  workflow-state files. Maintain the stage checklist in the skill's conversational
  output.
- **Platforms and deployment constraints**: Keep resources as relative links within
  the plugin so installed plugin copies can resolve canonical skill instructions.
- **Compatibility and data handling**: Operate only on the confirmed target project,
  never assume this plugin checkout is the consumer, and follow each canonical
  skill's existing Git, confirmation, and data-handling constraints.

## Constitution Check

- **Project-aware changes**: Pass. Add only the requested plugin skill and directly
  related README documentation; do not assume consumer project source layout or
  technology.
- **Agreed scope**: Pass. Preserve the user-approved sequence and optional test stage.
  Keep the canonical skills authoritative for their stage behavior.
- **Safe and clear behavior**: Pass. Stop on failed preflight or a blocked/declined
  stage; preserve each skill's approval gates; commit only approved configured
  events, never push or deploy.
- **Demonstrated quality**: Pass with a verification limitation. There is no existing
  automated test suite for skill orchestration; validate metadata and links statically
  and exercise requirements through a documented manual acceptance walkthrough.
- **Simple delivery**: Pass. No helper scripts, dependencies, storage, or edits to
  generated consumer-project files are needed.

## Design and Source Boundaries

- Add `skills/feature-workflow/SKILL.md` with `name: feature-workflow` and a concise
  description. Link the canonical stage files with relative Markdown paths.
- Present the complete stage list before preflight, including the optional `tests`
  stage. Show preflight as current while it runs; show each requested stage as pending,
  current, completed, skipped, or blocked as appropriate. Mark unrequested tests as
  skipped and later stages as not started after a blocker. Do not claim a stage
  completed merely because it was named or listed.
- Preflight: confirm the target repository; check compatible `.specify/` management,
  the required CLI and supported Python when CLI verification is needed, and a
  readable non-empty `.specify/memory/constitution.md`. Use read-only inspection;
  report missing/incompatible setup and stop without running `init` or `constitution`.
- At each handoff, mark the completed stage and next current stage in the task list.
- Process supported commit events using the target's `git-config.yml`,
  `extension.yml`, and existing platform script. Validate configuration, report
  disabled/missing-config skips, and block on missing enabled-event resources or
  commit failures. Review all changes and obtain approval before each commit because
  the script stages all changes; preserve unrelated work and verify actual outcomes.
  Avoid duplicate hooks and empty commits. Do not invent convergence or tests events.
- Follow each existing stage's canonical instructions and user prompts. Where
  client-level skill invocation is not available, read/follow its canonical linked
  `SKILL.md` instructions; do not print slash commands as a substitute for execution.
  Successful completion advances to the next stage without an extra approval prompt,
  but never bypasses a stage-specific confirmation, question, feedback checkpoint,
  or failure stop.
- Run `tests` after `converge` only when explicitly requested. Honor its
  same-session independence warning and request for confirmation before writing
  tests if this workflow authored implementation in the same session.
- At completion, report stage outcomes, commit hashes/events, and remaining work.
  Do not invoke or recommend a final `git-commit` stage or catch-all commit.
- Update the relevant README feature-workflow example and skills table to document
  the new entry point and retain the existing manual sequence as needed. Do not edit
  other canonical skill files, `plugin.json`, runtime scripts, or consumer `.specify/`.

## Verification

| Requirement | Check or command | Expected result |
| --- | --- | --- |
| FR-001 / NFR-001 | Inspect `skills/feature-workflow/SKILL.md` frontmatter and README links/table | Skill name matches the directory; the skill is discoverable with supported invocation names and relative links resolve. |
| FR-002 / SC-003 | Manually walk preflight with compatible setup, missing marker/CLI, and absent/empty/unreadable constitution cases | Compatible target proceeds; invalid setup reports the exact blocker and stops without setup writes or stage execution. |
| FR-003 / SC-001 | Manually trace displayed required-stage order | All ten required skills appear once and are followed in the specified order. |
| FR-004 / FR-006 / SC-004 / SC-007 | Walk success, prompt/approval, failure, and user-decline handoffs against each canonical skill | Success advances without an extra approval; canonical gates are preserved; a blocker prevents later stages from starting. |
| FR-005 / SC-002 | Inspect task-list behavior through successive stage transitions | Exactly one stage is current, or the workflow clearly shows paused, complete, or blocked state; remaining stages are accurately pending/skipped. |
| FR-007 / SC-005 | Run walkthrough with and without explicit tests request | Separate tests stage runs only when requested, after converge; implement verification remains required. |
| FR-008 / SC-006 | Inspect event configuration/approval/failure paths and completion output | Only approved enabled supported events commit; disabled events skip, failures block, outcomes are verified, and no final git-commit stage/reminder or push occurs. |
| FR-009 | Exercise missing-input and blocked-stage paths | Outcomes and blockers are reported accurately; no unrun stage or check is described as successful. |
| All changed Markdown | `git diff --check` and inspect new relative links/frontmatter | No whitespace errors, unresolved placeholders, mismatched skill metadata, or broken relative links. |

Record actual outcomes in `verification.md`, not as implied results here.
No automated type check, build, accessibility, performance, or unit-test command
applies to this Markdown-only change; do not add a test framework for it. Run the
repository's established checks if one is identified during implementation.

## Risks and Decisions

- **Skill orchestration semantics**: A skill command printed in chat is not an
  invocation. The orchestrator must execute the stage behavior by following the
  canonical skill instructions/resources and report actual progress.
- **Prompt accumulation**: Existing skills independently request confirmations or
  user feedback. Keep those prompts at their corresponding stages; automatic
  handoffs apply only after a stage succeeds with no pending decision.
- **Tests independence**: `tests` is designed for a separate session. If the
  orchestrated implementation happened in the same session, its instructions require
  a warning and user confirmation before test authoring.
- **Existing README edit**: `README.md` is already modified in the worktree. Inspect
  and preserve those changes when adding the skill entry and example.
- No unresolved technical decisions or new dependencies identified.

## Delivery

Review the orchestration instructions and manual acceptance walkthrough before
implementation proceeds. Changes are additive: remove the new skill and its README
entry to roll back. Preserve the existing per-skill commands and behavior for users
who do not choose the orchestrator.

No research, data-model, contract, or quickstart documents are needed.
