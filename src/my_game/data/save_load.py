"""
存档系统模块 - 负责游戏进度的保存和加载。
"""

import json
import os
from typing import Optional, Any


def save_game(game: Any, filename: str = "savegame.json") -> None:
    """
    保存游戏进度到文件。

    Args:
        game: 游戏对象
        filename: 保存文件名

    Raises:
        IOError: 如果保存过程中出现错误
    """
    save_data = {
        "player": {
            "name": game.player.name,
            "health": game.player.health,
            "max_health": game.player.max_health,
            "experience": game.player.experience,
            "level": game.player.level,
            "money": game.player.money,
            "inventory": game.player.inventory.copy(),
            "equipment": game.player.equipment.copy(),
            "stats": game.player.stats.copy(),
        },
        "current_scene": game.current_scene,
        "scenes": {
            scene_id: {
                "items": scene.items.copy(),
                "characters": scene.characters.copy(),
                "connections": scene.connections.copy(),
            }
            for scene_id, scene in game.scenes.items()
        },
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise IOError(f"保存游戏时出错: {e}")


def load_game(filename: str = "savegame.json") -> Optional[Any]:
    """
    从文件加载游戏进度。

    Args:
        filename: 存档文件名

    Returns:
        加载后的游戏对象，失败时返回 None

    Raises:
        IOError: 如果加载过程中出现错误
    """
    if not os.path.exists(filename):
        raise IOError(f"存档文件 {filename} 不存在")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            save_data = json.load(f)
    except Exception as e:
        raise IOError(f"读取存档时出错: {e}")

    return _reconstruct_game(save_data)


def _reconstruct_game(save_data: dict) -> Optional[Any]:
    """
    从保存的数据重构游戏对象。

    Args:
        save_data: 保存的数据

    Returns:
        重构后的游戏对象
    """
    try:
        from src.my_game.core.game import Game
        from src.my_game.core.player import Player
        from src.my_game.core.scene import RoomScene

        # 创建游戏对象
        game = Game()

        # 重构玩家对象
        player_data = save_data.get("player", {})
        game.player = Player(
            name=player_data.get("name", "冒险者"),
            health=player_data.get("health", 100),
            max_health=player_data.get("max_health", 100),
            experience=player_data.get("experience", 0),
            level=player_data.get("level", 1),
            money=player_data.get("money", 0),
        )
        # 恢复背包和装备
        if "inventory" in player_data:
            for item in player_data["inventory"]:
                game.player.add_item(item)
        if "equipment" in player_data:
            for slot, item in player_data["equipment"].items():
                if item and item in game.player.inventory:
                    game.player.equip_item(item, slot)
        # 恢复属性
        if "stats" in player_data:
            game.player.stats = player_data["stats"]

        # 重构场景
        if "scenes" in save_data:
            for scene_id, scene_data in save_data["scenes"].items():
                # 暂时简化场景重构 - 需要根据场景类型重构
                # 这里我们假设所有场景都是 RoomScene 类型
                scene = RoomScene(
                    scene_id=scene_id,
                    name=scene_id,
                    description="从存档中加载的场景",
                    connections=scene_data.get("connections", {}),
                    items=scene_data.get("items", []),
                    characters=scene_data.get("characters", []),
                )
                game.add_scene(scene)

        # 恢复当前场景
        if "current_scene" in save_data:
            game.current_scene = save_data["current_scene"]

        return game

    except Exception as e:
        print(f"重构游戏时出错: {e}")
        return None


def list_saves(directory: str = ".", extension: str = ".json") -> list:
    """
    列出指定目录中的所有存档文件。

    Args:
        directory: 要搜索的目录
        extension: 存档文件扩展名

    Returns:
        存档文件列表
    """
    saves = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(extension) and filename.startswith("savegame"):
                saves.append(filename)
        saves.sort()
    except Exception as e:
        print(f"列出存档时出错: {e}")
    return saves


def delete_save(filename: str) -> bool:
    """
    删除存档文件。

    Args:
        filename: 要删除的存档文件名

    Returns:
        删除成功返回 True，否则返回 False
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return True
    except Exception as e:
        print(f"删除存档时出错: {e}")
    return False


def get_save_info(filename: str) -> Optional[dict]:
    """
    获取存档的基本信息，用于存档选择界面。

    Args:
        filename: 存档文件名

    Returns:
        存档信息字典，包含玩家名称、等级、场景等，失败时返回 None
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        info = {
            "filename": filename,
            "player_name": save_data.get("player", {}).get("name", "未知"),
            "player_level": save_data.get("player", {}).get("level", 1),
            "current_scene": save_data.get("current_scene", "未知场景"),
            "health": f"{save_data.get('player', {}).get('health', 0)}/{save_data.get('player', {}).get('max_health', 0)}",
            "money": save_data.get("player", {}).get("money", 0),
        }

        return info
    except Exception as e:
        print(f"获取存档信息时出错: {e}")
        return None


def check_save_exists(filename: str = "savegame.json") -> bool:
    """
    检查存档文件是否存在。

    Args:
        filename: 要检查的存档文件名

    Returns:
        文件存在返回 True，否则返回 False
    """
    return os.path.exists(filename)


def backup_save(filename: str = "savegame.json") -> None:
    """
    创建存档的备份。

    Args:
        filename: 要备份的存档文件名

    Raises:
        IOError: 如果备份过程中出现错误
    """
    if os.path.exists(filename):
        import shutil

        backup_filename = filename + ".bak"
        try:
            shutil.copy2(filename, backup_filename)
        except Exception as e:
            raise IOError(f"备份存档时出错: {e}")
