```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## 项目概述

这是一个名为 `my_game` 的 Python 项目，目前处于早期开发阶段。项目包含一个功能完整的计算器模块和全面的测试基础设施，同时为游戏开发奠定了基础。

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
- **运行单个测试文件**: `pytest tests/test_smoke.py` 或 `pytest tests/test_calculator.py`
- **运行单个测试函数**: `pytest tests/test_calculator.py::TestCalculator::test_add_positive_numbers`
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
│       ├── __init__.py   # 包入口文件 (当前仅打印 "hello world")
│       └── calculator.py # 功能完整的计算器模块，包含故意设置的 bug 用于测试
├── src/my_game.egg-info/ # Python 包元数据目录
├── tests/
│   ├── test_smoke.py     # 基础烟雾测试
│   └── test_calculator.py # 计算器模块的详细测试，包含对故意设置的 bug 的测试
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
- `src/my_game/` - 游戏的主要源代码目录，目前包含计算器模块
  - `__init__.py` - 包入口点，当前实现简单的 "hello world" 输出
  - `calculator.py` - 功能完整的计算器模块，包含基础运算、高级运算和统计功能

### 测试目录
- `tests/` - 包含项目的测试文件
  - `test_smoke.py` - 基础烟雾测试，验证简单的数学运算
  - `test_calculator.py` - 计算器模块的详细测试，包含对故意设置的 bug 的测试

### 关键技术栈
- **语言**: Python 3.10+
- **代码检查**: Ruff 0.6.9
- **测试框架**: pytest 8.3.3
- **版本控制**: Git

## 测试

项目包含全面的测试基础设施：
- **基础测试**: `test_smoke.py` 验证简单数学运算
- **详细测试**: `test_calculator.py` 包含 150+ 行测试代码，测试计算器模块的每个功能
- **边界条件测试**: 包含对异常处理和边界条件的测试
- **故意设置的 bug 测试**: 对 calculator.py 中故意设置的 bug 的测试

## 代码功能概述

### calculator.py 主要功能

1. **基础运算**: 加法、减法、乘法、除法
2. **高级运算**: 幂运算、阶乘
3. **统计功能**: 计算平均值、找到最大值
4. **异常处理**: 对无效输入和边界条件的处理

### 故意设置的 bug (用于测试目的)

- 除法函数缺少对除数为零的检查
- 幂运算对负指数的处理有缺陷
- 阶乘函数缺少对负数的检查
- 计算平均值函数缺少对空列表的检查
- 找到最大值函数在空列表情况下返回 None 而不是抛出异常
