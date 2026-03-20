# -*- coding: utf-8 -*-
"""
家具模组服务端逻辑
功能：
1. 斧子右键改变家具样式
2. 玩家右键椅子/沙发坐下
3. 玩家移动/方块被破坏时自动站起
"""
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle
from .config import (
    AXE_NAMES, ALL_BLOCK_CYCLES, CHAIR_LIST, SIT_ANIMATION_NAME, SEAT_HEIGHT,
    BED_BLOCKS, DOUBLE_BED, SINGLE_BED, DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END,
    HOSTILE_MOBS, NIGHT_START_TIME, SLEEP_HEIGHT_OFFSET, MONSTER_CHECK_RADIUS, BED_CLEARANCE_HEIGHT
)

# ============================================================
# 全局数据存储
# ============================================================

# 坐下的玩家数据 {playerId: {"pos": (x,y,z), "seat_pos": (x,y,z)}}
sitting_players = {}

# 玩家上次坐下操作时间 {playerId: timestamp}
last_sit_time = {}

# ============================================================
# 睡觉玩家数据存储
# ============================================================

# 正在睡觉的玩家 {playerId: {"bed_pos": (x,y,z), "start_time": timestamp, "partner_id": playerId or None}}
sleeping_players = {}

# 玩家上次床交互时间 {playerId: timestamp}
last_bed_use_time = {}

# ============================================================
# 斧子改变家具样式功能
# ============================================================

def _cycle_block(comp, block_pos, block_name, dimension):
    """
    循环切换方块类型
    :param comp: 方块信息组件
    :param block_pos: 方块位置 (x, y, z)
    :param block_name: 当前方块名称
    :param dimension: 维度ID
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
    物品使用事件 - 处理斧子改变家具样式
    """
    item_dict = args["itemDict"]
    block_pos = args["x"], args["y"], args["z"]
    block_name = args["blockName"]
    dimension = args["dimensionId"]
    
    # 检查是否是斧子右键可循环方块
    if item_dict.get('newItemName', '') in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
        _cycle_block(comp, block_pos, block_name, dimension)

# ============================================================
# 坐下/站起功能
# ============================================================

@Listen(Events.ServerBlockUseEvent)
def on_block_use(args):
    """
    方块使用事件 - 处理玩家坐下/站起
    """
    block_name = args['blockName']
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    
    # 获取玩家主手物品
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    hand_item = item_comp.GetPlayerItem(2, 0, False)  # posType=2 表示主手
    item_name = hand_item.get('newItemName', '') if hand_item else ''
    
    # 如果手持斧子且方块支持样式切换，则跳过坐下功能（交给 on_item_use 处理）
    if item_name in AXE_NAMES and block_name in ALL_BLOCK_CYCLES:
        return
    
    # 检查是否是可坐下的方块
    if block_name not in CHAIR_LIST:
        return
    
    # 冷却检查，防止 tick 级别连续触发
    now = time.time()
    last_time = last_sit_time.get(player_id, 0)
    if now - last_time < 0.3:
        return
    last_sit_time[player_id] = now
    
    # 执行坐下或站起
    if player_id in sitting_players:
        stand_up(player_id)
    else:
        sit_down(player_id, x, y, z)

def sit_down(player_id, x, y, z):
    """
    玩家坐下
    :param player_id: 玩家ID
    :param x, y, z: 方块坐标
    """
    comp = serverApi.GetEngineCompFactory()
    
    # 计算座位位置（方块中心上方）
    seat_pos = (x + 0.5, y + SEAT_HEIGHT, z + 0.5)
    
    # 设置玩家位置
    pos_comp = comp.CreatePos(player_id)
    pos_comp.SetFootPos(seat_pos)
    
    # 记录玩家坐下数据
    sitting_players[player_id] = {
        "pos": (x, y, z),       # 方块位置
        "seat_pos": seat_pos    # 座位位置
    }
    
    # 通知客户端播放坐下动画
    Call(player_id, "PlaySitAnim")

def stand_up(player_id):
    """
    玩家站起
    :param player_id: 玩家ID
    """
    if player_id not in sitting_players:
        return
    
    # 清除坐下数据
    del sitting_players[player_id]
    
    # 通知客户端停止动画
    Call(player_id, "StopSitAnim")

# ============================================================
# 自动站起检测
# ============================================================

@Listen(Events.OnScriptTickServer)
def on_tick():
    """
    每帧检测 - 玩家移动时自动站起
    """
    comp = serverApi.GetEngineCompFactory()
    
    for player_id, data in list(sitting_players.items()):
        pos_comp = comp.CreatePos(player_id)
        current_pos = pos_comp.GetFootPos()
        
        if current_pos:
            # 计算玩家当前位置与座位位置的距离
            dx = current_pos[0] - data["seat_pos"][0]
            dy = current_pos[1] - data["seat_pos"][1]
            dz = current_pos[2] - data["seat_pos"][2]
            
            # 如果玩家离开了座位，自动站起
            if dx*dx + dy*dy + dz*dz > 0.3:
                stand_up(player_id)

@Listen(Events.DestroyBlockEvent)
def on_block_destroy(args):
    """
    方块被破坏事件 - 坐着的玩家自动站起
    """
    pos = (args['x'], args['y'], args['z'])
    
    for pid, data in list(sitting_players.items()):
        if data["pos"] == pos:
            stand_up(pid)

# ============================================================
# 床功能
# ============================================================

def get_other_bed_part(x, y, z, aux, is_double_bed):
    """
    获取双人床另一侧的位置
    :param x, y, z: 当前床的位置
    :param aux: 方块朝向数据
    :param is_double_bed: 是否为双人床
    :return: 另一侧位置或None
    """
    if not is_double_bed:
        return None
    
    # 根据aux值确定朝向，计算另一侧位置
    # aux: 0=北(-Z), 1=东(+X), 2=南(+Z), 3=西(-X)
    direction_map = {
        0: (0, 0, -1),  # 北
        1: (1, 0, 0),   # 东
        2: (0, 0, 1),   # 南
        3: (-1, 0, 0)   # 西
    }
    
    dx, dy, dz = direction_map.get(aux, (0, 0, 0))
    return (x + dx, y + dy, z + dz)

def check_bed_clearance(x, y, z, dimension):
    """
    检查床上方是否有足够空间
    :return: 是否空旷
    """
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId)
    
    for i in range(1, BED_CLEARANCE_HEIGHT + 1):
        block = comp.GetBlockNew((x, y + i, z), dimension)
        if block and block.get('name') != 'minecraft:air':
            return False
    return True

def check_monsters_nearby(x, y, z, dimension):
    """
    检查周围是否有敌对生物
    :return: 是否有怪物
    """
    comp = serverApi.GetEngineCompFactory()
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    
    # 获取范围内的所有实体
    start_pos = (x - MONSTER_CHECK_RADIUS, y - MONSTER_CHECK_RADIUS, z - MONSTER_CHECK_RADIUS)
    end_pos = (x + MONSTER_CHECK_RADIUS, y + MONSTER_CHECK_RADIUS, z + MONSTER_CHECK_RADIUS)
    entities = game_comp.GetEntitiesInSquareArea(None, start_pos, end_pos, dimension)
    
    for entity_id in entities:
        engine_type_comp = comp.CreateEngineType(entity_id)
        entity_type = engine_type_comp.GetEngineTypeStr()
        if entity_type in HOSTILE_MOBS:
            return True
    return False

def get_sleeping_player_on_bed(x, y, z):
    """
    获取指定位置床上正在睡觉的玩家
    :return: 玩家ID或None
    """
    for player_id, data in sleeping_players.items():
        bed_x, bed_y, bed_z = data["bed_pos"]
        if bed_x == x and bed_y == y and bed_z == z:
            return player_id
    return None

def start_sleep(player_id, x, y, z, dimension, is_double_bed=False, partner_id=None):
    """
    开始睡觉流程
    """
    comp = serverApi.GetEngineCompFactory()
    
    # 计算睡觉位置（床的中心点）
    sleep_pos = (x + 0.5, y + SLEEP_HEIGHT_OFFSET, z + 0.5)
    
    # 传送玩家到床上
    pos_comp = comp.CreatePos(player_id)
    pos_comp.SetFootPos(sleep_pos)
    
    # 记录睡觉数据
    sleeping_players[player_id] = {
        "bed_pos": (x, y, z),
        "start_time": time.time(),
        "partner_id": partner_id,
        "is_double_bed": is_double_bed
    }
    
    # 通知客户端开始睡觉（使用坐下动画 + 黑屏效果）
    Call(player_id, "StartSleep")
    
    # 如果是双人床且另一侧有玩家，同步开始睡觉
    if partner_id and partner_id in sleeping_players:
        Call(partner_id, "StartSleep")

def wake_up(player_id, wake_reason="manual"):
    """
    玩家起床
    :param player_id: 玩家ID
    :param wake_reason: 起床原因（manual手动, move移动, hurt受伤, destroy床被破坏）
    """
    if player_id not in sleeping_players:
        return
    
    data = sleeping_players[player_id]
    x, y, z = data["bed_pos"]
    partner_id = data.get("partner_id")
    
    # 清除睡觉数据
    del sleeping_players[player_id]
    
    # 通知客户端停止睡觉
    Call(player_id, "StopSleep")
    
    # 将玩家传送到床旁边（避免卡在床里）
    comp = serverApi.GetEngineCompFactory()
    pos_comp = comp.CreatePos(player_id)
    # 传送到床的一侧
    wake_pos = (x + 0.5, y, z + 1.5)
    pos_comp.SetFootPos(wake_pos)
    
    # 如果有搭档，搭档也起床
    if partner_id and partner_id in sleeping_players:
        wake_up(partner_id, "partner_wake")

def check_sleep_conditions(x, y, z, dimension):
    """
    检查睡觉条件
    :return: (是否满足, 原因消息)
    """
    comp = serverApi.GetEngineCompFactory()
    
    # 检查上方空间
    if not check_bed_clearance(x, y, z, dimension):
        return False, "床上方空间不足，无法躺下"
    
    # 检查周围怪物
    if check_monsters_nearby(x, y, z, dimension):
        return False, "周围有怪物游荡，无法入睡"
    
    # 检查时间和天气
    time_comp = comp.CreateTime(serverApi.GetLevelId)
    weather_comp = comp.CreateWeather(serverApi.GetLevelId)
    
    current_time = time_comp.GetTime()
    is_thunder = weather_comp.IsThunder()
    is_night = current_time > NIGHT_START_TIME
    
    # 雷暴天气或夜晚都可以睡觉
    if not (is_thunder or is_night):
        return False, "白天无法睡觉，只能在夜晚或雷暴天气时入睡"
    
    return True, ""

@Listen(Events.ServerBlockUseEvent)
def on_bed_use(args):
    """
    床方块使用事件
    """
    block_name = args['blockName']
    
    # 检查是否是床方块
    if block_name not in BED_BLOCKS:
        return
    
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    dimension = args['dimensionId']
    aux = args['aux']
    
    # 检查维度 - 末地和地狱直接阻止（无提示）
    if dimension in [DIMENSION_NETHER, DIMENSION_END]:
        return
    
    # 冷却检查
    now = time.time()
    last_time = last_bed_use_time.get(player_id, 0)
    if now - last_time < 0.5:
        return
    last_bed_use_time[player_id] = now
    
    # 如果玩家已经在睡觉，起床
    if player_id in sleeping_players:
        wake_up(player_id, "manual")
        return
    
    comp = serverApi.GetEngineCompFactory()
    
    # 设置重生点（立即执行）
    player_comp = comp.CreatePlayer(player_id)
    player_comp.SetPlayerRespawnPos((x, y, z), dimension)
    
    # 发送提示
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    game_comp.SetOneTipMessage(player_id, "已设置重生点")
    
    # 检查睡觉条件
    can_sleep, reason = check_sleep_conditions(x, y, z, dimension)
    if not can_sleep:
        game_comp.SetOneTipMessage(player_id, reason)
        return
    
    # 检查是否为双人床
    is_double_bed = block_name == DOUBLE_BED
    partner_id = None
    
    if is_double_bed:
        # 获取另一侧床的位置
        other_pos = get_other_bed_part(x, y, z, aux, is_double_bed)
        if other_pos:
            other_x, other_y, other_z = other_pos
            # 检查另一侧床上是否已有玩家在睡觉
            partner_id = get_sleeping_player_on_bed(other_x, other_y, other_z)
    
    # 开始睡觉
    start_sleep(player_id, x, y, z, dimension, is_double_bed, partner_id)

@Listen(Events.OnScriptTickServer)
def on_sleep_tick():
    """
    睡觉检测 - 检查是否需要跳过夜晚或起床
    """
    if not sleeping_players:
        return
    
    comp = serverApi.GetEngineCompFactory()
    now = time.time()
    
    for player_id, data in list(sleeping_players.items()):
        # 检查是否睡满3秒
        if now - data["start_time"] >= 3:
            # 设置时间为早晨
            time_comp = comp.CreateTime(serverApi.GetLevelId)
            time_comp.SetTime(0)
            
            # 所有睡觉的玩家起床
            for pid in list(sleeping_players.keys()):
                wake_up(pid, "morning")
            break
        
        # 检查玩家是否移动（距离判断）
        x, y, z = data["bed_pos"]
        sleep_pos = (x + 0.5, y + SLEEP_HEIGHT_OFFSET, z + 0.5)
        
        pos_comp = comp.CreatePos(player_id)
        current_pos = pos_comp.GetFootPos()
        
        if current_pos:
            dx = current_pos[0] - sleep_pos[0]
            dy = current_pos[1] - sleep_pos[1]
            dz = current_pos[2] - sleep_pos[2]
            
            # 如果玩家离开床超过0.5格，自动起床
            if dx*dx + dy*dy + dz*dz > 0.5:
                wake_up(player_id, "move")

@Listen(Events.DestroyBlockEvent)
def on_bed_destroy(args):
    """
    床被破坏事件 - 正在睡觉的玩家起床
    """
    pos = (args['x'], args['y'], args['z'])
    
    for player_id, data in list(sleeping_players.items()):
        if data["bed_pos"] == pos:
            wake_up(player_id, "destroy")

@Listen(Events.MobDieEvent)
def on_player_die(args):
    """
    玩家死亡事件 - 正在睡觉的玩家清除状态
    """
    # 注意：MobDieEvent 包含所有生物死亡，需要判断是否是玩家
    entity_id = args.get('id') or args.get('entityId')
    if entity_id in sleeping_players:
        del sleeping_players[entity_id]

@Listen(Events.PlayerHurtEvent)
def on_player_hurt(args):
    """
    玩家受伤事件 - 正在睡觉的玩家起床
    """
    player_id = args['entityId']
    if player_id in sleeping_players:
        wake_up(player_id, "hurt")