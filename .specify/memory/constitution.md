# Spec Kit Software Skills Constitution

**Status**: Maintainer-directed generic software workflow
**Last Amended**: 2026-11-24

## Core Principles

### I. Project-Aware Changes
Follow this project's architecture, supported runtimes, conventions, and existing tools.
Requirements determine technology choices. Do not import another project's assumptions.

### II. Agreed Scope
Specify intended behavior, compatibility, exclusions, and testable acceptance criteria.
Ask about material ambiguity and record user answers separately from assumptions.
Keep the specification, plan, tasks, and implementation consistent as feedback arrives.

### III. Safe and Clear Behavior
Preserve unrelated work and intended behavior. Do not commit credentials or disclose
sensitive data. Report failures through the project's established mechanisms.
Seek explicit approval for destructive operations and changes outside agreed scope.

### IV. Demonstrated Quality
Use focused tests and existing checks for changed behavior. Define measurable workloads
and thresholds when performance matters. Record actual results, failures, and untested
checks separately from intended targets. Never claim unperformed human approval.

### V. Simple Delivery
Prefer the smallest maintainable implementation that satisfies the agreed requirements.
Reuse existing helpers, avoid speculative dependencies, and update related documentation.

## Governance

This constitution governs development of the plugin, not its consumer projects.
Canonical skills, templates, and runtime remain independent of consumer technology.
Project initialization must preserve existing governance and reject incompatible tooling.
Generated project-local copies are not canonical package sources.

Amendments require the owner's direction, a dated rationale, and review of affected
feature documents.
Branching, committing, pushing, and publishing remain under explicit user control.

### Amendment Rationale

2026-11-24: The maintainer requested a reusable, generic software skill plugin.
Replace domain-specific requirements with project-aware workflow, explicit ownership,
safe initialization, feedback, and demonstrated verification. Update the shared
instructions, canonical skills, templates, tooling, and repository documentation together.
