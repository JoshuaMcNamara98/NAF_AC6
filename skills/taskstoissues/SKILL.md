---
name: taskstoissues
description: Publish selected feature tasks as GitHub issues only after confirming the destination repository and user approval.
disable-model-invocation: true
---

# Publish tasks to issues

Read and follow [the shared workflow](../../docs/workflow.md).

1. Run `paths --require spec plan tasks`, verify the feature, and read its artifacts.
2. Determine the intended GitHub repository from its remote and confirm it with the user.
   Never use the plugin repository as the destination by default.
3. Read existing issues and any task-to-issue mapping to avoid duplicates. Present the
   proposed issue grouping, titles, bodies, dependencies, and destination for approval.
4. After explicit approval, use the available GitHub integration to create or update
   issues. If authentication or write tooling is unavailable, report the blocker;
   do not claim publication or silently switch destinations.
5. Record actual issue URLs and task mappings in `issues.md` inside the feature.
   Report partial failures and dependencies honestly. Never close issues automatically.
