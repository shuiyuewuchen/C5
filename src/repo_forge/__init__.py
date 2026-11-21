"""repo-forge - a config-driven GitHub repository scaffold generator.

Turn a small JSON/YAML config into a complete, professional, push-ready
open-source repository: README, LICENSE, CI, issue templates, community
files, tests and a runnable source skeleton.

The project intentionally depends only on the Python standard library, so a
freshly cloned repository can be used within five minutes.
"""

from .config import ConfigError, load_config, validate_config
from .generator import generate, plan
from .utils import slugify, package_name

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "ConfigError",
    "load_config",
    "validate_config",
    "generate",
    "plan",
    "slugify",
    "package_name",
]
