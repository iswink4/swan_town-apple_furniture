# -*- coding: utf-8 -*-
"""
模块名称: interact_bed.py
功能描述: 处理床交互逻辑，包括单人床/双人床睡觉功能

事件监听:
- ServerBlockUseEvent: 玩家右键点击床方块时触发
- OnScriptTickServer: 服务端每帧触发，用于检测睡满3秒跳过夜晚
- DestroyBlockEvent: 床方块被破坏时触发
- MobDieEvent: 玩家死亡时触发，清除睡觉状态
- PlayerHurtEvent: 玩家受伤时触发，强制起床

外部依赖:
- QuModLibs.Server: 服务端基础API
- config: BED_BLOCKS（床方块列表）, DOUBLE_BED（双人床）, SINGLE_BED（单人床）,
          DIMENSION_*（维度常量）, HOSTILE_MOBS（敌对生物列表）, NIGHT_START_TIME,
          SLEEP_HEIGHT_OFFSET, MONSTER_CHECK_RADIUS, BED_CLEARANCE_HEIGHT

全局状态:
- sleeping_players: dict - 正在睡觉的玩家数据
  格式: {playerId: {"bed_pos": (x,y,z), "start_time": timestamp, 
                    "partner_id": playerId or None, "is_double_bed": bool}}
- last_bed_use_time: dict - 玩家上次床交互时间戳（冷却用）
  格式: {playerId: timestamp}

实现逻辑:
1. 监听方块使用事件，检查是否是床方块
2. 末地和地狱直接阻止（无提示）
3. 检查冷却时间（0.5秒），设置重生点
4. 检查睡觉条件（空间、怪物、时间/天气）
5. 双人床检测另一侧是否有玩家，支持同步睡觉
6. 开始睡觉：传送玩家、记录状态、通知客户端（黑屏+朝上视角）
7. OnScriptTickServer检测睡满3秒，设置时间为早晨，所有睡觉玩家起床
8. 检测玩家离开床（距离>0.5）、床被破坏、受伤、死亡时强制起床

跨端通信:
- Call(playerId, "StartSleep"): 通知客户端开始睡觉（黑屏+锁定视角）
- Call(playerId, "StopSleep"): 通知客户端停止睡觉（恢复视野）

双人床同步机制:
- 通过 aux 值确定床的朝向，计算另一侧位置
- 检查另一侧床上是否已有玩家，自动设为 partner_id
- 双方同时收到 StartSleep 通知，同时 wake_up

注意事项:
- 睡觉位置：床中心 + SLEEP_HEIGHT_OFFSET(0.6)
- 起床位置：床旁边 (z+1.5)
- 怪物检测范围：MONSTER_CHECK_RADIUS(8格)立方体区域
- 上方空间检查：BED_CLEARANCE_HEIGHT(2格)
"""
import time
from ..QuModLibs.Server import *
from ..config import (
    BED_BLOCKS, DOUBLE_BED, SINGLE_BED,
    DIMENSION_NETHER, DIMENSION_END,
    HOSTILE_MOBS, NIGHT_START_TIME, SLEEP_HEIGHT_OFFSET,
    MONSTER_CHECK_RADIUS, BED_CLEARANCE_HEIGHT
)


# ============================================================
# 全局状态
# ============================================================

# 正在睡觉的玩家数据
# 格式: {playerId: {"bed_pos": (x,y,z), "start_time": timestamp,
#                   "partner_id": playerId or None, "is_double_bed": bool}}
sleeping_players = {}

# 玩家上次床交互时间戳，用于冷却检查
# 格式: {playerId: timestamp}
last_bed_use_time = {}




# ============================================================
# 核心功能
# ============================================================

def get_other_bed_part(x, y, z, aux, is_double_bed):
    """
    获取双人床另一侧的位置
    
    根据床的 aux 值（朝向数据）计算另一侧床方块的位置。
    单人床直接返回 None。
    
    Args:
        x, y, z: int - 当前床的位置坐标
        aux: int - 方块朝向数据 (0=北, 1=东, 2=南, 3=西)
        is_double_bed: bool - 是否为双人床
    
    Returns:
        tuple or None - 另一侧位置 (x, y, z) 或 None（单人床）
    
    Note:
        aux 值对应方向：
        - 0: 北 (-Z)
        - 1: 东 (+X)
        - 2: 南 (+Z)
        - 3: 西 (-X)
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
    
    检查床上方 BED_CLEARANCE_HEIGHT 格内是否都是空气。
    
    Args:
        x, y, z: int - 床的位置坐标
        dimension: int - 维度ID
    
    Returns:
        bool - 是否空旷（可以睡觉）
    
    Note:
        如果上方有任何非空气方块，返回 False
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
    
    在 MONSTER_CHECK_RADIUS 范围内搜索敌对生物。
    
    Args:
        x, y, z: int - 中心位置坐标
        dimension: int - 维度ID
    
    Returns:
        bool - 是否有怪物（True=有怪物，不能睡觉）
    
    Note:
        检测范围是边长为 2*MONSTER_CHECK_RADIUS+1 的立方体
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
    
    Args:
        x, y, z: int - 床的位置坐标
    
    Returns:
        str or None - 玩家ID 或 None（床上无人）
    """
    for player_id, data in sleeping_players.items():
        bed_x, bed_y, bed_z = data["bed_pos"]
        if bed_x == x and bed_y == y and bed_z == z:
            return player_id
    return None


def start_sleep(player_id, x, y, z, dimension, is_double_bed=False, partner_id=None):
    """
    开始睡觉流程
    
    传送玩家到床上，记录睡觉状态，并通知客户端显示睡觉效果。
    
    Args:
        player_id: str - 玩家实体ID
        x, y, z: int - 床的位置坐标
        dimension: int - 维度ID
        is_double_bed: bool - 是否为双人床
        partner_id: str or None - 双人床另一侧玩家的ID
    
    Returns:
        None
    
    Side Effects:
        - 修改 sleeping_players 全局状态
        - 传送玩家到睡觉位置
        - 调用 Call 通知客户端开始睡觉效果
        - 如果 partner_id 有效，也会通知搭档
    
    Note:
        睡觉位置计算：床中心 + SLEEP_HEIGHT_OFFSET(0.6)
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
    
    # 通知客户端开始睡觉（黑屏效果 + 锁定视角朝天）
    Call(player_id, "StartSleep")
    
    # 如果是双人床且另一侧有玩家，同步开始睡觉
    if partner_id and partner_id in sleeping_players:
        Call(partner_id, "StartSleep")


def wake_up(player_id, wake_reason="manual"):
    """
    玩家起床
    
    清除睡觉状态，通知客户端恢复视野，将玩家传送到床旁边。
    
    Args:
        player_id: str - 玩家实体ID
        wake_reason: str - 起床原因，可选值：
            - "manual": 手动起床（再次右键床）
            - "move": 玩家离开床
            - "hurt": 玩家受伤
            - "destroy": 床被破坏
            - "morning": 早晨到来（睡满3秒）
            - "partner_wake": 搭档起床（双人床）
    
    Returns:
        None
    
    Side Effects:
        - 修改 sleeping_players 全局状态（删除对应项）
        - 传送玩家到床旁边（避免卡在床上）
        - 调用 Call 通知客户端停止睡觉效果
        - 如果是双人床且搭档还在睡，搭档也会起床
    
    Note:
        起床位置：床旁边 (x+0.5, y, z+1.5)
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
    
    综合检查是否满足睡觉的所有条件。
    
    Args:
        x, y, z: int - 床的位置坐标
        dimension: int - 维度ID
    
    Returns:
        tuple - (是否满足: bool, 原因消息: str)
        - 满足时返回 (True, "")
        - 不满足时返回 (False, "具体原因")
    
    Check List:
        1. 床上方空间是否充足
        2. 周围是否有敌对生物
        3. 是否为夜晚或雷暴天气
    
    Note:
        夜晚定义：时间 > NIGHT_START_TIME (12500 = 18:45)
        雷暴天气也可以睡觉
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


# ============================================================
# 事件处理
# ============================================================

@Listen(Events.ServerBlockUseEvent)
def on_bed_use(args):
    """
    床方块使用事件处理
    
    当玩家右键点击床方块时触发，处理设置重生点、检查睡觉条件、开始/结束睡觉。
    
    Args:
        args: 事件参数字典，包含:
            - blockName: 方块名称
            - playerId: 玩家ID
            - x, y, z: 方块坐标
            - dimensionId: 维度ID
            - aux: 方块朝向数据
    
    Returns:
        None
    
    Logic:
        1. 检查是否是床方块
        2. 末地和地狱直接阻止（无提示）
        3. 检查冷却时间（0.5秒）
        4. 如果已在睡觉，执行起床
        5. 设置重生点，发送提示
        6. 检查睡觉条件
        7. 检查是否为双人床，检测另一侧是否有玩家
        8. 开始睡觉
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
    player_comp = comp.CreatePlayer(player_id)
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    
    current_pos = (x, y, z)
    
    # 检查该床是否是玩家实际的重生点（使用引擎数据）
    actual_respawn = player_comp.GetPlayerRespawnPos()
    respawn_pos = None
    if actual_respawn:
        respawn_pos = actual_respawn.get("pos")
        if respawn_pos:
            respawn_pos = tuple(respawn_pos)
    is_current_spawn = (
        respawn_pos == current_pos and
        actual_respawn and
        actual_respawn.get("dimensionId") == dimension
    )
    
    if not is_current_spawn:
        # 设置重生点并发送提示
        game_comp.SetOneTipMessage(player_id, "已设置重生点")
        player_comp.SetPlayerRespawnPos(current_pos, dimension)
        return  # 本次点击不检查睡眠条件
    
    # 该床已是重生点，检查睡觉条件
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
    
    服务端每帧触发，检查所有睡觉的玩家：
    1. 是否睡满3秒 -> 跳过夜晚，所有玩家起床
    2. 是否离开床 -> 自动起床
    
    Args:
        无（事件触发，无参数）
    
    Returns:
        None
    
    Logic:
        遍历 sleeping_players：
        - 如果睡满3秒：设置时间为0（早晨），所有睡觉玩家起床
        - 如果离开床超过0.5格：自动起床
    
    Performance:
        O(n)，n为睡觉的玩家数量，每帧执行一次
        一旦有玩家睡满3秒，会立即跳出循环（break）
    """
    if not sleeping_players:
        return
    
    comp = serverApi.GetEngineCompFactory()
    now = time.time()
    
    for player_id, data in list(sleeping_players.items()):
        # 跳过刚入睡的玩家（等待位置同步）
        if now - data["start_time"] < 0.5:
            continue
        
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
            if dx*dx + dy*dy + dz*dz > 0.25:  # 0.5^2 = 0.25
                wake_up(player_id, "move")


@Listen(Events.DestroyBlockEvent)
def on_bed_destroy(args):
    """
    床被破坏事件 - 正在睡觉的玩家起床，重置重生点
    
    当床方块被破坏时触发：
    - 强制正在使用该床的玩家起床
    - 将该床设为重生点的玩家重置到世界出生点
    
    Args:
        args: 事件参数字典，包含:
            - x, y, z: 被破坏的方块坐标
            - dimensionId: 维度ID
    
    Returns:
        None
    """
    pos = (args['x'], args['y'], args['z'])
    dimension = args['dimensionId']
    
    comp = serverApi.GetEngineCompFactory()
    game_comp = comp.CreateGame(serverApi.GetLevelId)
    
    # 获取世界出生点
    world_spawn_pos = game_comp.GetSpawnPosition()
    world_spawn_dim = game_comp.GetSpawnDimension()
    
    # 遍历所有在线玩家，检查重生点是否在这个床上
    for player_id in serverApi.GetPlayerList():
        player_comp = comp.CreatePlayer(player_id)
        actual_respawn = player_comp.GetPlayerRespawnPos()
        
        if actual_respawn:
            respawn_pos = actual_respawn.get("pos")
            respawn_dim = actual_respawn.get("dimensionId")
            
            if respawn_pos == pos and respawn_dim == dimension:
                player_comp.SetPlayerRespawnPos(world_spawn_pos, world_spawn_dim)
    
    # 睡觉玩家起床逻辑
    for player_id, data in list(sleeping_players.items()):
        if data["bed_pos"] == pos:
            wake_up(player_id, "destroy")


@Listen(Events.MobDieEvent)
def on_player_die(args):
    """
    玩家死亡事件 - 正在睡觉的玩家清除状态
    
    当生物死亡时触发，如果是正在睡觉的玩家，清除其睡觉状态。
    
    Args:
        args: 事件参数字典，包含:
            - id 或 entityId: 死亡的实体ID
    
    Returns:
        None
    
    Note:
        MobDieEvent 包含所有生物死亡，需要判断是否是正在睡觉的玩家
        死亡时只清除状态，不调用 wake_up（玩家已死亡，不需要传送）
    """
    # 注意：MobDieEvent 包含所有生物死亡，需要判断是否是玩家
    entity_id = args.get('id') or args.get('entityId')
    if entity_id in sleeping_players:
        del sleeping_players[entity_id]


@Listen(Events.PlayerHurtEvent)
def on_player_hurt(args):
    """
    玩家受伤事件 - 正在睡觉的玩家起床
    
    当玩家受伤时触发，强制正在睡觉的玩家起床。
    
    Args:
        args: 事件参数字典，包含:
            - entityId: 受伤的玩家ID
    
    Returns:
        None
    
    Note:
        受伤会立即唤醒玩家，与原版 Minecraft 行为一致
    """
    player_id = args['entityId']
    if player_id in sleeping_players:
        wake_up(player_id, "hurt")
