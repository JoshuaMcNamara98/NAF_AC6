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
