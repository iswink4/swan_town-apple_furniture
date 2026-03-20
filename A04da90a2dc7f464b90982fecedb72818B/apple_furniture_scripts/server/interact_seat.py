# -*- coding: utf-8 -*-
"""
模块名称: interact_seat.py
功能描述: 处理座椅交互逻辑，包括椅子/沙发坐下和站起功能

事件监听:
- ServerBlockUseEvent: 玩家右键点击方块时触发
- OnScriptTickServer: 服务端每帧触发，用于检测玩家离开
- DestroyBlockEvent: 方块被破坏时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: CHAIR_LIST（可坐下方块列表）, SEAT_HEIGHT（座位高度）
- interact_block: 需要检查是否触发斧子切换而非坐下

全局状态:
- sitting_players: dict - 正在坐着的玩家数据
  格式: {playerId: {"pos": (x,y,z), "seat_pos": (x,y,z)}}
- last_sit_time: dict - 玩家上次坐下操作时间戳
  格式: {playerId: timestamp}

实现逻辑:
1. 监听方块使用事件，检查是否是可坐下方块
2. 如果手持斧子且方块支持样式切换，跳过（交给interact_block处理）
3. 检查冷却时间（0.3秒），防止tick级连续触发
4. 执行坐下：传送玩家到座位位置，记录状态，通知客户端播放动画
5. 执行站起：清除状态，通知客户端停止动画
6. OnScriptTickServer检测玩家是否离开座位（距离>0.3），自动站起
7. DestroyBlockEvent检测椅子被破坏，坐着的玩家自动站起

跨端通信:
- Call(playerId, "PlaySitAnim"): 通知客户端播放坐下动画
- Call(playerId, "StopSitAnim"): 通知客户端停止动画

注意事项:
- 坐下位置计算：方块中心 + SEAT_HEIGHT偏移
- 自动站起距离阈值：0.3格（平方距离0.09）
- 与interact_block模块协同：斧子右键优先触发样式切换
"""
import time
from ..QuModLibs.Server import *
from ..config import CHAIR_LIST, SEAT_HEIGHT, AXE_NAMES, ALL_BLOCK_CYCLES


# ============================================================
# 全局状态
# ============================================================

# 正在坐着的玩家数据
# 格式: {playerId: {"pos": (x,y,z), "seat_pos": (x,y,z)}}
sitting_players = {}

# 玩家上次坐下操作时间戳，用于冷却检查
# 格式: {playerId: timestamp}
last_sit_time = {}


# ============================================================
# 核心功能
# ============================================================

def sit_down(player_id, x, y, z):
    """
    执行玩家坐下操作
    
    将玩家传送到座位位置，记录坐下状态，并通知客户端播放坐下动画。
    
    Args:
        player_id: str - 玩家实体ID
        x, y, z: int - 椅子方块坐标
    
    Returns:
        None
    
    Side Effects:
        - 修改 sitting_players 全局状态
        - 调用 Call 通知客户端播放动画
        - 传送玩家到座位位置
    """
    comp = serverApi.GetEngineCompFactory()
    
    # 计算座位位置（方块中心上方）
    seat_pos = (x + 0.5, y + SEAT_HEIGHT, z + 0.5)
    
    # 设置玩家位置
    pos_comp = comp.CreatePos(player_id)
    pos_comp.SetFootPos(seat_pos)
    
    # 记录玩家坐下数据
    sitting_players[player_id] = {
        "pos": (x, y, z),       # 方块位置
        "seat_pos": seat_pos    # 座位位置
    }
    
    # 通知客户端播放坐下动画
    Call(player_id, "PlaySitAnim")


def stand_up(player_id):
    """
    执行玩家站起操作
    
    清除玩家坐下状态，并通知客户端停止动画。
    
    Args:
        player_id: str - 玩家实体ID
    
    Returns:
        None
    
    Side Effects:
        - 修改 sitting_players 全局状态（删除对应项）
        - 调用 Call 通知客户端停止动画
    
    Note:
        如果玩家不在 sitting_players 中，直接返回不做任何操作
    """
    if player_id not in sitting_players:
        return
    
    # 清除坐下数据
    del sitting_players[player_id]
    
    # 通知客户端停止动画
    Call(player_id, "StopSitAnim")


# ============================================================
# 事件处理
# ============================================================

@Listen(Events.ServerBlockUseEvent)
def on_block_use(args):
    """
    方块使用事件处理 - 处理玩家坐下/站起
    
    当玩家右键点击方块时触发，判断是否是可坐下方块，
    并处理坐下/站起的切换逻辑。
    
    Args:
        args: 事件参数字典，包含:
            - blockName: 方块名称
            - playerId: 玩家ID
            - x, y, z: 方块坐标
            - 其他ServerBlockUseEvent标准字段
    
    Returns:
        None
    
    Logic:
        1. 获取玩家主手物品
        2. 如果手持斧子且方块支持样式切换，跳过（交给interact_block处理）
        3. 检查是否是可坐下方块
        4. 检查冷却时间（0.3秒）
        5. 如果已在坐着，执行站起；否则执行坐下
    """
    block_name = args['blockName']
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    
    # 获取玩家主手物品
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    hand_item = item_comp.GetPlayerItem(2, 0, False)  # posType=2 表示主手
    item_name = hand_item.get('newItemName', '') if hand_item else ''
    
    # 如果手持斧子且方块支持样式切换，则跳过坐下功能（交给 interact_block 处理）
    if item_name in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        return
    
    # 检查是否是可坐下的方块
    if block_name not in CHAIR_LIST:
        return
    
    # 冷却检查，防止 tick 级别连续触发
    now = time.time()
    last_time = last_sit_time.get(player_id, 0)
    if now - last_time < 0.3:
        return
    last_sit_time[player_id] = now
    
    # 执行坐下或站起
    if player_id in sitting_players:
        stand_up(player_id)
    else:
        sit_down(player_id, x, y, z)


@Listen(Events.OnScriptTickServer)
def on_tick():
    """
    每帧检测 - 玩家移动时自动站起
    
    服务端每帧触发，检查所有坐着的玩家是否离开了座位，
    如果距离超过阈值则自动执行站起。
    
    Args:
        无（事件触发，无参数）
    
    Returns:
        None
    
    Logic:
        遍历 sitting_players，计算当前位置与座位位置的距离（平方），
        如果超过 0.3（即平方距离 > 0.09），调用 stand_up
    
    Performance:
        O(n)，n为坐着的玩家数量，每帧执行一次
    """
    comp = serverApi.GetEngineCompFactory()
    
    for player_id, data in list(sitting_players.items()):
        pos_comp = comp.CreatePos(player_id)
        current_pos = pos_comp.GetFootPos()
        
        if current_pos:
            # 计算玩家当前位置与座位位置的距离（平方距离，避免开方）
            dx = current_pos[0] - data["seat_pos"][0]
            dy = current_pos[1] - data["seat_pos"][1]
            dz = current_pos[2] - data["seat_pos"][2]
            
            # 如果玩家离开了座位（距离 > 0.3），自动站起
            if dx*dx + dy*dy + dz*dz > 0.09:  # 0.3^2 = 0.09
                stand_up(player_id)


@Listen(Events.DestroyBlockEvent)
def on_block_destroy(args):
    """
    方块被破坏事件 - 坐着的玩家自动站起
    
    当方块被破坏时触发，检查是否有玩家正坐在该位置，
    如果有则强制站起。
    
    Args:
        args: 事件参数字典，包含:
            - x, y, z: 被破坏的方块坐标
            - 其他DestroyBlockEvent标准字段
    
    Returns:
        None
    
    Note:
        遍历 sitting_players，匹配方块坐标，匹配则调用 stand_up
    """
    pos = (args['x'], args['y'], args['z'])
    
    for player_id, data in list(sitting_players.items()):
        if data["pos"] == pos:
            stand_up(player_id)
