# -*- coding: utf-8 -*-
"""
模块名称: interact_block.py
功能描述: 处理方块交互逻辑，包括斧子右键循环切换家具样式

事件监听:
- ItemUseOnAfterServerEvent: 玩家使用物品点击方块后触发

外部依赖:
- QuModLibs.Server: 服务端基础API（serverApi, Events, Listen, Call等）
- QuModLibs.Util: QThrottle装饰器用于限流
- config: AXE_NAMES（斧子列表）, ALL_BLOCK_CYCLES（方块循环映射）

实现逻辑:
1. 监听物品使用事件
2. 检查是否是斧子右键点击可循环方块
3. 调用 _cycle_block 执行样式切换
4. 使用 QThrottle 限流（0.2秒间隔），防止tick级连续触发

注意事项:
- 本模块无持久化状态
- 样式切换基于 config.ALL_BLOCK_CYCLES 配置的字典映射
- 切换时保留原方块的aux数据（朝向等）
"""
from ..QuModLibs.Server import *
from ..QuModLibs.Util import QThrottle
from ..config import AXE_NAMES, ALL_BLOCK_CYCLES


def _cycle_block(comp, block_pos, block_name, dimension):
    """
    循环切换方块类型
    
    根据 ALL_BLOCK_CYCLES 映射表，将当前方块切换到下一个样式。
    切换时保留原方块的aux值（朝向、状态等）。
    
    Args:
        comp: 方块信息组件 (BlockInfoComponent)
        block_pos: 方块位置元组 (x, y, z)
        block_name: 当前方块名称
        dimension: 维度ID
    
    Returns:
        None
    
    Example:
        swan_town:table1 -> swan_town:table2 -> swan_town:table3 -> swan_town:table4 -> swan_town:table1
    """
    old_block_dict = comp.GetBlockNew(block_pos, dimension)
    old_aux = old_block_dict['aux']
    block_dict = {
        'name': ALL_BLOCK_CYCLES[block_name],
        'aux': old_aux
    }
    comp.SetBlockNew(block_pos, block_dict, 0, dimension)


@Listen(Events.ItemUseOnAfterServerEvent)
@QThrottle(intervalTime=0.2)
def on_item_use(args):
    """
    物品使用事件处理 - 斧子改变家具样式
    
    当玩家使用斧子右键点击支持样式循环的方块时，触发样式切换。
    使用 QThrottle 装饰器进行0.2秒限流，防止连续快速点击导致的问题。
    
    Args:
        args: 事件参数字典，包含:
            - itemDict: 物品信息字典
            - x, y, z: 方块坐标
            - blockName: 方块名称
            - dimensionId: 维度ID
    
    Returns:
        None
    
    Note:
        需要在 config.ALL_BLOCK_CYCLES 中配置方块循环映射才能生效
    """
    item_dict = args["itemDict"]
    block_pos = args["x"], args["y"], args["z"]
    block_name = args["blockName"]
    dimension = args["dimensionId"]
    
    # 检查是否是斧子右键可循环方块
    if item_dict.get('newItemName', '') in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
        _cycle_block(comp, block_pos, block_name, dimension)
