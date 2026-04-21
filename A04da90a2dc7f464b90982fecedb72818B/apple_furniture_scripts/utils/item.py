# -*- coding: utf-8 -*-
"""
物品操作工具模块
提供获取玩家手持物品、检查空手等公共操作
"""

from ..QuModLibs.Server import serverApi


def get_hand_item(player_id):
    """
    获取玩家主手物品
    
    Args:
        player_id: 玩家ID
    
    Returns:
        dict: 物品信息字典，无物品返回None
    
    Example:
        item = get_hand_item(player_id)
        if item:
            item_name = item.get('newItemName', '')
    """
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    return hand_item


def get_hand_item_name(player_id):
    """
    获取玩家主手物品名称
    
    Args:
        player_id: 玩家ID
    
    Returns:
        str: 物品名称，无物品返回空字符串
    
    Example:
        item_name = get_hand_item_name(player_id)
        if item_name == 'minecraft:water_bucket':
            # 处理水桶逻辑...
    """
    item = get_hand_item(player_id)
    if not item:
        return ''
    return item.get('newItemName', '')


def is_empty_hand(player_id):
    """
    检查玩家是否空手
    
    Args:
        player_id: 玩家ID
    
    Returns:
        bool: True=空手，False=有物品
    
    Example:
        if is_empty_hand(player_id):
            # 空手交互逻辑...
    """
    item = get_hand_item(player_id)
    if not item:
        return True
    item_name = item.get('newItemName', '')
    return item_name == '' or item_name == 'minecraft:air'


def get_selected_slot(player_id):
    """
    获取玩家当前选中的背包槽位
    
    Args:
        player_id: 玩家ID
    
    Returns:
        int: 槽位索引
    """
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    return item_comp.GetSelectSlotId()


def spawn_item_to_slot(player_id, item_dict, slot=-1):
    """
    生成物品到玩家背包槽位
    
    Args:
        player_id: 玩家ID
        item_dict: 物品信息字典 {'newItemName': 'xxx', 'count': n}
        slot: 槽位索引，-1表示自动寻找空槽位
    
    Returns:
        bool: 是否成功
    
    Example:
        spawn_item_to_slot(player_id, {'newItemName': 'minecraft:bucket', 'count': 1})
    """
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    return item_comp.SpawnItemToPlayerInv(item_dict, player_id, slot)