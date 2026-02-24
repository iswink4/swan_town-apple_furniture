# -*- coding: utf-8 -*-
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle

def __init__(self,namespace,system_name):
    ServerSystem.__init__(self,namespace,system_name)
    self.sit=0

@Listen(Events.ItemUseOnAfterServerEvent)
@QThrottle(intervalTime=0.2)
def change(args):
    '''
    原版斧子改变家具样式
    :param args: 事件参数
    :return: None
    '''
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
    # 桌子循环映射
    table_cycle = {
        'swan_town:table1': 'swan_town:table2',
        'swan_town:table2': 'swan_town:table3',
        'swan_town:table3': 'swan_town:table4',
        'swan_town:table4': 'swan_town:table1'
    }
    # 沙发循环
    sofa_cycle = {
        'swan_town:sofa1': 'swan_town:sofa2',
        'swan_town:sofa2': 'swan_town:sofa3',
        'swan_town:sofa3': 'swan_town:sofa4',
        'swan_town:sofa4': 'swan_town:sofa1'
    }
    # 长凳循环
    stool_cycle = {
        'swan_town:stool': 'swan_town:stool1',
        'swan_town:stool1': 'swan_town:stool2',
        'swan_town:stool2': 'swan_town:stool3',
        'swan_town:stool3': 'swan_town:stool',
    }
    # 画循环
    picture_cycle = {
        'swan_town:picture1': 'swan_town:picture2',
        'swan_town:picture2': 'swan_town:picture3',
        'swan_town:picture3': 'swan_town:picture1',
    }
    # 电视循环
    tv_cycle = {
        'swan_town:tv1': 'swan_town:tv2',
        'swan_town:tv2': 'swan_town:tv1',
    }
    # 电脑循环
    computer_cycle = {
        'swan_town:computer1': 'swan_town:computer2',
        'swan_town:computer2': 'swan_town:computer1',
    }
    # 窗帘循环1
    curtain_cycle1 = {
        'swan_town:curtain11': 'swan_town:curtain12',
        'swan_town:curtain12': 'swan_town:curtain13',
        'swan_town:curtain13': 'swan_town:curtain14',
        'swan_town:curtain14': 'swan_town:curtain15',
        'swan_town:curtain15': 'swan_town:curtain16',
        'swan_town:curtain16': 'swan_town:curtain17',
        'swan_town:curtain17': 'swan_town:curtain11',
    }
    # 窗帘循环2
    curtain_cycle2 = {
        'swan_town:curtain21': 'swan_town:curtain22',
        'swan_town:curtain22': 'swan_town:curtain23',
        'swan_town:curtain23': 'swan_town:curtain24',
        'swan_town:curtain24': 'swan_town:curtain21',
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
    # 检查当前方块是否在沙发循环映射中
    if block_name in sofa_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': sofa_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在长凳循环映射中
    if block_name in stool_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': stool_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在画循环映射中
    if block_name in picture_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': picture_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在电视循环映射中
    if block_name in tv_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': tv_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在电脑循环映射中
    if block_name in computer_cycle and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': computer_cycle[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在窗帘循环1映射中
    if block_name in curtain_cycle1 and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': curtain_cycle1[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
    # 检查当前方块是否在窗帘循环2映射中
    if block_name in curtain_cycle2 and item_dict['newItemName'] in axe_name:
        old_block_dict=comp.GetBlockNew(block_pos,dimension)
        old_aux=old_block_dict['aux']
        block_dict = {
            'name': curtain_cycle2[block_name],
            'aux': old_aux
        }
        comp.SetBlockNew((block_pos), block_dict, 0, dimension)
@Listen(Events.ServerBlockUseEvent)
def use(args):
    '''
    家具交互
    :param args: 事件参数
    :return: None
    '''
    block_name = args['blockName']
    player_id = args['playerId']
    x=args['x']
    y=args['y']
    z=args['z']
    
    timercomp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
    commandcomp = serverApi.GetEngineCompFactory().CreateCommand(serverApi.GetLevelId())
    playercomp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    
    chair_list = [
        'swan_town:sofa1',
        'swan_town:sofa2',
        'swan_town:sofa3',
        'swan_town:sofa4',
    ]
    
        