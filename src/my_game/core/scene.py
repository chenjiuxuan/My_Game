"""
场景系统模块 - 定义游戏场景的抽象基类和接口。

场景是游戏中的基本单位，包含位置描述、可交互对象和导航选项。
支持多种场景类型，如房间、战斗、谜题等。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class Scene(ABC):
    """场景抽象基类。"""

    def __init__(
        self,
        scene_id: str,
        name: str,
        description: str,
        connections: Dict[str, str] = None,
    ):
        """
        初始化场景。

        Args:
            scene_id: 场景唯一标识符
            name: 场景名称
            description: 场景详细描述
            connections: 场景连接字典，格式为 {方向: 目标场景ID}
        """
        self.scene_id = scene_id
        self.name = name
        self.description = description
        self.connections = connections or {}
        self.items: List[str] = []
        self.characters: List[str] = []

    @abstractmethod
    def enter(self, player: Any) -> None:
        """进入场景时的操作。"""
        pass

    @abstractmethod
    def exit(self, player: Any) -> None:
        """离开场景时的操作。"""
        pass

    def add_item(self, item_name: str) -> None:
        """添加物品到场景中。"""
        if item_name not in self.items:
            self.items.append(item_name)

    def remove_item(self, item_name: str) -> None:
        """从场景中移除物品。"""
        if item_name in self.items:
            self.items.remove(item_name)

    def add_character(self, character_name: str) -> None:
        """添加角色到场景中。"""
        if character_name not in self.characters:
            self.characters.append(character_name)

    def remove_character(self, character_name: str) -> None:
        """从场景中移除角色。"""
        if character_name in self.characters:
            self.characters.remove(character_name)

    def get_connection(self, direction: str) -> Optional[str]:
        """
        获取指定方向的连接场景ID。

        Args:
            direction: 方向（如 'north', 'east', 'west', 'south' 等）

        Returns:
            目标场景ID，如果没有连接则返回 None
        """
        return self.connections.get(direction.lower())


class RoomScene(Scene):
    """普通房间场景类。"""

    def __init__(
        self,
        scene_id: str,
        name: str,
        description: str,
        connections: Dict[str, str] = None,
        items: List[str] = None,
        characters: List[str] = None,
    ):
        """
        初始化房间场景。

        Args:
            scene_id: 场景唯一标识符
            name: 场景名称
            description: 场景详细描述
            connections: 场景连接字典，格式为 {方向: 目标场景ID}
            items: 场景中的物品列表
            characters: 场景中的角色列表
        """
        super().__init__(scene_id, name, description, connections)
        if items:
            for item in items:
                self.add_item(item)
        if characters:
            for character in characters:
                self.add_character(character)

    def enter(self, player: Any) -> None:
        """进入房间场景。"""
        print(f"你进入了 {self.name}")

    def exit(self, player: Any) -> None:
        """离开房间场景。"""
        print(f"你离开了 {self.name}")

    def get_info(self) -> str:
        """获取房间详细信息。"""
        info = f"\n{self.name}\n{'='*len(self.name)}\n"
        info += f"{self.description}\n"

        if self.connections:
            info += "\n连接的方向: "
            info += ", ".join(self.connections.keys())

        if self.items:
            info += "\n房间中的物品: "
            info += ", ".join(self.items)

        if self.characters:
            info += "\n房间中的角色: "
            info += ", ".join(self.characters)

        return info


class CombatScene(Scene):
    """战斗场景类。"""

    def __init__(
        self,
        scene_id: str,
        name: str,
        description: str,
        enemy: str,
        enemy_stats: Dict[str, int],
        connections: Dict[str, str] = None,
    ):
        """
        初始化战斗场景。

        Args:
            scene_id: 场景唯一标识符
            name: 场景名称
            description: 场景详细描述
            enemy: 敌人名称
            enemy_stats: 敌人属性字典
            connections: 场景连接字典，格式为 {方向: 目标场景ID}
        """
        super().__init__(scene_id, name, description, connections)
        self.enemy = enemy
        self.enemy_stats = enemy_stats
        self.combat_active = True

    def enter(self, player: Any) -> None:
        """进入战斗场景。"""
        print(f"你进入了 {self.name}")
        print(f"注意！{self.enemy} 出现了！")
        self.combat_active = True

    def exit(self, player: Any) -> None:
        """离开战斗场景。"""
        print(f"战斗结束，你离开了 {self.name}")

    def end_combat(self) -> None:
        """结束战斗。"""
        self.combat_active = False

    def get_enemy_info(self) -> str:
        """获取敌人信息。"""
        info = f"\n敌人: {self.enemy}"
        for stat, value in self.enemy_stats.items():
            info += f"\n{stat}: {value}"
        return info
