"""
玩家系统模块 - 管理角色状态、属性和物品。
"""

from typing import List, Dict


class Player:
    """
    玩家类 - 管理角色状态、属性和物品。
    """

    def __init__(
        self,
        name: str = "冒险者",
        health: int = 100,
        max_health: int = 100,
        experience: int = 0,
        level: int = 1,
        money: int = 0,
    ):
        """
        初始化玩家对象。

        Args:
            name: 角色名称
            health: 当前生命值
            max_health: 最大生命值
            experience: 经验值
            level: 等级
            money: 金币数量
        """
        self.name = name
        self.health = health
        self.max_health = max_health
        self.experience = experience
        self.level = level
        self.money = money
        self.inventory: List[str] = []
        self.equipment: Dict[str, str] = {
            "weapon": "",
            "armor": "",
            "helmet": "",
            "boots": "",
        }
        self.stats: Dict[str, int] = {
            "strength": 10,
            "dexterity": 10,
            "intelligence": 10,
            "constitution": 10,
        }

    def get_health_percentage(self) -> float:
        """计算当前生命值百分比。"""
        return (self.health / self.max_health) * 100

    def is_alive(self) -> bool:
        """检查玩家是否存活。"""
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        """
        受到伤害。

        Args:
            damage: 伤害值
        """
        self.health = max(0, self.health - damage)

    def heal(self, amount: int) -> None:
        """
        恢复生命值。

        Args:
            amount: 恢复量
        """
        self.health = min(self.max_health, self.health + amount)

    def add_experience(self, amount: int) -> bool:
        """
        增加经验值，可能会升级。

        Args:
            amount: 经验值数量

        Returns:
            是否升级
        """
        self.experience += amount
        leveled_up = False
        while self.experience >= self._get_required_experience():
            self._level_up()
            leveled_up = True
        return leveled_up

    def _get_required_experience(self) -> int:
        """计算当前等级升级所需经验值。"""
        return 100 * (self.level**2)

    def _level_up(self) -> None:
        """升级处理。"""
        self.level += 1
        self.experience -= 100 * ((self.level - 1) ** 2)  # 减去升级前等级所需的经验值
        self.max_health += 20
        self.health = self.max_health
        for stat in self.stats:
            self.stats[stat] += 2
        print(f"恭喜！你升到了 {self.level} 级！")

    def add_item(self, item: str) -> None:
        """
        添加物品到背包。

        Args:
            item: 物品名称
        """
        self.inventory.append(item)

    def remove_item(self, item: str) -> bool:
        """
        从背包移除物品。

        Args:
            item: 物品名称

        Returns:
            是否成功移除
        """
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        """
        检查是否拥有物品。

        Args:
            item: 物品名称

        Returns:
            是否拥有该物品
        """
        return item in self.inventory

    def equip_item(self, item: str, slot: str) -> bool:
        """
        装备物品。

        Args:
            item: 物品名称
            slot: 装备槽（weapon, armor, helmet, boots）

        Returns:
            是否成功装备
        """
        if item in self.inventory and slot in self.equipment:
            # 如果已有装备，先卸下放入背包
            if self.equipment[slot]:
                self.inventory.append(self.equipment[slot])
            # 装备新物品
            self.equipment[slot] = item
            self.inventory.remove(item)
            return True
        return False

    def unequip_item(self, slot: str) -> bool:
        """
        卸下装备。

        Args:
            slot: 装备槽（weapon, armor, helmet, boots）

        Returns:
            是否成功卸下
        """
        if slot in self.equipment and self.equipment[slot]:
            self.inventory.append(self.equipment[slot])
            self.equipment[slot] = ""
            return True
        return False

    def get_strength(self) -> int:
        """获取力量属性（包括装备加成）。"""
        return self.stats["strength"] + self._get_equipment_bonus("strength")

    def get_dexterity(self) -> int:
        """获取敏捷属性（包括装备加成）。"""
        return self.stats["dexterity"] + self._get_equipment_bonus("dexterity")

    def get_intelligence(self) -> int:
        """获取智力属性（包括装备加成）。"""
        return self.stats["intelligence"] + self._get_equipment_bonus("intelligence")

    def get_constitution(self) -> int:
        """获取体质属性（包括装备加成）。"""
        return self.stats["constitution"] + self._get_equipment_bonus("constitution")

    def _get_equipment_bonus(self, stat: str) -> int:
        """计算装备对属性的加成。"""
        # 简单的装备加成系统示例
        bonuses = {
            "weapon": {"strength": 5},
            "armor": {"constitution": 5},
            "helmet": {"intelligence": 3},
            "boots": {"dexterity": 3},
        }

        bonus = 0
        for slot, item in self.equipment.items():
            if item and slot in bonuses and stat in bonuses[slot]:
                bonus += bonuses[slot][stat]
        return bonus

    def get_attack_power(self) -> int:
        """计算攻击力（基于力量和武器）。"""
        base_attack = self.get_strength()
        weapon_bonus = 5 if self.equipment["weapon"] else 0
        return base_attack + weapon_bonus

    def get_defense(self) -> int:
        """计算防御力（基于体质和防具）。"""
        base_defense = self.get_constitution()
        armor_bonus = 5 if self.equipment["armor"] else 0
        helmet_bonus = 2 if self.equipment["helmet"] else 0
        boots_bonus = 1 if self.equipment["boots"] else 0
        return base_defense + armor_bonus + helmet_bonus + boots_bonus

    def get_inventory_info(self) -> str:
        """获取背包信息字符串。"""
        if not self.inventory:
            return "背包是空的。"
        return "背包中的物品: " + ", ".join(self.inventory)

    def get_equipment_info(self) -> str:
        """获取装备信息字符串。"""
        info = ""
        for slot, item in self.equipment.items():
            info += f"{slot.capitalize()}: {item if item else '无'}\n"
        return info.strip()

    def get_status_info(self) -> str:
        """获取玩家状态信息。"""
        health_bar = (
            "["
            + "=" * int(self.get_health_percentage() / 10)
            + " " * int(10 - self.get_health_percentage() / 10)
            + "]"
        )
        info = f"""
{self.name} (等级 {self.level})
生命值: {self.health}/{self.max_health} {health_bar}
经验值: {self.experience}/{self._get_required_experience()}
金币: {self.money}

属性:
力量: {self.get_strength()} ({self.stats['strength']} + 装备加成)
敏捷: {self.get_dexterity()} ({self.stats['dexterity']} + 装备加成)
智力: {self.get_intelligence()} ({self.stats['intelligence']} + 装备加成)
体质: {self.get_constitution()} ({self.stats['constitution']} + 装备加成)

攻击力: {self.get_attack_power()}
防御力: {self.get_defense()}

{self.get_equipment_info()}

{self.get_inventory_info()}
"""
        return info.strip()
