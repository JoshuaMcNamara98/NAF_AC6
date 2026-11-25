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

After each successful stage with no pending decision, mark it completed, make the
next stage current, and continue without an extra approval prompt. Preserve every
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
Git operations must obey their canonical skill's approval rules. Never stage, commit,
push, deploy, publish, or alter remotes on behalf of the user.

## Optional tests and completion

After `converge`, run [`tests`](../tests/SKILL.md) only if the user explicitly
requested it. Otherwise leave it skipped. If the user requests it later but before
workflow completion, change its status to pending and run it after `converge`. If
requested, follow its tests-only constraints, including its recommendation to use a
separate session. If the current session authored the implementation, warn the user
and obtain its required confirmation before writing tests. Do not treat this optional
stage as a substitute for implementation verification.

When all required stages and any requested tests stage finish, report the actual
outcomes, skipped checks, and remaining work. Remind the user to run
[`git-commit`](../git-commit/SKILL.md) to finalize changes; do not invoke it or commit
automatically.
