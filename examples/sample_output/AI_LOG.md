# AI 使用日志（AI_LOG.md）

> 项目：hello-forge ｜ 记录周期：2026-11-10 → 2026-11-21 ｜ 工具：WorkBuddy（AI 编程助手）

本项目遵循 Elite20「AI-First」原则。下表记录 AI 参与的**每一轮**工作，
包含原始 prompt 意图、AI 产出、人工审校与失败/修正记录，确保过程可追溯、可复现。

## 一、总览

| 阶段 | AI 怎么用 | 人工做了什么 | 对应产物 |
|------|-----------|--------------|----------|
| 项目初始化 | 生成 repo 骨架、`.gitignore`、目录结构建议 | 裁剪掉过度设计，确定 src-layout | 目录结构、`.gitignore` |
| 核心代码 | 编写 `config.py` / `generator.py` / `cli.py` 初稿 | 修正边界情况、补充错误信息 | `src/hello_forge/*.py` |
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
对本项目属于过度设计。手动裁剪掉冗余配置，最终确定 25 个模板文件；保留 Makefile 作为统一入口。

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
git clone https://github.com/your-github-id/hello-forge.git && cd hello-forge
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make test        # 验证 AI 生成的测试确实通过
make demo        # 验证 README 中的示例输出可复现
```
