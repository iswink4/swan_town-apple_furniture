# -*- coding: utf-8 -*-
"""
模块名称: interact_drainage.py
功能描述: 处理水槽/浴缸排水功能

事件监听:
- ServerBlockUseEvent: 玩家点击方块时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: DRAINAGE_BLOCKS, DRAINAGE_DURATION, DRAINAGE_COOLDOWN
- utils: cooldown_check, replace_block, is_empty_hand

实现逻辑:
1. 玩家空手点击支持排水的方块（浴缸/水槽）
2. 方块替换为排水动画方块（放水中状态）
3. 0.5秒后替换为排水完成方块
4. 使用冷却时间防止连续触发

事件冲突处理:
========================================
ServerBlockUseEvent 与多个模块共用：

- placeholder.py 优先处理占位方块转发
- interact_hand.py 处理空手切换
- 本模块只处理空手点击 DRAINAGE_BLOCKS 中方块的情况
- 其他情况自动跳过（block_name not in DRAINAGE_BLOCKS）
- 检查玩家是否空手

注意事项:
- 使用定时器实现延迟替换
- 需要记录方块位置以避免重复触发
"""

from ..QuModLibs.Server import *
from ..config import DRAINAGE_BLOCKS, DRAINAGE_DURATION, DRAINAGE_COOLDOWN
from ..utils import cooldown_check, replace_block, is_empty_hand


draining_blocks = {}


def _start_drainage(block_pos, draining_block, final_block, dimension):
    """
    开始排水流程
    
    执行两阶段方块替换：
    1. 立即替换为排水动画方块
    2. DRAINAGE_DURATION 秒后替换为最终方块
    """
    replace_block(block_pos, draining_block, dimension)
    
    def on_drainage_complete():
        comp = serverApi.GetEngineCompFactory()
        block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
        current_block = block_comp.GetBlockNew(block_pos, dimension)
        if current_block['name'] == draining_block:
            replace_block(block_pos, final_block, dimension)
        
        if block_pos in draining_blocks:
            del draining_blocks[block_pos]
    
    game_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId)
    game_comp.AddTimer(DRAINAGE_DURATION, on_drainage_complete)


@Listen(Events.ServerBlockUseEvent)
def on_drainage_block_use(args):
    """
    排水方块交互事件处理
    
    当玩家空手点击支持排水的方块时，触发排水流程。
    """
    block_name = args['blockName']
    
    if block_name not in DRAINAGE_BLOCKS:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    # 检查是否空手（使用 utils 工具函数）
    if not is_empty_hand(player_id):
        return
    
    # 防止正在排水的方块重复触发
    if block_pos in draining_blocks:
        return
    
    # 冷却检查（使用 utils 工具函数）
    if not cooldown_check(player_id, DRAINAGE_COOLDOWN):
        return
    
    draining_blocks[block_pos] = True
    
    draining_block, final_block = DRAINAGE_BLOCKS[block_name]
    _start_drainage(block_pos, draining_block, final_block, dimension)