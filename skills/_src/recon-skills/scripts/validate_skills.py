#!/usr/bin/env python3
"""Validate structural and portability rules for the skill catalog."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = (
    "When to Use",
    "Prerequisites",
    "How to Run",
    "Procedure",
    "Pitfalls",
    "Verification",
)
FORBIDDEN_RUNTIME_PATTERNS = {
    "Hermes runtime": re.compile(r"\bHermes\b", re.IGNORECASE),
    "Hermes data path": re.compile(r"(?:/opt/data|\.hermes/)"),
    "runtime delegation API": re.compile(r"\bdelegate_task\b"),
    "removed orchestration skill": re.compile(r"\bparallel-recon-triad\b"),
    "private runtime address": re.compile(r"\b172\.20\.0\.\d+\b"),
    "runtime security bypass": re.compile(r"\bTirith\b", re.IGNORECASE),
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "private output path": re.compile(
        r"(?:/root/output|\$OUTDIR/recon_output)", re.IGNORECASE
    ),
    "campaign result section": re.compile(
        r"^## Real Production (?:Results|Example)\s*$", re.MULTILINE
    ),
    "runtime-specific write workaround": re.compile(
        r"\bwrite_file blocked\b", re.IGNORECASE
    ),
    "legacy engagement placeholder": re.compile(
        r"\[(?:RETAILER|MATTRESS_RETAILER|REAL_ESTATE|WINE_STORE|"
        r"RETAIL_CHAIN|ENTERTAINMENT|GOV_PORTAL|DELIVERY_PLATFORM)\]"
    ),
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Skill:
    path: Path
    name: str
    related: tuple[str, ...]
    text: str


def parse_frontmatter(path: Path) -> tuple[dict[str, str], tuple[str, ...], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter delimiter") from exc

    values: dict[str, str] = {}
    related: list[str] = []
    in_related = False

    for line in lines[1:end]:
        inline_related = re.match(r"^\s+related_skills:\s*\[(.*)\]\s*$", line)
        if inline_related:
            related.extend(
                item.strip().strip("\"'")
                for item in inline_related.group(1).split(",")
                if item.strip()
            )
            in_related = False
            continue
        if re.match(r"^\s+related_skills:\s*$", line):
            in_related = True
            continue
        if in_related:
            item = re.match(r"^\s+-\s+([a-zA-Z0-9_-]+)\s*$", line)
            if item:
                related.append(item.group(1))
                continue
            if line.strip():
                in_related = False

        item = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*?)\s*$", line)
        if item:
            values[item.group(1)] = item.group(2).strip("\"'")

    return values, tuple(related), text


def local_markdown_links(path: Path, text: str) -> list[Path]:
    links: list[Path] = []
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        if not (
            target.startswith(("./", "../"))
            or re.fullmatch(r"[A-Za-z0-9_./-]+\.(?:md|py|sh|js|ya?ml|json)", target)
        ):
            continue
        links.append((path.parent / target).resolve())
    return links


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skills: list[Skill] = []

    paths = sorted(ROOT.glob("**/SKILL.md"))
    if not paths:
        errors.append("catalog: no SKILL.md files found")

    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            values, related, text = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        name = values.get("name", "")
        if not name:
            errors.append(f"{rel}: missing frontmatter name")
        elif not NAME_PATTERN.fullmatch(name):
            errors.append(f"{rel}: invalid skill name {name!r}")

        if not values.get("description"):
            errors.append(f"{rel}: missing frontmatter field description")
        for field in ("version", "license", "platforms"):
            if not values.get(field):
                warnings.append(f"{rel}: missing recommended frontmatter field {field}")

        skills.append(Skill(path=path, name=name, related=related, text=text))

        for section in REQUIRED_SECTIONS:
            if not re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE):
                warnings.append(f"{rel}: missing section {section!r}")

        for label, pattern in FORBIDDEN_RUNTIME_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{rel}: contains {label}")

        for target in local_markdown_links(path, text):
            if not target.exists():
                errors.append(
                    f"{rel}: broken local Markdown link "
                    f"{target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}"
                )

    by_name: dict[str, list[Path]] = {}
    for skill in skills:
        by_name.setdefault(skill.name, []).append(skill.path)
    for name, duplicates in sorted(by_name.items()):
        if name and len(duplicates) > 1:
            joined = ", ".join(str(path.relative_to(ROOT)) for path in duplicates)
            errors.append(f"duplicate skill name {name!r}: {joined}")

    names = set(by_name)
    for skill in skills:
        for related in skill.related:
            if related not in names:
                errors.append(
                    f"{skill.path.relative_to(ROOT)}: unknown related skill {related!r}"
                )

    for root_doc in ("README.md", "AGENTS.md", "SOUL.md"):
        path = ROOT / root_doc
        if not path.exists():
            errors.append(f"{root_doc}: missing root document")
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_RUNTIME_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{root_doc}: contains {label}")

    for path in sorted(ROOT.glob("**/*.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{rel}: contains {label}")

    print(f"Validated {len(skills)} skills.")
    if warnings:
        shown = warnings if "--verbose" in sys.argv else warnings[:20]
        print(f"\nWarnings ({len(warnings)}, showing {len(shown)}):")
        for warning in shown:
            print(f"  WARN  {warning}")
        if len(shown) < len(warnings):
            print("  ... run with --verbose to show every warning")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  ERROR {error}")
        return 1

    print(f"\nNo structural errors. Style warnings: {len(warnings)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
