# Spec Kit Software Skills

A VS Code agent plugin for planning, building, and verifying features in existing
software projects.

## Install the plugin

1. In VS Code, run **Chat: Install Plugin from Source** from the Command Palette.
2. Enter this repository's Git URL or the absolute path to its local clone.
3. Choose **User** scope to use the skills across projects.
4. Open your application project, start a fresh Copilot chat, and check
   **Chat: Open Customizations** or the chat `/` menu for the skills.

This is an agent plugin, not a VSIX extension or standalone AI runtime. Use a
VS Code/Copilot client that supports
[Agent Plugins 1.0](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference).
For private repositories, the client must have Git access and allow plugin installation.

## Start a fresh project

Open your application repository in VS Code and start a chat. Initialize project-local
tooling once, then tailor the project's engineering principles:

```text
/speckit:init
/speckit:constitution Follow this project's existing contributor rules.
```

Initialization requires Python 3.10+ and adds the tooling and templates under `.specify/`.
Feature documents go under `specs/`.

## Develop a feature

For example, to add a button that imports a JSON file:

```text
/speckit:specify Add a button to import a JSON file.
/speckit:clarify
/speckit:plan
/speckit:tasks
/speckit:analyze
/speckit:implement
```

Run `clarify` when material questions remain. Review the specification and plan before
implementation; ask for the full workflow if you want the agent to continue through
review checkpoints. Give feedback in the same chat—the skills update related documents
when requirements change. The agent reports failed, blocked, and untested checks.

### Add unit tests in a separate session

After implementation, start a fresh agent chat and invoke:

```text
/speckit:tests specs/001-json-import-button
```

Use your feature's specs directory. Without a path, the skill verifies the selected
feature. It supports existing implementations with incomplete feature documents and
does not require initialization when an explicit specs directory is provided.
It reuses existing test locations, frameworks, fixtures, and commands, testing relevant
behavioral edge cases rather than line execution alone.

The skill changes unit-test source files only, runs relevant tests, and reports results,
missing inputs, untested cases, and evidence-backed suspected defects in chat. It does
not fix production code or install dependencies.

## Skills and when to use them

| Skill | What it does and when to use it |
| --- | --- |
| [`init`](skills/init/SKILL.md) | Set up project-local tooling and templates once per project. |
| [`constitution`](skills/constitution/SKILL.md) | Create or update the project's engineering principles after initialization. |
| [`specify`](skills/specify/SKILL.md) | Start each feature by writing its scope, user scenarios, and acceptance criteria. |
| [`clarify`](skills/clarify/SKILL.md) | Resolve important unanswered requirements and update the specification. |
| [`plan`](skills/plan/SKILL.md) | Decide how the feature fits the existing project and how it will be verified. |
| [`tasks`](skills/tasks/SKILL.md) | Turn the agreed specification and plan into ordered, testable work items. |
| [`analyze`](skills/analyze/SKILL.md) | Check the spec, plan, and tasks for inconsistencies before implementation; read-only. |
| [`implement`](skills/implement/SKILL.md) | Carry out the agreed tasks, run checks, and record verification. Invoke when ready to implement. |
| [`tests`](skills/tests/SKILL.md) | In a separate session, add and run requirement-driven unit tests using available specs and existing test conventions. |
| [`converge`](skills/converge/SKILL.md) | Compare completed work with acceptance criteria and add tasks for concrete gaps. |
| [`checklist`](skills/checklist/SKILL.md) | Review requirements in a chosen area, such as accessibility or compatibility. |
| [`taskstoissues`](skills/taskstoissues/SKILL.md) | Publish tasks as GitHub issues only after confirming the destination and approving the proposal. |
| [`git-feature`](skills/git-feature/SKILL.md) | Create an approved numbered feature branch. |
| [`git-validate`](skills/git-validate/SKILL.md) | Validate a numbered feature branch and find matching specifications. |
| [`git-remote`](skills/git-remote/SKILL.md) | Detect whether the origin remote is a GitHub repository without contacting it. |
| [`git-commit`](skills/git-commit/SKILL.md) | Commit explicitly reviewed and approved changes. |

Use the command names shown by your client: some clients display `/speckit:<skill>`,
while others show plain skill names such as `plan`.

## Plugin development

Canonical sources are [skills](skills/), [scripts](scripts/), [templates](templates/),
and [shared workflow guidance](docs/workflow.md). Repository-specific instructions are
in [AGENTS.md](AGENTS.md).
