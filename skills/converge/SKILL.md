---
name: converge
description: Compare implemented code and verification against the selected feature's requirements and append only concrete remaining work to its tasks.
---

# Converge on the agreed scope

Read and follow [the shared workflow](../../docs/workflow.md).

1. Run `paths --require spec plan tasks` and verify the feature. Read its artifacts,
   verification evidence, relevant code, and tests.
2. Compare each acceptance criterion with actual behavior and evidence. Run focused
   checks when needed. Separate missing behavior, failures, and unverified claims.
3. Append actionable remaining tasks with new stable IDs, requirement references,
   exact paths, dependencies, and verification. Preserve existing task history; reopen
   incorrectly completed tasks explicitly with the observed reason.
4. Do not broaden requirements, rewrite completed implementation, or manufacture work
   to reach a task count. Ask if the proposed remedy changes agreed scope.
5. Report gaps and added/reopened tasks. Resume implementation only if the user requested
   it; otherwise stop with the concrete next steps.
