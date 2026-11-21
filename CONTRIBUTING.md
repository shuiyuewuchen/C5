# 贡献指南

感谢你愿意让 repo-forge 变得更好！本项目欢迎 bug 报告、文档改进、新模板与代码贡献。

## 开始之前

1. 先搜一下 [已有 Issue](https://github.com/shuiyuewuchen/C5/issues)，避免重复。
2. 大改动请先开 Issue 讨论方案，避免白做。
3. 遵守 [行为准则](./CODE_OF_CONDUCT.md)。

## 本地开发环境

```bash
git clone https://github.com/shuiyuewuchen/C5.git
cd C5
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

模板集中在 `src/repo_forge/templates.py` 的 `TEMPLATES` 字典中：

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
