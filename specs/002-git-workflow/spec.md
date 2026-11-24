# Feature Specification: Safe Git Workflow Skills

**Created**: 2026-11-24
**Status**: Draft
**Input**: Add user-controlled Git workflow skills for feature branch creation, branch validation, remote detection, and commits.
**Branch**: `002-git-workflow` (feature documents are independent of this directory)

## User Scenarios & Testing

### US1 - Validate a feature branch against its specification (Priority: P1)

As a maintainer, I want to verify the current branch name and find its matching
specification directory so I can catch missing or mismatched feature documentation.

**Independent Test**: Run validation on a sequential branch and a timestamp branch,
each with and without a matching `specs/` directory, and inspect the reported result.

**Acceptance Scenarios**:

1. **Given** a branch named with a supported sequential or timestamp prefix, **When**
   validation runs, **Then** it reports the branch as valid and reports the matching
   `specs/<prefix>-*` directory when one exists.
2. **Given** a validly named branch with no matching spec directory, **When** validation
   runs, **Then** it warns that no matching directory was found without treating the
   specification and branch as coupled.
3. **Given** a branch that does not match either naming convention, **When** validation
   runs, **Then** it reports the branch as invalid and shows accepted naming examples.
4. **Given** Git or a Git repository is unavailable, **When** validation runs, **Then**
   it uses the documented `SPECIFY_FEATURE` fallback when set, otherwise warns that
   validation was skipped.

### US2 - Create a feature branch with user approval (Priority: P1)

As a maintainer, I want branch creation to respect the target repository's state and
my explicit choices so existing work is not lost or changed unexpectedly.

**Independent Test**: Review the proposed target branch, base, current worktree, and
branch name before execution; verify the skill stops when the extension is missing or
required remote-ref side effects have not been approved.

**Acceptance Scenarios**:

1. **Given** the user has not confirmed the repository, current branch, base commit,
   worktree state, and branch name, **When** branch creation is requested, **Then** the
   skill gathers and confirms those details before switching branches.
2. **Given** sequential branch numbering may fetch and prune remote-tracking refs,
   **When** that behavior is required, **Then** the skill discloses it and obtains
   approval before running the script.
3. **Given** the target project lacks the Git extension, **When** branch creation is
   requested, **Then** the skill asks before copying it and does not overwrite existing
   files.
4. **Given** a branch is created, **When** the skill reports completion, **Then** it
   reports the resulting branch and errors, and does not create a spec directory,
   commit, or push.

### US3 - Identify the origin remote without contacting it (Priority: P1)

As a maintainer, I want to know whether the configured origin is a GitHub repository
without exposing credentials or changing repository state.

**Independent Test**: Check absent, non-GitHub, HTTPS GitHub, and SSH GitHub origin
URLs; verify no remote contact or configuration change occurs.

**Acceptance Scenarios**:

1. **Given** origin is configured with a supported GitHub URL, **When** detection runs,
   **Then** it reports GitHub status and the verified owner and repository.
2. **Given** origin is absent, malformed, or does not point to `github.com`, **When**
   detection runs, **Then** it reports no verified GitHub repository and does not infer
   one from other context.
3. **Given** a remote URL contains credentials, **When** the result is reported, **Then**
   credentials are omitted.

### US4 - Commit only reviewed and explicitly approved changes (Priority: P1)

As a maintainer, I want to review the exact proposed commit and its file scope before
any changes are staged or committed.

**Independent Test**: Exercise the skill with staged, unstaged, and untracked changes;
verify it proposes the exact branch, files, message, and trailers and does not commit
without approval.

**Acceptance Scenarios**:

1. **Given** there are staged, unstaged, or untracked changes, **When** the skill is
   invoked, **Then** it inspects them and proposes the exact branch, files, message,
   and required trailers for approval.
2. **Given** commit automation is disabled or explicit approval is absent, **When**
   the skill or hook is considered, **Then** it does not stage or commit changes.
3. **Given** the configured script would stage all changes, **When** a commit is
   proposed, **Then** this behavior is disclosed and unrelated work is preserved.
4. **Given** an approved commit cannot be made with the approved message or required
   trailers, **When** the script cannot satisfy those constraints, **Then** the skill
   stops rather than substituting a different commit.
5. **Given** a commit has been made, **When** the user has not separately approved a
   push, **Then** no push occurs.

### US5 - Choose the feature branch before specification work (Priority: P1)

As a maintainer, I want to confirm whether new work belongs on the current branch or
needs a new feature branch before feature documents are created.

**Independent Test**: Invoke `specify` on `main` and on an existing feature branch;
verify it asks which branch should hold the work before initialization or
feature-specific analysis and follows the approved branch workflow before continuing
when a new branch is selected.

**Acceptance Scenarios**:

1. **Given** `specify` starts in a Git repository, **When** it inspects the target
   repository and current branch, **Then** it asks whether the work belongs on the
   current branch or needs a new one before project initialization or feature-specific
   analysis, regardless of the branch name.
2. **Given** the current branch is `main`, `master`, `develop`, `development`,
   `staging`, `production`, or matches `release/*`, **When** `specify` starts, **Then**
   it requires a new feature branch even if the user initially chooses to stay.
3. **Given** a branch name is not in the known shared-branch set and its status is
   unclear, **When** `specify` runs the preflight, **Then** it asks whether the branch
   is shared before allowing work to continue on it.
4. **Given** the user chooses a new branch or the current branch is shared, **When**
   `specify` continues, **Then** it asks for the required branch-creation details and
   approval, prepares managed Spec Kit tooling if needed, automatically invokes and
   follows `git-feature` in the same invocation, verifies the created branch, and only
   then begins feature-specific work.
5. **Given** the user confirms a non-shared current branch is intended, **When**
   `specify` continues, **Then** it does not switch branches and records the actual
   branch.
6. **Given** the user declines, a required confirmation is missing, or branch creation
   fails, **When** the preflight cannot complete, **Then** `specify` stops before
   feature-specific work or document writes.
7. **Given** Git or a Git repository is unavailable, **When** `specify` starts, **Then**
   it explains that branch creation cannot run and asks whether to proceed without it;
   it continues only if the user confirms.
8. **Given** `.specify/` is unmanaged or incompatible, **When** a new branch is needed
   before specification work, **Then** `specify` stops and reports the tooling conflict
   instead of copying the Git extension into that directory.

### Edge Cases

- The branch has a valid prefix but the corresponding feature directory uses a
  different name or is absent.
- Git is unavailable, the current directory is not a repository, or no origin remote
  is configured.
- The target project's extension is missing or has existing files that must not be
  overwritten.
- The worktree contains unrelated staged, unstaged, or untracked files.
- The configured commit message or required trailers cannot be produced as approved.

## Requirements

### Functional Requirements

- **FR-001**: The plugin provides `git-feature`, `git-validate`, `git-remote`, and
  `git-commit` skills that use the bundled Git extension against the confirmed target
  repository. `git-feature` can be directly invoked or used by the `specify` branch
  preflight; the other Git skills remain user-invoked.
- **FR-002**: Branch validation accepts sequential prefixes matching
  `^[0-9]{3,}-` and timestamp prefixes matching `^[0-9]{8}-[0-9]{6}-`. It reports a
  matching `specs/<prefix>-*` directory or warns when none exists; branch and spec
  directories remain independent.
- **FR-003**: Branch validation reports invalid names and accepted examples. When Git
  is unavailable or the directory is not a repository, it follows the documented
  `SPECIFY_FEATURE` fallback or reports that validation was skipped.
- **FR-004**: Before creating a branch, the skill confirms the target repository,
  current branch, base commit, worktree state, and branch name with the user, and
  preserves existing changes.
- **FR-005**: The branch-creation skill discloses and obtains approval for sequential
  numbering operations that fetch and prune remote-tracking refs. It does not create
  spec directories, commit, or push.
- **FR-006**: If the target project lacks the Git extension, branch-creation and
  commit workflows ask before copying bundled files and never overwrite existing
  files.
- **FR-007**: Remote detection examines the configured origin without contacting it or
  changing configuration. It reports a GitHub repository only when the URL is verified
  to point to `github.com`, and never exposes URL credentials.
- **FR-008**: Before any commit, the skill inspects staged, unstaged, and untracked
  changes and obtains explicit approval for the exact branch, file scope, message, and
  required trailers.
- **FR-009**: Commit automation is disabled by default. Because the upstream script can
  stage all changes, the skill discloses that effect and does not run it without
  explicit approval. It does not make empty commits, substitute unapproved messages,
  or push without separate approval.
- **FR-010**: The Git skills preserve unrelated work and do not stage, commit, push,
  change remotes, or execute extension hooks except as explicitly approved for the
  requested operation.
- **FR-011**: At the start of every Git-backed `specify` invocation, it confirms the
  target repository and current branch, then asks whether the feature belongs on the
  current branch or needs a new one. This occurs before project initialization or
  feature-specific analysis and clarification, and does not depend on branch naming.
- **FR-012**: When the user requests a new branch from `specify` or a new branch is
  required by the shared-branch rule, it asks for the branch-creation details and
  approval, then automatically invokes and follows the `git-feature` skill in the same
  invocation before any feature-specific work. It verifies the resulting branch and
  stops before feature-specific work if the workflow is declined, blocked, or fails.
- **FR-013**: If Git or a repository is unavailable during the `specify` branch
  preflight, it reports the limitation and asks whether to continue without branch
  creation; it continues only on confirmation and does not initialize Git or switch
  branches silently.
- **FR-014**: `specify` requires a new feature branch when the current branch is
  `main`, `master`, `develop`, `development`, `staging`, `production`, or matches
  `release/*`. For other ambiguous branch names, it asks whether the branch is shared;
  shared branches also require a new feature branch.
- **FR-015**: If a new branch is needed and Spec Kit tooling is missing, `specify`
  initializes managed tooling after the branch-choice prompt and before installing or
  running the Git extension. If `.specify/` is unmanaged or incompatible, it stops
  without mixing tooling. No feature-specific analysis or document writes occur until
  the new branch is verified.

### Nonfunctional Requirements

- The bundled Git scripts support Bash and PowerShell environments.
- Git operations must remain explicit and reviewable; unavailable Git or repository
  context must be reported rather than silently treated as success.
- Performance thresholds are not applicable to these interactive repository workflows.

### Key Entities

- **Feature branch**: A Git branch named with a sequential or timestamp prefix.
- **Feature directory**: A numbered directory under `specs/`; it can exist independently
  of a branch with the same prefix.
- **Origin remote**: The configured Git remote whose URL may identify a GitHub
  repository.
- **Commit proposal**: The approved branch, file scope, commit message, and trailers.

## Success Criteria

- **SC-001**: Validation correctly reports each supported branch-prefix form, invalid
  names, matching spec directories, missing-directory warnings, and the documented
  no-Git fallback in focused checks.
- **SC-002**: Branch creation does not switch branches before the target, branch,
  base, worktree, and name are confirmed; any required fetch/prune behavior is
  approved in advance.
- **SC-003**: Remote detection reports only evidence-backed GitHub identities for
  `github.com` URLs, omits credentials, and performs no network or configuration
  changes.
- **SC-004**: No commit is made before approval of its exact scope and message; the
  all-changes staging effect is disclosed, automation defaults off, and no push occurs
  without separate approval.
- **SC-005**: The Git skills preserve unrelated changes and report missing
  prerequisites or failures without success-shaped fallbacks.
- **SC-006**: On every Git-backed `specify` invocation, the user is asked to choose the
  current branch or a new branch before project initialization or feature-specific
  analysis. When a new branch is selected, the `git-feature` workflow completes and
  the resulting branch is verified before further feature work begins.
- **SC-007**: `specify` never continues feature work on the known shared branch names
  or a user-identified shared branch; it verifies a new feature branch first.

## Scope and Dependencies

**Included**: Four Git skills for branch creation, branch validation, origin detection,
and controlled commits; a `specify` branch preflight that can follow the `git-feature`
workflow in the same invocation; their bundled Git extension commands, configuration,
Bash/PowerShell scripts, and related plugin documentation.

**Excluded**: Automatically invoking extension hooks; creating specification
directories as part of branch creation; unapproved branch switching, staging,
committing, pushing, remote changes, deployment, or issue publication; changing
consumer-project Git policy.

**Dependencies**: Git for repository operations; the target project's
`.specify/extensions/git/` when running upstream branch or commit commands; managed
Spec Kit tooling when needed to install that extension; user approval for operations
that change branch or commit state.

## Clarifications

- 2026-11-24: The user confirmed the existing work is for Git skills and requested a
  matching `specs/` directory so `git-validate` can find it and pass.
- 2026-11-24: The user requested a recommended `git-feature`-before-`specify` workflow
  and a `specify` check that can create a new branch when the user requests one.
- 2026-11-24: The user confirmed the branch preflight should occur immediately after
  repository/current-branch detection and before feature analysis or clarification,
  on every Git-backed `specify` invocation, including existing feature branches.
- 2026-11-24: The user requires a new feature branch on shared branches, including the
  common names `main`, `master`, `develop`, `development`, `staging`, `production`,
  and `release/*`; ambiguous names must be checked with the user.
- 2026-11-24: If Git is unavailable, the user wants `specify` to ask whether to
  continue without branch creation and proceed only after confirmation.

## Assumptions

- The feature covers the four Git skills and bundled extension represented by the
  current `002-git-workflow` changes; no additional Git workflows are included.
- Feature directories remain independent of branch names; this directory matches the
  branch prefix to support the requested validation check.
- A new branch selected during `specify` follows the existing `git-feature` approval
  steps; running it in the same invocation does not waive branch, worktree, base, or
  fetch/prune confirmations.
- If initialization is needed, it occurs after the early branch decision but before
  invoking `git-feature`; this prerequisite setup does not include feature-specific
  analysis or spec creation.
