#  hello-forge

> 输入一句话需求，输出一份可直接推送的仓库骨架。

[![CI](https://github.com/your-github-id/hello-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/your-github-id/hello-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

**一句话：输入 一份配置，输出 完整仓库骨架。**

---

## 解决什么问题

<!-- 为什么需要这个项目？没有它之前怎么做？有了它之后怎么做？ -->

手动搭建一个新项目时，README、License、.gitignore、Issue 模板、CI 配置每次都要重新写一遍，既费时间又容易遗漏。不同人写出来的仓库质量参差不齐，别人 clone 下来经常跑不起来。

hello-forge 把这套最佳实践固化成模板：只需要维护一份配置，就能生成结构一致、文档齐全、开箱即跑的仓库，让作者专注于代码本身。

| | 没有 hello-forge | 有了 hello-forge |
|---|---|---|
| 过程 | 手工重复、容易漏项、没有统一标准 | 一份配置，一次性生成完整结构 |
| 质量 | 靠记忆和运气 | 模板化 + 自动化测试兜底 |
| 协作 | 别人看不懂、跑不起来 | README / Issue 模板 / 贡献指南齐全 |

## 特性

- 零运行时依赖，clone 后可立即运行
- 一份配置生成 README / License / CI / Issue 模板
- 生成前校验配置，错误信息可操作
- 默认不覆盖已有文件

## 快速开始

> 前置要求：Python 3.9+，仅需标准库（YAML 配置为可选项）。

### 安装

```bash
git clone https://github.com/your-github-id/hello-forge.git
cd hello-forge
pip install -e .
```

也可以在克隆后**不安装**直接运行：

```bash
./repo-forge --help        # macOS / Linux
python -m repo_forge --help # 任意平台（需先 pip install -e .）
```

### 使用

```bash
python -m hello_forge --help
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
hello-forge/
├── README.md               # 本文件
├── LICENSE                 # MIT
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
│   └── hello_forge/
│       ├── __init__.py     # 包入口 / 版本号
│       ├── __main__.py     # python -m hello_forge
│       └── core.py         # 核心逻辑（按需扩展）
├── examples/
│   ├── basic.json
│   └── sample_output/      # 真实运行生成的示例产物
├── tests/                  # 单元测试（标准库 unittest）
└── .github/                # Issue / PR 模板 + CI workflow
```

## 技术栈

- 语言：Python 3.9+
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

MIT © 2026 your-github-id。详见 [LICENSE](./LICENSE)。

---

> 由 [repo-forge](https://github.com/your-github-id/hello-forge) 生成并维护。欢迎 star、fork、提 Issue。
