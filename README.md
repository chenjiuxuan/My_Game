# My_Game - 文字冒险/交互式故事游戏

一个基于 Python 的文字冒险/交互式故事游戏，具有完整的场景系统、玩家管理和战斗机制。

## 功能特点

### 🎮 游戏系统
- **场景系统**：支持房间场景和战斗场景，包含丰富的环境描述和交互元素
- **玩家管理**：完整的属性系统（力量、敏捷、智力、体质）、装备和物品管理
- **战斗机制**：回合制战斗系统，包含敌人属性、攻击、防御和技能
- **存档功能**：支持游戏进度的保存和加载
- **彩色界面**：控制台支持彩色输出，提供更好的视觉体验

### 🎯 游戏内容
- 5个精心设计的场景：村庄入口、森林小径、森林空地、小酒馆和森林洞穴
- 多种角色交互：卫兵、村民、商人、老巫师等
- 丰富的物品系统：木剑、回复药水、金币、麦酒等
- 战斗敌人：巨魔（具有独特的攻击和防御属性）

## 快速开始

### 1. 安装依赖
```bash
# 克隆仓库
git clone https://github.com/chenjiuxuan/My_Game.git
cd My_Game

# 创建虚拟环境（可选但推荐）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements-dev.txt
```

### 2. 运行游戏
```bash
# 方法1：直接运行
python -m src.my_game

# 方法2：从源代码运行
python -m pip install -e .
my_game
```

## 游戏命令

### 移动命令
- `north` 或 `n` - 向北移动
- `south` 或 `s` - 向南移动
- `east` 或 `e` - 向东移动
- `west` 或 `w` - 向西移动

### 交互命令
- `look` 或 `l` - 查看当前场景信息
- `status` 或 `stat` - 查看玩家状态
- `inventory` 或 `i` - 查看背包内容
- `pick <物品名>` - 捡起物品
- `drop <物品名>` - 丢弃物品
- `use <物品名>` - 使用物品

### 系统命令
- `save [文件名]` - 保存游戏进度（默认 savegame.json）
- `load [文件名]` - 加载游戏进度（默认 savegame.json）
- `help` - 显示帮助信息
- `quit` 或 `exit` - 退出游戏

## 游戏场景

### 1. 村庄入口（entrance）
- **描述**：宁静的村庄入口，有卫兵巡逻
- **连接场景**：森林小径（东）、小酒馆（西）
- **物品**：金币
- **角色**：卫兵

### 2. 森林小径（forest_path）
- **描述**：蜿蜒的森林小径，树木茂密
- **连接场景**：村庄入口（西）、森林空地（东）
- **物品**：回复药水
- **角色**：松鼠

### 3. 森林空地（forest_clearing）
- **描述**：开阔的森林空地，中央有古老橡树
- **连接场景**：森林小径（西）、森林洞穴（东）
- **物品**：蘑菇、草药
- **角色**：老巫师

### 4. 小酒馆（tavern）
- **描述**：温暖的酒馆，弥漫着麦酒和烤面包的香气
- **连接场景**：村庄入口（东）
- **物品**：麦酒、烤面包
- **角色**：调酒师、村民

### 5. 森林洞穴（forest_cave）
- **描述**：黑暗的洞穴，充满危险
- **连接场景**：森林空地（西）
- **敌人**：巨魔（生命值：50，攻击力：5，防御力：2）

## 开发信息

### 项目结构
```
My_Game/
├── src/my_game/
│   ├── core/              # 核心游戏逻辑
│   │   ├── game.py        # 游戏主循环和控制中心
│   │   ├── player.py      # 玩家系统实现
│   │   └── scene.py       # 场景系统实现
│   ├── data/              # 数据管理
│   │   └── save_load.py   # 存档系统实现
│   ├── ui/                # 用户界面
│   │   └── console.py     # 控制台用户界面
│   └── __init__.py        # 游戏入口和场景配置
├── tests/                 # 测试文件
│   ├── test_player.py     # 玩家系统测试
│   ├── test_scene.py      # 场景系统测试
│   └── test_smoke.py      # 基础测试
├── requirements-dev.txt   # 开发依赖
├── pyproject.toml         # 项目配置
└── README.md              # 项目文档
```

### 测试
```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_player.py

# 运行单个测试函数
pytest tests/test_player.py::TestPlayerInitialization::test_basic_initialization

# 显示详细测试输出
pytest -v
```

### 代码质量检查
```bash
# 运行 Ruff 检查
ruff check src/ tests/

# 自动修复 Ruff 问题
ruff check --fix src/ tests/

# 运行 Ruff 格式化
ruff format src/ tests/

# 完整代码质量检查
pre-commit run --all-files
```

## 学习要点

该项目展示了以下 Python 编程概念：
- 面向对象编程（OOP）设计
- 游戏开发架构
- 控制台界面设计
- 文件操作和数据序列化
- 异常处理
- 测试驱动开发（TDD）

## 许可证

[MIT License](LICENSE) - 详见 LICENSE 文件
