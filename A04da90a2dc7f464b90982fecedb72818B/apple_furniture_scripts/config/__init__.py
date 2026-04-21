# -*- coding: utf-8 -*-
"""
配置模块入口
导出所有配置变量，保持向后兼容

原有导入方式仍然有效：
    from config import AXE_NAMES
    from config import ALL_BLOCK_CYCLES, CHAIR_LIST
"""

# ============================================================
# 物品配置
# ============================================================
from .items import AXE_NAMES, BUCKET_EMPTY, BUCKET_WATER

# ============================================================
# 常量配置
# ============================================================
from .constants import (
    DIMENSION_OVERWORLD, DIMENSION_NETHER, DIMENSION_END,
    NIGHT_START_TIME,
    BUCKET_INTERACT_COOLDOWN, HAND_INTERACT_COOLDOWN,
    ICE_MAKER_COOLDOWN, DRAINAGE_DURATION, DRAINAGE_COOLDOWN,
    SEAT_HEIGHT, SLEEP_HEIGHT_OFFSET,
    MONSTER_CHECK_RADIUS, BED_CLEARANCE_HEIGHT,
    SIT_ANIMATION_NAME,
    HOSTILE_MOBS,
)

# ============================================================
# 方块循环配置（斧子交互）
# ============================================================
from .cycles_axe import BLOCK_CYCLES, ALL_BLOCK_CYCLES

# ============================================================
# 方块循环配置（空手交互）
# ============================================================
from .cycles_hand import HAND_BLOCK_CYCLES, ALL_HAND_BLOCK_CYCLES

# ============================================================
# 家具配置
# ============================================================
from .furniture import (
    CHAIR_LIST,
    BED_BLOCKS,
    DOUBLE_BEDS, SINGLE_BEDS,
    DOUBLE_BED, SINGLE_BED,
    REFRIGERATOR_CONTAINERS, WARDROBE_CONTAINERS,
)

# ============================================================
# 水桶交互配置
# ============================================================
from .water import WATER_TANK_BLOCKS

# ============================================================
# 占位方块配置
# ============================================================
from .placeholder import (
    PLACEHOLDER_TYPES, PLACEHOLDER_DEFAULT_TYPE,
    PLACEHOLDER_CONFIG, PLACEHOLDER_FURNITURES, ALL_PLACEHOLDER_BLOCKS,
)

# ============================================================
# 排水功能配置
# ============================================================
from .drainage import DRAINAGE_BLOCKS

# ============================================================
# 冰箱制冰配置
# ============================================================
from .ice_maker import ICE_MAKER_BLOCKS, ICE_BLOCK_NAME, ICE_PRODUCE_COUNT