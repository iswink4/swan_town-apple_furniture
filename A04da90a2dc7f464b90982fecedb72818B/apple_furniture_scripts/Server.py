# -*- coding: utf-8 -*-
"""
家具模组服务端逻辑
功能：
1. 斧子右键改变家具样式
2. 玩家右键椅子/沙发坐下
3. 玩家移动/方块被破坏时自动站起
"""
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle
from .config import AXE_NAMES, ALL_BLOCK_CYCLES, CHAIR_LIST, SIT_ANIMATION_NAME, SEAT_HEIGHT

# ============================================================
# 全局数据存储
# ============================================================

# 坐下的玩家数据 {playerId: {"pos": (x,y,z), "seat_pos": (x,y,z)}}
sitting_players = {}

# 玩家上次坐下操作时间 {playerId: timestamp}
last_sit_time = {}

# ============================================================
# 斧子改变家具样式功能
# ============================================================

def _cycle_block(comp, block_pos, block_name, dimension):
    """
    循环切换方块类型
    :param comp: 方块信息组件
    :param block_pos: 方块位置 (x, y, z)
    :param block_name: 当前方块名称
    :param dimension: 维度ID
    """
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    block_dict = {
        'name': ALL_BLOCK_CYCLES[block_name],
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, block_dict, 0, dimension)

@Listen(Events.ItemUseOnAfterServerEvent)
@QThrottle(intervalTime=0.2)
def on_item_use(args):
    """
    物品使用事件 - 处理斧子改变家具样式
    """
    item_dict = args["itemDict"]
    block_pos = args["x"], args["y"], args["z"]
    block_name = args["blockName"]
    dimension = args["dimensionId"]
    
    # 检查是否是斧子右键可循环方块
    if item_dict.get('newItemName', '') in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
        _cycle_block(comp, block_pos, block_name, dimension)

# ============================================================
# 坐下/站起功能
# ============================================================

@Listen(Events.ServerBlockUseEvent)
def on_block_use(args):
    """
    方块使用事件 - 处理玩家坐下/站起
    """
    block_name = args['blockName']
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    
    # 获取玩家主手物品
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    hand_item = item_comp.GetPlayerItem(2, 0, False)  # posType=2 表示主手
    item_name = hand_item.get('newItemName', '') if hand_item else ''
    
    # 如果手持斧子且方块支持样式切换，则跳过坐下功能（交给 on_item_use 处理）
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

def sit_down(player_id, x, y, z):
    """
    玩家坐下
    :param player_id: 玩家ID
    :param x, y, z: 方块坐标
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
    玩家站起
    :param player_id: 玩家ID
    """
    if player_id not in sitting_players:
        return
    
    # 清除坐下数据
    del sitting_players[player_id]
    
    # 通知客户端停止动画
    Call(player_id, "StopSitAnim")

# ============================================================
# 自动站起检测
# ============================================================

@Listen(Events.OnScriptTickServer)
def on_tick():
    """
    每帧检测 - 玩家移动时自动站起
    """
    comp = serverApi.GetEngineCompFactory()
    
    for player_id, data in list(sitting_players.items()):
        pos_comp = comp.CreatePos(player_id)
        current_pos = pos_comp.GetFootPos()
        
        if current_pos:
            # 计算玩家当前位置与座位位置的距离
            dx = current_pos[0] - data["seat_pos"][0]
            dy = current_pos[1] - data["seat_pos"][1]
            dz = current_pos[2] - data["seat_pos"][2]
            
            # 如果玩家离开了座位，自动站起
            if dx*dx + dy*dy + dz*dz > 0.3:
                stand_up(player_id)

@Listen(Events.DestroyBlockEvent)
def on_block_destroy(args):
    """
    方块被破坏事件 - 坐着的玩家自动站起
    """
    pos = (args['x'], args['y'], args['z'])
    
    for pid, data in list(sitting_players.items()):
        if data["pos"] == pos:
            stand_up(pid)