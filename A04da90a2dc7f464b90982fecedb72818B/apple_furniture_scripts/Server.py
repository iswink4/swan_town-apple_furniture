# -*- coding: utf-8 -*-
import time

from A04da90a2dc7f464b90982fecedb72818B.apple_furniture_scripts.QuModLibs.Client import clientApi
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
    #if block_name in table_cycle and item_dict['newItemName'] in axe_name:
    #    block_dict = {
    #        'name': table_cycle[block_name]
    #    }
    #    comp.SetBlockNew((block_pos), block_dict, 0, dimension)
@Listen(Events.ServerEntityTryPlaceBlockEvent)
def offset(args):
    block_pos=args["x"],args["y"],args["z"]
    block_name=args["fullName"]
    dimension=args["dimensionId"]
    print(block_name)

    