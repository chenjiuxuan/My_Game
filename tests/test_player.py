"""
玩家系统测试模块。
"""

from src.my_game.core.player import Player


class TestPlayerInitialization:
    """测试玩家初始化"""

    def test_basic_initialization(self):
        """测试基本初始化"""
        player = Player("测试玩家")
        assert player.name == "测试玩家"
        assert player.health == 100
        assert player.max_health == 100
        assert player.experience == 0
        assert player.level == 1
        assert player.money == 0

    def test_custom_initialization(self):
        """测试自定义属性初始化"""
        player = Player(
            name="自定义玩家", health=50, max_health=150, experience=500, level=5, money=1000
        )
        assert player.name == "自定义玩家"
        assert player.health == 50
        assert player.max_health == 150
        assert player.experience == 500
        assert player.level == 5
        assert player.money == 1000

    def test_initial_inventory_and_equipment(self):
        """测试初始背包和装备"""
        player = Player("测试玩家")
        assert isinstance(player.inventory, list)
        assert isinstance(player.equipment, dict)
        assert len(player.inventory) == 0
        for slot in ["weapon", "armor", "helmet", "boots"]:
            assert slot in player.equipment
            assert player.equipment[slot] == ""


class TestPlayerStats:
    """测试玩家属性"""

    def test_initial_stats(self):
        """测试初始属性值"""
        player = Player("测试玩家")
        assert player.stats["strength"] == 10
        assert player.stats["dexterity"] == 10
        assert player.stats["intelligence"] == 10
        assert player.stats["constitution"] == 10

    def test_get_stat_methods(self):
        """测试属性获取方法"""
        player = Player("测试玩家")
        assert player.get_strength() == 10
        assert player.get_dexterity() == 10
        assert player.get_intelligence() == 10
        assert player.get_constitution() == 10

    def test_health_percentage(self):
        """测试生命值百分比计算"""
        player = Player("测试玩家")
        player.health = 75
        assert player.get_health_percentage() == 75.0

        player.health = 50
        assert player.get_health_percentage() == 50.0

        player.health = 0
        assert player.get_health_percentage() == 0.0

    def test_is_alive(self):
        """测试存活状态判断"""
        player = Player("测试玩家")
        assert player.is_alive() is True

        player.health = 1
        assert player.is_alive() is True

        player.health = 0
        assert player.is_alive() is False


class TestPlayerActions:
    """测试玩家动作"""

    def test_take_damage(self):
        """测试受到伤害"""
        player = Player("测试玩家")
        initial_health = player.health
        damage = 25
        player.take_damage(damage)
        assert player.health == initial_health - damage

    def test_take_more_damage_than_health(self):
        """测试受到超过生命值的伤害"""
        player = Player("测试玩家")
        player.health = 20
        player.take_damage(50)
        assert player.health == 0

    def test_heal(self):
        """测试治疗"""
        player = Player("测试玩家")
        player.health = 50
        player.heal(30)
        assert player.health == 80

    def test_heal_to_full(self):
        """测试治疗到满血"""
        player = Player("测试玩家")
        player.health = 75
        player.heal(50)
        assert player.health == 100

    def test_add_experience(self):
        """测试添加经验值"""
        player = Player("测试玩家")
        initial_exp = player.experience
        exp_to_add = 50
        player.add_experience(exp_to_add)
        assert player.experience == initial_exp + exp_to_add

    def test_level_up(self):
        """测试升级"""
        player = Player("测试玩家")
        # 升级到2级需要 100 * (1^2) = 100 经验值
        player.add_experience(100)
        assert player.level == 2
        assert player.experience == 0

    def test_multiple_levels(self):
        """测试连续升级"""
        player = Player("测试玩家")
        # 升级到3级需要 100 + 400 = 500 经验值
        player.add_experience(500)
        assert player.level == 3


class TestPlayerInventory:
    """测试玩家背包"""

    def test_add_and_remove_item(self):
        """测试添加和移除物品"""
        player = Player("测试玩家")
        item = "木剑"
        player.add_item(item)
        assert item in player.inventory
        assert player.has_item(item) is True

        player.remove_item(item)
        assert item not in player.inventory
        assert player.has_item(item) is False

    def test_remove_nonexistent_item(self):
        """测试移除不存在的物品"""
        player = Player("测试玩家")
        result = player.remove_item("不存在的物品")
        assert result is False

    def test_has_item(self):
        """测试物品存在检查"""
        player = Player("测试玩家")
        item = "金币"
        assert player.has_item(item) is False
        player.add_item(item)
        assert player.has_item(item) is True


class TestPlayerEquipment:
    """测试玩家装备系统"""

    def test_equip_item(self):
        """测试装备物品"""
        player = Player("测试玩家")
        item = "铁剑"
        player.add_item(item)
        result = player.equip_item(item, "weapon")
        assert result is True
        assert item not in player.inventory
        assert player.equipment["weapon"] == item

    def test_equip_nonexistent_item(self):
        """测试装备不存在的物品"""
        player = Player("测试玩家")
        result = player.equip_item("不存在的物品", "weapon")
        assert result is False

    def test_equip_to_full_slot(self):
        """测试装备到已装备的槽位"""
        player = Player("测试玩家")
        initial_item = "木剑"
        new_item = "铁剑"
        player.add_item(initial_item)
        player.add_item(new_item)
        player.equip_item(initial_item, "weapon")
        player.equip_item(new_item, "weapon")
        assert initial_item in player.inventory
        assert player.equipment["weapon"] == new_item

    def test_unequip_item(self):
        """测试卸下装备"""
        player = Player("测试玩家")
        item = "铁剑"
        player.add_item(item)
        player.equip_item(item, "weapon")
        result = player.unequip_item("weapon")
        assert result is True
        assert item in player.inventory
        assert player.equipment["weapon"] == ""

    def test_unequip_empty_slot(self):
        """测试卸下空槽位的装备"""
        player = Player("测试玩家")
        result = player.unequip_item("weapon")
        assert result is False


class TestPlayerAttackAndDefense:
    """测试攻击和防御计算"""

    def test_base_attack_and_defense(self):
        """测试基础攻击力和防御力"""
        player = Player("测试玩家")
        # 基础攻击力 = 力量 + 装备加成（初始无装备）
        assert player.get_attack_power() == 10
        # 基础防御力 = 体质 + 装备加成（初始无装备）
        assert player.get_defense() == 10

    def test_weapon_bonus(self):
        """测试武器加成"""
        player = Player("测试玩家")
        player.add_item("木剑")
        player.equip_item("木剑", "weapon")
        assert player.get_attack_power() > 10

    def test_armor_bonus(self):
        """测试防具加成"""
        player = Player("测试玩家")
        player.add_item("铁甲")
        player.equip_item("铁甲", "armor")
        assert player.get_defense() > 10


class TestPlayerStatusInfo:
    """测试玩家状态信息"""

    def test_get_status_info(self):
        """测试获取状态信息字符串"""
        player = Player("测试玩家")
        status = player.get_status_info()
        assert isinstance(status, str)
        assert len(status) > 0
        assert player.name in status
        assert f"等级 {player.level}" in status

    def test_get_equipment_info(self):
        """测试获取装备信息字符串"""
        player = Player("测试玩家")
        info = player.get_equipment_info()
        assert isinstance(info, str)
        assert len(info) > 0
        for slot in ["weapon", "armor", "helmet", "boots"]:
            assert slot.capitalize() in info

    def test_get_inventory_info(self):
        """测试获取背包信息字符串"""
        player = Player("测试玩家")
        player.add_item("木剑")
        player.add_item("回复药水")
        info = player.get_inventory_info()
        assert isinstance(info, str)
        assert "木剑" in info
        assert "回复药水" in info


class TestLevelingSystem:
    """测试升级系统"""

    def test_required_experience_calculation(self):
        """测试升级所需经验计算"""
        player = Player("测试玩家")
        assert player._get_required_experience() == 100

        player.level = 2
        assert player._get_required_experience() == 400

        player.level = 3
        assert player._get_required_experience() == 900

    def test_level_up_attributes(self):
        """测试升级时属性增加"""
        player = Player("测试玩家")
        initial_max_health = player.max_health
        initial_strength = player.stats["strength"]

        player.add_experience(100)
        assert player.max_health > initial_max_health
        assert player.stats["strength"] > initial_strength
        for stat in player.stats:
            assert player.stats[stat] > 10


class TestPlayerCombatMechanics:
    """测试玩家战斗机制"""

    def test_combat_power_calculation(self):
        """测试战斗数值计算"""
        player = Player("测试玩家")
        # 基础攻击力应该接近力量值（无装备）
        assert 10 <= player.get_attack_power() <= 15
        # 基础防御力应该接近体质值（无装备）
        assert 10 <= player.get_defense() <= 15

    def test_equipment_affects_combat_power(self):
        """测试装备影响战斗数值"""
        player = Player("测试玩家")
        base_attack = player.get_attack_power()
        base_defense = player.get_defense()
        player.add_item("铁剑")
        player.add_item("铁甲")
        player.add_item("头盔")
        player.add_item("靴子")
        player.equip_item("铁剑", "weapon")
        player.equip_item("铁甲", "armor")
        player.equip_item("头盔", "helmet")
        player.equip_item("靴子", "boots")
        assert player.get_attack_power() > base_attack
        assert player.get_defense() > base_defense
