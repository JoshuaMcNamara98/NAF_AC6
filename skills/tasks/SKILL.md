---
name: tasks
description: Break the selected software feature's specification and plan into dependency-ordered, verifiable implementation tasks.
---

# Generate implementation tasks

Read and follow [the shared workflow](../../docs/workflow.md).

1. Resolve paths with `paths --require spec plan`. Verify the feature and read its spec,
   plan, constitution, and any supporting design documents. Stop for material blockers.
2. Run:
   ```sh
   python .specify/scripts/speckit.py --project . tasks
   ```
   Existing tasks are preserved. When revising, retain completed tasks and their evidence;
   explicitly reopen affected tasks if changed requirements invalidate their completion.
3. Write concrete tasks with stable IDs, user-story/requirement references, exact source
   paths, explicit prerequisites, and acceptance checks. Group by user outcome.
   Include focused tests for changed behavior and related documentation and verification.
4. Mark parallel tasks only when their prerequisites and touched files are independent.
   Do not invent a fixed setup phase, database, API layer, or new testing framework.
5. Record requested user-review checkpoints and known blockers. Map every required
   outcome to at least one task and every task to agreed scope.
6. Report coverage, execution order, and readiness for analysis or implementation.
