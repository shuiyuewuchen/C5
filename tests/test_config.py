"""配置加载与校验的单元测试。"""

import json
import tempfile
import unittest
from pathlib import Path

from repo_forge.config import ConfigError, load_config, validate_config
from repo_forge.utils import as_bool, display_name, package_name, slugify

BASE = {"name": "demo-tool", "description": "输入 A，输出 B。", "owner": "alice"}


class SlugifyTest(unittest.TestCase):
    def test_ascii_and_punctuation(self):
        self.assertEqual(slugify("My Awesome Tool!"), "my-awesome-tool")
        self.assertEqual(slugify("  spaced  name  "), "spaced-name")

    def test_unicode_only_input_is_rejected_loudly(self):
        with self.assertRaises(ValueError):
            slugify("中文名")

    def test_package_name_edge_cases(self):
        self.assertEqual(package_name("repo-forge"), "repo_forge")
        self.assertEqual(package_name("2fast 2furious"), "pkg_2fast_2furious")

    def test_display_name(self):
        self.assertEqual(display_name("repo-forge"), "Repo Forge")

    def test_as_bool(self):
        self.assertTrue(as_bool("yes"))
        self.assertFalse(as_bool("off"))
        self.assertTrue(as_bool(None, True))


class ValidateConfigTest(unittest.TestCase):
    def test_defaults_are_filled(self):
        cfg = validate_config(dict(BASE))
        self.assertEqual(cfg["slug"], "demo-tool")
        self.assertEqual(cfg["package"], "demo_tool")
        self.assertEqual(cfg["license"], "MIT")
        self.assertEqual(cfg["repo_url"], "https://github.com/alice/demo-tool")
        self.assertTrue(cfg["ci"])
        self.assertTrue(cfg["community"])

    def test_custom_values_win(self):
        cfg = validate_config(
            {
                **BASE,
                "license": "Apache-2.0",
                "language": "Documentation",
                "python_version": "3.11",
                "keywords": ["a", "b"],
                "ci": False,
                "year": 2024,
            }
        )
        self.assertEqual(cfg["license"], "Apache-2.0")
        self.assertEqual(cfg["python_version"], "3.11")
        self.assertEqual(cfg["keywords"], ["a", "b"])
        self.assertFalse(cfg["ci"])
        self.assertEqual(cfg["year"], 2024)

    def test_missing_required_fields(self):
        with self.assertRaises(ConfigError) as ctx:
            validate_config({})
        text = str(ctx.exception)
        self.assertIn("'name' is required", text)
        self.assertIn("'description' is required", text)

    def test_invalid_license_is_listed(self):
        with self.assertRaises(ConfigError) as ctx:
            validate_config({**BASE, "license": "GPL-3.0"})
        self.assertIn("Apache-2.0", str(ctx.exception))

    def test_unknown_key_is_listed(self):
        with self.assertRaises(ConfigError) as ctx:
            validate_config({**BASE, "typo_key": 1})
        self.assertIn("typo_key", str(ctx.exception))

    def test_bad_python_version(self):
        with self.assertRaises(ConfigError):
            validate_config({**BASE, "python_version": "2.7"})

    def test_chinese_only_name_gives_actionable_error(self):
        with self.assertRaises(ConfigError) as ctx:
            validate_config({**BASE, "name": "中文工具"})
        self.assertIn("ASCII", str(ctx.exception))

    def test_keywords_must_be_strings(self):
        with self.assertRaises(ConfigError):
            validate_config({**BASE, "keywords": [1, 2]})

    def test_install_and_usage_defaults(self):
        cfg = validate_config(dict(BASE))
        self.assertIn("git clone", cfg["install"])
        self.assertIn("python -m demo_tool", cfg["usage"])


class LoadConfigTest(unittest.TestCase):
    def test_missing_file(self):
        with self.assertRaises(ConfigError) as ctx:
            load_config("/definitely/not/here.json")
        self.assertIn("not found", str(ctx.exception))

    def test_valid_json(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "c.json"
            p.write_text(json.dumps(BASE), encoding="utf-8")
            self.assertEqual(load_config(p)["name"], "demo-tool")

    def test_invalid_json_reports_line(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text('{"name": }', encoding="utf-8")
            with self.assertRaises(ConfigError) as ctx:
                load_config(p)
            self.assertIn("line", str(ctx.exception))

    def test_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "c.toml"
            p.write_text("x = 1", encoding="utf-8")
            with self.assertRaises(ConfigError) as ctx:
                load_config(p)
            self.assertIn("Unsupported", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
