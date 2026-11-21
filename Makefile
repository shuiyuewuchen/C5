.PHONY: help install test demo lint clean

PYTHON ?= python3
PKG    ?= repo_forge

help:  ## 显示可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install:  ## 以可编辑模式安装（含 dev 依赖）
	$(PYTHON) -m pip install -e ".[dev]"

test:  ## 运行全部单元测试
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:  ## 真实运行生成器，产出 examples/sample_output
	PYTHONPATH=src $(PYTHON) -m repo_forge.cli init --config examples/basic.json --out examples/sample_output --force

lint:  ## 静态检查（需 pip install -e ".[dev]"）
	$(PYTHON) -m ruff check src tests

clean:  ## 清理构建与缓存产物
	rm -rf build dist *.egg-info .coverage htmlcov .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
