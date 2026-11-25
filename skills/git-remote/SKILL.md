---
name: git-remote
description: Detect the origin remote and identify GitHub repositories without contacting the remote.
disable-model-invocation: true
---

# Detect a Git remote

Confirm the target repository, then follow the upstream
[remote command](../../.specify/extensions/git/commands/speckit.git.remote.md)
against that repository. Report whether origin is configured and whether it is GitHub;
report the owner and repository only when verified. Do not expose credentials in a
remote URL. Detection does not fetch, push, or change configuration. A push requires
separate explicit approval of the remote and branch.
