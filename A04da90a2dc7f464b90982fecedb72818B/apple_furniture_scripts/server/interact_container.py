# -*- coding: utf-8 -*-
"""
模块名称: interact_container.py
功能描述: 处理存储容器交互音效

事件监听:
- ServerBlockUseEvent: 玩家点击方块时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: CONTAINER_BLOCKS（存储容器方块列表）

实现逻辑:
1. 监听方块点击事件
2. 检查是否是存储容器方块
3. 播放 block.barrel.open 音效

注意事项:
- 存储容器方块在 config.CONTAINER_BLOCKS 中配置
- 音效使用原版 playsound 指令播放
- 使用冷却时间防止连续触发
"""
import time
from ..QuModLibs.Server import *
from ..config import CONTAINER_BLOCKS


# 交互冷却记录
last_interact_time = {}

# 冷却时间（秒）
CONTAINER_INTERACT_COOLDOWN = 0.3


@Listen(Events.ServerBlockUseEvent)
def on_container_use(args):
    """
    存储容器交互事件处理

    当玩家点击存储容器方块时，播放打开音效。

    Args:
        args: 事件参数字典，包含:
            - blockName: 方块名称
            - playerId: 玩家ID
            - x, y, z: 方块坐标
            - dimensionId: 维度ID

    Returns:
        None
    """
    block_name = args['blockName']

    # 只处理存储容器方块
    if block_name not in CONTAINER_BLOCKS:
        return

    player_id = args['playerId']

    # 冷却检查
    now = time.time()
    last_time = last_interact_time.get(player_id, 0)
    if now - last_time < CONTAINER_INTERACT_COOLDOWN:
        return
    last_interact_time[player_id] = now

    # 播放打开音效
    cmd_comp = serverApi.GetEngineCompFactory().CreateCommand(serverApi.GetLevelId)
    cmd_comp.SetCommand("playsound block.barrel.open @s ~ ~ ~ 1 1", player_id)
