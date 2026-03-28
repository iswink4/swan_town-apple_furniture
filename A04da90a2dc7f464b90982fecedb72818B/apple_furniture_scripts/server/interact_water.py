# -*- coding: utf-8 -*-
"""
模块名称: interact_water.py
功能描述: 处理水桶交互逻辑，支持空桶装水、水桶放水，可选方块替换

事件监听:
- ServerBlockUseEvent: 玩家右键点击方块时触发（空桶装水）
- ServerItemUseOnEvent: 玩家对方块使用物品之前触发（水桶放水）

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: WATER_TANK_BLOCKS, BUCKET_INTERACT_COOLDOWN

实现逻辑:
1. 空桶装水：
   - 检查 enable_fill 是否启用
   - 执行装水（空桶 → 水桶）
   - 如果 fill_replace 有值，替换方块
2. 水桶放水：
   - 检查 enable_empty 是否启用
   - 如果启用：取消原版行为，执行放水（水桶 → 空桶）
   - 如果未启用：允许原版放水行为
   - 如果 empty_replace 有值，替换方块

注意事项:
- 使用冷却时间防止连续触发
- 替换方块时保留aux值（朝向等）
- posType=2 表示主手物品
"""

import time
from ..QuModLibs.Server import *
from ..config import WATER_TANK_BLOCKS, BUCKET_INTERACT_COOLDOWN


last_interact_time = {}

BUCKET_EMPTY = 'minecraft:bucket'
BUCKET_WATER = 'minecraft:water_bucket'


def _parse_block_config(block_name):
    """
    解析方块配置，返回统一格式
    
    Args:
        block_name: 方块名称
    
    Returns:
        dict: 配置字典，包含:
            - enable_fill: 是否启用装水
            - enable_empty: 是否启用放水
            - fill_replace: 装水时替换的目标方块
            - empty_replace: 放水时替换的目标方块
    """
    config = WATER_TANK_BLOCKS.get(block_name, {})
    return {
        'enable_fill': config.get('enable_fill', True),
        'enable_empty': config.get('enable_empty', True),
        'fill_replace': config.get('fill_replace'),
        'empty_replace': config.get('empty_replace'),
    }


def _replace_block(block_pos, new_block_name, dimension):
    """
    替换方块，保留aux值
    
    Args:
        block_pos: 方块位置元组
        new_block_name: 新方块名称
        dimension: 维度ID
    
    Returns:
        None
    """
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    new_block_dict = {
        'name': new_block_name,
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, new_block_dict, 0, dimension)


@Listen(Events.ServerBlockUseEvent)
def on_water_tank_use(args):
    """
    水槽交互事件处理 - 空桶装水
    
    当玩家右键点击水槽方块时，如果手持空桶则执行装水操作。
    根据配置决定是否替换方块。
    """
    block_name = args['blockName']
    
    if block_name not in WATER_TANK_BLOCKS:
        return
    
    config = _parse_block_config(block_name)
    
    if not config['enable_fill']:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    
    if not hand_item:
        return
    
    item_name = hand_item.get('newItemName', '')
    item_count = hand_item.get('count', 0)
    
    if item_name != BUCKET_EMPTY:
        return
    
    now = time.time()
    last_time = last_interact_time.get(player_id, 0)
    if now - last_time < BUCKET_INTERACT_COOLDOWN:
        return
    last_interact_time[player_id] = now
    
    if item_count == 1:
        water_bucket = {
            'newItemName': BUCKET_WATER,
            'count': 1
        }
        item_comp.SpawnItemToPlayerInv(water_bucket, player_id, selected_slot)
    else:
        empty_bucket = {
            'newItemName': BUCKET_EMPTY,
            'count': item_count - 1
        }
        water_bucket = {
            'newItemName': BUCKET_WATER,
            'count': 1
        }
        if not item_comp.SpawnItemToPlayerInv(water_bucket, player_id, -1):
            return
        item_comp.SpawnItemToPlayerInv(empty_bucket, player_id, selected_slot)
    
    if config['fill_replace']:
        _replace_block(block_pos, config['fill_replace'], dimension)


@Listen(Events.ServerItemUseOnEvent)
def on_item_use_on(args):
    """
    物品使用事件处理 - 水桶放水
    
    当玩家手持水桶对方块使用时，检查配置决定行为：
    - 如果启用放水：取消原版行为，执行自定义放水
    - 如果未启用：允许原版放水行为
    根据配置决定是否替换方块。
    """
    block_name = args['blockName']
    
    if block_name not in WATER_TANK_BLOCKS:
        return
    
    config = _parse_block_config(block_name)
    
    if not config['enable_empty']:
        return
    
    item_dict = args['itemDict']
    if not item_dict:
        return
    
    item_name = item_dict.get('newItemName', '')
    
    if item_name != BUCKET_WATER:
        return
    
    entity_id = args['entityId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    block_pos = (x, y, z)
    
    now = time.time()
    last_time = last_interact_time.get(entity_id, 0)
    if now - last_time < BUCKET_INTERACT_COOLDOWN:
        args['ret'] = True
        return
    last_interact_time[entity_id] = now
    
    args['ret'] = True
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(entity_id)
    selected_slot = item_comp.GetSelectSlotId()
    
    empty_bucket = {
        'newItemName': BUCKET_EMPTY,
        'count': 1
    }
    item_comp.SpawnItemToPlayerInv(empty_bucket, entity_id, selected_slot)
    
    if config['empty_replace']:
        _replace_block(block_pos, config['empty_replace'], dimension)