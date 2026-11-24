# Plugin development

This repository packages reusable software-development skills; it is not a consumer
application. Follow [docs/workflow.md](docs/workflow.md) for skill behavior and
[.specify/memory/constitution.md](.specify/memory/constitution.md) for this repository's
governance.

## Canonical sources

- `plugin.json` defines Agent Plugins metadata.
- `skills/<name>/SKILL.md` is the canonical skill source; its frontmatter name must match
  the directory. Keep linked resources relative to the skill file.
- `scripts/speckit.py` and `templates/` are canonical. Do not edit generated copies under
  a consumer project's `.specify/`.
- Consumer projects own their specifications, source layout, technology choices, and
  engineering policies. Never treat this plugin checkout as the default target.

## Changes and verification

- Preserve unrelated staged and unstaged work. Do not switch branches, commit, push,
  publish issues, or deploy without explicit instruction.
- Select and verify the intended feature before running feature-specific tooling; feature
  directories are independent of branch names.
- For runtime changes, verify initialization, preservation, explicit failures, and the
  affected CLI flow. Keep manifest and runtime versions consistent.
- For skill changes, verify metadata, relative resources, target scope, feedback handling,
  and user controls. Do not claim live VS Code installation was tested by static checks.
