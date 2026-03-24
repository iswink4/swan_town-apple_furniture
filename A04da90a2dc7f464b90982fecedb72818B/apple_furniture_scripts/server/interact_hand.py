# -*- coding: utf-8 -*-
"""
模块名称: interact_hand.py
功能描述: 处理空手点击方块的循环切换功能

事件监听:
- ServerBlockUseEvent: 玩家点击方块时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: ALL_HAND_BLOCK_CYCLES, HAND_INTERACT_COOLDOWN

实现逻辑:
1. 玩家空手点击支持循环的方块
2. 切换到下一个样式
3. 使用冷却时间防止连续触发

注意事项:
- 与斧子交互逻辑类似，但无需手持物品
- 冷却时间可独立配置
"""
import time
from ..QuModLibs.Server import *
from ..config import ALL_HAND_BLOCK_CYCLES, HAND_INTERACT_COOLDOWN


# 交互冷却记录
last_interact_time = {}


def _cycle_block(comp, block_pos, block_name, dimension):
    """
    循环切换方块类型
    
    根据 ALL_HAND_BLOCK_CYCLES 映射表，将当前方块切换到下一个样式。
    切换时保留原方块的aux值（朝向、状态等）。
    
    Args:
        comp: 方块信息组件 (BlockInfoComponent)
        block_pos: 方块位置元组 (x, y, z)
        block_name: 当前方块名称
        dimension: 维度ID
    
    Returns:
        None
    """
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    block_dict = {
        'name': ALL_HAND_BLOCK_CYCLES[block_name],
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, block_dict, 0, dimension)


@Listen(Events.ServerBlockUseEvent)
def on_hand_block_use(args):
    """
    空手方块交互事件处理
    
    当玩家空手点击支持循环的方块时，触发样式切换。
    
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
    
    # 只处理空手交互的方块
    if block_name not in ALL_HAND_BLOCK_CYCLES:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    # 检查是否空手（主手无物品）
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    
    # 主手有物品时不处理
    if hand_item:
        return
    
    # 冷却检查
    now = time.time()
    last_time = last_interact_time.get(player_id, 0)
    if now - last_time < HAND_INTERACT_COOLDOWN:
        return
    last_interact_time[player_id] = now
    
    # 执行方块切换
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    _cycle_block(block_comp, block_pos, block_name, dimension)