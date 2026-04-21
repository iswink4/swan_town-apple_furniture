# -*- coding: utf-8 -*-
"""
模块名称: interact_ice.py
功能描述: 冰箱制冰功能，玩家手持水桶点击冰箱生成冰块

事件监听:
- ServerItemUseOnEvent: 手持水桶点击冰箱时触发

实现逻辑:
1. 检测手持水桶点击冰箱（主方块或占位方块）
2. 获取冰箱主方块位置（处理占位方块情况）
3. 水桶替换为空桶
4. 优先合并已有冰块（不满64），否则放入空槽位
5. 显示提示消息

事件冲突处理:
========================================
ServerItemUseOnEvent 与 interact_water.py 共用此事件：

- 本模块需要最高优先级处理冰箱制冰
- 必须在 interact_water.py 之前导入（见 Server.py）
- 检测到冰箱时立即设置 args['ret'] = True 取消原版行为
- 取消行为后阻止容器打开和放水

关键点:
- args['ret'] = True 必须在确认是冰箱后立即设置
- 防止原版容器打开（冰箱主方块）或放水（占位方块）
- BlockEntityData 不支持 .get() 方法，必须使用 safe_get

注意事项:
- 需处理占位方块情况，从 BlockEntityData 获取主方块位置
- 容器满时不消耗水桶，提示冰箱已满
- 水桶堆叠数量>1时减少数量，生成空桶到背包
"""

import time
from ..QuModLibs.Server import *
from ..config import ICE_MAKER_BLOCKS, ALL_PLACEHOLDER_BLOCKS, ICE_BLOCK_NAME, ICE_PRODUCE_COUNT, ICE_MAKER_COOLDOWN
from .placeholder import safe_get


last_ice_time = {}

BUCKET_WATER = 'minecraft:water_bucket'
BUCKET_EMPTY = 'minecraft:bucket'


def get_main_block_from_placeholder(block_pos, dimension):
    """
    从占位方块获取主方块位置
    
    Args:
        block_pos: 占位方块位置
        dimension: 维度ID
    
    Returns:
        tuple or None: 主方块位置
    """
    comp = serverApi.GetEngineCompFactory()
    block_entity_comp = comp.CreateBlockEntityData(serverApi.GetLevelId)
    data = block_entity_comp.GetBlockEntityData(dimension, block_pos)
    
    # BlockEntityData 不支持 .get() 方法，必须使用 safe_get
    main_pos = safe_get(data, 'main_block')
    if main_pos:
        return tuple(main_pos)
    return None


def find_slot_for_ice(main_pos, dimension, amount=16):
    """
    找到可放入冰块的槽位，优先合并已有冰块
    
    Args:
        main_pos: 冰箱主方块位置
        dimension: 维度ID
        amount: 要放入的冰块数量
    
    Returns:
        bool: True=成功放入，False=容器已满
    """
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(serverApi.GetLevelId)
    container_size = item_comp.GetContainerSize(main_pos, dimension)
    
    # 首先尝试找到已有冰块且不满64的槽位
    for slot in range(container_size):
        item = item_comp.GetContainerItem(main_pos, slot, dimension)
        if item and item.get('newItemName') == ICE_BLOCK_NAME:
            current_count = item.get('count', 0)
            if current_count < 64:
                new_count = min(current_count + amount, 64)
                item_comp.SpawnItemToContainer({
                    'newItemName': ICE_BLOCK_NAME,
                    'count': new_count
                }, slot, main_pos, dimension)
                return True
    
    # 其次找空槽位
    for slot in range(container_size):
        item = item_comp.GetContainerItem(main_pos, slot, dimension)
        if item is None or item.get('newItemName') == 'minecraft:air':
            item_comp.SpawnItemToContainer({
                'newItemName': ICE_BLOCK_NAME,
                'count': amount
            }, slot, main_pos, dimension)
            return True
    
    return False


@Listen(Events.ServerItemUseOnEvent)
def on_ice_maker_use(args):
    """
    冰箱制冰事件处理
    
    当玩家手持水桶点击冰箱时触发，执行制冰逻辑。
    注意：args['ret'] = True 需要在确认是冰箱后立即设置，以取消原版行为。
    """
    block_name = args.get('blockName', '')
    item_dict = args.get('itemDict', {})
    
    if not item_dict:
        return
    
    item_name = item_dict.get('newItemName', '')
    if item_name != BUCKET_WATER:
        return
    
    player_id = args.get('entityId')
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    block_pos = (x, y, z)
    
    # 获取主方块位置并立即取消原版行为
    # 关键：确认是冰箱后立即设置 args['ret'] = True，防止原版容器打开/放水
    main_pos = None
    
    if block_name in ICE_MAKER_BLOCKS:
        # 直接点击冰箱主方块 → 立即取消原版行为（容器打开 + 放水）
        args['ret'] = True
        main_pos = block_pos
    elif block_name in ALL_PLACEHOLDER_BLOCKS:
        # 点击占位方块，检查是否是冰箱的占位
        main_pos = get_main_block_from_placeholder(block_pos, dimension)
        if main_pos:
            comp = serverApi.GetEngineCompFactory()
            block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
            main_block = block_comp.GetBlockNew(main_pos, dimension)
            if main_block.get('name') in ICE_MAKER_BLOCKS:
                # 确认是冰箱的占位 → 立即取消原版行为（放水）
                args['ret'] = True
            else:
                # 不是冰箱的占位，不取消原版行为
                return
        else:
            # 无法获取主方块位置，不取消原版行为
            return
    else:
        # 不是冰箱，不取消原版行为
        return
    
    # 冷却检查（原版行为已在上方取消）
    now = time.time()
    last_time = last_ice_time.get(player_id, 0)
    if now - last_time < ICE_MAKER_COOLDOWN:
        return
    last_ice_time[player_id] = now
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    
    # 检查容器是否有空间
    if not find_slot_for_ice(main_pos, dimension, ICE_PRODUCE_COUNT):
        game_comp.SetOneTipMessage(player_id, "冰箱已满")
        return
    
    # 水桶替换为空桶
    bucket_count = item_dict.get('count', 1)
    selected_slot = item_comp.GetSelectSlotId()
    
    if bucket_count == 1:
        empty_bucket = {
            'newItemName': BUCKET_EMPTY,
            'count': 1
        }
        item_comp.SpawnItemToPlayerInv(empty_bucket, player_id, selected_slot)
    else:
        # 水桶堆叠数量>1，减少数量
        remaining_water = {
            'newItemName': BUCKET_WATER,
            'count': bucket_count - 1
        }
        empty_bucket = {
            'newItemName': BUCKET_EMPTY,
            'count': 1
        }
        item_comp.SpawnItemToPlayerInv(remaining_water, player_id, selected_slot)
        item_comp.SpawnItemToPlayerInv(empty_bucket, player_id, -1)
    
    game_comp.SetOneTipMessage(player_id, "制冰成功")