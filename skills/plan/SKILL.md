---
name: plan
description: Design a minimal implementation plan for the selected feature using the target project's architecture, conventions, and verification tools.
---

# Plan implementation

Read and follow [the shared workflow](../../docs/workflow.md).

1. Resolve paths with `paths --require spec`. Verify the feature, then read its spec,
   quality checklist, constitution, relevant source, manifests, and existing tests.
   Stop for unresolved material requirements.
2. Run:
   ```sh
   python .specify/scripts/speckit.py --project . plan
   ```
   This seeds `plan.md` only if absent; an existing plan is preserved.
3. Fill the plan with repository findings, reused helpers, supported versions,
   source boundaries, interfaces, error behavior, data handling, compatibility,
   risks, and the smallest approach satisfying the spec. Justify new dependencies.
4. Define acceptance checks mapped to requirements: focused tests, relevant type
   checks/builds, and any required accessibility or performance verification.
   Record actual runnable commands and expected outcomes, not guessed tooling.
5. Resolve material technical decisions with the user. Check project governance before
   and after design. Create research, data-model, contract, or quickstart documents
   only when the feature needs them.
6. Present the plan, tradeoffs, blockers, and requested review checkpoints.
   Do not implement or generate tasks unless the user requested continuation.
