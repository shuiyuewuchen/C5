"""Allow ``python -m repo_forge``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
