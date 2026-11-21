"""Render templates into a target directory.

The public API is intentionally tiny:

    plan(cfg, out)                 -> list[FilePlan]
    generate(cfg, out, force=...)  -> GenerateResult

`plan()` never touches the filesystem, which makes conflict handling easy to
test and lets the CLI show a preview before any destructive write.
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .templates import LICENSE_TEXTS, TEMPLATES

_PLACEHOLDER_RE = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")

# Files that are only emitted when the matching feature flag is enabled.
_COMMUNITY_FILES = {
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/CODEOWNERS",
}
_CI_FILES = {".github/workflows/ci.yml"}
_AI_FILES = {"AI_LOG.md", "docs/AAR.md"}
_LICENSE_FILES = {"LICENSE"}


@dataclass
class FilePlan:
    """One intended filesystem write."""

    path: Path
    content: str
    action: str  # "create" | "skip" | "overwrite"
    executable: bool = False

    @property
    def relative(self) -> str:
        return self.path.name if self.path.parent == Path(".") else str(self.path)


@dataclass
class GenerateResult:
    """Summary of a completed generation run."""

    output_dir: Path
    created: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    overwritten: List[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.created) + len(self.skipped) + len(self.overwritten)

    def as_text(self) -> str:
        lines = [
            "✔ 配置校验 .................... OK",
            "✔ 生成文件 .................... %d 个（新建 %d / 跳过 %d / 覆盖 %d）"
            % (self.total, len(self.created), len(self.skipped), len(self.overwritten)),
            "✔ 无未替换占位符 .............. OK",
            "✔ 输出目录 .................... %s" % self.output_dir,
        ]
        return "\n".join(lines)


def build_context(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Derive all values referenced by templates from a validated config."""
    ctx: Dict[str, Any] = dict(cfg)
    ctx["keywords_csv"] = ", ".join('"%s"' % k for k in cfg.get("keywords", []))
    ctx["features_bullets"] = "\n".join(
        "- %s" % f for f in cfg.get("features", [])
    ) or "- 零依赖、开箱即用"
    ctx["python_version_compact"] = cfg.get("python_version", "3.9").replace(".", "")[:2]
    ctx["date"] = _dt.date.today().isoformat()
    ctx["license_badge"] = cfg.get("license", "MIT")
    return ctx


def render(text: str, context: Dict[str, Any], max_passes: int = 3) -> str:
    """Replace ``{{KEY}}`` tokens. Unknown keys are left intact on purpose.

    Rendering is iterative because a config value may itself contain a
    placeholder (e.g. the default ``problem_statement`` embeds ``{{name}}``).
    A small fixed number of passes avoids infinite recursion on cyclic refs.
    """

    def _sub(match: re.Match[str]) -> str:
        key = match.group(1)
        value = context.get(key, match.group(0))
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    for _ in range(max_passes):
        rendered = _PLACEHOLDER_RE.sub(_sub, text)
        if rendered == text:
            break
        text = rendered
    return text


def unresolved_placeholders(text: str) -> List[str]:
    """Return sorted unique placeholder names still present in *text*."""
    return sorted(set(_PLACEHOLDER_RE.findall(text)))


def _selected_templates(cfg: Dict[str, Any]) -> Iterable[tuple[str, str]]:
    for key, body in TEMPLATES.items():
        if key in _LICENSE_FILES and not cfg.get("license_file"):
            continue
        if key in _COMMUNITY_FILES and not cfg.get("community", True):
            continue
        if key in _CI_FILES and not cfg.get("ci", True):
            continue
        if key in _AI_FILES and not cfg.get("ai_assisted", True):
            continue
        # examples/basic.json is a demo of *this* tool, but the generated repo
        # should carry its own minimal example instead of a copy of ours.
        if key == "examples/basic.json":
            continue
        yield key, body


def _license_text(cfg: Dict[str, Any]) -> str | None:
    name = cfg.get("license")
    return LICENSE_TEXTS.get(name) if name else None


def plan(cfg: Dict[str, Any], output_dir: str | Path, force: bool = False) -> List[FilePlan]:
    """Compute the write plan without touching the filesystem."""
    ctx = build_context(cfg)
    out = Path(output_dir).expanduser()
    plans: List[FilePlan] = []

    for key, body in _selected_templates(cfg):
        rendered_key = render(key, ctx)
        target = out / rendered_key
        content = render(body, ctx)
        if target.exists():
            action = "overwrite" if force else "skip"
        else:
            action = "create"
        plans.append(
            FilePlan(
                path=Path(rendered_key),
                content=content,
                action=action,
                executable=rendered_key == "repo-forge",
            )
        )

    license_body = _license_text(cfg)
    if license_body and cfg.get("license_file"):
        target_key = str(cfg["license_file"])
        target = out / target_key
        plans.append(
            FilePlan(
                path=Path(target_key),
                content=render(license_body, ctx),
                action=("overwrite" if force else "skip") if target.exists() else "create",
            )
        )

    return plans


def generate(
    cfg: Dict[str, Any],
    output_dir: str | Path,
    force: bool = False,
    *,
    strict: bool = True,
) -> GenerateResult:
    """Render all selected templates into *output_dir*.

    Args:
        cfg: a **validated** config dict (see :func:`validate_config`).
        output_dir: destination directory (created if missing).
        force: overwrite existing files. Without it, existing files are kept.
        strict: if True, refuse to write when a template still has unresolved
            placeholders. This is the guard that caught the historical
            ``python_version_compact`` bug.

    Returns:
        GenerateResult with per-file actions.
    """
    out = Path(output_dir).expanduser()
    file_plans = plan(cfg, out, force=force)

    if strict:
        bad: Dict[str, List[str]] = {}
        for item in file_plans:
            missing = unresolved_placeholders(item.content)
            if missing:
                bad[str(item.path)] = missing
        if bad:
            detail = "; ".join(
                "%s -> %s" % (p, ", ".join(keys)) for p, keys in sorted(bad.items())
            )
            raise ValueError("模板存在未替换占位符: " + detail)

    out.mkdir(parents=True, exist_ok=True)
    result = GenerateResult(output_dir=out)

    for item in file_plans:
        target = out / item.path
        if item.action == "skip":
            result.skipped.append(str(item.path))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8")
        if item.executable:
            target.chmod(0o755)
        if item.action == "overwrite":
            result.overwritten.append(str(item.path))
        else:
            result.created.append(str(item.path))

    return result
