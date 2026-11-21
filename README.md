# 🛠️ repo-forge

> 输入一份 JSON/YAML 配置，输出一个文档齐全、社区要素完备、clone 后 5 分钟可运行的 GitHub 开源仓库骨架。

[![CI](https://github.com/your-github-id/repo-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/your-github-id/repo-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![零运行时依赖](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](./pyproject.toml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

**一句话：输入一份 JSON/YAML 项目配置，输出一个可直接 `git push` 的专业仓库骨架。**

---

## 解决什么问题

手动搭建一个新项目时，README、License、`.gitignore`、Issue 模板、CI 配置每次都要重新写一遍，既费时间又容易遗漏。不同人写出来的仓库质量参差不齐，别人 clone 下来经常跑不起来——这正是 Elite20 C5 反复强调的失败模式。

`repo-forge` 把开源仓库的最佳实践固化成模板：只需维护一份配置，就能生成结构一致、文档齐全、开箱即跑的仓库，让作者专注于代码本身。

| 环节 | 没有 repo-forge | 有了 repo-forge |
|------|----------------|----------------|
| 初始化 | 手动创建 20+ 文件，复制粘贴旧项目 | 一份配置，一条命令 |
| 质量 | 靠记忆和运气，常漏 License / AI 日志 | 模板内建，逐项对照 C5 清单 |
| 可复现性 | 别人 clone 后缺依赖、跑不起来 | 零运行时依赖，5 分钟可验证 |
| 协作 | 没有 Issue 模板，贡献者不知从何下手 | 贡献指南 / Issue / PR 模板齐全 |
| 迭代 | 改完代码忘了改文档 | CI 自动跑 `make demo` 校验示例 |

它同时是 C5 挑战的**能力证明载体**：每个生成物都自带 `AI_LOG.md`（AI 使用日志）、`ATTRIBUTION.md`（拿来说明）、`CHANGELOG.md` 与社区要素，把「AI-First」与「拿来主义」从口号变成可复现的产出。

## 特性

- **零运行时依赖** —— 只用 Python 标准库；YAML 支持是可选增强。
- **26 个文件一次生成** —— README / LICENSE / CI / Issue 模板 / 行为准则 / 安全策略 / 贡献指南 / AAR 复盘模板。
- **失败要响亮** —— 配置错误给出可操作的中文提示，明确指出错在哪个字段。
- **不覆盖本地改动** —— 默认跳过已存在文件，`--force` 才覆盖，且 `plan()` 可先预演。
- **占位符严格校验** —— 渲染后若残留 `KEY` 占位符，直接拒绝写入（这条断言曾抓到真实 bug）。
- **四种开源协议** —— MIT / Apache-2.0 / BSD-3-Clause / Unlicense 全文模板。
- **CI 就绪** —— 生成即带 GitHub Actions，覆盖 Python 3.9 / 3.11 / 3.13。

## 快速开始

> 前置要求：Python 3.9+。无需安装任何第三方包。

### 安装

```bash
git clone https://github.com/your-github-id/repo-forge.git
cd repo-forge
# 方式 A：免安装，直接运行
./repo-forge --help
# 方式 B：可编辑安装（推荐，获得命令行入口）
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
repo-forge --help
```

### 使用

```bash
# 1) 先校验配置（不写任何文件）
repo-forge validate --config examples/basic.json

# 2) 预演将要写入的文件
repo-forge init --config examples/basic.json --out ./my-repo --dry-run

# 3) 真正生成
repo-forge init --config examples/basic.json --out ./my-repo

# 4) 交互式生成（无需写配置文件）
repo-forge init --interactive --out ./my-repo
```

常用命令：

| 命令 | 作用 |
|------|------|
| `make test` | 运行全部单元测试（标准库 unittest） |
| `make demo` | 真实运行生成器，重建 `examples/sample_output/` |
| `make lint` | ruff 静态检查（需 `.[dev]`） |
| `repo-forge list-templates` | 列出全部内置模板及其输出路径 |

## 示例

输入（`examples/basic.json`）：

```json
{
  "name": "hello-forge",
  "description": "输入一句话需求，输出一份可直接推送的仓库骨架。",
  "owner": "your-github-id",
  "license": "MIT",
  "language": "Python",
  "python_version": "3.9",
  "keywords": ["scaffold", "github", "automation"],
  "features": [
    "零运行时依赖，clone 后可立即运行",
    "一份配置生成 README / License / CI / Issue 模板",
    "生成前校验配置，错误信息可操作"
  ],
  "ci": true,
  "community": true,
  "ai_assisted": true
}
```

命令：

```bash
repo-forge init --config examples/basic.json --out ./my-repo
```

真实输出（节选）：

```text
✔ 配置校验 .................... OK
✔ 生成文件 .................... 26 个（新建 26 / 跳过 0 / 覆盖 0）
✔ 无未替换占位符 .............. OK
✔ 输出目录 .................... my-repo

下一步:
  cd my-repo
  ./repo-forge --help    # 免安装验证
  make test              # 运行测试
```

生成的目录：

```text
my-repo/
├── README.md
├── LICENSE
├── AI_LOG.md
├── ATTRIBUTION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── Makefile
├── pyproject.toml
├── repo-forge
├── .editorconfig
├── .gitignore
├── .github/
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/{bug_report,feature_request}.md
│   └── workflows/ci.yml
├── docs/AAR.md
├── examples/README.md
├── src/hello_forge/{__init__,__main__,core}.py
└── tests/test_smoke.py
```

完整产物见 [`examples/sample_output/`](./examples/sample_output/)（由 `make demo` 真实生成，非手写展示文件）。

### 配置字段参考

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | ✅ | — | 项目名，需含 ASCII 字母/数字，自动生成 slug 与包名 |
| `description` | ✅ | — | 一句话描述，写入 README 与 pyproject |
| `owner` | 否 | `your-github-id` | GitHub 用户名，用于生成仓库链接 |
| `license` | 否 | `MIT` | `MIT` / `Apache-2.0` / `BSD-3-Clause` / `Unlicense` / `None` |
| `language` | 否 | `Python` | 主要语言标签 |
| `python_version` | 否 | `3.9` | 最低 Python 版本 |
| `keywords` | 否 | `[]` | 关键词列表 |
| `features` | 否 | `[]` | 写入 README 的特性列表 |
| `ci` / `community` / `ai_assisted` | 否 | `true` | 特性开关，关闭则不生成对应文件 |
| `input_hint` / `output_hint` | 否 | 通用文案 | README 的「一句话」输入输出 |
| `problem_statement` | 否 | 通用文案 | README 的「解决什么问题」正文 |
| `repo_url` | 否 | 由 owner+name 推导 | 自定义仓库地址 |

## 项目结构

```text
repo-forge/
├── README.md                  # 本文件
├── LICENSE                    # MIT
├── AI_LOG.md                  # AI 使用日志（7 轮迭代记录）
├── ATTRIBUTION.md             # 拿来说明 / 借鉴来源
├── CHANGELOG.md               # 版本记录（SemVer）
├── CONTRIBUTING.md            # 贡献指南
├── CODE_OF_CONDUCT.md         # 行为准则
├── SECURITY.md                # 安全策略
├── Makefile                   # 常用命令统一入口
├── pyproject.toml             # PEP 621 元数据 / 命令行入口
├── repo-forge                 # 免安装启动脚本
├── .editorconfig / .gitignore
├── src/repo_forge/
│   ├── __init__.py            # 公共 API / 版本号
│   ├── __main__.py            # python -m repo_forge
│   ├── cli.py                 # argparse 子命令与错误码
│   ├── config.py              # 配置加载 / 默认值 / 校验
│   ├── generator.py           # plan() / generate() / 渲染守卫
│   ├── templates.py           # 内置模板库 + 协议正文
│   └── utils.py               # pure 函数工具
├── examples/
│   ├── basic.json             # 最小配置示例
│   ├── README.md
│   └── sample_output/         # make demo 的真实产物
├── docs/
│   └── AAR.md                 # 行动后反思（含失败经验与改进方案）
├── tests/
│   ├── test_config.py
│   ├── test_generator.py
│   ├── test_cli.py
│   └── test_smoke.py
└── .github/                   # Issue / PR 模板 + CI workflow + CODEOWNERS
```

## 技术栈

- 语言：Python 3.9+（仅标准库：`argparse` / `pathlib` / `unittest` / `dataclasses`）
- 可选依赖：PyYAML（YAML 配置）、ruff / coverage（开发期）
- 测试：标准库 `unittest`，共 40+ 用例，覆盖配置边界、渲染守卫、冲突策略与 CLI 端到端
- 模板引擎：自研 `KEY` 占位替换（避开模板内 Python/JSON 花括号与 `str.format` 的冲突）
- AI 集成：开发全流程由 WorkBuddy 辅助，详见 [AI_LOG.md](./AI_LOG.md)

## 设计原则

1. **可复现优先** —— 零隐式依赖，clone 后 5 分钟内必须能跑通。
2. **失败要响亮** —— 配置错误立即给出可操作的提示，绝不悄悄生成半成品。
3. **先看后写** —— `plan()` 预演三类文件（新建 / 跳过 / 覆盖），CLI 支持 `--dry-run`。
4. **拿来要声明** —— 所有借鉴来源写入 ATTRIBUTION.md。
5. **社区要素内建** —— License、贡献指南、Issue 模板、CI 都是默认产物，不是可选项。

## 测试

```bash
make test
```

覆盖重点：

- `test_config.py`：默认值、非法协议、未知字段、中文名边界、JSON 错误行号
- `test_generator.py`：全部模板无残留占位符、四种协议、特性开关、`--force` 语义、路径安全、可执行位
- `test_cli.py`：`--help` / `version` / `validate` / `init` / `--dry-run` 端到端与退出码
- `test_smoke.py`：clone 后的最小可运行路径

## AI 生成说明

本项目使用 AI 辅助开发，详见 [AI_LOG.md](./AI_LOG.md)。AI 参与了项目结构初始化、核心代码编写、模板设计、测试生成、文档撰写与代码审查；人工负责需求定义、边界修正、真实运行验证与最终审校。7 轮迭代中的两次失败（YAML 缺依赖报错不友好、README 写成口号）也如实记录在该文件中。

## 借鉴来源

本项目参考了以下来源，详见 [ATTRIBUTION.md](./ATTRIBUTION.md)：Python 官方文档（pathlib / argparse / unittest）、Elite20 C5 挑战说明、Keep a Changelog、Semantic Versioning、Conventional Commits、Contributor Covenant、GitHub Docs、PEP 518/561/621、Anthropic skill-creator 文档。

## License

MIT © 2026 Elite20。详见 [LICENSE](./LICENSE)。

---

> 欢迎 star、fork、提 Issue。把你的 C4 技能变成一个全世界都能用的项目，就是 C5 的本质。
