---
name: clarify
description: Resolve material ambiguity in the selected software feature specification through focused user questions.
---

# Clarify requirements

Read and follow [the shared workflow](../../docs/workflow.md).

1. Resolve feature paths with `paths --require spec` and verify the intended feature.
   Read its spec, quality checklist, and relevant project context.
2. Identify omissions or conflicts that materially affect scope, behavior, interfaces,
   compatibility, data handling, accessibility, or verification.
3. Ask up to five prioritized questions per invocation. Offer concrete choices when
   useful and explain their consequences. Use the client's structured question tool
   when available; wait for answers rather than assuming consent.
4. Update the spec's dated Clarifications section and the affected requirements and
   acceptance scenarios. Keep user answers separate from unresolved assumptions.
5. If a plan or tasks already exist, update directly dependent content or mark it as
   needing revision before implementation continues. Update the quality checklist.
6. Report resolved questions, remaining blockers, and the appropriate next stage.
