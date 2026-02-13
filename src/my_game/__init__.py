"""
文字冒险/交互式故事游戏 - 入口点模块。
"""

from typing import Any


__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "一个基于 Python 的文字冒险游戏引擎"


def create_game_instance() -> Any:
    """
    创建并配置游戏实例。

    Returns:
        配置好的游戏实例
    """
    from src.my_game.core.game import Game
    from src.my_game.core.scene import RoomScene, CombatScene

    # 创建游戏实例
    game = Game()

    # 创建场景
    # 入口场景
    entrance = RoomScene(
        "entrance",
        "村庄入口",
        "这是一个宁静的村庄入口，有一条小路通向村庄内部。你可以看到西边有一个小酒馆，东边是一个森林入口。",
        connections={"east": "forest_path", "west": "tavern"},
        items=["金币"],
        characters=["卫兵"],
    )
    game.add_scene(entrance)

    # 森林小径
    forest_path = RoomScene(
        "forest_path",
        "森林小径",
        "一条蜿蜒的森林小径，周围树木茂密，阳光透过树叶洒下斑驳的光影。空气中弥漫着清新的森林气息。",
        connections={"west": "entrance", "east": "forest_clearing"},
        items=["回复药水"],
        characters=["松鼠"],
    )
    game.add_scene(forest_path)

    # 森林空地
    forest_clearing = RoomScene(
        "forest_clearing",
        "森林空地",
        "一个开阔的森林空地，中央有一个古老的橡树。树周围有一些蘑菇和草药。",
        connections={"west": "forest_path"},
        items=["蘑菇", "草药"],
        characters=["老巫师"],
    )
    game.add_scene(forest_clearing)

    # 村庄酒馆
    tavern = RoomScene(
        "tavern",
        "小酒馆",
        "温暖的酒馆里弥漫着麦酒和烤面包的香气。几张木桌旁坐着一些村民，正在交谈。吧台后面有一位调酒师。",
        connections={"east": "entrance"},
        items=["麦酒", "烤面包"],
        characters=["调酒师", "村民"],
    )
    game.add_scene(tavern)

    # 战斗场景
    forest_cave = CombatScene(
        "forest_cave",
        "森林洞穴",
        "一个黑暗的森林洞穴，空气中弥漫着淡淡的硫磺味。洞穴深处传来低沉的吼叫声。",
        "巨魔",
        {"health": 50, "attack": 5, "defense": 2},
        connections={"west": "forest_clearing"},
    )
    game.add_scene(forest_cave)

    # 设置初始场景
    game.set_initial_scene("entrance")

    return game


def main() -> None:
    """游戏主入口点。"""
    try:
        # 创建游戏实例
        game = create_game_instance()

        # 初始化玩家
        name = input("请输入你的名字: ").strip()
        if not name:
            name = "冒险者"
        game.initialize_player(name)

        # 开始游戏
        game.start()

    except KeyboardInterrupt:
        print("\n游戏被中断")
    except Exception as e:
        print(f"\n游戏错误: {e}")
        import traceback

        print(traceback.format_exc())


if __name__ == "__main__":
    main()
