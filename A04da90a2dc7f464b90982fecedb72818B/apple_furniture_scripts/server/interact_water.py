# -*- coding: utf-8 -*-
"""
模块名称: interact_water.py
功能描述: 处理水桶交互逻辑，支持空桶装水、水桶倒水

事件监听:
- ServerBlockUseEvent: 玩家右键点击方块时触发（空桶装水）
- ServerItemUseOnEvent: 玩家对方块使用物品之前触发（水桶倒水）

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: WATER_TANK_BLOCKS, BUCKET_INTERACT_COOLDOWN

实现逻辑:
1. 玩家手持空桶点击方块 -> 装水（空桶变水桶）
2. 玩家手持水桶点击方块 -> 倒水（水桶变空桶）
3. 多个空桶时：减少1个空桶，在背包空位生成水桶
4. 背包满时不执行操作

注意事项:
- 使用冷却时间防止连续触发
- posType=2 表示主手物品
- 水桶倒水使用 ServerItemUseOnEvent 并设置 ret=True 取消原版行为
"""
import time
from ..QuModLibs.Server import *
from ..config import WATER_TANK_BLOCKS, BUCKET_INTERACT_COOLDOWN


# 交互冷却记录
last_interact_time = {}

# 物品常量
BUCKET_EMPTY = 'minecraft:bucket'
BUCKET_WATER = 'minecraft:water_bucket'


@Listen(Events.ServerBlockUseEvent)
def on_water_tank_use(args):
    """
    水槽交互事件处理 - 空桶装水
    
    当玩家右键点击水槽方块时，如果手持空桶则执行装水操作。
    """
    block_name = args['blockName']
    
    if block_name not in WATER_TANK_BLOCKS:
        return
    
    player_id = args['playerId']
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    
    # 获取当前选中槽位和主手物品
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    
    if not hand_item:
        return
    
    item_name = hand_item.get('newItemName', '')
    item_count = hand_item.get('count', 0)
    
    # 只处理空桶
    if item_name != BUCKET_EMPTY:
        return
    
    # 冷却检查
    now = time.time()
    last_time = last_interact_time.get(player_id, 0)
    if now - last_time < BUCKET_INTERACT_COOLDOWN:
        return
    last_interact_time[player_id] = now
    
    # 空桶装水
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


@Listen(Events.ServerItemUseOnEvent)
def on_item_use_on(args):
    """
    物品使用事件处理 - 水桶倒水
    
    当玩家手持水桶对方块使用时，检查是否点击了水槽方块，
    如果是则取消原版放水行为并将水桶变为空桶。
    """
    block_name = args['blockName']
    
    if block_name not in WATER_TANK_BLOCKS:
        return
    
    item_dict = args['itemDict']
    if not item_dict:
        return
    
    item_name = item_dict.get('newItemName', '')
    
    # 只处理水桶
    if item_name != BUCKET_WATER:
        return
    
    entity_id = args['entityId']
    
    # 冷却检查
    now = time.time()
    last_time = last_interact_time.get(entity_id, 0)
    if now - last_time < BUCKET_INTERACT_COOLDOWN:
        args['ret'] = True
        return
    last_interact_time[entity_id] = now
    
    # 取消原版放水行为
    args['ret'] = True
    
    # 水桶变空桶
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(entity_id)
    selected_slot = item_comp.GetSelectSlotId()
    
    empty_bucket = {
        'newItemName': BUCKET_EMPTY,
        'count': 1
    }
    item_comp.SpawnItemToPlayerInv(empty_bucket, entity_id, selected_slot)