"""冒烟测试：确保 clone 后的最小可运行路径成立。"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SmokeTest(unittest.TestCase):
    def test_module_help_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "hello_forge", "--help"],
            cwd=ROOT,
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("init", result.stdout)

    def test_readme_exists(self):
        self.assertTrue((ROOT / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
