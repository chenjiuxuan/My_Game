"""
场景系统测试模块。
"""

from src.my_game.core.scene import RoomScene, CombatScene


class TestScene:
    """场景基类测试"""

    def test_initialization(self):
        """测试场景初始化"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间", {"north": "next_scene"})
        assert scene.scene_id == "test_scene"
        assert scene.name == "测试房间"
        assert scene.description == "这是一个测试房间"
        assert "north" in scene.connections
        assert scene.connections["north"] == "next_scene"
        assert len(scene.items) == 0
        assert len(scene.characters) == 0

    def test_add_item(self):
        """测试添加物品"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        scene.add_item("测试物品")
        assert "测试物品" in scene.items
        assert len(scene.items) == 1

    def test_remove_item(self):
        """测试移除物品"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        scene.add_item("测试物品")
        scene.remove_item("测试物品")
        assert "测试物品" not in scene.items
        assert len(scene.items) == 0

    def test_add_character(self):
        """测试添加角色"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        scene.add_character("测试角色")
        assert "测试角色" in scene.characters
        assert len(scene.characters) == 1

    def test_remove_character(self):
        """测试移除角色"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        scene.add_character("测试角色")
        scene.remove_character("测试角色")
        assert "测试角色" not in scene.characters
        assert len(scene.characters) == 0

    def test_get_connection(self):
        """测试获取场景连接"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间", {"north": "next_scene"})
        assert scene.get_connection("north") == "next_scene"
        assert scene.get_connection("south") is None

    def test_direct_connection_access(self):
        """测试直接访问连接属性"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间", {"north": "next_scene"})
        assert isinstance(scene.connections, dict)
        assert len(scene.connections) == 1


class TestRoomScene:
    """房间场景测试"""

    def test_initialization_with_items_and_characters(self):
        """测试带有物品和角色的场景初始化"""
        items = ["金币", "木剑"]
        characters = ["村民", "商人"]
        scene = RoomScene(
            "test_scene", "测试房间", "这是一个测试房间", {"north": "next_scene"}, items, characters
        )
        assert len(scene.items) == 2
        for item in items:
            assert item in scene.items
        assert len(scene.characters) == 2
        for character in characters:
            assert character in scene.characters

    def test_enter_and_exit(self, capsys):
        """测试进入和离开场景"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        player_mock = type("MockPlayer", (), {})()
        scene.enter(player_mock)
        captured = capsys.readouterr()
        assert "你进入了 测试房间" in captured.out

        scene.exit(player_mock)
        captured = capsys.readouterr()
        assert "你离开了 测试房间" in captured.out

    def test_get_info(self):
        """测试获取场景信息"""
        scene = RoomScene(
            "test_scene",
            "测试房间",
            "这是一个测试房间",
            {"north": "next_scene"},
            ["金币"],
            ["村民"],
        )
        info = scene.get_info()
        assert "测试房间" in info
        assert "这是一个测试房间" in info
        assert "连接的方向: north" in info
        assert "房间中的物品: 金币" in info
        assert "房间中的角色: 村民" in info


class TestCombatScene:
    """战斗场景测试"""

    def test_initialization(self):
        """测试战斗场景初始化"""
        enemy_stats = {"health": 50, "attack": 5, "defense": 2}
        scene = CombatScene(
            "combat_scene",
            "战斗场景",
            "这是一个危险的战斗场景",
            "巨魔",
            enemy_stats,
            {"north": "exit"},
        )
        assert scene.scene_id == "combat_scene"
        assert scene.name == "战斗场景"
        assert scene.enemy == "巨魔"
        assert scene.enemy_stats == enemy_stats
        assert scene.combat_active is True

    def test_enter_and_exit(self, capsys):
        """测试进入和离开战斗场景"""
        scene = CombatScene("combat_scene", "战斗场景", "战斗场景", "巨魔", {"health": 50})
        player_mock = type("MockPlayer", (), {})()
        scene.enter(player_mock)
        captured = capsys.readouterr()
        assert "你进入了 战斗场景" in captured.out
        assert "注意！巨魔 出现了！" in captured.out

        scene.exit(player_mock)
        captured = capsys.readouterr()
        assert "战斗结束" in captured.out

    def test_end_combat(self):
        """测试结束战斗"""
        scene = CombatScene("combat_scene", "战斗场景", "战斗场景", "巨魔", {"health": 50})
        assert scene.combat_active is True
        scene.end_combat()
        assert scene.combat_active is False

    def test_get_enemy_info(self):
        """测试获取敌人信息"""
        enemy_stats = {"health": 50, "attack": 5, "defense": 2}
        scene = CombatScene("combat_scene", "战斗场景", "战斗场景", "巨魔", enemy_stats)
        info = scene.get_enemy_info()
        assert "敌人: 巨魔" in info
        assert "health: 50" in info
        assert "attack: 5" in info
        assert "defense: 2" in info


class TestSceneConnections:
    """场景连接测试"""

    def test_multiple_connections(self):
        """测试多个场景连接"""
        connections = {
            "north": "north_scene",
            "south": "south_scene",
            "east": "east_scene",
            "west": "west_scene",
        }
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间", connections)
        assert len(scene.connections) == 4
        assert "north" in scene.connections
        assert "south" in scene.connections
        assert "east" in scene.connections
        assert "west" in scene.connections
        assert scene.get_connection("north") == "north_scene"
        assert scene.get_connection("south") == "south_scene"
        assert scene.get_connection("east") == "east_scene"
        assert scene.get_connection("west") == "west_scene"

    def test_connection_case_insensitive(self):
        """测试连接方向不区分大小写"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间", {"north": "next_scene"})
        assert scene.get_connection("North") == "next_scene"
        assert scene.get_connection("NORTH") == "next_scene"
        assert scene.get_connection("north") == "next_scene"


class TestSceneItems:
    """场景物品管理测试"""

    def test_add_multiple_items(self):
        """测试添加多个物品"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        items = ["金币", "木剑", "回复药水"]
        for item in items:
            scene.add_item(item)
        assert len(scene.items) == 3
        for item in items:
            assert item in scene.items

    def test_remove_nonexistent_item(self):
        """测试移除不存在的物品"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        original_length = len(scene.items)
        scene.remove_item("不存在的物品")
        assert len(scene.items) == original_length

    def test_duplicate_items(self):
        """测试重复添加相同物品"""
        scene = RoomScene("test_scene", "测试房间", "这是一个测试房间")
        scene.add_item("金币")
        scene.add_item("金币")
        assert scene.items.count("金币") == 1
        assert len(scene.items) == 1
