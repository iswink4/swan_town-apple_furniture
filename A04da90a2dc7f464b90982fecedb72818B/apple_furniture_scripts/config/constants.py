# -*- coding: utf-8 -*-
"""
常量配置
定义游戏中的常量值（维度ID、时间、冷却时间等）
"""

# ============================================================
# 维度ID
# ============================================================
DIMENSION_OVERWORLD = 0
DIMENSION_NETHER = 1
DIMENSION_END = 2

# ============================================================
# 时间常量
# ============================================================
# 夜晚开始时间（12500 = 18:45）
NIGHT_START_TIME = 12500

# ============================================================
# 冷却时间（秒）
# ============================================================
BUCKET_INTERACT_COOLDOWN = 0.3
HAND_INTERACT_COOLDOWN = 0.2
ICE_MAKER_COOLDOWN = 0.3
DRAINAGE_DURATION = 0.5
DRAINAGE_COOLDOWN = 1.0

# ============================================================
# 高度偏移
# ============================================================
SEAT_HEIGHT = 0.5
SLEEP_HEIGHT_OFFSET = 0.8

# ============================================================
# 检测范围
# ============================================================
MONSTER_CHECK_RADIUS = 8
BED_CLEARANCE_HEIGHT = 2

# ============================================================
# 动画名称
# ============================================================
SIT_ANIMATION_NAME = "animation.sit_chair"

# ============================================================
# 敌对生物类型列表（用于睡觉检测）
# ============================================================
HOSTILE_MOBS = [
    'minecraft:zombie',
    'minecraft:skeleton',
    'minecraft:creeper',
    'minecraft:spider',
    'minecraft:enderman',
    'minecraft:witch',
    'minecraft:husk',
    'minecraft:stray',
    'minecraft:drowned',
    'minecraft:phantom',
    'minecraft:slime',
    'minecraft:ghast',
    'minecraft:magma_cube',
    'minecraft:blaze',
    'minecraft:piglin',
    'minecraft:piglin_brute',
    'minecraft:hoglin',
    'minecraft:zoglin',
    'minecraft:zombified_piglin',
    'minecraft:wither_skeleton',
]