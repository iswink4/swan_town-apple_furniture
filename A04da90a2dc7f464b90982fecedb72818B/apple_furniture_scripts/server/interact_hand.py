# -*- coding: utf-8 -*-
"""
模块名称: interact_hand.py
功能描述: 处理空手点击方块的循环切换功能

事件监听:
- ServerBlockUseEvent: 玩家点击方块时触发

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: ALL_HAND_BLOCK_CYCLES, HAND_INTERACT_COOLDOWN
- utils: cooldown_check, cycle_block, is_empty_hand

实现逻辑:
1. 玩家空手点击支持循环的方块
2. 切换到下一个样式
3. 使用冷却时间防止连续触发

事件冲突处理:
========================================
ServerBlockUseEvent 与多个模块共用：

- placeholder.py 优先处理占位方块转发（第344行）
- 本模块在 placeholder 之后处理
- 只处理空手点击 ALL_HAND_BLOCK_CYCLES 中方块的情况
- 其他情况自动跳过（block_name not in ALL_HAND_BLOCK_CYCLES）
- 检查玩家是否空手（主手无物品）

注意事项:
- 与斧子交互逻辑类似，但无需手持物品
- 冷却时间可独立配置
"""
from ..QuModLibs.Server import *
from ..config import ALL_HAND_BLOCK_CYCLES, HAND_INTERACT_COOLDOWN
from ..utils import cooldown_check, cycle_block, is_empty_hand


@Listen(Events.ServerBlockUseEvent)
def on_hand_block_use(args):
    """
    空手方块交互事件处理
    
    当玩家空手点击支持循环的方块时，触发样式切换。
    """
    block_name = args['blockName']
    
    # 只处理空手交互的方块
    if block_name not in ALL_HAND_BLOCK_CYCLES:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    # 检查是否空手（使用 utils 工具函数）
    if not is_empty_hand(player_id):
        return
    
    # 冷却检查（使用 utils 工具函数）
    if not cooldown_check(player_id, HAND_INTERACT_COOLDOWN):
        return
    
    # 执行方块切换（使用 utils 工具函数）
    cycle_block(block_pos, block_name, dimension, ALL_HAND_BLOCK_CYCLES)