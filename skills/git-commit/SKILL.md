---
name: git-commit
description: Review and commit explicitly approved changes using the upstream Git extension.
disable-model-invocation: true
---

# Commit approved changes

Confirm the target repository and inspect its Git status, staged and unstaged diffs,
and untracked files without exposing secrets. Propose the exact branch, files, commit
message, and required trailers; ask for explicit approval before each commit.

The upstream [commit command](../../.specify/extensions/git/commands/speckit.git.commit.md)
uses the target project's `.specify/extensions/git/` scripts and configuration. If
the extension is missing, stop and ask before copying the bundled extension into the
target project; do not overwrite existing files.

The upstream script stages **all** changes and commits them when enabled for the
event. It is disabled by default. Explain this behavior and do not run it unless all
changes, the configured message, and the event are explicitly approved. Preserve
unrelated work and do not enable automatic commits without approval. If the script
cannot produce an approved message or required trailers, stop rather than making a
different commit. Do not create an empty commit or push without separate approval.
