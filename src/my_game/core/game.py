"""
游戏主循环和控制中心模块 - 协调整个游戏流程。
"""

from typing import Dict
from src.my_game.core.player import Player
from src.my_game.core.scene import Scene
from src.my_game.ui.console import ConsoleInterface
from src.my_game.data.save_load import save_game, load_game


class Game:
    """游戏控制中心类。"""

    def __init__(self):
        """初始化游戏对象。"""
        self.player: Player = None
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: str = ""
        self.ui = ConsoleInterface()
        self.is_running: bool = False

    def initialize_player(self, name: str = "冒险者") -> None:
        """
        初始化玩家角色。

        Args:
            name: 玩家名称
        """
        self.player = Player(name)
        # 给玩家一些初始物品
        initial_items = ["木剑", "布衣", "回复药水"]
        for item in initial_items:
            self.player.add_item(item)

        # 自动装备初始物品
        if "木剑" in self.player.inventory:
            self.player.equip_item("木剑", "weapon")
        if "布衣" in self.player.inventory:
            self.player.equip_item("布衣", "armor")

    def add_scene(self, scene: Scene) -> None:
        """
        添加场景到游戏中。

        Args:
            scene: 场景对象
        """
        self.scenes[scene.scene_id] = scene

    def set_initial_scene(self, scene_id: str) -> None:
        """
        设置游戏初始场景。

        Args:
            scene_id: 初始场景ID
        """
        if scene_id in self.scenes:
            self.current_scene = scene_id

    def get_current_scene(self) -> Scene:
        """获取当前场景对象。"""
        return self.scenes[self.current_scene]

    def navigate(self, direction: str) -> bool:
        """
        导航到其他场景。

        Args:
            direction: 移动方向

        Returns:
            是否成功导航
        """
        current_scene = self.get_current_scene()
        next_scene_id = current_scene.get_connection(direction)

        if next_scene_id and next_scene_id in self.scenes:
            current_scene.exit(self.player)
            self.current_scene = next_scene_id
            self.get_current_scene().enter(self.player)
            return True

        self.ui.print_error("无法向该方向移动")
        return False

    def look_around(self) -> None:
        """查看当前场景信息。"""
        current_scene = self.get_current_scene()
        self.ui.print_scene_info(current_scene)

    def show_inventory(self) -> None:
        """显示玩家背包。"""
        self.ui.print_inventory(self.player)

    def show_status(self) -> None:
        """显示玩家状态。"""
        self.ui.print_status(self.player)

    def pick_up_item(self, item_name: str) -> bool:
        """
        捡起场景中的物品。

        Args:
            item_name: 物品名称

        Returns:
            是否成功捡起
        """
        current_scene = self.get_current_scene()
        if item_name in current_scene.items:
            current_scene.remove_item(item_name)
            self.player.add_item(item_name)
            self.ui.print_success(f"你捡起了 {item_name}")
            return True

        self.ui.print_error(f"场景中没有 {item_name}")
        return False

    def drop_item(self, item_name: str) -> bool:
        """
        丢弃物品到场景中。

        Args:
            item_name: 物品名称

        Returns:
            是否成功丢弃
        """
        if self.player.remove_item(item_name):
            current_scene = self.get_current_scene()
            current_scene.add_item(item_name)
            self.ui.print_success(f"你丢弃了 {item_name}")
            return True

        self.ui.print_error(f"你没有 {item_name}")
        return False

    def use_item(self, item_name: str) -> bool:
        """
        使用物品。

        Args:
            item_name: 物品名称

        Returns:
            是否成功使用
        """
        if item_name in self.player.inventory:
            if item_name == "回复药水":
                self.player.heal(50)
                self.player.remove_item(item_name)
                self.ui.print_success("你使用了回复药水，恢复了 50 点生命值")
                return True

        self.ui.print_error(f"{item_name} 无法使用")
        return False

    def save_game(self, filename: str = "savegame.json") -> bool:
        """
        保存游戏进度。

        Args:
            filename: 存档文件名

        Returns:
            是否成功保存
        """
        try:
            save_game(self, filename)
            self.ui.print_success(f"游戏已保存到 {filename}")
            return True
        except Exception as e:
            self.ui.print_error(f"保存失败: {str(e)}")
            return False

    def load_game(self, filename: str = "savegame.json") -> bool:
        """
        加载游戏进度。

        Args:
            filename: 存档文件名

        Returns:
            是否成功加载
        """
        try:
            loaded_game = load_game(filename)
            if loaded_game:
                self.__dict__.update(loaded_game.__dict__)
                self.ui.print_success(f"游戏已从 {filename} 加载")
                return True
        except Exception as e:
            self.ui.print_error(f"加载失败: {str(e)}")
        return False

    def start(self) -> None:
        """启动游戏主循环。"""
        self.is_running = True
        self.ui.print_welcome()
        self.get_current_scene().enter(self.player)
        self.look_around()

        while self.is_running:
            self.ui.print_prompt()
            command = input("> ").strip()

            if not command:
                continue

            self.handle_command(command)

    def handle_command(self, command: str) -> None:
        """
        处理玩家命令。

        Args:
            command: 玩家输入的命令
        """
        command_parts = command.split()
        main_command = command_parts[0].lower()

        # 移动命令
        if main_command in ["north", "n"]:
            self.navigate("north")
            self.look_around()
        elif main_command in ["south", "s"]:
            self.navigate("south")
            self.look_around()
        elif main_command in ["east", "e"]:
            self.navigate("east")
            self.look_around()
        elif main_command in ["west", "w"]:
            self.navigate("west")
            self.look_around()

        # 交互命令
        elif main_command in ["look", "l"]:
            self.look_around()
        elif main_command in ["inventory", "i"]:
            self.show_inventory()
        elif main_command in ["status", "stat", "s"]:
            self.show_status()
        elif main_command in ["pick", "take"]:
            if len(command_parts) > 1:
                item_name = " ".join(command_parts[1:])
                self.pick_up_item(item_name)
            else:
                self.ui.print_error("请指定要捡起的物品")
        elif main_command in ["drop"]:
            if len(command_parts) > 1:
                item_name = " ".join(command_parts[1:])
                self.drop_item(item_name)
            else:
                self.ui.print_error("请指定要丢弃的物品")
        elif main_command in ["use"]:
            if len(command_parts) > 1:
                item_name = " ".join(command_parts[1:])
                self.use_item(item_name)
            else:
                self.ui.print_error("请指定要使用的物品")

        # 系统命令
        elif main_command in ["save"]:
            filename = command_parts[1] if len(command_parts) > 1 else "savegame.json"
            self.save_game(filename)
        elif main_command in ["load"]:
            filename = command_parts[1] if len(command_parts) > 1 else "savegame.json"
            self.load_game(filename)
        elif main_command in ["help"]:
            self.show_help()
        elif main_command in ["quit", "exit"]:
            self.quit_game()

        # 未识别命令
        else:
            self.ui.print_error("未识别的命令，请使用 help 查看可用命令")

    def show_help(self) -> None:
        """显示帮助信息。"""
        self.ui.print_help()

    def quit_game(self) -> None:
        """退出游戏。"""
        self.is_running = False
        self.ui.print_goodbye()

    def handle_combat(self) -> bool:
        """
        处理战斗逻辑。

        Returns:
            是否成功处理（用于扩展）
        """
        current_scene = self.get_current_scene()
        if hasattr(current_scene, "combat_active") and current_scene.combat_active:
            self.ui.print_combat_info(current_scene)
            self.ui.print_status(self.player)
            return True
        return False
