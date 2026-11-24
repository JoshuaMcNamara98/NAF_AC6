---
name: checklist
description: Review software feature requirements for completeness, clarity, and testability in a user-selected area.
---

# Check requirements quality

Read and follow [the shared workflow](../../docs/workflow.md).

1. Run `paths --require spec`, verify the feature, and read its spec and available plan.
2. Identify the requested focus, such as API contracts, accessibility, compatibility,
   privacy, or reliability. Ask if the intended audience or review depth materially
   changes the checklist.
3. Create a descriptively named checklist under the selected feature's `checklists/`,
   starting from `.specify/templates/checklist-template.md`. Preserve existing checklists.
4. Write concise questions about requirement quality, with stable IDs and references
   to affected requirements. Include relevant edge cases, ambiguity, and consistency.
   Do not substitute implementation tests or claim that code has passed.
5. Record evidence for resolved items and remaining gaps; report the checklist and blockers.
