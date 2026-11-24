# Tasks: [FEATURE NAME]

**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## Format

Use `- [ ] T001 [US1] Description with exact target paths`.
Each task identifies the requirement it satisfies and its acceptance check.
Add `[P]` only for independent tasks without shared-file or prerequisite conflicts.
Replace these examples with actual work; do not impose a fixed infrastructure phase.

## US1 - [User goal]

- [ ] T001 [US1] Add focused regression tests in [actual path] for FR-001.
- [ ] T002 [US1] Implement FR-001 in [actual paths]. Depends on T001.
- [ ] T003 [US1] Verify SC-001 using [planned command or procedure]. Depends on T002.

## Documentation and Final Verification

- [ ] T004 Update [directly affected documentation].
- [ ] T005 Record commands, outcomes, failures, and untested checks in verification.md.

## Dependencies and Checkpoints

[Explicit prerequisites, valid parallel work, and requested user-review checkpoints]

## Blockers

[Blocked task IDs, reasons, and decisions needed; unchecked is not complete]
