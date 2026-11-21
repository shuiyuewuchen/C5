"""CLI 端到端测试（不写当前目录，全部在临时目录中完成）。"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from repo_forge.cli import main
from repo_forge.config import validate_config

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "repo_forge", *args],
        cwd=ROOT,
        env={"PYTHONPATH": SRC, "PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
    )


class CliTest(unittest.TestCase):
    def test_help_lists_subcommands(self):
        p = run_cli("--help")
        self.assertEqual(p.returncode, 0, p.stderr)
        for word in ("init", "validate", "list-templates", "version"):
            self.assertIn(word, p.stdout)

    def test_version(self):
        p = run_cli("version")
        self.assertEqual(p.returncode, 0)
        self.assertIn("0.3", p.stdout)

    def test_validate_ok(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "c.json"
            cfg.write_text(
                json.dumps({"name": "cli-demo", "description": "d", "owner": "alice"}),
                encoding="utf-8",
            )
            p = run_cli("validate", "--config", str(cfg))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("配置有效", p.stdout)

    def test_validate_bad_config_exit_code(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "bad.json"
            cfg.write_text("{}", encoding="utf-8")
            p = run_cli("validate", "--config", str(cfg))
            self.assertEqual(p.returncode, 1)
            self.assertIn("配置错误", p.stderr)

    def test_init_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "c.json"
            out = Path(td) / "out"
            cfg.write_text(
                json.dumps({"name": "cli-demo", "description": "d", "owner": "alice"}),
                encoding="utf-8",
            )
            p = run_cli("init", "--config", str(cfg), "--out", str(out))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue((out / "README.md").is_file())
            self.assertIn("生成文件", p.stdout)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "c.json"
            out = Path(td) / "out"
            cfg.write_text(
                json.dumps({"name": "cli-demo", "description": "d", "owner": "alice"}),
                encoding="utf-8",
            )
            p = run_cli("init", "--config", str(cfg), "--out", str(out), "--dry-run")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("DRY RUN", p.stdout)
            self.assertFalse(out.exists())

    def test_list_templates(self):
        p = run_cli("list-templates")
        self.assertEqual(p.returncode, 0)
        self.assertIn("README.md", p.stdout)

    def test_main_callable(self):
        self.assertEqual(main(["version"]), 0)


if __name__ == "__main__":
    unittest.main()
