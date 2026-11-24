#!/usr/bin/env python3
"""Project-local feature scaffolding for the bundled Spec Kit skills."""

import argparse
import json
import re
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    print("ERROR: Spec Kit tooling requires Python 3.10 or newer.", file=sys.stderr)
    raise SystemExit(1)

PLUGIN_NAME = "speckit"
VERSION = "0.1.0"
TEMPLATES = (
    "constitution",
    "spec",
    "plan",
    "tasks",
    "checklist",
    "verification",
)


class WorkflowError(Exception):
    """An invalid project, installation, or workflow prerequisite."""


def safe_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise WorkflowError(f"Path must stay inside the project: {value}") from exc
    if ".." in relative.parts:
        raise WorkflowError(f"Parent traversal is not allowed: {value}")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise WorkflowError(f"Symlinked workflow paths are not allowed: {current}")
    return candidate


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot read JSON at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"Expected a JSON object at {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def require_installation(root: Path) -> None:
    metadata = safe_path(root, ".specify/speckit-plugin.json")
    if not metadata.is_file():
        raise WorkflowError("Project tooling is not initialized. Run the plugin's init skill first.")
    value = read_json(metadata)
    if value.get("name") != PLUGIN_NAME or value.get("version") != VERSION:
        raise WorkflowError(
            f"Incompatible project tooling at {metadata}; expected {PLUGIN_NAME} {VERSION}. "
            "Review a migration before replacing any project files."
        )


def template_text(base: Path, name: str) -> str:
    path = safe_path(base, f"templates/{name}-template.md")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise WorkflowError(f"Template is empty: {path}")
    return text


def initialize(root: Path) -> dict:
    specify = safe_path(root, ".specify")
    if specify.exists():
        require_installation(root)

    source = Path(__file__).resolve()
    base = source.parent.parent
    resources = {
        ".specify/.gitignore": b"# Per-checkout active feature selection\nfeature.json\n",
        ".specify/scripts/speckit.py": source.read_bytes(),
        **{
            f".specify/templates/{name}-template.md": template_text(base, name).encode("utf-8")
            for name in TEMPLATES
        },
        ".specify/memory/constitution.md": template_text(base, "constitution").encode("utf-8"),
    }
    destinations = {name: safe_path(root, name) for name in resources}
    metadata = safe_path(root, ".specify/speckit-plugin.json")
    for name, destination in destinations.items():
        if destination.exists() and not destination.is_file():
            raise WorkflowError(f"Expected a file, refusing initialization: {destination}")
        if name.endswith("/scripts/speckit.py") and destination.exists():
            if destination.read_bytes() != resources[name]:
                raise WorkflowError(
                    f"Installed runtime differs from this plugin: {destination}. "
                    "Review a migration; no files were overwritten."
                )
        for parent in destination.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise WorkflowError(f"Expected a directory: {parent}")

    created = []
    preserved = []
    for name, destination in destinations.items():
        if destination.exists():
            preserved.append(name)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(resources[name])
            created.append(name)
    if not metadata.exists():
        with metadata.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps({"name": PLUGIN_NAME, "version": VERSION}, indent=2) + "\n")
        created.append(metadata.relative_to(root).as_posix())
    return {"PROJECT": str(root), "VERSION": VERSION, "CREATED": created, "PRESERVED": preserved}


def feature_path(root: Path, value: str) -> Path:
    path = safe_path(root, value)
    if any(part.casefold() == ".git" for part in path.relative_to(root).parts):
        raise WorkflowError("Feature directories must not be inside Git metadata.")
    if path == root or path.is_relative_to(root / ".specify"):
        raise WorkflowError("A feature directory must be separate from the project root and .specify.")
    return path


def selected_feature(root: Path) -> Path:
    state = safe_path(root, ".specify/feature.json")
    if not state.is_file():
        raise WorkflowError("No selected feature. Run create or select first.")
    value = read_json(state).get("feature_directory")
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError(f"Missing nonempty feature_directory at {state}")
    return feature_path(root, value)


def select_feature(root: Path, feature: Path) -> None:
    state = safe_path(root, ".specify/feature.json")
    if state.exists() and not state.is_file():
        raise WorkflowError(f"Expected a selection file: {state}")
    write_json(state, {"feature_directory": feature.relative_to(root).as_posix()})


def feature_paths(root: Path, feature: Path, required: list[str]) -> dict:
    result = {
        "PROJECT": str(root),
        "FEATURE_DIR": str(feature),
        "FEATURE_SPEC": str(safe_path(root, str(feature / "spec.md"))),
        "IMPL_PLAN": str(safe_path(root, str(feature / "plan.md"))),
        "TASKS": str(safe_path(root, str(feature / "tasks.md"))),
    }
    if not feature.is_dir():
        raise WorkflowError(f"Selected feature directory does not exist: {feature}")
    for name in dict.fromkeys(["spec", *required]):
        path = safe_path(root, str(feature / f"{name}.md"))
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise WorkflowError(f"Required {name}.md is missing or empty: {path}")
    return result


def create_feature(root: Path, name: str, description: str, directory: str | None) -> dict:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 80:
        raise WorkflowError("Feature name must be 1-80 lowercase letters/digits separated by hyphens.")
    if not description.strip():
        raise WorkflowError("Feature description must not be empty.")
    state = safe_path(root, ".specify/feature.json")
    if state.exists():
        selected_feature(root)
    text = template_text(root / ".specify", "spec")
    if directory:
        feature = feature_path(root, directory)
    else:
        specs = safe_path(root, "specs")
        numbers = []
        if specs.exists():
            if not specs.is_dir():
                raise WorkflowError(f"Expected a specs directory: {specs}")
            for entry in specs.iterdir():
                match = re.match(r"^(\d{3,})-", entry.name)
                if match:
                    numbers.append(int(match.group(1)))
        feature = feature_path(root, f"specs/{max(numbers, default=0) + 1:03d}-{name}")
    if feature.exists():
        raise WorkflowError(f"Feature path already exists; use select to revise it: {feature}")
    spec = safe_path(root, str(feature / "spec.md"))
    feature.mkdir(parents=True, exist_ok=False)
    with spec.open("x", encoding="utf-8") as stream:
        stream.write(text)
    with (feature / "request.md").open("x", encoding="utf-8") as stream:
        stream.write("# Feature Request\n\n" + description.strip() + "\n")
    select_feature(root, feature)
    return feature_paths(root, feature, ["spec"])


def seed_artifact(root: Path, kind: str) -> dict:
    feature = selected_feature(root)
    result = feature_paths(root, feature, ["spec", "plan"] if kind == "tasks" else ["spec"])
    destination = safe_path(root, str(feature / f"{kind}.md"))
    if destination.exists():
        if not destination.is_file() or not destination.read_text(encoding="utf-8").strip():
            raise WorkflowError(f"Existing artifact is not a nonempty file: {destination}")
        result["CREATED"] = False
    else:
        text = template_text(root / ".specify", kind)
        with destination.open("x", encoding="utf-8") as stream:
            stream.write(text)
        result["CREATED"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Explicit existing target project root")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Install missing project resources without overwriting")
    create = commands.add_parser("create", help="Create and select one feature, without Git operations")
    create.add_argument("--name", required=True)
    create.add_argument("--description", required=True)
    create.add_argument("--feature", help="Optional project-contained feature directory")
    select = commands.add_parser("select", help="Explicitly select an existing feature")
    select.add_argument("--feature", required=True)
    paths = commands.add_parser("paths", help="Resolve and validate the selected feature")
    paths.add_argument("--require", nargs="+", choices=["spec", "plan", "tasks"], default=[])
    commands.add_parser("plan", help="Seed plan.md only when absent; requires spec.md")
    commands.add_parser("tasks", help="Seed tasks.md only when absent; requires spec.md and plan.md")
    args = parser.parse_args(argv)

    try:
        root = Path(args.project).resolve(strict=True)
        if not root.is_dir():
            raise WorkflowError(f"Project is not a directory: {root}")
        if args.command == "init":
            result = initialize(root)
        else:
            require_installation(root)
            if args.command == "create":
                result = create_feature(root, args.name, args.description, args.feature)
            elif args.command == "select":
                feature = feature_path(root, args.feature)
                result = feature_paths(root, feature, ["spec"])
                select_feature(root, feature)
            elif args.command == "paths":
                result = feature_paths(root, selected_feature(root), args.require)
            else:
                result = seed_artifact(root, args.command)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (WorkflowError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
