"""生成器测试：占位符、冲突策略、特性开关、路径安全。"""

import tempfile
import unittest
from pathlib import Path

from repo_forge.config import validate_config
from repo_forge.generator import (
    build_context,
    generate,
    plan,
    render,
    unresolved_placeholders,
)
from repo_forge.templates import TEMPLATES

BASE = {
    "name": "demo-tool",
    "description": "输入配置，输出仓库。",
    "owner": "alice",
    "license": "MIT",
}


class RenderTest(unittest.TestCase):
    def test_known_placeholder(self):
        self.assertEqual(render("Hi {{name}}", {"name": "X"}), "Hi X")

    def test_unknown_placeholder_is_preserved_for_detection(self):
        self.assertEqual(render("{{missing}}", {}), "{{missing}}")
        self.assertEqual(unresolved_placeholders("{{b}} {{a}} {{b}}"), ["a", "b"])

    def test_braces_in_templates_are_not_interpreted(self):
        text = 'cfg = {"a": 1}\nvalue = {{name}}'
        self.assertEqual(render(text, {"name": "ok"}), 'cfg = {"a": 1}\nvalue = ok')

    def test_boolean_rendering(self):
        self.assertEqual(render("{{ci}}", {"ci": True}), "true")
        self.assertEqual(render("{{ci}}", {"ci": False}), "false")


class BuildContextTest(unittest.TestCase):
    def test_derived_keys_present(self):
        ctx = build_context(validate_config(dict(BASE)))
        for key in ("keywords_csv", "features_bullets", "python_version_compact", "date"):
            self.assertIn(key, ctx)


class GenerateTest(unittest.TestCase):
    def test_all_templates_render_without_placeholders(self):
        cfg = validate_config(dict(BASE))
        ctx = build_context(cfg)
        leftovers = {}
        for name, body in TEMPLATES.items():
            missing = unresolved_placeholders(render(body, ctx))
            if missing:
                leftovers[name] = missing
        self.assertEqual(leftovers, {}, "未替换占位符: %s" % leftovers)

    def test_generate_creates_expected_core_files(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            result = generate(validate_config(dict(BASE)), out)
            self.assertGreater(result.total, 15)
            self.assertEqual(result.skipped, [])
            for rel in (
                "README.md", "LICENSE", "AI_LOG.md", "ATTRIBUTION.md",
                "CONTRIBUTING.md", "CHANGELOG.md", ".gitignore",
                ".github/workflows/ci.yml", ".github/ISSUE_TEMPLATE/bug_report.md",
                "src/demo_tool/__init__.py", "src/demo_tool/__main__.py",
                "src/demo_tool/core.py", "tests/test_smoke.py",
            ):
                self.assertTrue((out / rel).is_file(), "缺少 %s" % rel)

    def test_default_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            generate(validate_config(dict(BASE)), out)
            (out / "README.md").write_text("LOCAL EDIT", encoding="utf-8")
            result = generate(validate_config(dict(BASE)), out)
            self.assertIn("README.md", result.skipped)
            self.assertEqual((out / "README.md").read_text(encoding="utf-8"), "LOCAL EDIT")

    def test_force_overwrites(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            generate(validate_config(dict(BASE)), out)
            (out / "README.md").write_text("OLD", encoding="utf-8")
            result = generate(validate_config(dict(BASE)), out, force=True)
            self.assertIn("README.md", result.overwritten)
            self.assertNotIn("OLD", (out / "README.md").read_text(encoding="utf-8"))

    def test_feature_flags_remove_files(self):
        cfg = validate_config(
            {**BASE, "ci": False, "community": False, "ai_assisted": False, "license": "None"}
        )
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            generate(cfg, out)
            for rel in (
                ".github/workflows/ci.yml", "CONTRIBUTING.md",
                "AI_LOG.md", "docs/AAR.md", "LICENSE",
            ):
                self.assertFalse((out / rel).exists(), "不应生成 %s" % rel)

    def test_license_variants(self):
        for lic in ("MIT", "Apache-2.0", "BSD-3-Clause", "Unlicense"):
            with self.subTest(license=lic), tempfile.TemporaryDirectory() as td:
                out = Path(td) / "out"
                generate(validate_config({**BASE, "license": lic}), out)
                text = (out / "LICENSE").read_text(encoding="utf-8")
                self.assertIn("2026", text) if lic != "Unlicense" else self.assertIn("public domain", text)

    def test_plan_is_side_effect_free(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            items = plan(validate_config(dict(BASE)), out)
            self.assertGreater(len(items), 15)
            self.assertFalse(out.exists(), "plan() 不应创建目录")

    def test_no_path_escapes_output_dir(self):
        cfg = validate_config({**BASE, "name": "safe-name"})
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            items = plan(cfg, out)
            for item in items:
                self.assertFalse(str(item.path).startswith("/"))
                self.assertNotIn("..", Path(item.path).parts)

    def test_executable_bit_on_launcher(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            generate(validate_config(dict(BASE)), out)
            self.assertTrue((out / "repo-forge").stat().st_mode & 0o111)

    def test_chinese_description_renders_utf8(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            generate(validate_config(dict(BASE)), out)
            self.assertIn("输入配置，输出仓库。", (out / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
