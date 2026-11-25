---
name: git-feature
description: Create a numbered Git feature branch after confirming its name and base.
---

# Create a Git feature branch

Confirm the target repository, current branch, base commit, worktree state, and
branch name with the user before switching. Preserve existing changes.

The bundled creation script creates the new branch from the current `HEAD` and has no
separate base option. Verify that `HEAD` is the user-approved base before running it.
If not, obtain approval to move to the intended base and recheck the worktree first.

Use the target project's `.specify/extensions/git/commands/speckit.git.feature.md`
and its accompanying platform script. If the extension is missing, stop and ask
before copying the bundled extension into the target project; do not overwrite
existing files. The bundled extension is located at
[../../.specify/extensions/git/](../../.specify/extensions/git/).

The upstream sequential-numbering script can fetch and prune remote-tracking refs;
disclose and obtain approval for those effects before running it. For an explicitly
approved exact name, use the upstream `GIT_BRANCH_NAME` override. Report the resulting
branch and errors. Do not create a spec directory, commit, or push without approval.
