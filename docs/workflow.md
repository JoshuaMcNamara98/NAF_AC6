# Shared skill workflow

Use this guidance when running a bundled skill. All paths refer to the **target
project**, not the installed plugin.

## Project and feature

- Confirm the target repository and requested feature before writing. Read its agent
  instructions, contributor guidance, constitution, relevant source, manifests, and tests.
- Inspect Git status and preserve staged and unrelated changes. Do not initialize Git,
  switch branches, commit, push, publish issues, or deploy unless requested.
- Follow the target project's architecture, conventions, supported runtimes, accessibility
  requirements, and existing tools. The plugin's constitution is not consumer policy.
- Use a verified Python 3.10+ executable (`python`, `python3`, or a versioned executable);
  no third-party Python packages are needed.

## Initialize and select

The `tests` skill uses the tests-only exception below instead of initialization or
selection writes.

- Check `.specify/speckit-plugin.json`. If tooling is missing, run the `init` skill.
  If `.specify/` is unmanaged or has an incompatible version, stop and explain the
  migration needed; do not overwrite or mix tooling.
- Resolve the intended feature with:

  ```sh
  python .specify/scripts/speckit.py --project . paths
  ```

  Verify that it matches the request. Select the intended feature explicitly when needed:

  ```sh
  python .specify/scripts/speckit.py --project . select --feature specs/001-json-import-button
  ```

- Feature documents default to `specs/NNN-short-name/`; implementation stays in the
  project's source layout. Feature directories are independent of Git branches.
- Use templates from the target project's `.specify/templates/`. Resolve skill resources
  relative to the installed skill, not from an assumed plugin location.
- CLI output is JSON on stdout and errors on stderr. Stop on failure; do not invent paths
  or report success after an error.

## Specify, plan, and implement

- Gather behavior, users, exclusions, compatibility, dependencies, and testable acceptance
  criteria. Separate confirmed answers from assumptions; ask about material ambiguity.
- Present the specification and plan for review before implementation. Continue through
  checkpoints only when the user requests the full workflow.
- If feedback changes scope or behavior, update the specification, plan, and tasks before
  continuing. Cosmetic feedback does not require restarting the workflow.
- Implement the smallest complete change using project conventions. Add focused tests and
  run the smallest relevant checks, including applicable type checks and builds.
- Record actual commands, results, failures, and untested checks in the feature's
  `verification.md`. Mark tasks complete only when their acceptance criteria pass; report
  blockers and remaining work explicitly.
- Do not infer approval for consequential changes, human review, deployment, or release.

## Skill commands

Use the skill invocation mechanism and names exposed by the current client. Plugin-aware
clients may show commands such as `/speckit:plan`; others may show plain names such as
`plan`. Printing a slash command does not invoke it. This plugin has no automatic commit
hooks or executable lifecycle hooks.

The explicitly invoked Git skills operate on existing repositories using the bundled
Git tooling. They do not require feature selection or initialize Git. A branch, commit,
or push requires explicit user approval; review each proposed commit and preserve
unrelated changes.

## Tests-only exception

The manually invoked `tests` skill supports existing implementations with incomplete
feature documents or no initialized tooling. Use an explicit specs directory when
provided; otherwise verify the selected feature using read-only paths resolution when
available. Report missing or invalid inputs and ask for the intended feature or missing
behavioral decisions. Do not initialize tooling or write selection or feature files.

For this skill only, author unit-test source files and report results and findings in
chat. Do not change production code, test configuration, dependencies, CI, requirements,
plans, tasks, or verification documents; do not install dependencies. The feedback and
verification-document instructions above do not authorize those writes during `tests`.
If feedback changes requirements, pause for revision through the appropriate stage.

Reuse project test conventions and run the narrowest relevant existing safe command.
Repair only demonstrable defects in this invocation's tests, never weaken expectations
to hide implementation failures. Preserve unrelated work and report failures, missing
inputs, untested cases, and evidence-backed suspected defects explicitly. Do not stage,
commit, push, deploy, or publish issues. These exceptions do not change any other skill's
initialization, regression-testing, feedback, or verification responsibilities.
