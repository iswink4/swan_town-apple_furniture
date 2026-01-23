# -*- coding: utf-8 -*-
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle

@Listen(Events.ItemUseOnAfterServerEvent)
@QThrottle(intervalTime=0.2)
def change(args):
    item_dict=args["itemDict"]
    block_pos=args["x"],args["y"],args["z"]
    block_name=args["blockName"]
    dimension=args["dimensionId"]
    comp=serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
    # 原版斧子
    axe_name={
        'minecraft:axe',
        'minecraft:wooden_axe',
        'minecraft:stone_axe',
        'minecraft:iron_axe',
        'minecraft:diamond_axe',
        'minecraft:netherite_axe',
        'minecraft:golden_axe',
    }
    # 桌子状态循环映射
    table_cycle = {
        'swan_town:table1': 'swan_town:table2',
        'swan_town:table2': 'swan_town:table3',
        'swan_town:table3': 'swan_town:table4',
        'swan_town:table4': 'swan_town:table1'
    }
    
    # 检查当前方块是否在循环映射中
    # 桌子循环
    if block_name in table_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': table_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
        
    # 橱柜循环
    cabinet_cycle = {
        'swan_town:cabinet1': 'swan_town:cabinet2',
        'swan_town:cabinet2': 'swan_town:cabinet3',
        'swan_town:cabinet3': 'swan_town:cabinet1'
    }
    # 检查当前方块是否在橱柜循环映射中
    if block_name in cabinet_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': cabinet_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
        
    # 沙发循环
    sofa_cycle = {
        'swan_town:sofa1': 'swan_town:sofa2',
        'swan_town:sofa2': 'swan_town:sofa3',
        'swan_town:sofa3': 'swan_town:sofa4',
        'swan_town:sofa4': 'swan_town:sofa1'
    }
    # 检查当前方块是否在沙发循环映射中
    if block_name in sofa_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': sofa_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
        
    #  长凳循环
    stool_cycle = {
        'swan_town:stool1': 'swan_town:stool2',
        'swan_town:stool2': 'swan_town:stool3',
        'swan_town:stool3': 'swan_town:stool1',
    }
    # 检查当前方块是否在 stool循环映射中
    if block_name in stool_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': stool_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
        
    