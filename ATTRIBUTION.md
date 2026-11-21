# 拿来说明（ATTRIBUTION.md）

> 原则：凡有所学，必有所标。以下列出本项目借鉴/参考的来源与复用范围。

## 一、直接复用（代码 / 文本）

| 来源 | 许可 | 复用内容 | 位置 |
|------|------|----------|------|
| Python Software Foundation — `pathlib` 官方文档 | PSF License | 路径规范化与 `Path` 用法模式 | `src/repo_forge/config.py`, `generator.py` |
| Python Software Foundation — `argparse` / `unittest` 文档 | PSF License | CLI 子命令结构、测试组织方式 | `cli.py`, `tests/` |
| Python Software Foundation — `importlib.resources` 设计思路 | PSF License | 包内资源定位思路（本项目简化为相对 `__file__`） | `generator.py` |
| Massachusetts Institute of Technology — MIT License 文本 | MIT | 协议模板 | `LICENSE` |

## 二、结构 / 规范参考（未复制原文）

| 来源 | 参考内容 |
|------|----------|
| C5 GitHub Repository 挑战说明（CHALLENGE.md，EduSeed Elite20） | README 标准模板结构、提交文件命名、检查清单 |
| Anthropic — `skill-creator` 文档 | 「渐进式披露」与「清晰触发条件」的文档组织思想 |
| Keep a Changelog v1.1.0 | CHANGELOG 的分类与日期格式 |
| Semantic Versioning 2.0.0 | `0.x.y` 版本语义 |
| Conventional Commits v1.0.0 | 提交信息规范 |
| Contributor Covenant v2.1 | 行为准则 |
| GitHub Docs — Issue / PR 模板语法 | `.github/ISSUE_TEMPLATE/*` 与 PR 模板结构 |
| PEP 621 / PEP 518 | `pyproject.toml` 元数据与构建系统配置 |
| PEP 561 | `py.typed` 标记文件 |

## 三、AI 生成内容声明

本项目由 WorkBuddy（AI 编程助手）辅助完成，包括：目录结构建议、核心代码初稿、
测试用例初稿、README / CONTRIBUTING / CHANGELOG 初稿、代码审查意见。
所有内容均经人工审校、真实运行验证与边界修正，详见 [AI_LOG.md](./AI_LOG.md)。

## 四、明确未使用的内容

- 未复制任何第三方项目的源代码文件。
- 未使用任何需要联网才能正常运行的运行时依赖。
- 未引用未经核实的统计数据或基准测试结果。

## 五、如果你复用了本项目

欢迎 fork！请保留本文件与 `LICENSE`，并在你的 `ATTRIBUTION.md` 中补充：
> 「本项目结构参考了 repo-forge（https://github.com/shuiyuewuchen/C5）」。
