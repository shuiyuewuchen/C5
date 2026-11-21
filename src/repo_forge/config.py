"""Config loading, schema defaults and validation.

Design goal: fail loudly and clearly on bad input.  A generator that silently
accepts a malformed config produces a broken repository, which is the exact
failure mode C5 warns about ("someone clones it and cannot run it").
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from .utils import as_bool, current_year, display_name, package_name, slugify

SUPPORTED_LICENSES = ("MIT", "Apache-2.0", "BSD-3-Clause", "Unlicense", "None")
SUPPORTED_LANGUAGES = (
    "Python", "TypeScript", "JavaScript", "Go", "Rust", "Java",
    "Shell", "Documentation", "PromptSet",
)

DEFAULT_CONFIG: Dict[str, Any] = {
    "name": None,
    "description": None,
    "owner": "your-github-id",
    "author": None,
    "language": "Python",
    "python_version": "3.9",
    "license": "MIT",
    "keywords": [],
    "install": None,
    "usage": None,
    "ci": True,
    "community": True,
    "ai_assisted": True,
    "year": None,
    "input_hint": None,
    "output_hint": None,
    "problem_statement": None,
}

_PY_VERSION_RE = re.compile(r"^3\.(8|9|10|11|12|13)(\.\d+)?$")


class ConfigError(ValueError):
    """Raised when a config file is unreadable, malformed or invalid."""


def _read_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on optional dep
        raise ConfigError(
            "Reading .yaml/.yml requires PyYAML. Either install it "
            "(`pip install PyYAML`) or use a .json config file instead."
        ) from exc
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ConfigError("Invalid YAML in %s: %s" % (path, exc)) from exc
    if not isinstance(data, dict):
        raise ConfigError("YAML config must be a mapping/object at the top level.")
    return data


def load_config(path: str | Path) -> Dict[str, Any]:
    """Load a JSON or YAML config file into a raw dict."""
    cfg_path = Path(path).expanduser()
    if not cfg_path.is_file():
        raise ConfigError("Config file not found: %s" % cfg_path)

    suffix = cfg_path.suffix.lower()
    if suffix == ".json":
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError(
                "Invalid JSON in %s (line %d, column %d): %s"
                % (cfg_path, exc.lineno, exc.colno, exc.msg)
            ) from exc
        if not isinstance(data, dict):
            raise ConfigError("JSON config must be an object at the top level.")
        return data
    if suffix in {".yaml", ".yml"}:
        return _read_yaml(cfg_path)
    raise ConfigError(
        "Unsupported config extension %r. Use .json, .yaml or .yml." % suffix
    )


def validate_config(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Merge *raw* with defaults, validate every field, return a normalized copy.

    The returned dict is the single source of truth used by the renderer.
    """
    if not isinstance(raw, dict):
        raise ConfigError("Config must be a mapping/object.")

    unknown = sorted(
        set(raw) - set(DEFAULT_CONFIG)
        - {"features", "repo_url", "emoji"}
    )
    if unknown:
        raise ConfigError("Unknown config keys: %s" % ", ".join(unknown))

    cfg = dict(DEFAULT_CONFIG)
    cfg.update(raw)
    errors: List[str] = []

    # name
    name = cfg.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("'name' is required and must be a non-empty string.")
        name = "untitled"
    else:
        name = name.strip()

    # description
    description = cfg.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("'description' is required and must be a non-empty string.")
        description = "输入 X，输出 Y。（请替换为一句话描述）"

    # owner / author
    owner = str(cfg.get("owner") or "your-github-id").strip()
    if not owner:
        owner = "your-github-id"
    author = str(cfg.get("author") or owner).strip()

    # license
    license_name = str(cfg.get("license") or "MIT").strip()
    if license_name not in SUPPORTED_LICENSES:
        errors.append(
            "'license' must be one of: %s" % ", ".join(SUPPORTED_LICENSES)
        )

    # language
    language = str(cfg.get("language") or "Python").strip()
    if language not in SUPPORTED_LANGUAGES:
        errors.append(
            "'language' must be one of: %s" % ", ".join(SUPPORTED_LANGUAGES)
        )

    # python_version
    python_version = str(cfg.get("python_version") or "3.9").strip()
    if not _PY_VERSION_RE.match(python_version):
        errors.append(
            "'python_version' must look like 3.9 / 3.11 / 3.12 etc."
        )

    # keywords
    keywords = cfg.get("keywords") or []
    if not isinstance(keywords, list) or not all(
        isinstance(k, str) and k.strip() for k in keywords
    ):
        errors.append("'keywords' must be a list of non-empty strings.")
        keywords = []
    else:
        keywords = [k.strip() for k in keywords]

    # features (optional, free-form list shown in README)
    features = cfg.get("features") or []
    if not isinstance(features, list) or not all(
        isinstance(f, str) and f.strip() for f in features
    ):
        errors.append("'features' must be a list of non-empty strings.")
        features = []

    # year
    year = cfg.get("year")
    if year is None:
        year = current_year()
    elif not isinstance(year, int) or not (2000 <= year <= 2200):
        errors.append("'year' must be an integer between 2000 and 2200.")
        year = current_year()

    # derived / normalized values
    try:
        slug = slugify(name)
        pkg = package_name(name)
    except ValueError as exc:
        errors.append(
            "'name' 必须包含至少一个 ASCII 字母或数字，才能生成合法的 slug/包名（%s）" % exc
        )
        slug, pkg = "untitled", "untitled_pkg"
    repo_url = str(cfg.get("repo_url") or "").strip() or (
        "https://github.com/%s/%s" % (owner, slug)
    )
    install = str(cfg.get("install") or "").strip() or (
        "git clone %s.git\ncd %s\npip install -e ." % (repo_url, slug)
    )
    usage = str(cfg.get("usage") or "").strip() or (
        "%s --help" % ("python -m " + pkg if language == "Python" else slug)
    )

    input_hint = str(cfg.get("input_hint") or "").strip() or "一份配置"
    output_hint = str(cfg.get("output_hint") or "").strip() or "完整仓库骨架"
    problem_statement = str(cfg.get("problem_statement") or "").strip() or (
        "手动搭建一个新项目时，README、License、.gitignore、Issue 模板、CI 配置"
        "每次都要重新写一遍，既费时间又容易遗漏。不同人写出来的仓库质量参差不齐，"
        "别人 clone 下来经常跑不起来。\n\n"
        "{{name}} 把这套最佳实践固化成模板：只需要维护一份配置，就能生成结构一致、"
        "文档齐全、开箱即跑的仓库，让作者专注于代码本身。"
    )

    if errors:
        raise ConfigError("Invalid config:\n  - " + "\n  - ".join(errors))

    return {
        "name": name,
        "slug": slug,
        "package": pkg,
        "display_name": display_name(name),
        "description": description.strip(),
        "owner": owner,
        "author": author,
        "repo_url": repo_url,
        "language": language,
        "python_version": python_version,
        "license": license_name,
        "license_file": {
            "MIT": "LICENSE",
            "Apache-2.0": "LICENSE",
            "BSD-3-Clause": "LICENSE",
            "Unlicense": "LICENSE",
            "None": None,
        }[license_name],
        "keywords": keywords,
        "features": features,
        "install": install,
        "usage": usage,
        "ci": as_bool(cfg.get("ci"), True),
        "community": as_bool(cfg.get("community"), True),
        "ai_assisted": as_bool(cfg.get("ai_assisted"), True),
        "year": year,
        "emoji": str(cfg.get("emoji") or "").strip(),
        "input_hint": input_hint,
        "output_hint": output_hint,
        "problem_statement": problem_statement,
    }
