---
name: init
description: Initialize safe, project-local Spec Kit tooling and templates before running the software feature workflow.
---

# Initialize a project

Read and follow [the shared workflow](../../docs/workflow.md).

1. Confirm the target repository root. Verify a Python 3.10+ executable. Inspect existing
   `.specify/` and project instructions. Do not assume the target is the plugin checkout.
2. Explain that initialization adds project-local tooling, editable templates, and a
   baseline constitution without modifying source, Git state, or agent instructions.
3. Locate the [bundled CLI](../../scripts/speckit.py) relative to this skill's installed
   file. Resolve its actual absolute path and run it with the verified interpreter:
   ```sh
   python "<absolute-plugin-path>/scripts/speckit.py" --project "<target-root>" init
   ```
   Angle-bracket paths are placeholders; substitute confirmed paths, never execute them
   literally. Do not depend on plugin-root environment expansion in Markdown.
4. Check the JSON result. An exact reinstall preserves existing files. An unmanaged
   `.specify/`, different tooling version, or conflicting packaged file fails explicitly.
   Report the conflict; propose a reviewed migration rather than overwriting it.
5. Report created and preserved files. Recommend tailoring the project constitution.
   Resume the requested stage if initialization was its prerequisite.
