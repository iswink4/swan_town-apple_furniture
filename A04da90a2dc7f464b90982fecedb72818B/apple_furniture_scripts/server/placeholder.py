# -*- coding: utf-8 -*-
"""
模块名称: placeholder.py
功能描述: 占位方块系统，支持大型家具的多格碰撞箱

数据存储: 使用 BlockEntityData 持久化存储
- 家具方块: {'placeholders': [(x,y,z), ...]}
- 占位方块: {'main_block': (x,y,z), 'furniture': str, 'placeholder_type': str}

事件监听:
- ServerEntityTryPlaceBlockEvent: 放置前检测空间是否足够
- EntityPlaceBlockAfterServerEvent: 放置家具时同步放置占位方块
- ServerPlayerTryDestroyBlockEvent: 玩家尝试破坏方块时连锁销毁
- ServerBlockUseEvent: 空手交互转发
- ItemUseOnAfterServerEvent: 斧子交互转发
"""
from ..QuModLibs.Server import *
from ..config import PLACEHOLDER_TYPES, PLACEHOLDER_DEFAULT_TYPE, PLACEHOLDER_CONFIG, PLACEHOLDER_FURNITURES, ALL_PLACEHOLDER_BLOCKS
from ..config import ALL_BLOCK_CYCLES, AXE_NAMES, ALL_HAND_BLOCK_CYCLES, CHAIR_LIST, BED_BLOCKS
from ..config import DIMENSION_NETHER, DIMENSION_END


# ============================================================
# 工具函数
# ============================================================

def rotate_offset(offset, aux):
    """根据方块朝向旋转偏移量"""
    dx, dy, dz = offset
    if aux == 0:
        return (dx, dy, dz)
    elif aux == 1:
        return (-dz, dy, dx)
    elif aux == 2:
        return (-dx, dy, -dz)
    elif aux == 3:
        return (dz, dy, -dx)
    return (dx, dy, dz)


def get_block_entity_data(dimension, pos):
    """获取可写的方块实体数据"""
    comp = serverApi.GetEngineCompFactory().CreateBlockEntityData(serverApi.GetLevelId)
    return comp.GetBlockEntityData(dimension, pos)


def safe_get(data, key, default=None):
    """安全获取 BlockEntityData 中的数据"""
    if data is None:
        return default
    try:
        value = data[key]
        return value if value is not None else default
    except:
        return default


def check_placeholder_space(x, y, z, dimension, furniture_name, aux):
    """
    检查占位方块位置是否有足够空间
    
    Returns:
        bool: True=可放置, False=空间不足
    """
    if furniture_name not in PLACEHOLDER_CONFIG:
        return True
    
    config = PLACEHOLDER_CONFIG[furniture_name]
    offsets = config.get('offsets', [])
    
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    
    for offset in offsets:
        dx, dy, dz = rotate_offset(offset, aux)
        check_pos = (x + dx, y + dy, z + dz)
        
        block_dict = block_comp.GetBlockNew(check_pos, dimension)
        block_name = block_dict.get('name', '') if block_dict else ''
        
        if block_name and block_name != 'minecraft:air':
            return False
    
    return True


# ============================================================
# 核心功能
# ============================================================

def place_placeholders(x, y, z, dimension, furniture_name, aux):
    """放置家具时，同步放置关联的占位方块"""
    if furniture_name not in PLACEHOLDER_CONFIG:
        return []
    
    config = PLACEHOLDER_CONFIG[furniture_name]
    offsets = config.get('offsets', [])
    placeholder_type = config.get('type', PLACEHOLDER_DEFAULT_TYPE)
    placeholder_block = PLACEHOLDER_TYPES.get(placeholder_type, PLACEHOLDER_TYPES[PLACEHOLDER_DEFAULT_TYPE])
    
    placed_positions = []
    
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    
    for offset in offsets:
        dx, dy, dz = rotate_offset(offset, aux)
        placeholder_pos = (x + dx, y + dy, z + dz)
        
        if block_comp.SetBlockNew(placeholder_pos, {'name': placeholder_block, 'aux': 0}, 0, dimension):
            placed_positions.append(placeholder_pos)
    
    all_placeholders = list(placed_positions)
    
    for placeholder_pos in placed_positions:
        placeholder_data = get_block_entity_data(dimension, placeholder_pos)
        if placeholder_data is not None:
            placeholder_data['main_block'] = (x, y, z)
            placeholder_data['furniture'] = furniture_name
            placeholder_data['all_placeholders'] = all_placeholders
            placeholder_data['placeholder_type'] = placeholder_type
    
    if placed_positions:
        main_data = get_block_entity_data(dimension, (x, y, z))
        if main_data is not None:
            main_data['placeholders'] = placed_positions
    
    return placed_positions


def destroy_furniture_group(x, y, z, dimension, is_placeholder=False):
    """销毁家具组"""
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    current_pos = (x, y, z)
    
    if is_placeholder:
        placeholder_data = get_block_entity_data(dimension, (x, y, z))
        if placeholder_data:
            main_pos = safe_get(placeholder_data, 'main_block')
            all_placeholders = safe_get(placeholder_data, 'all_placeholders', [])
            
            if main_pos:
                main_pos = tuple(main_pos)
            all_placeholders = [tuple(p) for p in all_placeholders]
            
            if main_pos:
                for pos in all_placeholders:
                    if pos != current_pos:
                        block_comp.SetBlockNew(pos, {'name': 'minecraft:air', 'aux': 0}, 0, dimension)
                
                block_comp.SetBlockNew(main_pos, {'name': 'minecraft:air', 'aux': 0}, 0, dimension)
    else:
        main_data = get_block_entity_data(dimension, (x, y, z))
        if main_data:
            placeholders = safe_get(main_data, 'placeholders', [])
            placeholders = [tuple(p) for p in placeholders]
            for pos in placeholders:
                block_comp.SetBlockNew(pos, {'name': 'minecraft:air', 'aux': 0}, 0, dimension)


def get_main_block_info(placeholder_pos, dimension):
    """从占位方块获取主方块信息"""
    data = get_block_entity_data(dimension, placeholder_pos)
    if data:
        return (safe_get(data, 'main_block'), safe_get(data, 'furniture'))
    return None


# ============================================================
# 床交互功能
# ============================================================

def handle_bed_interaction(player_id, main_pos, dimension, main_x, main_y, main_z):
    """处理床交互（设置重生点 + 睡觉）"""
    if dimension in [DIMENSION_NETHER, DIMENSION_END]:
        return
    
    from .interact_bed import sleeping_players, last_bed_use_time
    import time
    
    now = time.time()
    if now - last_bed_use_time.get(player_id, 0) < 0.5:
        return
    last_bed_use_time[player_id] = now
    
    if player_id in sleeping_players:
        from .interact_bed import wake_up
        wake_up(player_id, "manual")
        return
    
    comp = serverApi.GetEngineCompFactory()
    player_comp = comp.CreatePlayer(player_id)
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    
    # 确保 main_pos 是元组格式
    main_pos = tuple(main_pos) if main_pos else None
    
    actual_respawn = player_comp.GetPlayerRespawnPos()
    respawn_pos = None
    if actual_respawn:
        respawn_pos = actual_respawn.get("pos")
        if respawn_pos:
            respawn_pos = tuple(respawn_pos)
    
    is_current_spawn = (
        respawn_pos == main_pos and
        actual_respawn and
        actual_respawn.get("dimensionId") == dimension
    )
    
    if not is_current_spawn:
        game_comp.SetOneTipMessage(player_id, "已设置重生点")
        player_comp.SetPlayerRespawnPos(main_pos, dimension)
        return
    
    from .interact_bed import check_sleep_conditions, start_sleep
    can_sleep, reason = check_sleep_conditions(main_x, main_y, main_z, dimension)
    if not can_sleep:
        game_comp.SetOneTipMessage(player_id, reason)
        return
    
    start_sleep(player_id, main_x, main_y, main_z, dimension)


# ============================================================
# 事件处理
# ============================================================

@Listen(Events.ServerEntityTryPlaceBlockEvent)
def on_try_place_block(args):
    """方块放置前事件 - 检测占位位置是否有空间"""
    block_name = args.get('fullName', '')
    if block_name not in PLACEHOLDER_FURNITURES:
        return
    
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    aux = args.get('auxData', 0)
    entity_id = args.get('entityId')
    
    if not check_placeholder_space(x, y, z, dimension, block_name, aux):
        args['cancel'] = True
        
        if entity_id:
            comp = serverApi.GetEngineCompFactory()
            game_comp = comp.CreateGame(serverApi.GetLevelId)
            game_comp.SetOneTipMessage(entity_id, "空间不足！")


@Listen(Events.EntityPlaceBlockAfterServerEvent)
def on_block_placed(args):
    """方块放置事件"""
    block_name = args.get('fullName', '')
    if block_name not in PLACEHOLDER_FURNITURES:
        return
    
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    aux = args.get('auxData', 0)
    
    place_placeholders(x, y, z, dimension, block_name, aux)


@Listen(Events.ServerPlayerTryDestroyBlockEvent)
def on_try_destroy_block(args):
    """玩家尝试破坏方块事件"""
    block_name = args.get('fullName', '')
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    
    if block_name in ALL_PLACEHOLDER_BLOCKS:
        destroy_furniture_group(x, y, z, dimension, is_placeholder=True)
    elif block_name in PLACEHOLDER_FURNITURES:
        destroy_furniture_group(x, y, z, dimension, is_placeholder=False)


@Listen(Events.ServerBlockUseEvent)
def on_placeholder_use(args):
    """方块使用事件"""
    block_name = args.get('blockName', '')
    if block_name not in ALL_PLACEHOLDER_BLOCKS:
        return
    
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    player_id = args.get('playerId')
    
    main_info = get_main_block_info((x, y, z), dimension)
    if not main_info:
        return
    
    main_pos, furniture_name = main_info
    if not main_pos or not furniture_name:
        return
    
    main_x, main_y, main_z = main_pos
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    selected_slot = item_comp.GetSelectSlotId()
    hand_item = item_comp.GetPlayerItem(2, selected_slot, False)
    item_name = hand_item.get('newItemName', '') if hand_item else ''
    
    if item_name and item_name != 'minecraft:air':
        if item_name in AXE_NAMES and furniture_name in ALL_BLOCK_CYCLES:
            block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
            old_aux = block_comp.GetBlockNew(main_pos, dimension).get('aux', 0)
            block_comp.SetBlockNew(main_pos, {'name': ALL_BLOCK_CYCLES[furniture_name], 'aux': old_aux}, 0, dimension)
        return
    
    if furniture_name in ALL_HAND_BLOCK_CYCLES:
        block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
        old_aux = block_comp.GetBlockNew(main_pos, dimension).get('aux', 0)
        block_comp.SetBlockNew(main_pos, {'name': ALL_HAND_BLOCK_CYCLES[furniture_name], 'aux': old_aux}, 0, dimension)
        return
    
    if furniture_name in CHAIR_LIST:
        from .interact_seat import sitting_players, sit_down, stand_up, last_sit_time
        import time
        
        now = time.time()
        if now - last_sit_time.get(player_id, 0) < 0.3:
            return
        last_sit_time[player_id] = now
        
        if player_id in sitting_players:
            stand_up(player_id)
        else:
            sit_down(player_id, main_x, main_y, main_z)
        return
    
    if furniture_name in BED_BLOCKS:
        handle_bed_interaction(player_id, main_pos, dimension, main_x, main_y, main_z)
        return


@Listen(Events.ItemUseOnAfterServerEvent)
def on_item_use_on_placeholder(args):
    """物品使用事件"""
    block_name = args.get('blockName', '')
    if block_name not in ALL_PLACEHOLDER_BLOCKS:
        return
    
    item_name = args.get('itemDict', {}).get('newItemName', '')
    if item_name not in AXE_NAMES:
        return
    
    x, y, z = args.get('x'), args.get('y'), args.get('z')
    dimension = args.get('dimensionId', 0)
    
    main_info = get_main_block_info((x, y, z), dimension)
    if not main_info:
        return
    
    main_pos, furniture_name = main_info
    if not main_pos or not furniture_name or furniture_name not in ALL_BLOCK_CYCLES:
        return
    
    comp = serverApi.GetEngineCompFactory()
    block_comp = comp.CreateBlockInfo(serverApi.GetLevelId)
    old_aux = block_comp.GetBlockNew(main_pos, dimension).get('aux', 0)
    block_comp.SetBlockNew(main_pos, {'name': ALL_BLOCK_CYCLES[furniture_name], 'aux': old_aux}, 0, dimension)