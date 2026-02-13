```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## 项目概述

这是一个名为 `my_game` 的 Python 项目，目前处于早期开发阶段。项目包含基本的 CI 配置和测试基础设施。

## 常用命令

### 开发环境

- **创建虚拟环境**: `python -m venv .venv`
- **激活虚拟环境**:
  - Windows: `.venv\Scripts\activate`
  - Unix/macOS: `source .venv/bin/activate`
- **安装依赖**: `pip install -r requirements-dev.txt`

### 代码质量

- **运行 Ruff 检查**: `ruff check src/ tests/`
- **自动修复 Ruff 问题**: `ruff check --fix src/ tests/`
- **运行 Ruff 格式化**: `ruff format src/ tests/`
- **完整代码质量检查 (pre-commit)**: `pre-commit run --all-files`

### 测试

- **运行所有测试**: `pytest`
- **运行单个测试文件**: `pytest tests/test_smoke.py`
- **运行单个测试函数**: `pytest tests/test_smoke.py::test_smoke`
- **显示详细测试输出**: `pytest -v`

## 项目结构

```
My_Game/
├── .github/              # GitHub 相关配置 (ISSUE_TEMPLATE, PR 模板等)
│   └── workflows/
│       └── ci.yml        # CI/CD 配置文件
├── .claude/
│   └── settings.local.json  # Claude Code 权限配置
├── src/
│   └── my_game/          # 主源代码目录
│       └── __init__.py   # 包入口文件 (当前仅打印 "hello world")
├── tests/
│   └── test_smoke.py     # 基础烟雾测试
├── .pre-commit-config.yaml  # pre-commit 钩子配置
├── pyproject.toml        # 项目配置文件 (Ruff 和 pytest 配置)
├── requirements-dev.txt  # 开发依赖
└── README.md             # 项目说明文档
```

## 代码规范

- 使用 Ruff 进行代码检查和格式化
- Ruff 配置在 `pyproject.toml` 中，包含:
  - 行长度限制: 100 字符
  - Python 目标版本: 3.10+
- pre-commit 钩子包括:
  - Ruff 检查和自动修复
  - Ruff 代码格式化
  - 尾随空格和文件结束符检查

## CI/CD

项目已配置 GitHub CI 流水线，位于 `.github/workflows/ci.yml`，包含以下功能:
- 支持 Python 3.10, 3.11, 3.12 版本
- 自动运行 Ruff 检查和格式化验证
- 自动运行 pytest 测试
- 依赖缓存优化

## 代码架构

项目采用简约的架构设计：

### 核心代码目录
- `src/my_game/` - 游戏的主要源代码目录，目前包含基础包结构
  - `__init__.py` - 包入口点，当前实现简单的 "hello world" 输出

### 测试目录
- `tests/` - 包含项目的测试文件
  - `test_smoke.py` - 基础烟雾测试，验证简单的数学运算

### 关键技术栈
- **语言**: Python 3.10+
- **代码检查**: Ruff 0.6.9
- **测试框架**: pytest 8.3.3
- **版本控制**: Git

## 测试

目前只有一个简单的烟雾测试 `test_smoke.py`，它验证 `1 + 1 == 2`。
