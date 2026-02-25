# -*- coding: utf-8 -*-
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle
from .config import AXE_NAMES, ALL_BLOCK_CYCLES, CHAIR_LIST

def __init__(self,namespace,system_name):
    ServerSystem.__init__(self,namespace,system_name)
    self.sit=0

def _cycle_block(comp, block_pos, block_name, dimension):
    '''
    循环切换方块类型
    :param comp: 方块信息组件
    :param block_pos: 方块位置
    :param block_name: 当前方块名称
    :param dimension: 维度ID
    :return: None
    '''
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    block_dict = {
        'name': ALL_BLOCK_CYCLES[block_name],
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, block_dict, 0, dimension)

@Listen(Events.ItemUseOnAfterServerEvent)
@QThrottle(intervalTime=0.2)
def change(args):
    '''
    原版斧子改变家具样式
    :param args: 事件参数
    :return: None
    '''
    item_dict = args["itemDict"]
    block_pos = args["x"], args["y"], args["z"]
    block_name = args["blockName"]
    dimension = args["dimensionId"]
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
    
    # 检查当前方块是否在循环映射中，且使用的是斧子
    if item_dict['newItemName'] in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        _cycle_block(comp, block_pos, block_name, dimension)

@Listen(Events.ServerBlockUseEvent)
def use(args):
    '''
    家具交互
    :param args: 事件参数
    :return: None
    '''
    block_name = args['blockName']
    player_id = args['playerId']
    x = args['x']
    y = args['y']
    z = args['z']
    
    timercomp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
    commandcomp = serverApi.GetEngineCompFactory().CreateCommand(serverApi.GetLevelId())
    playercomp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
