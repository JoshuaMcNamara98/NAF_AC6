---
name: analyze
description: Read-only consistency analysis of the selected feature's specification, plan, tasks, and project governance before implementation.
---

# Analyze feature consistency

Read and follow [the shared workflow](../../docs/workflow.md).

1. Run `paths --require spec plan tasks` and verify the selected feature.
2. Read its spec, plan, tasks, supporting design documents, and constitution.
   This skill is read-only: do not edit artifacts or change task completion.
3. Check requirement coverage, contradictions, unclear acceptance criteria, scope drift,
   missing verification, unsupported repository assumptions, dependency ordering,
   shared-file parallel conflicts, and governance violations.
4. Report findings with severity, precise document references, affected requirement/task
   IDs, and a concrete remedy. Distinguish evidence from uncertainty.
5. State whether material blockers remain. Offer a targeted correction path, but do not
   apply it without user direction. Never equate a clean analysis with verified code.
