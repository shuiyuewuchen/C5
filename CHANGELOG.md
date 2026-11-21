# Changelog

All notable changes to this project are documented in this file.
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [0.3.0] - 2026-11-21

### Added
- 新增 `validate` 子命令：生成前先校验配置，错误就地报告。
- 新增 `--force` 选项：可控覆盖已有文件，避免误删用户改动。
- 新增 `repo_forge/py.typed`，声明 PEP 561 类型支持。
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

[0.3.0]: https://github.com/shuiyuewuchen/C5/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/shuiyuewuchen/C5/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shuiyuewuchen/C5/releases/tag/v0.1.0
