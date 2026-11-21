"""Small pure helpers shared by config validation and template rendering."""

from __future__ import annotations

import datetime as _dt
import re
from typing import Any

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_PKG_RE = re.compile(r"[^a-z0-9_]")


def slugify(value: str) -> str:
    """Return a URL/filesystem-safe slug.

    >>> slugify("My Awesome Tool!")
    'my-awesome-tool'
    """
    value = (value or "").strip().lower()
    slug = _SLUG_RE.sub("-", value).strip("-")
    if not slug:
        raise ValueError("slugify(): empty result from %r" % (value,))
    return slug


def package_name(value: str) -> str:
    """Return a valid Python package identifier derived from a project name.

    >>> package_name("repo-forge")
    'repo_forge'
    """
    slug = slugify(value).replace("-", "_")
    pkg = _PKG_RE.sub("", slug).strip("_")
    if not pkg:
        raise ValueError("package_name(): empty result from %r" % (value,))
    if pkg[0].isdigit():
        pkg = "pkg_" + pkg
    return pkg


def display_name(value: str) -> str:
    """Human-friendly title: 'repo-forge' -> 'Repo Forge'."""
    return " ".join(word.capitalize() for word in slugify(value).split("-"))


def current_year() -> int:
    """Return the current local year (kept in a helper for testability)."""
    return _dt.date.today().year


def as_bool(value: Any, default: bool = True) -> bool:
    """Coerce common config representations into a bool."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "y"}
    return default
