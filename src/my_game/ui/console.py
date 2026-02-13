"""
控制台用户界面模块 - 处理游戏与用户之间的交互。
"""

from src.my_game.core.player import Player
from src.my_game.core.scene import Scene


class ConsoleInterface:
    """控制台用户界面类。"""

    def __init__(self):
        """初始化控制台界面。"""
        self.colors = {
            "reset": "\033[0m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "bold": "\033[1m",
        }
        # 尝试检测是否支持彩色输出（Windows 可能需要 colorama 包）
        try:
            import sys

            self.supports_color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        except Exception:
            self.supports_color = False

    def _colorize(self, text: str, color: str) -> str:
        """
        对文本进行着色（如果支持彩色输出）。

        Args:
            text: 原始文本
            color: 颜色代码

        Returns:
            着色后的文本
        """
        if self.supports_color and color in self.colors:
            return f"{self.colors[color]}{text}{self.colors['reset']}"
        return text

    def print_welcome(self) -> None:
        """打印游戏欢迎信息。"""
        welcome_text = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    欢迎来到文字冒险游戏！                                 ║
║    Welcome to Text Adventure Game!                        ║
║                                                           ║
║    在这个冒险中，你将探索神秘的地下城，与怪物战斗，        ║
║    寻找宝藏，揭示隐藏的秘密。                              ║
║                                                           ║
║    使用 'help' 命令查看可用命令列表。                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(welcome_text)

    def print_goodbye(self) -> None:
        """打印再见信息。"""
        print("\n感谢您的游戏！再见！")

    def print_prompt(self) -> None:
        """打印命令提示符。"""
        print("\n请输入命令:", end=" ")

    def print_scene_info(self, scene: Scene) -> None:
        """
        打印场景信息。

        Args:
            scene: 场景对象
        """
        if hasattr(scene, "get_info"):
            print(scene.get_info())
        else:
            print(f"\n{scene.name}")
            print(scene.description)

            if scene.connections:
                print("\n连接的方向: ", ", ".join(scene.connections.keys()))

    def print_status(self, player: Player) -> None:
        """
        打印玩家状态。

        Args:
            player: 玩家对象
        """
        print(player.get_status_info())

    def print_inventory(self, player: Player) -> None:
        """
        打印玩家背包。

        Args:
            player: 玩家对象
        """
        print(player.get_inventory_info())

    def print_combat_info(self, scene: Scene) -> None:
        """
        打印战斗信息。

        Args:
            scene: 战斗场景对象
        """
        if hasattr(scene, "get_enemy_info"):
            print(scene.get_enemy_info())

    def print_error(self, message: str) -> None:
        """
        打印错误信息。

        Args:
            message: 错误信息
        """
        print(self._colorize(f"❌ 错误: {message}", "red"))

    def print_success(self, message: str) -> None:
        """
        打印成功信息。

        Args:
            message: 成功信息
        """
        print(self._colorize(f"✅ 成功: {message}", "green"))

    def print_warning(self, message: str) -> None:
        """
        打印警告信息。

        Args:
            message: 警告信息
        """
        print(self._colorize(f"⚠️ 警告: {message}", "yellow"))

    def print_help(self) -> None:
        """打印帮助信息。"""
        help_text = """
可用命令列表:

移动命令:
  north (n)      向北移动
  south (s)      向南移动
  east (e)       向东移动
  west (w)       向西移动

交互命令:
  look (l)       查看当前场景信息
  status (stat)  查看玩家状态
  inventory (i)  查看背包
  pick <物品>    捡起物品（例如：pick 金币）
  drop <物品>    丢弃物品（例如：drop 木剑）
  use <物品>     使用物品（例如：use 回复药水）

系统命令:
  help           显示此帮助信息
  save [文件名]   保存游戏进度（默认文件名: savegame.json）
  load [文件名]   加载游戏进度（默认文件名: savegame.json）
  quit (exit)    退出游戏

示例:
  输入 'n' 或 'north' 向北移动
  输入 'pick 金币' 捡起金币
  输入 'use 回复药水' 使用回复药水
"""
        print(help_text)

    def print_combat_commands(self) -> None:
        """打印战斗命令。"""
        combat_text = """
战斗命令:
  attack (a)     攻击敌人
  defend (d)     防御，减少受到的伤害
  run (r)        尝试逃跑（可能失败）
  use <物品>     使用物品（例如：use 回复药水）
"""
        print(combat_text)

    def print_dialogue(self, speaker: str, text: str) -> None:
        """
        打印对话文本。

        Args:
            speaker: 说话者
            text: 对话内容
        """
        print(f"{self._colorize(speaker, 'cyan')}: {text}")

    def get_input(self, prompt: str = "请输入: ") -> str:
        """
        获取用户输入。

        Args:
            prompt: 输入提示

        Returns:
            用户输入的文本
        """
        return input(prompt).strip()

    def confirm_action(self, message: str) -> bool:
        """
        确认用户操作。

        Args:
            message: 确认信息

        Returns:
            用户是否确认
        """
        while True:
            response = input(f"{message} (y/n): ").lower().strip()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                self.print_error("请输入 y 或 n")

    def clear_screen(self) -> None:
        """清除控制台屏幕。"""
        import os

        os.system("cls" if os.name == "nt" else "clear")

    def print_separator(self, length: int = 50) -> None:
        """
        打印分隔线。

        Args:
            length: 分隔线长度
        """
        print("\n" + "-" * length + "\n")
