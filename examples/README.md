# examples/

本目录提供最小可运行示例。

- `basic.json` —— 一份完整的配置示例。
- `sample_output/` —— 使用 `make demo` 真实生成的产物（不是手写的展示文件）。

## 复现

```bash
make demo
# 等价于：
PYTHONPATH=src python -m repo_forge.cli init \
  --config examples/basic.json --out examples/sample_output --force
```
