# -*- coding: utf-8 -*-
"""
方块操作工具模块
提供方块循环切换、方块替换等公共操作
"""

from ..QuModLibs.Server import serverApi


def cycle_block(block_pos, block_name, dimension, cycle_map):
    """
    循环切换方块类型，保留aux值
    
    Args:
        block_pos: 方块位置元组 (x, y, z)
        block_name: 当前方块名称
        dimension: 维度ID
        cycle_map: 循环映射字典（如 ALL_BLOCK_CYCLES）
    
    Returns:
        bool: True=成功切换，False=方块不在循环映射中
    
    Example:
        cycle_block((10, 5, 20), 'swan_town:table1', 0, ALL_BLOCK_CYCLES)
    """
    if block_name not in cycle_map:
        return False
    
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    
    old_block_dict = block_comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    
    new_block_dict = {
        'name': cycle_map[block_name],
        'aux': old_aux
    }
    block_comp.SetBlockNew(block_pos, new_block_dict, 0, dimension)
    return True


def replace_block(block_pos, new_block_name, dimension, keep_aux=True):
    """
    替换方块，可选保留aux值
    
    Args:
        block_pos: 方块位置元组 (x, y, z)
        new_block_name: 新方块名称
        dimension: 维度ID
        keep_aux: 是否保留原方块的aux值（朝向等）
    
    Returns:
        None
    
    Example:
        replace_block((10, 5, 20), 'swan_town:light1_off', 0)
        replace_block((10, 5, 20), 'minecraft:air', 0, keep_aux=False)
    """
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    
    if keep_aux:
        old_block_dict = block_comp.GetBlockNew(block_pos, dimension)
        old_aux = old_block_dict['aux']
        new_block_dict = {'name': new_block_name, 'aux': old_aux}
    else:
        new_block_dict = {'name': new_block_name, 'aux': 0}
    
    block_comp.SetBlockNew(block_pos, new_block_dict, 0, dimension)


def get_block_aux(block_pos, dimension):
    """
    获取方块的aux值
    
    Args:
        block_pos: 方块位置元组
        dimension: 维度ID
    
    Returns:
        int: aux值（朝向等）
    """
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    block_dict = block_comp.GetBlockNew(block_pos, dimension)
    return block_dict['aux']


def get_block_name(block_pos, dimension):
    """
    获取方块名称
    
    Args:
        block_pos: 方块位置元组
        dimension: 维度ID
    
    Returns:
        str: 方块名称
    """
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    block_dict = block_comp.GetBlockNew(block_pos, dimension)
    return block_dict['name']