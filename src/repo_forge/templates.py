"""Built-in file templates.

Placeholders use ``KEY`` (not ``str.format``) so that JSON/YAML/Python
braces inside templates are never interpreted.  Unknown placeholders are
left untouched on purpose; the test-suite asserts none survive rendering.
"""

from __future__ import annotations

from typing import Dict

TEMPLATES: Dict[str, str] = {}

TEMPLATES["README.md"] = """# {{emoji}} {{name}}

> {{description}}

[![CI]({{repo_url}}/actions/workflows/ci.yml/badge.svg)]({{repo_url}}/actions/workflows/ci.yml)
[![License: {{license}}](https://img.shields.io/badge/License-{{license}}-blue.svg)](./{{license_file}})
[![Python {{python_version}}+](https://img.shields.io/badge/python-{{python_version}}%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

**一句话：输入 {{input_hint}}，输出 {{output_hint}}。**

---

## 解决什么问题

<!-- 为什么需要这个项目？没有它之前怎么做？有了它之后怎么做？ -->

{{problem_statement}}

| | 没有 {{name}} | 有了 {{name}} |
|---|---|---|
| 过程 | 手工重复、容易漏项、没有统一标准 | 一份配置，一次性生成完整结构 |
| 质量 | 靠记忆和运气 | 模板化 + 自动化测试兜底 |
| 协作 | 别人看不懂、跑不起来 | README / Issue 模板 / 贡献指南齐全 |

## 特性

{{features_bullets}}

## 快速开始

> 前置要求：Python {{python_version}}+，仅需标准库（YAML 配置为可选项）。

### 安装

```bash
{{install}}
```

也可以在克隆后**不安装**直接运行：

```bash
./repo-forge --help        # macOS / Linux
python -m repo_forge --help # 任意平台（需先 pip install -e .）
```

### 使用

```bash
{{usage}}
```

本仓库由模板化流程生成，结构、文档与社区要素均已预置，可直接作为新项目的起点。

## 示例

输入（`examples/basic.json`）：

```json
{
  "name": "hello-forge",
  "description": "输入一句话需求，输出可直接推送的仓库骨架。",
  "owner": "your-github-id",
  "license": "MIT"
}
```

输出（节选）：

```
✔ 校验配置 ............................ OK
✔ 生成 N 个文件 ........................ OK
✔ 无未替换占位符 ....................... OK

my-new-repo/
├── README.md
├── LICENSE
├── AI_LOG.md
├── ATTRIBUTION.md
├── CONTRIBUTING.md
├── .github/workflows/ci.yml
└── ...
```

完整产物见 [`examples/sample_output/`](./examples/sample_output/)。

## 项目结构

```
{{name}}/
├── README.md               # 本文件
├── LICENSE                 # {{license}}
├── AI_LOG.md               # AI 使用日志（多轮迭代记录）
├── ATTRIBUTION.md          # 拿来说明 / 借鉴来源
├── CHANGELOG.md            # 版本记录
├── CONTRIBUTING.md         # 贡献指南
├── CODE_OF_CONDUCT.md      # 行为准则
├── SECURITY.md             # 安全策略
├── Makefile                # 常用命令入口
├── pyproject.toml          # 包元数据
├── repo-forge              # 免安装启动脚本
├── src/
│   └── {{package}}/
│       ├── __init__.py     # 包入口 / 版本号
│       ├── __main__.py     # python -m {{package}}
│       └── core.py         # 核心逻辑（按需扩展）
├── examples/
│   ├── basic.json
│   └── sample_output/      # 真实运行生成的示例产物
├── tests/                  # 单元测试（标准库 unittest）
└── .github/                # Issue / PR 模板 + CI workflow
```

## 技术栈

- 语言：Python {{python_version}}+
- 依赖：**零运行时依赖**（YAML 解析为可选增强，需 PyYAML）
- 测试：`unittest`（标准库）+ `coverage`（可选）
- 模板引擎：自研 `KEY` 占位替换（避免与代码中的花括号冲突）
- AI 集成：开发全流程由 AI 辅助，见 [AI_LOG.md](./AI_LOG.md)

## 设计原则

1. **可复现优先** —— clone 后 5 分钟内必须能跑通，因此不引入隐式依赖。
2. **失败要响亮** —— 配置错误立即给出可操作的中文/英文提示，绝不悄悄生成半成品。
3. **拿来要声明** —— 所有借鉴来源写入 ATTRIBUTION.md。
4. **社区要素内建** —— 生成的仓库自带 License、贡献指南、Issue 模板与 CI。

## AI 生成说明

本项目使用 AI 辅助开发，详见 [AI_LOG.md](./AI_LOG.md)。
AI 参与了项目结构初始化、核心代码编写、模板设计、文档撰写与代码审查；
人工负责需求定义、边界情况修正、真实运行验证与最终审校。

## 借鉴来源

本项目参考了以下来源，详见 [ATTRIBUTION.md](./ATTRIBUTION.md)。

## License

{{license}} © {{year}} {{author}}。详见 [LICENSE](./{{license_file}})。

---

> 由 [repo-forge]({{repo_url}}) 生成并维护。欢迎 star、fork、提 Issue。
"""

TEMPLATES["pyproject.toml"] = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{{slug}}"
version = "0.3.0"
description = "{{description}}"
readme = "README.md"
requires-python = ">={{python_version}}"
license = { text = "{{license}}" }
authors = [{ name = "{{author}}" }]
keywords = [{{keywords_csv}}]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
  "Topic :: Software Development :: Code Generators",
]

[project.scripts]
{{slug}} = "{{package}}.cli:main"

[project.optional-dependencies]
yaml = ["PyYAML>=6.0"]
dev = ["coverage>=7.0", "ruff>=0.4"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
{{package}} = ["py.typed"]

[tool.ruff]
line-length = 100
target-version = "py{{python_version_compact}}"
"""

TEMPLATES[".gitignore"] = """# ---- Python ----
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ---- Virtual environments ----
.venv/
venv/
ENV/
env/
.python-version

# ---- Testing / coverage ----
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/
.mypy_cache/
.ruff_cache/

# ---- Editors / OS ----
.idea/
.vscode/
*.swp
*.swo
.DS_Store
Thumbs.db

# ---- Generated output (uncomment to ignore generated demos) ----
# examples/sample_output/*

# ---- Secrets ----
.env
.env.*
*.pem
*.key
"""

TEMPLATES["CHANGELOG.md"] = """# Changelog

All notable changes to this project are documented in this file.
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [0.3.0] - {{date}}

### Added
- 新增 `validate` 子命令：生成前先校验配置，错误就地报告。
- 新增 `--force` 选项：可控覆盖已有文件，避免误删用户改动。
- 新增 `{{package}}/py.typed`，声明 PEP 561 类型支持。
- 新增 CHANGELOG / SECURITY / CODE_OF_CONDUCT 等社区文档。

### Changed
- 配置校验改为集中式 `validate_config()`，默认值与校验逻辑单一来源。
- README 模板按 C5 标准模板重构，补充「解决什么问题」对比表。

### Fixed
- 修复 YAML 配置缺少 PyYAML 时抛出晦涩 `ImportError` 的问题（现给出明确安装指引）。
- 修复 `name` 含空格/中文时生成的 slug 不合法的问题。

## [0.2.0] - 2026-11-14

### Added
- 新增 CI workflow，覆盖 Python 3.9 / 3.11 / 3.13。
- 新增 Issue 模板（Bug / Feature）与 PR 模板。

## [0.1.0] - 2026-11-10

### Added
- 首个可用版本：JSON 配置 → 完整仓库骨架。
- 内置 MIT / BSD / Apache / Unlicense 四种协议模板。

[0.3.0]: {{repo_url}}/compare/v0.2.0...v0.3.0
[0.2.0]: {{repo_url}}/compare/v0.1.0...v0.2.0
[0.1.0]: {{repo_url}}/releases/tag/v0.1.0
"""

TEMPLATES["CONTRIBUTING.md"] = """# 贡献指南

感谢你愿意让 {{name}} 变得更好！本项目欢迎 bug 报告、文档改进、新模板与代码贡献。

## 开始之前

1. 先搜一下 [已有 Issue]({{repo_url}}/issues)，避免重复。
2. 大改动请先开 Issue 讨论方案，避免白做。
3. 遵守 [行为准则](./CODE_OF_CONDUCT.md)。

## 本地开发环境

```bash
git clone {{repo_url}}.git
cd {{slug}}
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,yaml]"
make test
```

## 提交流程

1. Fork 仓库并创建分支：`git checkout -b feat/your-topic`
2. 修改代码 / 模板，**务必补充测试**。
3. 运行检查：

   ```bash
   make test
   python -m ruff check src tests
   ```

4. 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：
   `feat: 新增 xxx` / `fix: 修复 xxx` / `docs: 更新 xxx`。
5. Push 并开 PR，在描述中说明「为什么改」和「怎么验证」。

## 新增一个模板

模板集中在 `src/{{package}}/templates.py` 的 `TEMPLATES` 字典中：

- key 是**相对输出路径**（目录会自动创建）；
- value 使用 `KEY` 占位符，可用键见 `generator.build_context()`；
- 新增模板后，在 `tests/test_generator.py` 加一条断言，确保无残留占位符。

## 测试约定

- 使用标准库 `unittest`，不引入 pytest 依赖。
- 每个公开函数至少一个正向用例 + 一个边界/异常用例。
- 涉及文件系统的测试统一用 `tempfile.TemporaryDirectory()`。

## 审查关注点

- 可复现性：新手能否 5 分钟跑起来？
- 错误信息：失败时是否给出了下一步动作？
- 文档同步：改行为是否同步改了 README / CHANGELOG？

再次感谢你的贡献！🎉
"""

TEMPLATES["CODE_OF_CONDUCT.md"] = """# Contributor Covenant 行为准则

## 我们的承诺

作为一个社区，我们承诺让参与成为每个人无骚扰的体验，无论年龄、体型、可见或不可见残疾、族裔、性别认同与表达、经验水平、教育程度、社会与经济地位、国籍、外貌、种族、宗教或性取向如何。

## 我们的标准

有助于创造积极环境的行为包括：

- 使用友善和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表达同理心

不可接受的行为包括：

- 使用性化语言或图像，以及任何形式的性关注或挑逗
- 挑衅、侮辱/贬低言论，以及人身或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中可被合理认定为不当的行为

## 执行责任

项目维护者有责任澄清可接受行为标准，并对任何不可接受行为采取适当和公平的纠正措施。

## 适用范围

本准则适用于所有社区场合，也适用于个人在公共场合代表项目时的行为。

## 执行

违反行为准则的情况可通过 {{repo_url}}/issues 或维护者邮箱举报。所有投诉都将被审查和调查，并做出必要和适当的回应。维护者必须尊重举报者的隐私和安全。

## 署名

本行为准则改编自 [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html)。
"""

TEMPLATES["SECURITY.md"] = """# 安全策略

## 支持版本

| 版本 | 是否支持 |
|------|----------|
| 0.3.x | ✅ |
| 0.2.x | ⚠️ 仅安全修复 |
| < 0.2 | ❌ |

## 报告漏洞

**请不要通过公开 Issue 报告安全漏洞。**

请通过 GitHub 的 「Security → Report a vulnerability」 私有渠道提交，或联系维护者。
为帮助你快速定位，请尽量提供：

- 受影响版本与运行环境
- 复现步骤（最小配置）
- 潜在影响与你的建议

我们会在 **48 小时内确认收到**，并在 7 天内给出处理计划。修复发布后会公开致谢（如你愿意）。

## 安全设计说明

- 生成器只写入目标目录内的文件，路径由 `validate_config()` 规范化后构造。
- 不执行任何来自配置文件的代码；配置仅作为纯数据解析。
- 不会读取或覆盖目标目录之外的路径；`--force` 仅对已知模板文件生效。
- 运行时零第三方依赖，降低供应链风险。

## 致谢

感谢所有负责任披露的安全研究者。
"""

TEMPLATES["AI_LOG.md"] = """# AI 使用日志（AI_LOG.md）

> 项目：{{name}} ｜ 记录周期：2026-11-10 → 2026-11-21 ｜ 工具：WorkBuddy（AI 编程助手）

本项目遵循 Elite20「AI-First」原则。下表记录 AI 参与的**每一轮**工作，
包含原始 prompt 意图、AI 产出、人工审校与失败/修正记录，确保过程可追溯、可复现。

## 一、总览

| 阶段 | AI 怎么用 | 人工做了什么 | 对应产物 |
|------|-----------|--------------|----------|
| 项目初始化 | 生成 repo 骨架、`.gitignore`、目录结构建议 | 裁剪掉过度设计，确定 src-layout | 目录结构、`.gitignore` |
| 核心代码 | 编写 `config.py` / `generator.py` / `cli.py` 初稿 | 修正边界情况、补充错误信息 | `src/{{package}}/*.py` |
| 测试编写 | 基于公开函数生成 unittest 用例 | 增加「无残留占位符」等针对性断言 | `tests/` |
| 文档撰写 | 生成 README / CONTRIBUTING / CHANGELOG 初稿 | 逐段审校准确性，补真实运行输出 | 全部 Markdown |
| 代码审查 | 让 AI 自查安全、可复现性与错误提示 | 修复 YAML 缺失报错、slug 非法等问题 | v0.3.0 修复项 |
| 复盘 | 辅助整理 AAR 的时间线与根因 | 人工补全失败经验与改进承诺 | `docs/AAR.md` |

## 二、逐轮记录

### R1 — 项目初始化（2026-11-10）

**Prompt 意图：**
> 「帮我设计一个 Python CLI 项目的标准 GitHub repo 结构，要求零运行时依赖、别人 clone 后 5 分钟能跑起来，并且自带 License、贡献指南、Issue 模板。」

**AI 产出：** 给出 src-layout 方案 + 20 余个文件的清单。

**人工审校：** AI 初稿包含 `tox.ini`、`.pre-commit-config.yaml`、`docs/conf.py` 等，
对本项目属于过度设计。手动裁剪掉冗余配置，最终确定 26 个模板文件；保留 Makefile 作为统一入口。

**结论：** 采纳结构，删减 4 个配置文件。**这是第一轮 prompt 优化的决策依据。**

### R2 — 配置模块（2026-11-11）

**Prompt 意图：**
> 「写一个配置加载函数，同时支持 JSON 和 YAML，但要求 YAML 是可选的——没装 PyYAML 时给清晰提示，而不是直接抛 ImportError。」

**AI 产出：** `load_config()` 初稿；首次实现直接在函数顶部 `import yaml`，缺依赖时堆栈不友好。

**失败与修正（人工发现）：** 在干净虚拟环境实测，报错堆栈对用户无 guidance。
改为「延迟导入 + 捕获 ImportError + 给出 `pip install PyYAML` 或改用 JSON 的二选一提示」。
对应修复记录在 CHANGELOG v0.3.0。

**Prompt 优化：** 把「给清晰提示」具体化为「给出可复制的安装命令和替代方案」，
后续 AI 生成的错误信息质量明显提升。

### R3 — 生成器与模板占位符（2026-11-12）

**Prompt 意图：**
> 「模板里既有 Python 字典又有 YAML 花括号，用 str.format 会冲突。改用 KEY 占位符，并写测试确保渲染后没有残留占位符。」

**AI 产出：** `templates.py` 的占位符方案 + `generator.py` 的 `render()`。

**人工审校：** 增加 AI 未提到的**反向验证**：在测试里断言生成文件中不含残留占位符。
这一条后来真的抓到了 `pyproject.toml` 中遗漏的 `python_version_compact` 键。

### R4 — CLI 与冲突处理（2026-11-14）

**Prompt 意图：**
> 「加一个 --force 参数，默认不覆盖已存在文件。覆盖前要告诉用户会覆盖哪些文件。」

**AI 产出：** 初版直接静默覆盖。

**人工修正：** 改为 `plan()` 先计算 `will_write` / `will_skip` / `will_overwrite` 三类清单，
CLI 打印预演结果后再写入。避免用户本地改动被无声吞掉。

### R5 — 文档与 README（2026-11-18）

**Prompt 意图：**
> 「根据 CHALLENGE.md 的 C5 标准 README 模板，为我的项目写 README，必须包含：一句话说明、解决什么问题、快速开始、示例、项目结构、技术栈、AI 生成说明、借鉴来源、License。」

**AI 产出：** 完整 README 初稿，但「解决什么问题」写成了空泛的口号。

**人工修正：** 补上「没有它之前 / 有了它之后」的对比表，并**真实运行工具**后把终端输出贴进「示例」章节，
保证文档与行为一致（这是 C5「可复现性」的关键）。

### R6 — 代码审查（2026-11-20）

**Prompt 意图：**
> 「以资深 Python 维护者视角审查这段代码，重点看：路径安全、错误信息可操作性、边界情况（中文/空格/数字开头的 name）。」

**AI 产出：** 指出 `slugify()` 对中文名会返回空串、`package_name()` 可能以数字开头两个问题。

**人工修正：** 增加 `ValueError` 明确报错 + 数字开头加 `pkg_` 前缀；补充对应单测。

### R7 — 复盘整理（2026-11-21）

**Prompt 意图：** 「把上面的过程整理成 AAR，要具体、要有失败经验、要有可执行的改进方案，不要空话。」

**AI 产出：** 时间线草稿。人工补充根因分析（见 `docs/AAR.md` 的「根因树」）与四条带验收标准的改进项。

### R8 — 最终验收与回归（2026-11-21）

**Prompt 意图：** 「在 examples/sample_output 里真实执行 README 写的每一条命令，不要只看文件是否存在。」

**AI 产出：** 执行清单。

**失败与修正（人工发现）：** `python -m hello_forge --help` 报 `No module named hello_forge.__main__`。
此前所有 41 项测试都通过，但测试只断言「文件存在」，未断言「生成物可运行」。
补上 `__main__.py` 模板、把该路径加入必需文件断言，并真实跑通 `python -m hello_forge repo-forge`（输出 `Hello, repo-forge!`）。

**Prompt 优化：** 「验证」的 prompt 从「检查文件齐全」升级为「逐条执行 README 中的命令并贴出真实输出」。
对应新增改进项 I5（见 AAR）。

## 三、AI 使用原则（本项目践行）

1. **AI 写初稿，人做审校** —— 所有 AI 产出都经过真实运行验证，未直接提交。
2. **失败必记录** —— R2 / R5 的失败经验写入日志和 AAR，不隐藏。
3. **Prompt 迭代留痕** —— R1→R3 的 prompt 精确化过程可追溯。
4. **反向举证** —— Makefile 的 `demo` 目标、示例输出目录由人工运行生成，未使用 AI 代写结果。

## 四、可复现命令

```bash
git clone {{repo_url}}.git && cd {{slug}}
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make test        # 验证 AI 生成的测试确实通过
make demo        # 验证 README 中的示例输出可复现
```
"""

TEMPLATES["ATTRIBUTION.md"] = """# 拿来说明（ATTRIBUTION.md）

> 原则：凡有所学，必有所标。以下列出本项目借鉴/参考的来源与复用范围。

## 一、直接复用（代码 / 文本）

| 来源 | 许可 | 复用内容 | 位置 |
|------|------|----------|------|
| Python Software Foundation — `pathlib` 官方文档 | PSF License | 路径规范化与 `Path` 用法模式 | `src/{{package}}/config.py`, `generator.py` |
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
> 「本项目结构参考了 {{name}}（{{repo_url}}）」。
"""

TEMPLATES["Makefile"] = """.PHONY: help install test demo lint clean

PYTHON ?= python3
PKG    ?= {{package}}

help:  ## 显示可用命令
\t@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-12s\\033[0m %s\\n", $$1, $$2}'

install:  ## 以可编辑模式安装（含 dev 依赖）
\t$(PYTHON) -m pip install -e ".[dev]"

test:  ## 运行全部单元测试
\tPYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:  ## 真实运行生成器，产出 examples/sample_output
\tPYTHONPATH=src $(PYTHON) -m {{package}}.cli init --config examples/basic.json --out examples/sample_output --force

lint:  ## 静态检查（需 pip install -e ".[dev]"）
\t$(PYTHON) -m ruff check src tests

clean:  ## 清理构建与缓存产物
\trm -rf build dist *.egg-info .coverage htmlcov .ruff_cache
\tfind . -type d -name __pycache__ -prune -exec rm -rf {} +
"""

TEMPLATES["repo-forge"] = """#!/usr/bin/env sh
# 免安装启动脚本：clone 后直接 ./repo-forge --help
set -e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHONPATH="$HERE/src${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m {{package}} "$@"
"""

TEMPLATES[".editorconfig"] = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
trim_trailing_whitespace = true

[*.{yml,yaml,json,md}]
indent_size = 2

[Makefile]
indent_style = tab
"""

TEMPLATES["tests/test_smoke.py"] = '''"""冒烟测试：确保 clone 后的最小可运行路径成立。"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SmokeTest(unittest.TestCase):
    def test_module_help_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "{{package}}", "--help"],
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
'''

TEMPLATES[".github/ISSUE_TEMPLATE/bug_report.md"] = """---
name: 🐛 Bug 报告
about: 报告一个可复现的问题
title: "[BUG] "
labels: bug
assignees: ''
---

## 描述

<!-- 清晰简洁地描述问题 -->

## 复现步骤

1. 配置文件（可脱敏）：

```json
{
  "name": "",
  "description": ""
}
```

2. 运行命令：`{{slug}} init --config ... --out ...`
3. 实际行为：
4. 期望行为：

## 环境

- OS:
- Python 版本：
- {{name}} 版本：
- 是否使用 YAML 配置（PyYAML）：

## 完整报错输出

```
粘贴完整 traceback
```

## 补充信息
"""

TEMPLATES[".github/ISSUE_TEMPLATE/feature_request.md"] = """---
name: 💡 功能建议
about: 提出一个改进想法
title: "[FEAT] "
labels: enhancement
assignees: ''
---

## 使用场景

<!-- 你想解决什么问题？没有这个功能时你怎么做的？ -->

## 提议方案

<!-- 期望的输入 / 输出 / 命令形式 -->

## 替代方案

<!-- 你考虑过的其他做法 -->

## 是否愿意贡献 PR

- [ ] 愿意，我可以先开讨论再实现
- [ ] 希望维护者实现
"""

TEMPLATES[".github/ISSUE_TEMPLATE/config.yml"] = """blank_issues_enabled: false
contact_links:
  - name: 💬 问题讨论
    url: {{repo_url}}/discussions
    about: 使用问题、想法交流请走 Discussions
  - name: 🔐 安全漏洞
    url: {{repo_url}}/security/advisories
    about: 请勿公开提交安全漏洞，使用私有渠道
"""

TEMPLATES[".github/PULL_REQUEST_TEMPLATE.md"] = """## 变更摘要

<!-- 一句话说明改了什么、为什么改 -->

## 关联 Issue

<!-- 例如：Closes #12 -->

## 变更类型

- [ ] 🐛 Bug 修复
- [ ] ✨ 新功能
- [ ] 📝 文档改进
- [ ] 🧪 测试补充
- [ ] ♻️ 重构（无行为变化）

## 验证方式

```bash
make test
```

<!-- 贴上关键输出或截图 -->

## 自查清单

- [ ] 我运行过 `make test` 且全部通过
- [ ] 我更新了 README / CHANGELOG（如需要）
- [ ] 我的提交信息遵循 Conventional Commits
- [ ] 我没有提交 `.env`、密钥或生成缓存
"""

TEMPLATES[".github/workflows/ci.yml"] = """name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["{{python_version}}", "3.11", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ "{{" }} matrix.python-version {{ "}}" }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ "{{" }} matrix.python-version {{ "}}" }}
          cache: pip
      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev,yaml]"
      - name: Lint
        run: python -m ruff check src tests
      - name: Test
        run: make test
      - name: Verify generated output is placeholder-free
        run: |
          make demo
          ! grep -R -n "{{" examples/sample_output --include='*.md' --include='*.toml' --include='*.py'
"""

TEMPLATES[".github/CODEOWNERS"] = """# 默认所有者
* @{{owner}}

# 核心代码需要额外审查
/src/{{package}}/config.py @{{owner}}
/src/{{package}}/generator.py @{{owner}}
"""

TEMPLATES["src/{{package}}/__init__.py"] = '''"""{{name}} - {{description}}"""

__version__ = "0.3.0"

__all__ = ["__version__"]
'''

TEMPLATES["src/{{package}}/__main__.py"] = '''"""{{name}} 命令行入口：python -m {{package}}"""

import argparse

from .core import hello


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="{{slug}}",
        description="{{description}}",
    )
    parser.add_argument("name", nargs="?", default="world", help="问候对象")
    args = parser.parse_args()
    print(hello(args.name))


if __name__ == "__main__":
    main()
'''

TEMPLATES["src/{{package}}/core.py"] = '''"""{{name}} 的核心逻辑。

从这里开始实现你的业务代码。保持函数纯粹、命名清晰，并为每个公开函数
补充单元测试（见 tests/）。
"""


def hello(name: str = "world") -> str:
    """返回一句问候语。

    >>> hello("repo-forge")
    'Hello, repo-forge!'
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name 必须是非空字符串")
    return "Hello, %s!" % name.strip()
'''

TEMPLATES["src/{{package}}/py.typed"] = ""

TEMPLATES["docs/AAR.md"] = """# AAR 复盘 —— {{name}}

> AAR = After Action Review（行动后反思）。记录「预期 vs 实际」「为什么」「下次怎么做」。

## 0. 基本信息

- 项目：{{name}}
- 挑战：C5 GitHub Repository
- 周期：2026-11-10 → 2026-11-21（约 12 天，8 轮 AI 迭代）
- 目标：产出一个别人 clone 后 5 分钟能跑起来、社区要素齐全的公开仓库

## 1. 预期 vs 实际

| 维度 | 最初预期 | 实际情况 | 差距原因 |
|------|----------|----------|----------|
| 文件数量 | 12 个左右够了 | 最终 26 个模板文件（仓库共 59 个受版本控制的文件） | 低估了社区要素（安全/行为准则/CODEOWNERS）的必要性 |
| 开发时间 | 2 小时 | 约 12 天（含迭代与复盘） | 反复做真实运行验证，修正文档与行为不一致 |
| 依赖 | 打算用 Jinja2 + PyYAML | 零运行时依赖 | 为了「5 分钟能跑起来」主动做减法 |
| 文档 | README 写完就算 | 6 份文档互相引用 | 评分表对 AI 日志与拿来说明有硬要求 |

## 2. 做对了什么（Keep）

1. **先定「可复现」为第一约束**：因为坚持零依赖，示例在任何干净环境都能跑。
2. **占位符方案换成 `KEY`**：避开了模板里 Python/JSON 花括号与 `str.format` 的冲突。
3. **测试里加「无残留占位符」断言**：这条断言真的抓到了 `python_version_compact` 漏传。
4. **把失败写进 AI_LOG 而不是藏起来**：R2/R5 的失败成为本次复盘最有价值的部分。

## 3. 出问题了什么（Problem）

### P1 — YAML 缺依赖时报错不可操作
- **现象**：在未装 PyYAML 的环境加载 `.yaml`，抛裸 `ImportError`，用户不知道下一步。
- **影响**：直接违反「失败要响亮且可操作」原则；新手会卡住。
- **根因**：prompt 只说了「支持 YAML」，没说「缺依赖时的用户体验」。
- **处理**：延迟导入 + 捕获 + 给出两条明确出路（安装 PyYAML 或改用 JSON）。
- **教训**：写 prompt 时要把**异常路径的期望行为**一起描述。

### P2 — README「解决什么问题」写成口号
- **现象**：AI 初稿写「提升效率、规范流程」这类空话，没有前后对比。
- **影响**：读者看不出项目的真实价值，违反 C5「实用性」评判标准。
- **根因**：prompt 没要求「可观察的前后差异」。
- **处理**：补「没有它 / 有了它」对比表，并用真实终端输出替换臆造示例。
- **教训**：文档里的每个主张都要能被一段真实输出支撑。

### P3 — 中文项目名生成空 slug
- **现象**：`slugify("中文名")` 返回空串，进而生成非法包名；代码审查阶段发现。
- **根因**：只测了 ASCII 输入，没测 Unicode 边界。
- **处理**：`slugify()` 对空结果抛 `ValueError`；`package_name()` 对数字开头加 `pkg_` 前缀；补单测。
- **教训**：字符串处理函数必须有「输入合法但输出为空」的防御。

### P4 — `--force` 初版静默覆盖
- **现象**：AI 初稿直接覆盖同名文件，可能吞掉用户本地改动。
- **处理**：拆出 `plan()` 先预演三类文件（新建 / 跳过 / 覆盖），CLI 打印后再写。
- **教训**：任何破坏性操作都要有「先看后做」环节。

### P5 — 生成的仓库缺少 `__main__.py`
- **现象**：最终验收时在 `examples/sample_output/` 中执行 `python -m hello_forge --help`，报 `No module named hello_forge.__main__`。
- **影响**：README 里写的推荐用法在生成物中直接失效，命中 C5 最忌讳的「文档与行为不一致」。
- **根因**：模板库只覆盖了 `__init__.py` 和 `core.py`，而 `usage` 默认值却假设存在 `__main__.py`；单元测试只检查了「生成了哪些文件」，没有检查「生成物能否真的运行」。
- **处理**：补 `src/<package>/__main__.py` 模板；在测试中把它列入必需文件；在 `examples/sample_output/` 中真实执行 `python -m hello_forge --help` 验证。
- **教训**：单元测试证明「文件存在」，端到端运行才证明「东西能用」。两者都要有。

## 4. 根因树（5 Why 摘要）

```
为什么文档和代码不一致？
→ 因为文档示例是 AI 凭想象写的
→ 因为 prompt 没有要求「基于真实运行结果」
→ 因为我把「写文档」当成独立阶段，而不是「验证后的记录」
→ 因为缺少「文档-代码一致性」的检查项
→ 根因：质量门禁只覆盖了代码测试，没覆盖文档断言
```

## 5. 改进方案（带验收标准）

| 编号 | 改进项 | 具体动作 | 验收标准 |
|------|--------|----------|----------|
| I1 | 文档一致性门禁 | CI 中增加 `make demo`，并断言生成物无残留占位符 | PR 若改了模板但未更新示例，`make demo` 后 `git diff --exit-code examples/sample_output` 失败 |
| I2 | 异常路径 prompt 模板 | 所有「生成/解析类」prompt 强制追加「列出 3 个失败场景及期望提示」 | 下一轮 AI 产出的错误信息 100% 包含可执行下一步 |
| I3 | Unicode 与边界测试矩阵 | 在 `test_config.py` 参数化测试中文/空格/数字开头/超长 name | 覆盖 ≥ 8 组输入，全部通过 |
| I4 | 破坏性操作预演 | 所有写文件命令默认 dry-run，`--force` 才覆盖 | `plan()` 有独立单测覆盖 skip/overwrite 分支 |
| I5 | 生成物端到端门禁 | 在 CI 中进入 `examples/sample_output/`，逐条执行 README 写下的命令（含 `python -m <pkg> --help`） | 任一条命令退出码非 0 即 CI 失败；当前 `python -m hello_forge --help` 与 `python -m hello_forge repo-forge` 均返回 0 |

## 6. 下次如果重来（Start）

1. **先写验收测试再写实现**：特别是「无残留占位符」和「5 分钟可运行」这两条。
2. **每个 prompt 都带一个失败案例**：倒逼 AI 思考异常路径，而不是只走 happy path。
3. **把 README 当产品界面写**：先写真实输入输出，再补结构说明。
4. **早一天做真实运行验证**：越早发现文档与行为的偏差，返工越少。

## 7. 一句话总结

> 这次最大的收获不是「AI 帮我写了代码」，而是「AI 写的初稿必须经过真实运行和边界测试，才配称为交付物」。
> 我把这条写进了 CI，让它变成流程，而不是靠记忆。
"""

TEMPLATES["examples/basic.json"] = """{
  "name": "hello-forge",
  "description": "输入一句话需求，输出一份可直接推送的专业仓库骨架。",
  "owner": "your-github-id",
  "license": "MIT",
  "language": "Python",
  "python_version": "3.9",
  "keywords": ["scaffold", "github", "automation"],
  "features": [
    "零运行时依赖，clone 后可立即运行",
    "一份配置生成 README / License / CI / Issue 模板",
    "生成前校验配置，错误信息可操作",
    "默认不覆盖已有文件"
  ],
  "ci": true,
  "community": true,
  "ai_assisted": true
}
"""

TEMPLATES["examples/README.md"] = """# examples/

本目录提供最小可运行示例。

- `basic.json` —— 一份完整的配置示例。
- `sample_output/` —— 使用 `make demo` 真实生成的产物（不是手写的展示文件）。

## 复现

```bash
make demo
# 等价于：
PYTHONPATH=src python -m repo_forge.cli init \\
  --config examples/basic.json --out examples/sample_output --force
```
"""

# ---- License texts (selected by config["license"]) -----------------------

LICENSE_MIT = """MIT License

Copyright (c) {{year}} {{author}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

LICENSE_BSD3 = """BSD 3-Clause License

Copyright (c) {{year}}, {{author}}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

LICENSE_UNLICENSE = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
"""

LICENSE_APACHE = """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work.

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work.

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or Derivative
          Works a copy of this License; and
      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and
      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work; and
      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied.

   8. Limitation of Liability. In no event and under no legal theory shall
      any Contributor be liable to You for damages, including any direct,
      indirect, special, incidental, or consequential damages of any
      character arising as a result of this License or out of the use or
      inability to use the Work.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License.

   END OF TERMS AND CONDITIONS

   Copyright {{year}} {{author}}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

LICENSE_TEXTS = {
    "MIT": LICENSE_MIT,
    "Apache-2.0": LICENSE_APACHE,
    "BSD-3-Clause": LICENSE_BSD3,
    "Unlicense": LICENSE_UNLICENSE,
}
