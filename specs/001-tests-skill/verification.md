# Verification: Tests Skill for Unit-Test Generation

**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Environment**: Linux; Python 3.11.13; plugin source checkout, not a newly loaded client installation.
**Date**: 2026-11-24

## Results

| Requirement / task | Command or procedure | Actual result | Status |
| --- | --- | --- | --- |
| FR-001, FR-002 / T001, T004 | Python metadata/resource assertions below | `Skill metadata and resource links passed` | Passed (static) |
| FR-001 through FR-012 / T001-T004 | Direct instruction review against the spec and plan matrix | All required instruction paths present; tests-only workflow exception and README are consistent | Passed (static) |
| T004 | Python Markdown link/whitespace check below, including untracked files | `Markdown links and whitespace passed (including untracked feature and skill files)` | Passed |
| Feature selection / T004 | `python .specify/scripts/speckit.py --project . paths --require spec plan tasks` | Resolved `specs/001-tests-skill/`; all three artifacts present | Passed |
| T004 | `git diff --check` | Exit 0, no whitespace findings | Passed |
| Compatibility / T004 | `git --no-pager diff --exit-code -- plugin.json scripts/speckit.py skills/implement/SKILL.md templates .specify` | Exit 0, no changes to these tracked resources | Passed |
| T002, T003 | `git --no-pager diff -- README.md docs/workflow.md` and direct new-skill read | Only the new invocation guidance, skill table entry, and scoped workflow exception were added | Passed (static) |
| Live client availability / T005 | `command -v copilot; command -v code; python --version` | Neither client executable found; Python 3.11.13 available | Blocked |
| SC-001 through SC-006 / T005 | Fresh-client live scenario matrix in tasks.md | No live cases run; packaging inspection does not establish behavior | Not run |

### Exact static Python check

Executed from the plugin repository root:

```sh
python - <<'PY'
from pathlib import Path
import re

skill = Path('skills/tests/SKILL.md')
text = skill.read_text(encoding='utf-8')
assert text.startswith('---\n')
header = text.split('---', 2)[1].splitlines()
assert 'name: tests' in header
assert any(line.startswith('description: ') and line[13:].strip() for line in header)
assert 'disable-model-invocation: true' in header
assert '../../docs/workflow.md' in text
assert (skill.parent / '../../docs/workflow.md').is_file()
assert 'skills/tests/SKILL.md' in Path('README.md').read_text(encoding='utf-8')
print('Skill metadata and resource links passed')
for path in [skill, Path('README.md'), Path('docs/workflow.md'), *Path('specs/001-tests-skill').rglob('*.md')]:
    content = path.read_text(encoding='utf-8')
    assert content.endswith('\n'), f'No final newline: {path}'
    for number, line in enumerate(content.splitlines(), 1):
        assert line.rstrip() == line, f'Trailing whitespace: {path}:{number}'
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
        if '://' not in target and not target.startswith('#'):
            assert (path.parent / target.split('#', 1)[0]).exists(), f'Broken link: {path}: {target}'
print('Markdown links and whitespace passed (including untracked feature and skill files)')
PY
```

### Static requirement mapping

- FR-001 / FR-002: Skill frontmatter and steps 1-2 define manual invocation, explicit
  path precedence, verified selection, and the visible-context confirmation gate.
- FR-003 / FR-004: Steps 2-3 and 5 handle unavailable artifacts and insufficient expected
  behavior without initialization or invented requirements.
- FR-005 / FR-006: Step 4 inspects existing and colocated tests and relevant
  multi-framework tooling; unsupported layout/runner choices prompt for clarification.
- FR-007: Steps 5 and 10 inventory relevant behavior and edge cases, reuse existing
  coverage, and report gaps without a line-coverage-only or exhaustive-testing claim.
- FR-008 / FR-012: Steps 6-7 and 10 plus the shared workflow exception restrict writes
  to test source and prohibit installation, configuration changes, and publication.
- FR-009 / FR-010: Steps 7-8 and 10 require focused runs, explicit blockers, test-only
  defect repair and reruns, and retention of genuine behavioral failures.
- FR-011: Step 9 requires evidence and uncertainty labels for potential bugs, missing
  exception handling, and dead code; lack of execution alone is not dead-code evidence.

## Remaining Work

T005 remains blocked and unchecked. Refresh/reinstall the canonical plugin in a compatible
client and use fresh isolated sessions to run every applicable scenario in the
[task matrix](tasks.md). None of these live cases have been verified:

- Explicit path with existing tests, including reuse and avoidance of duplicate coverage.
- Multiple test directories/frameworks and the correct feature-specific runner.
- Default selected feature and invalid/ambiguous/unavailable input handling.
- Older implementation with incomplete artifacts and undocumented outcomes.
- No test directory with documented tooling, and no inferable tooling.
- Passing focused run, faulty-test repair/rerun, and genuine implementation failure.
- Evidence-backed production/exception/dead-code findings.
- Missing runner/dependency reporting without installation.
- Visible same-session implementation warning/confirmation.
- Test-source-only worktree changes and preservation of unrelated files in each live run.

No framework, runtime, type-check, build, accessibility, or performance tooling was added.
No live VS Code installation or end-to-end agent behavior is claimed. Static checks
are sufficient for T004 only, not for SC-001 through SC-006 live acceptance.

## Feedback and Review

The user invoked implementation after read-only consistency analysis. The two
verification findings were addressed without changing product behavior: T005 now requires
all applicable matrix cases to pass, and the plan/tasks include an explicit
multi-framework case. Requirements and user decisions remain unchanged.
No commits, pushes, deployment, publication, installed-cache edits, or new agent sessions
were performed.
