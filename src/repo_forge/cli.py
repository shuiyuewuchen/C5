"""Command-line interface for repo-forge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

from . import __version__
from .config import DEFAULT_CONFIG, ConfigError, load_config, validate_config
from .generator import generate, plan
from .templates import TEMPLATES

EXIT_OK = 0
EXIT_CONFIG = 1
EXIT_IO = 2

_INTERACTIVE_FIELDS = (
    ("name", "项目名称", None),
    ("description", "一句话描述", None),
    ("owner", "GitHub 用户名", "your-github-id"),
    ("license", "开源协议 (MIT/Apache-2.0/BSD-3-Clause/Unlicense/None)", "MIT"),
    ("language", "主要语言 (Python/TypeScript/Go/Rust/Documentation/PromptSet)", "Python"),
    ("python_version", "Python 版本 (如 3.9)", "3.9"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-forge",
        description="配置驱动的 GitHub 仓库脚手架生成器（零运行时依赖）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  repo-forge init --config examples/basic.json --out ./my-repo
  repo-forge init --interactive --out ./my-repo
  repo-forge validate --config examples/basic.json
  repo-forge list-templates
""",
    )
    parser.add_argument("-V", "--version", action="version", version="repo-forge " + __version__)
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_init = sub.add_parser("init", aliases=["new", "generate"], help="生成一个新仓库")
    p_init.add_argument("-c", "--config", help="配置文件路径 (.json/.yaml/.yml)")
    p_init.add_argument("-o", "--out", default=".", help="输出目录（默认当前目录）")
    p_init.add_argument("-i", "--interactive", action="store_true", help="交互式输入配置")
    p_init.add_argument("-f", "--force", action="store_true", help="覆盖已存在的文件")
    p_init.add_argument("--dry-run", action="store_true", help="只预演，不写入磁盘")
    p_init.set_defaults(func=_cmd_init)

    p_val = sub.add_parser("validate", aliases=["check"], help="只校验配置文件")
    p_val.add_argument("-c", "--config", required=True, help="配置文件路径")
    p_val.set_defaults(func=_cmd_validate)

    p_list = sub.add_parser("list-templates", help="列出内置模板")
    p_list.set_defaults(func=_cmd_list)

    p_ver = sub.add_parser("version", help="显示版本号")
    p_ver.set_defaults(func=_cmd_version)

    return parser


def _interactive_config() -> Dict[str, Any]:
    print("交互式配置（直接回车使用默认值）\n")
    raw: Dict[str, Any] = {}
    for key, label, default in _INTERACTIVE_FIELDS:
        prompt = label + ((" [%s]" % default) if default else "") + ": "
        try:
            value = input(prompt).strip()
        except EOFError:
            raise ConfigError("交互式输入被中断（EOF）。请使用 --config 提供配置文件。")
        if value:
            raw[key] = value
        elif default is not None:
            raw[key] = default
    return raw


def _resolve_config(args: argparse.Namespace) -> Dict[str, Any]:
    if args.interactive:
        if args.config:
            raise ConfigError("--interactive 与 --config 不能同时使用。")
        raw = _interactive_config()
    else:
        if not args.config:
            raise ConfigError("请提供 --config 或使用 --interactive。")
        raw = load_config(args.config)
    return validate_config(raw)


def _cmd_init(args: argparse.Namespace) -> int:
    cfg = _resolve_config(args)
    out = Path(args.out).expanduser()

    if args.dry_run:
        items = plan(cfg, out, force=args.force)
        print("DRY RUN —— 不会写入任何文件\n")
        for item in items:
            print("  %-10s %s" % (item.action.upper(), item.path))
        print("\n共 %d 个文件。" % len(items))
        return EXIT_OK

    result = generate(cfg, out, force=args.force)
    print("\n" + result.as_text() + "\n")
    next_steps = [
        "  cd %s" % out,
        "  ./repo-forge --help    # 免安装验证",
        "  make test              # 运行测试",
    ]
    print("下一步:\n" + "\n".join(next_steps))
    return EXIT_OK


def _cmd_validate(args: argparse.Namespace) -> int:
    cfg = validate_config(load_config(args.config))
    print("✔ 配置有效")
    print("  项目: %s (%s)" % (cfg["name"], cfg["slug"]))
    print("  包名: %s" % cfg["package"])
    print("  协议: %s" % cfg["license"])
    print("  仓库: %s" % cfg["repo_url"])
    print("  模板: %d 个（不含 License 正文）" % len(TEMPLATES))
    return EXIT_OK


def _cmd_list(args: argparse.Namespace) -> int:
    print("内置模板（%d 个）:\n" % len(TEMPLATES))
    for key in sorted(TEMPLATES):
        print("  " + key)
    return EXIT_OK


def _cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns an integer suitable for ``sys.exit``."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return EXIT_OK

    try:
        return int(args.func(args))
    except ConfigError as exc:
        print("配置错误: %s" % exc, file=sys.stderr)
        return EXIT_CONFIG
    except (OSError, ValueError) as exc:
        print("执行失败: %s" % exc, file=sys.stderr)
        return EXIT_IO
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        return EXIT_IO


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
