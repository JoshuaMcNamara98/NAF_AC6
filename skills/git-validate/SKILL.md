---
name: git-validate
description: Validate the current Git feature branch and find matching specification directories.
disable-model-invocation: true
---

# Validate a Git feature branch

Confirm the target repository, then follow the upstream
[validation command](../../.specify/extensions/git/commands/speckit.git.validate.md)
against that repository. Report the branch and matching spec directories. An absent
spec directory is a warning; feature directories can be independent of branch names.
This skill does not stage, commit, or contact a remote.
