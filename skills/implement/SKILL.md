---
name: implement
description: Implement and verify the selected software feature's tasks, incorporating user feedback while preserving repository conventions and unrelated work.
disable-model-invocation: true
---

# Implement the agreed feature

Read and follow [the shared workflow](../../docs/workflow.md).

1. Run `paths --require spec plan tasks`. Verify the intended feature and read its
   spec, plan, tasks, constitution, supporting designs, and relevant source/tests.
   Inspect Git status and honor requested review checkpoints.
2. Check requirements checklist findings and artifact consistency. Ask before proceeding
   with unresolved material decisions or conflicts; do not treat unchecked items as approval.
3. Execute pending tasks in dependency order. Reuse existing helpers and tooling, keep
   changes scoped, add focused regression tests, and preserve supported behavior.
   Surface errors explicitly using project-standard handling.
4. Incorporate user feedback as it arrives. If it changes behavior or scope, update the
   spec, plan, and tasks before continuing. Pause for consequential decisions.
5. Run planned targeted tests, applicable type checks/builds, and acceptance procedures.
   If a check fails, fix in-scope causes and rerun it. Do not hide pre-existing failures.
6. Create or update `verification.md` using the project verification template. Record
   exact commands, environment, observed results, failures, and checks not run.
   Mark each task complete only after its acceptance check passes.
7. Report delivered behavior, verification, remaining work, and review needs. Do not
   automatically stage, commit, push, deploy, or create a pull request.
