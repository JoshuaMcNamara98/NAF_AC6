---
name: feature-workflow
description: Guide a complete feature through the project's approved branch, specification, planning, implementation, and convergence workflow.
---

# Run the feature workflow

Guide the user through the canonical skills in this exact order. This skill does not
replace those skills or their controls. Follow their instructions as the user-facing
stage is performed; naming a skill or printing its slash command does not mean that
stage ran.

Read and follow the shared [workflow guidance](../../docs/workflow.md). Canonical
stage instructions are linked below and are relative to this skill.

## Preflight and status

1. Confirm the target project and feature request. Do not assume the plugin checkout
   is the user's project. Read the target's `AGENTS.md` and relevant contributor
   guidance. Inspect its initial Git state and preserve existing changes.
2. Before running any workflow skill, show a task list with **Preflight** current and
   every required stage pending. Mark `tests` pending only if the user explicitly
   requested that optional stage; otherwise mark it skipped. Keep the list visible
   and update it at every stage transition. Use only these stage statuses: pending,
   current, completed, skipped, and blocked. For example:

   ```text
   - Preflight — current
   - git-feature — pending
   - git-remote — pending
   - specify — pending
   - git-validate — pending
   - clarify — pending
   - plan — pending
   - tasks — pending
   - analyze — pending
   - implement — pending
   - converge — pending
   - tests — skipped (optional; not requested)
   ```
3. Check the target project's managed Spec Kit installation without writing files:
   - Verify `.specify/speckit-plugin.json` exists, is readable valid JSON, and its
     `name` and `version` match `PLUGIN_NAME` and `VERSION` in the bundled
     [Spec Kit CLI](../../scripts/speckit.py).
   - Verify `.specify/scripts/speckit.py` exists and is byte-for-byte identical to
     the bundled CLI. Use a verified Python 3.10+ interpreter for runtime
     inspection or comparison. If compatibility cannot be established, report what
     failed and stop; do not repair, initialize, or overwrite tooling.
   - Verify `.specify/memory/constitution.md` exists, is readable, and contains
     non-whitespace content. Its presence is the prerequisite; do not infer that the
     `constitution` skill ran or require additional tailoring.
   - Do not run `paths` before `specify`: a new feature may not yet be selected.
     Do not run `init` or `constitution` automatically.
4. If the project root, managed tooling, or constitution cannot be verified, mark
   preflight blocked, explain the specific prerequisite, leave the workflow skills
   pending, and stop. If preflight succeeds, mark it completed and set the first
   workflow skill current.

## Required stages

Perform each stage in order. Follow its canonical instructions, including its
repository scope, prompts, approvals, feedback, and stop conditions. Use the client's
skill-invocation mechanism when it is available; otherwise follow that skill's
canonical instructions directly. Do not claim success merely because the instructions
were read. Mark a stage completed only after its work and required checks succeed.

1. [`git-feature`](../git-feature/SKILL.md)
2. [`git-remote`](../git-remote/SKILL.md)
3. [`specify`](../specify/SKILL.md)
4. [`git-validate`](../git-validate/SKILL.md)
5. [`clarify`](../clarify/SKILL.md)
6. [`plan`](../plan/SKILL.md)
7. [`tasks`](../tasks/SKILL.md)
8. [`analyze`](../analyze/SKILL.md)
9. [`implement`](../implement/SKILL.md)
10. [`converge`](../converge/SKILL.md)

Before each stage, process its configured `before_<skill>` commit event as described
below. After each successful stage, process its configured `after_<skill>` commit
event before marking it completed. With no pending decision, make the next stage
current and continue without an extra handoff approval prompt. Preserve every
stage-specific confirmation, question, review checkpoint, and user-feedback pause.
The user's request to run this complete workflow allows continuation past normal
stage review checkpoints, but it does not waive approvals or resolve material
decisions on the user's behalf.

If a stage fails, is declined, or lacks required input, mark that stage blocked and
report the evidence and blocker. Leave unstarted stages pending, state that the
workflow is blocked at that stage, and wait for the user's direction. Do not start a
later stage or claim that a blocked or unrun stage succeeded. If feedback changes
requirements, pause and update the spec, plan, and tasks before continuing.

The `git-remote` stage detects the configured origin without contacting it. Other
Git operations must obey their canonical skill's approval rules. Staging and commits
are allowed only for the configured, explicitly approved events below. Never push,
deploy, publish, or alter remotes on behalf of the user.

## Configured auto-commit events

Use the **target project's** `.specify/extensions/git/git-config.yml`, not the
installed plugin's configuration. A missing config disables auto-commit; report
that it is skipped and continue. If present, verify it is readable, valid YAML,
and that the relevant `auto_commit` values are booleans and messages are strings.
An event subsection must contain a boolean `enabled` value when present.
Report invalid configuration and block before running the affected stage or event;
do not silently treat invalid values as disabled.

Use the target's `.specify/extensions/git/extension.yml` to identify registered
commit hooks for the stage. The supported workflow events are `before_clarify`,
`before_plan`, `before_tasks`, `before_analyze`, `before_implement`, and
`after_specify`, `after_clarify`, `after_plan`, `after_tasks`, `after_analyze`,
`after_implement`. Do not invent events for `git-feature`, `git-remote`,
`git-validate`, `converge`, or `tests`, even when `auto_commit.default` is true.
For each supported event, use its subsection's explicit `enabled` value; otherwise
use `auto_commit.default`, which defaults to false. Report disabled events as
skipped without staging or committing.

For each enabled event:

1. Verify the target's registered hook and platform-appropriate auto-commit script
   exist. If missing or incompatible, report the blocker and stop; do not install
   or overwrite extension files automatically.
2. Follow the review and approval controls in
   [`git-commit`](../git-commit/SKILL.md): inspect the current branch, staged and
   unstaged diffs, and untracked files. Explain that the upstream script stages
   **all** changes. Propose the exact event, files, configured message (or the
   script's default message), and required trailers; obtain explicit approval
   before each commit. Configuration enables an event; it does not approve its
   contents. If unrelated work would be included or the script cannot produce the
   approved message/trailers, stop for user direction rather than changing the
   index, configuration, or commit scope silently.
3. Execute the target project's script with that event using the canonical
   [commit command](../../.specify/extensions/git/commands/speckit.git.commit.md).
   Do not run the installed plugin's script against its own checkout. If the
   client already executed the same hook for this stage, verify its result instead
   of running it twice.
4. Verify the actual commit and remaining Git state. A clean worktree needs no
   empty commit; report it as a no-change event. A failed or declined commit, or
   a script that skips an enabled event despite pending changes, blocks the
   current stage and later stages. Report the failure and any staged changes
   left by the script; do not reset them or claim success.

These events do not change individual skills' standalone behavior or authorize
commits during the optional tests-only stage.

## Optional tests and completion

After `converge`, run [`tests`](../tests/SKILL.md) only if the user explicitly
requested it. Otherwise leave it skipped. If the user requests it later but before
workflow completion, change its status to pending and run it after `converge`. If
requested, follow its tests-only constraints, including its recommendation to use a
separate session. If the current session authored the implementation, warn the user
and obtain its required confirmation before writing tests. Do not treat this optional
stage as a substitute for implementation verification.

When all required stages and any requested tests stage finish, report the actual
outcomes, commit hashes and events, skipped checks/events, and remaining work.
Report any uncommitted changes, including those from `converge` or optional `tests`.
Do not invoke or recommend a final `git-commit` stage, or make a catch-all final
commit.
