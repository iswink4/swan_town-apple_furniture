# -*- coding: utf-8 -*-
"""
模块名称: interact_drainage.py
功能描述: 处理水槽/浴缸排水功能

事件监听:
- ServerBlockUseEvent: 玩家点击方块时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: DRAINAGE_BLOCKS, DRAINAGE_DURATION, DRAINAGE_COOLDOWN

实现逻辑:
1. 玩家空手点击支持排水的方块（浴缸/水槽）
2. 方块替换为排水动画方块（放水中状态）
3. 0.5秒后替换为排水完成方块
4. 使用冷却时间防止连续触发

注意事项:
- 使用定时器实现延迟替换
- 需要记录方块位置以避免重复触发
"""

import time
from ..QuModLibs.Server import *
from ..config import DRAINAGE_BLOCKS, DRAINAGE_DURATION, DRAINAGE_COOLDOWN


last_drainage_time = {}

draining_blocks = {}


def _replace_block(comp, block_pos, new_block_name, dimension):
    """
    替换方块
    
    将指定位置的方块替换为新方块，保留原方块的aux值。
    
    Args:
        comp: 方块信息组件
        block_pos: 方块位置元组
        new_block_name: 新方块名称
        dimension: 维度ID
    
    Returns:
        None
    """
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    new_block_dict = {
        'name': new_block_name,
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, new_block_dict, 0, dimension)


def _start_drainage(block_pos, draining_block, final_block, dimension):
    """
    开始排水流程
    
    执行两阶段方块替换：
    1. 立即替换为排水动画方块
    2. 0.5秒后替换为最终方块
    
    Args:
        block_pos: 方块位置元组
        draining_block: 排水动画方块名称
        final_block: 最终方块名称
        dimension: 维度ID
    
    Returns:
        None
    """
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
    
    _replace_block(comp, block_pos, draining_block, dimension)
    
    def on_drainage_complete():
        current_block = comp.GetBlockNew(block_pos, dimension)
        if current_block['name'] == draining_block:
            _replace_block(comp, block_pos, final_block, dimension)
        
        if block_pos in draining_blocks:
            del draining_blocks[block_pos]
    
    game_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId)
    game_comp.AddTimer(DRAINAGE_DURATION, on_drainage_complete)


@Listen(Events.ServerBlockUseEvent)
def on_drainage_block_use(args):
    """
    排水方块交互事件处理
    
    当玩家空手点击支持排水的方块时，触发排水流程。
    
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
    
    if block_name not in DRAINAGE_BLOCKS:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    
    if hand_item:
        return
    
    if block_pos in draining_blocks:
        return
    
    now = time.time()
    last_time = last_drainage_time.get(player_id, 0)
    if now - last_time < DRAINAGE_COOLDOWN:
        return
    last_drainage_time[player_id] = now
    
    draining_blocks[block_pos] = True
    
    draining_block, final_block = DRAINAGE_BLOCKS[block_name]
    
    _start_drainage(block_pos, draining_block, final_block, dimension)