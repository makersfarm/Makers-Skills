#!/usr/bin/env python3
"""Validate skill metadata and repository trust signals."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SKILLS_JSON = ROOT / "skills.json"
README = ROOT / "README.md"
LLMS_INSTALL = ROOT / "llms.install.md"


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked = 0

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self) -> None:
        self.checked += 1


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing YAML frontmatter block"

    frontmatter: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return frontmatter, None
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return frontmatter, f"invalid frontmatter line {line_number}: expected 'key: value'"
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = unquote(value)

    return frontmatter, "unterminated YAML frontmatter block"


def skill_dirs() -> list[Path]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())


def validate_skill_files(reporter: Reporter) -> dict[str, dict[str, str]]:
    skills: dict[str, dict[str, str]] = {}

    if not SKILLS_DIR.exists():
        reporter.error("skills/ directory is missing")
        return skills

    for skill_dir in skill_dirs():
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"

        if not skill_md.exists():
            reporter.error(f"{rel(skill_md)} is missing")
            continue

        frontmatter, parse_error = parse_frontmatter(skill_md)
        if parse_error:
            reporter.error(f"{rel(skill_md)}: {parse_error}")
            continue

        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()

        if not name:
            reporter.error(f"{rel(skill_md)}: frontmatter is missing 'name'")
        elif name != skill_name:
            reporter.error(
                f"{rel(skill_md)}: frontmatter name '{name}' must match folder '{skill_name}'"
            )

        if not description:
            reporter.error(f"{rel(skill_md)}: frontmatter is missing 'description'")

        if not readme.exists():
            reporter.warn(f"{rel(skill_dir)} has no README.md")

        if name and description and name == skill_name:
            skills[skill_name] = {
                "name": name,
                "path": f"skills/{skill_name}",
                "skill_md": rel(skill_md),
            }
            reporter.ok()

    return skills


def load_skills_json(reporter: Reporter) -> object | None:
    if not SKILLS_JSON.exists():
        return None

    try:
        with SKILLS_JSON.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        reporter.error(f"{rel(SKILLS_JSON)} is not valid JSON: {exc}")
    return None


def records_from_skills_json(data: object, reporter: Reporter) -> list[dict[str, object]]:
    if data is None:
        return []

    if isinstance(data, list):
        return [record for record in data if isinstance(record, dict)]

    if isinstance(data, dict):
        skills = data.get("skills")
        if isinstance(skills, list):
            return [record for record in skills if isinstance(record, dict)]
        if isinstance(skills, dict):
            records = []
            for name, value in skills.items():
                if isinstance(value, dict):
                    record = dict(value)
                    record.setdefault("name", name)
                    records.append(record)
                else:
                    reporter.error(f"{rel(SKILLS_JSON)}: skill '{name}' must be an object")
            return records

    reporter.error(f"{rel(SKILLS_JSON)} must be a list or contain a 'skills' list/object")
    return []


def first_string(record: dict[str, object], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str):
            return value.strip()
    return ""


def normalize_skill_path(path_value: str) -> str:
    cleaned = path_value.replace("\\", "/").strip("/")
    if cleaned.endswith("/SKILL.md"):
        cleaned = cleaned[: -len("/SKILL.md")]
    return cleaned


def valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and bool(parsed.path.strip("/"))


def looks_like_raw_url(value: str) -> bool:
    parsed = urlparse(value)
    return valid_https_url(value) and (
        parsed.netloc == "raw.githubusercontent.com" or "/raw/" in parsed.path
    )


def looks_like_source_url(value: str) -> bool:
    parsed = urlparse(value)
    return valid_https_url(value) and parsed.netloc in {
        "github.com",
        "www.github.com",
    }


def validate_skills_json(reporter: Reporter, discovered: dict[str, dict[str, str]]) -> None:
    data = load_skills_json(reporter)
    if data is None:
        return

    records = records_from_skills_json(data, reporter)
    seen: set[str] = set()

    for index, record in enumerate(records, start=1):
        name = first_string(record, ("name", "id", "slug"))
        path_value = first_string(record, ("path", "skillPath", "skill_path", "directory", "dir"))
        label = name or f"record #{index}"

        if not name:
            reporter.error(f"{rel(SKILLS_JSON)}: record #{index} is missing name")
            continue
        if name not in discovered:
            reporter.error(f"{rel(SKILLS_JSON)}: '{name}' does not match a skills/* folder")
        else:
            seen.add(name)

        if not path_value:
            reporter.error(f"{rel(SKILLS_JSON)}: '{label}' is missing path")
        else:
            normalized = normalize_skill_path(path_value)
            expected = f"skills/{name}"
            if normalized != expected:
                reporter.error(
                    f"{rel(SKILLS_JSON)}: '{label}' path '{path_value}' must be '{expected}'"
                )

        raw_url = first_string(record, ("raw_url", "rawUrl", "raw", "rawURL"))
        source_url = first_string(record, ("source_url", "sourceUrl", "source", "url", "homepage"))

        if raw_url and not looks_like_raw_url(raw_url):
            reporter.error(f"{rel(SKILLS_JSON)}: '{label}' raw URL has an invalid shape")
        if source_url and not looks_like_source_url(source_url):
            reporter.error(f"{rel(SKILLS_JSON)}: '{label}' source URL has an invalid shape")

        reporter.ok()

    missing = sorted(set(discovered) - seen)
    for name in missing:
        reporter.error(f"{rel(SKILLS_JSON)}: missing entry for skill '{name}'")


def validate_readme_install_link(reporter: Reporter) -> None:
    if not LLMS_INSTALL.exists():
        return

    if not README.exists():
        reporter.error(f"{rel(README)} is missing but {rel(LLMS_INSTALL)} exists")
        return

    text = README.read_text(encoding="utf-8", errors="replace")
    if "llms.install.md" not in text:
        reporter.error(f"{rel(README)} must link to {rel(LLMS_INSTALL)}")
    else:
        reporter.ok()


def shell_scripts() -> list[Path]:
    candidates = []
    for pattern in ("*.sh", "*.bash"):
        candidates.extend(ROOT.rglob(pattern))
    return sorted(path for path in candidates if ".git" not in path.parts)


def find_bash() -> str | None:
    env_bash = os.environ.get("BASH")
    if env_bash and Path(env_bash).exists():
        return env_bash
    return shutil.which("bash")


def validate_shell_scripts_parse(reporter: Reporter) -> None:
    scripts = shell_scripts()
    if not scripts:
        return

    bash = find_bash()
    if not bash:
        reporter.warn("Bash is not available; skipped shell script syntax checks")
        return

    for script in scripts:
        result = subprocess.run(
            [bash, "-n", str(script)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip().splitlines()
            suffix = f": {details[0]}" if details else ""
            reporter.error(f"{rel(script)} failed shell syntax parse{suffix}")
        else:
            reporter.ok()


def print_summary(reporter: Reporter, discovered: dict[str, dict[str, str]]) -> None:
    print("Skill validation summary")
    print(f"- Repository: {ROOT}")
    print(f"- Skills discovered: {len(discovered)}")
    print(f"- Checks passed: {reporter.checked}")
    print(f"- Warnings: {len(reporter.warnings)}")
    print(f"- Errors: {len(reporter.errors)}")

    if reporter.warnings:
        print("\nWarnings:")
        for warning in reporter.warnings:
            print(f"  - {warning}")

    if reporter.errors:
        print("\nErrors:")
        for error in reporter.errors:
            print(f"  - {error}")
    else:
        print("\nResult: PASS")


def main() -> int:
    reporter = Reporter()
    discovered = validate_skill_files(reporter)
    validate_skills_json(reporter, discovered)
    validate_readme_install_link(reporter)
    validate_shell_scripts_parse(reporter)
    print_summary(reporter, discovered)
    return 1 if reporter.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
